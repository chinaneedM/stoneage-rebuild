"""Own Win32 observation helpers; no remote memory injection or game patches."""
import ctypes as C
from ctypes import wintypes as W
import os
import subprocess
import time

class Native:
    def __init__(self):
        if os.name!='nt':raise ValueError('native Windows only')
        self.u=C.WinDLL('user32',use_last_error=True);self.k=C.WinDLL('kernel32',use_last_error=True)
        self.k.OpenProcess.argtypes=[W.DWORD,W.BOOL,W.DWORD];self.k.OpenProcess.restype=W.HANDLE
        self.k.CloseHandle.argtypes=[W.HANDLE]
        self.k.QueryFullProcessImageNameW.argtypes=[W.HANDLE,W.DWORD,W.LPWSTR,C.POINTER(W.DWORD)]
        self.u.GetForegroundWindow.restype=W.HWND
        for name in ('GetClientRect','GetWindowRect'):
            getattr(self.u,name).argtypes=[W.HWND,C.POINTER(W.RECT)]
        self.u.ClientToScreen.argtypes=[W.HWND,C.POINTER(W.POINT)]
        self.u.GetWindowThreadProcessId.argtypes=[W.HWND,C.POINTER(W.DWORD)]
        self.u.GetClassNameW.argtypes=[W.HWND,W.LPWSTR,C.c_int]
        self.u.GetWindowTextW.argtypes=[W.HWND,W.LPWSTR,C.c_int]
        self.u.IsWindowVisible.argtypes=[W.HWND]
        self.u.SetForegroundWindow.argtypes=[W.HWND];self.u.SetFocus.argtypes=[W.HWND]
        self.u.ShowWindow.argtypes=[W.HWND,C.c_int]
        self.u.SetProcessDPIAware()
    def image(self,pid):
        h=self.k.OpenProcess(0x1000,False,pid)
        if not h:return ''
        try:
            b=C.create_unicode_buffer(2048);n=W.DWORD(len(b))
            return b.value if self.k.QueryFullProcessImageNameW(h,0,b,C.byref(n)) else ''
        finally:self.k.CloseHandle(h)
    def windows(self,pid):
        out=[]
        @C.WINFUNCTYPE(W.BOOL,W.HWND,W.LPARAM)
        def visit(h,arg):
            owner=W.DWORD();self.u.GetWindowThreadProcessId(h,C.byref(owner))
            if owner.value!=pid or not self.u.IsWindowVisible(h):return True
            title=C.create_unicode_buffer(161);klass=C.create_unicode_buffer(161)
            self.u.GetWindowTextW(h,title,161);self.u.GetClassNameW(h,klass,161)
            r=W.RECT();self.u.GetClientRect(h,C.byref(r));p=W.POINT(0,0);self.u.ClientToScreen(h,C.byref(p))
            out.append(dict(hwnd=int(h),pid=pid,klass=klass.value,title=title.value,
                            client_size=[r.right-r.left,r.bottom-r.top],client_origin=[p.x,p.y],image=self.image(pid)))
            return True
        self.u.EnumWindows(visit,0)
        return out
    def activate(self,window):
        h=window['hwnd'];other=self.u.GetWindowThreadProcessId(h,None);me=self.k.GetCurrentThreadId()
        attached=self.u.AttachThreadInput(me,other,True)
        try:self.u.ShowWindow(h,9);self.u.SetForegroundWindow(h);self.u.SetFocus(h);time.sleep(.15)
        finally:
            if attached:self.u.AttachThreadInput(me,other,False)
        return self.u.GetForegroundWindow()==h
    def click(self,window,x,y):
        class MI(C.Structure):
            _fields_=[('dx',W.LONG),('dy',W.LONG),('data',W.DWORD),('flags',W.DWORD),('time',W.DWORD),('extra',C.c_size_t)]
        class U(C.Union):_fields_=[('mi',MI)]
        class INPUT(C.Structure):_fields_=[('type',W.DWORD),('u',U)]
        self.u.SendInput.argtypes=[W.UINT,C.POINTER(INPUT),C.c_int];self.u.SendInput.restype=W.UINT
        origin=window['client_origin'];self.u.SetCursorPos(origin[0]+x,origin[1]+y);time.sleep(.15)
        down=INPUT();down.u.mi.flags=2;up=INPUT();up.u.mi.flags=4
        a=self.u.SendInput(1,C.byref(down),C.sizeof(INPUT));time.sleep(.2)
        b=self.u.SendInput(1,C.byref(up),C.sizeof(INPUT))
        return dict(client_point=[x,y],sendinput_down=a,sendinput_up=b,input_struct_bytes=C.sizeof(INPUT))

class JobProcess:
    """Create suspended, assign to one-process kill-on-close job, then resume."""
    def __init__(self,exe,args,cwd,env):
        self.k=C.WinDLL('kernel32',use_last_error=True)
        class BASIC(C.Structure):
            _fields_=[('t1',C.c_longlong),('t2',C.c_longlong),('flags',W.DWORD),
                ('minws',C.c_size_t),('maxws',C.c_size_t),('active',W.DWORD),('affinity',C.c_size_t),('priority',W.DWORD),('scheduling',W.DWORD)]
        class EXT(C.Structure):
            _fields_=[('basic',BASIC),('io',C.c_ulonglong*6),('pml',C.c_size_t),('jml',C.c_size_t),('ppml',C.c_size_t),('pjml',C.c_size_t)]
        class START(C.Structure):
            _fields_=[('cb',W.DWORD),('reserved',W.LPWSTR),('desktop',W.LPWSTR),('title',W.LPWSTR),
                ('x',W.DWORD),('y',W.DWORD),('xs',W.DWORD),('ys',W.DWORD),('xc',W.DWORD),('yc',W.DWORD),
                ('fill',W.DWORD),('flags',W.DWORD),('show',W.WORD),('reserved2bytes',W.WORD),('reserved2',C.c_void_p),
                ('stdin',W.HANDLE),('stdout',W.HANDLE),('stderr',W.HANDLE)]
        class PI(C.Structure):_fields_=[('process',W.HANDLE),('thread',W.HANDLE),('pid',W.DWORD),('tid',W.DWORD)]
        self.k.CreateJobObjectW.argtypes=[C.c_void_p,W.LPCWSTR];self.k.CreateJobObjectW.restype=W.HANDLE
        self.k.SetInformationJobObject.argtypes=[W.HANDLE,C.c_int,C.c_void_p,W.DWORD]
        self.k.QueryInformationJobObject.argtypes=[W.HANDLE,C.c_int,C.c_void_p,W.DWORD,C.c_void_p]
        self.k.AssignProcessToJobObject.argtypes=[W.HANDLE,W.HANDLE]
        self.k.ResumeThread.argtypes=[W.HANDLE];self.k.ResumeThread.restype=W.DWORD
        self.k.WaitForSingleObject.argtypes=[W.HANDLE,W.DWORD];self.k.GetExitCodeProcess.argtypes=[W.HANDLE,C.POINTER(W.DWORD)]
        self.k.TerminateJobObject.argtypes=[W.HANDLE,W.UINT];self.k.CloseHandle.argtypes=[W.HANDLE]
        self.k.TerminateProcess.argtypes=[W.HANDLE,W.UINT]
        self.k.CreateProcessW.argtypes=[W.LPCWSTR,W.LPWSTR,C.c_void_p,C.c_void_p,W.BOOL,W.DWORD,C.c_void_p,W.LPCWSTR,C.POINTER(START),C.POINTER(PI)]
        self.job=self.k.CreateJobObjectW(None,None);limit=EXT();limit.basic.flags=0x2008;limit.basic.active=1
        if not self.job or not self.k.SetInformationJobObject(self.job,9,C.byref(limit),C.sizeof(limit)):raise C.WinError(C.get_last_error())
        si=START();si.cb=C.sizeof(si);pi=PI();command=C.create_unicode_buffer(subprocess.list2cmdline([str(exe),*args]))
        environment=C.create_unicode_buffer('\0'.join(k+'='+v for k,v in sorted(env.items()))+'\0\0')
        if not self.k.CreateProcessW(str(exe),command,None,None,False,0x404,environment,str(cwd),C.byref(si),C.byref(pi)):raise C.WinError(C.get_last_error())
        self.handle=pi.process;self.pid=pi.pid
        if not self.k.AssignProcessToJobObject(self.job,self.handle):
            self.k.TerminateProcess(self.handle,2);raise C.WinError(C.get_last_error())
        readback=EXT()
        if not self.k.QueryInformationJobObject(self.job,9,C.byref(readback),C.sizeof(readback),None):raise C.WinError(C.get_last_error())
        self.job_state=dict(limit_flags=readback.basic.flags,active_process_limit=readback.basic.active,created_suspended=True,assigned_before_resume=True)
        if self.job_state['limit_flags']!=0x2008 or self.job_state['active_process_limit']!=1:raise ValueError('job limits conflict')
        if self.k.ResumeThread(pi.thread)==0xffffffff:raise C.WinError(C.get_last_error())
        self.k.CloseHandle(pi.thread)
    def poll(self):
        if self.k.WaitForSingleObject(self.handle,0)==258:return None
        value=W.DWORD();self.k.GetExitCodeProcess(self.handle,C.byref(value));return value.value
    def wait(self,seconds):
        self.k.WaitForSingleObject(self.handle,int(seconds*1000));return self.poll()
    def close(self):
        self.k.TerminateJobObject(self.job,3);self.k.CloseHandle(self.job);self.k.CloseHandle(self.handle)
