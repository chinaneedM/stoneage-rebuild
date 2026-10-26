/* Synthetic Win32 palette/input gate. Contains no original game bytes.
 * Controller commands affect ONLY this program's private window class. */
#define COBJMACROS
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <windowsx.h>
#include <ddraw.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const WCHAR *CLASS_NAME=L"StoneAgeP3DSyntheticOnly";
static HWND window;
static HPALETTE palette;
static PALETTEENTRY colors[256];
static int phase=0,mode_dd=0,moves=0,downs=0,ups=0,async_polls=0,painted=0,done=0;
static UINT realized=0,system_previous=0;
static DWORD started;
static LPDIRECTDRAW dd;
static LPDIRECTDRAWSURFACE primary,offscreen;
static LPDIRECTDRAWPALETTE ddpalette;
static LPDIRECTDRAWCLIPPER clipper;
static HRESULT ddcreate=E_FAIL,ddcoop=E_FAIL,ddprimary=E_FAIL,ddoff=E_FAIL,ddpal=E_FAIL,ddattach=E_FAIL,ddprimarypal=E_FAIL,ddblt=E_FAIL;

static void make_colors(void) {
    for(int i=0;i<256;i++) {
        colors[i].peRed=(BYTE)(i*73);colors[i].peGreen=(BYTE)(i*151);colors[i].peBlue=(BYTE)(i*199);
        colors[i].peFlags=PC_NOCOLLAPSE;
    }
    colors[0].peRed=colors[0].peGreen=colors[0].peBlue=0;
    colors[255].peRed=colors[255].peGreen=colors[255].peBlue=255;
    colors[42].peRed=222;colors[42].peGreen=0;colors[42].peBlue=0;
    colors[99].peRed=0;colors[99].peGreen=200;colors[99].peBlue=80;
    LOGPALETTE *p=(LOGPALETTE*)malloc(sizeof(LOGPALETTE)+255*sizeof(PALETTEENTRY));
    p->palVersion=0x300;p->palNumEntries=256;memcpy(p->palPalEntry,colors,sizeof(colors));
    palette=CreatePalette(p);free(p);
}
static void realize(HDC dc) {
    if(phase && !mode_dd && palette) {SelectPalette(dc,palette,FALSE);realized=RealizePalette(dc);}
}
static void dd_init(void) {
    ddcreate=DirectDrawCreate(NULL,&dd,NULL);if(FAILED(ddcreate))return;
    ddcoop=IDirectDraw_SetCooperativeLevel(dd,window,DDSCL_NORMAL);
    DDSURFACEDESC s={0};s.dwSize=sizeof(s);s.dwFlags=DDSD_CAPS;s.ddsCaps.dwCaps=DDSCAPS_PRIMARYSURFACE;
    ddprimary=IDirectDraw_CreateSurface(dd,&s,&primary,NULL);
    s.dwFlags=DDSD_CAPS|DDSD_WIDTH|DDSD_HEIGHT|DDSD_PIXELFORMAT;s.dwWidth=320;s.dwHeight=200;
    s.ddsCaps.dwCaps=DDSCAPS_OFFSCREENPLAIN|DDSCAPS_SYSTEMMEMORY;
    s.ddpfPixelFormat.dwSize=sizeof(DDPIXELFORMAT);s.ddpfPixelFormat.dwFlags=DDPF_RGB|DDPF_PALETTEINDEXED8;s.ddpfPixelFormat.dwRGBBitCount=8;
    ddoff=IDirectDraw_CreateSurface(dd,&s,&offscreen,NULL);
    PALETTEENTRY entries[256];memcpy(entries,colors,sizeof(entries));for(int i=0;i<256;i++)entries[i].peFlags=0;
    ddpal=IDirectDraw_CreatePalette(dd,DDPCAPS_8BIT|DDPCAPS_ALLOW256,entries,&ddpalette,NULL);
    if(offscreen&&ddpalette)ddattach=IDirectDrawSurface_SetPalette(offscreen,ddpalette);
    if(primary&&ddpalette)ddprimarypal=IDirectDrawSurface_SetPalette(primary,ddpalette);
    if(primary && SUCCEEDED(IDirectDraw_CreateClipper(dd,0,&clipper,NULL))) {
        IDirectDrawClipper_SetHWnd(clipper,0,window);IDirectDrawSurface_SetClipper(primary,clipper);
    }
}
static void draw_dd(void) {
    if(!offscreen||!primary)return;
    DDSURFACEDESC s={0};s.dwSize=sizeof(s);
    if(FAILED(IDirectDrawSurface_Lock(offscreen,NULL,&s,DDLOCK_WAIT,NULL)))return;
    for(int y=0;y<200;y++)for(int x=0;x<320;x++) {
        BYTE value=y<120?(x<160?42:99):(BYTE)((y-120)/5*16+x/20);
        if(ups && y>=160 && y<190 && x>=130 && x<190)value=255;
        ((BYTE*)s.lpSurface)[y*s.lPitch+x]=value;
    }
    IDirectDrawSurface_Unlock(offscreen,NULL);
    POINT p={0,0};ClientToScreen(window,&p);RECT target={p.x,p.y,p.x+320,p.y+200};
    ddblt=IDirectDrawSurface_Blt(primary,&target,offscreen,NULL,DDBLT_WAIT,NULL);
}
static void draw_gdi(HDC dc) {
    realize(dc);
    RECT a={0,0,160,120},b={160,0,320,120};
    HBRUSH red=CreateSolidBrush(phase?PALETTEINDEX(42):RGB(222,0,0));
    HBRUSH green=CreateSolidBrush(phase?PALETTEINDEX(99):RGB(0,200,80));
    FillRect(dc,&a,red);FillRect(dc,&b,green);DeleteObject(red);DeleteObject(green);
    for(int i=0;i<256;i++) {
        RECT r={(i%16)*20,120+(i/16)*5,(i%16+1)*20,125+(i/16)*5};
        HBRUSH brush=CreateSolidBrush(phase?PALETTEINDEX(i):RGB(colors[i].peRed,colors[i].peGreen,colors[i].peBlue));
        FillRect(dc,&r,brush);DeleteObject(brush);
    }
    if(ups){RECT r={130,160,190,190};FillRect(dc,&r,(HBRUSH)GetStockObject(WHITE_BRUSH));}
}
static void rgb(FILE *f,COLORREF c) {fprintf(f,"[%u,%u,%u]",GetRValue(c),GetGValue(c),GetBValue(c));}
static void report(void) {
    HDC dc=GetDC(window);POINT p={0,0};ClientToScreen(window,&p);
    COLORREF red=GetPixel(dc,40,40),green=GetPixel(dc,220,40);
    int bpp=GetDeviceCaps(dc,BITSPIXEL)*GetDeviceCaps(dc,PLANES),caps=GetDeviceCaps(dc,RASTERCAPS);
    FILE *f=fopen("live.tmp","wb");if(!f){ReleaseDC(window,dc);return;}
    fprintf(f,"{\"schema\":\"stoneage.p3d.synthetic_win32.v1\",\"original_client_executed\":false,\"pointer_bytes\":%u,\"windows_acp\":%u,\"mode\":\"%s\",\"phase\":%d,\"done\":%s,\"display_bpp\":%d,\"raster_palette_capability\":%s,\"foreground_matches\":%s,\"active_matches\":%s,\"focus_matches\":%s,\"client_origin\":[%ld,%ld],\"client_size\":[320,200],\"moves\":%d,\"downs\":%d,\"ups\":%d,\"async_down_polls\":%d,\"painted\":%d,\"palette_created\":%s,\"realized_entries_last\":%u,\"system_palette_previous\":%u,\"red_getpixel\":",
        (unsigned)sizeof(void*),(unsigned)GetACP(),mode_dd?"ddraw":"gdi",phase,done?"true":"false",bpp,caps&RC_PALETTE?"true":"false",
        GetForegroundWindow()==window?"true":"false",GetActiveWindow()==window?"true":"false",GetFocus()==window?"true":"false",p.x,p.y,moves,downs,ups,async_polls,painted,palette?"true":"false",realized,system_previous);
    rgb(f,red);fprintf(f,",\"green_getpixel\":");rgb(f,green);
    fprintf(f,",\"getpixel_valid\":%s,\"ddraw\":{\"create\":%ld,\"cooperative\":%ld,\"primary\":%ld,\"offscreen_8bit\":%ld,\"palette\":%ld,\"offscreen_attach\":%ld,\"primary_attach\":%ld,\"blt\":%ld}}\n",
        red!=CLR_INVALID&&green!=CLR_INVALID?"true":"false",(long)ddcreate,(long)ddcoop,(long)ddprimary,(long)ddoff,(long)ddpal,(long)ddattach,(long)ddprimarypal,(long)ddblt);
    fclose(f);MoveFileExA("live.tmp","live.json",MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH);ReleaseDC(window,dc);
}
static LRESULT CALLBACK proc(HWND w,UINT msg,WPARAM a,LPARAM b) {
    if(msg==WM_PAINT){PAINTSTRUCT p;HDC dc=BeginPaint(w,&p);if(phase&&mode_dd)draw_dd();else draw_gdi(dc);EndPaint(w,&p);painted++;return 0;}
    if(msg==WM_QUERYNEWPALETTE){HDC dc=GetDC(w);realize(dc);ReleaseDC(w,dc);InvalidateRect(w,NULL,FALSE);return phase?TRUE:FALSE;}
    if(msg==WM_PALETTECHANGED && (HWND)a!=w){InvalidateRect(w,NULL,FALSE);return 0;}
    if(msg==WM_MOUSEMOVE)moves++;
    if(msg==WM_LBUTTONDOWN)downs++;
    if(msg==WM_LBUTTONUP){ups++;InvalidateRect(w,NULL,FALSE);}
    if(msg==WM_APP+1){phase=1;HDC dc=GetDC(w);if(!mode_dd){system_previous=SetSystemPaletteUse(dc,SYSPAL_NOSTATIC);realize(dc);}else dd_init();ReleaseDC(w,dc);InvalidateRect(w,NULL,FALSE);report();return 0;}
    if(msg==WM_APP+2){done=1;report();DestroyWindow(w);return 0;}
    if(msg==WM_TIMER){if(GetAsyncKeyState(VK_LBUTTON)&0x8000)async_polls++;if(phase&&mode_dd)draw_dd();report();if(GetTickCount()-started>45000){done=1;report();DestroyWindow(w);}return 0;}
    if(msg==WM_DESTROY){if(system_previous){HDC dc=GetDC(w);SetSystemPaletteUse(dc,system_previous);ReleaseDC(w,dc);}PostQuitMessage(0);return 0;}
    return DefWindowProcW(w,msg,a,b);
}
static int controller(const char *command) {
    HWND w=FindWindowW(CLASS_NAME,NULL);if(!w)return 4;
    DWORD target=GetWindowThreadProcessId(w,NULL),self=GetCurrentThreadId();
    BOOL attached=AttachThreadInput(self,target,TRUE);BOOL foreground=SetForegroundWindow(w);SetFocus(w);Sleep(100);
    unsigned sent_down=0,sent_up=0;
    if(strstr(command,"palette"))PostMessageW(w,WM_APP+1,0,0);
    if(strstr(command,"finish"))PostMessageW(w,WM_APP+2,0,0);
    if(strstr(command,"click")) {
        POINT p={160,170};ClientToScreen(w,&p);SetCursorPos(p.x,p.y);
        INPUT i={0};i.type=INPUT_MOUSE;i.mi.dwFlags=MOUSEEVENTF_LEFTDOWN;sent_down=SendInput(1,&i,sizeof(i));
        Sleep(200);i.mi.dwFlags=MOUSEEVENTF_LEFTUP;sent_up=SendInput(1,&i,sizeof(i));
    }
    printf("{\"controller_only_own_synthetic_class\":true,\"attach_thread_input\":%s,\"set_foreground_return\":%s,\"foreground_matches\":%s,\"sendinput_down\":%u,\"sendinput_up\":%u}\n",attached?"true":"false",foreground?"true":"false",GetForegroundWindow()==w?"true":"false",sent_down,sent_up);fflush(stdout);
    if(attached)AttachThreadInput(self,target,FALSE);return 0;
}
int WINAPI WinMain(HINSTANCE instance,HINSTANCE previous,LPSTR command,int show) {
    if(strstr(command,"activate")||strstr(command,"palette")||strstr(command,"click")||strstr(command,"finish"))return controller(command);
    mode_dd=strstr(command,"ddraw")!=NULL;make_colors();
    WNDCLASSW c={0};c.lpfnWndProc=proc;c.hInstance=instance;c.lpszClassName=CLASS_NAME;RegisterClassW(&c);
    window=CreateWindowW(CLASS_NAME,L"SYNTHETIC palette and input only",WS_POPUP|WS_VISIBLE,30,30,320,200,NULL,NULL,instance,NULL);
    if(!window)return 2;SetForegroundWindow(window);SetFocus(window);UpdateWindow(window);
    started=GetTickCount();SetTimer(window,1,16,NULL);report();
    MSG msg;while(GetMessageW(&msg,NULL,0,0)>0){TranslateMessage(&msg);DispatchMessageW(&msg);}
    if(clipper)IDirectDrawClipper_Release(clipper);if(ddpalette)IDirectDrawPalette_Release(ddpalette);
    if(offscreen)IDirectDrawSurface_Release(offscreen);if(primary)IDirectDrawSurface_Release(primary);if(dd)IDirectDraw_Release(dd);
    if(palette)DeleteObject(palette);return 0;
}
