"""Numeric helper/caller metadata models on invented storage and explicit stubs only.

No binary loader, original payload, API/filesystem execution or native CALL.
"""
from collections import Counter
from tools.stoneage_tw10_savedata_transform_r53_model import ModelError
from tools.stoneage_tw10_savedata_writer_r55_model import WriterModel
BASE=0x400000
S=0x70010000
GLOBAL=25148844
MARKER=0x13572468

class Storage:
    def __init__(self):self.cells={};self.reads=[];self.writes=[]
    def valid(self,a,w):return type(a) is int and w in (1,2,4) and (S-131072<=a and a+w<=S+256 or GLOBAL<=a and a+w<=GLOBAL+127)
    def get(self,a,w):
        if not self.valid(a,w):raise ModelError('invented memory range')
        self.reads.append((a,w));return sum(self.cells.get(a+i,0)<<(8*i) for i in range(w))
    def put(self,a,w,v):
        if not self.valid(a,w):raise ModelError('invented memory range')
        self.writes.append((a,w));self.cells.update({a+i:(v>>(8*i))&255 for i in range(w)})
    def data(self,a,n):return bytes(self.get(a+i,1) for i in range(n))
    def fill(self,a,data):
        for i,v in enumerate(data):self.put(a+i,1,v)

class Machine:
    def __init__(self,rows,edges,root,regs,mem):
        self.by={r['site_rva']:r for r in rows};self.succ={a:[] for a in self.by};self.root=root;self.regs=regs;self.mem=mem;self.cf=None;self.zf=None;self.visits=Counter();self.probes=[]
        if root not in self.by or len(self.by)!=len(rows) or len(rows)>256:raise ModelError('frame inventory')
        for a,b in edges:
            if a not in self.by or b not in self.by:raise ModelError('frame edge')
            self.succ[a].append(b)
    def address(self,o):
        g=o['geometry']
        if g.get('segment_register') not in (None,'es'):raise ModelError('frame segment')
        return (self.regs.get(g.get('base_register'),0)+self.regs.get(g.get('index_register'),0)*g.get('index_scale',1)+g['relative_field_offset'])&0xffffffff
    def op(self,o,v=None):
        k=o['kind']
        if k=='register':
            if o['width_bytes']!=4:raise ModelError('frame register width')
            if v is None:return self.regs[o['register']]
            self.regs[o['register']]=v&0xffffffff
        elif k=='memory':
            a=self.address(o)
            if v is None:return self.mem.get(a,o['width_bytes'])
            self.mem.put(a,o['width_bytes'],v)
        elif k=='immediate' and v is None:return o['constant']
        else:raise ModelError('frame operand')
    def push(self,v):self.regs['esp']-=4;self.mem.put(self.regs['esp'],4,v)
    def pop(self):v=self.mem.get(self.regs['esp'],4);self.regs['esp']+=4;return v
    def branch(self,at,target,taken):
        other=[b for b in self.succ[at] if b!=target]
        if target not in self.succ[at] or len(other)!=1:raise ModelError('frame branch geometry')
        return target if taken else other[0]
    def step(self,at):
        r=self.by[at];m=r['mnemonic'];o=r['operands'];self.visits[at]+=1
        if m=='mov':self.op(o[0],self.op(o[1]))
        elif m=='lea':self.op(o[0],self.address(o[1]))
        elif m=='push':self.push(self.op(o[0]))
        elif m=='pop':self.op(o[0],self.pop())
        elif m in ('add','sub','cmp','test','xor'):
            a,b=self.op(o[0]),self.op(o[1]);v=a+b if m=='add' else a-b if m in ('sub','cmp') else a&b if m=='test' else a^b
            self.zf=(v&0xffffffff)==0;self.cf=a<b if m in ('sub','cmp') else a+b>0xffffffff if m=='add' else False
            if m not in ('cmp','test'):self.op(o[0],v)
            if m=='test' and o[0]['kind']=='memory':self.probes.append(self.address(o[0]))
        elif m in ('jb','jae','jne'):
            flag=self.zf if m=='jne' else self.cf
            if type(flag) is not bool:raise ModelError('undefined frame flags')
            return self.branch(at,self.op(o[0])-BASE,not flag if m in ('jae','jne') else flag)
        else:raise ModelError('unsupported frame mnemonic '+m)
        if len(self.succ[at])!=1:raise ModelError('frame fallthrough')
        return self.succ[at][0]

def helper(rows,edges,amount,mem=None,entry_esp=S-4,ecx=0x2468ace0,marker=MARKER,max_steps=4096):
    if type(amount) is not int or not 0<=amount<=65536 or type(max_steps) is not int or not 1<=max_steps<=4096:raise ModelError('invented helper bounds')
    mem=mem or Storage();mem.put(entry_esp,4,marker)
    m=Machine(rows,edges,0x49160,{'eax':amount,'ecx':ecx,'esp':entry_esp},mem);at=m.root
    for n in range(max_steps):
        if m.by[at]['mnemonic']=='ret':
            m.visits[at]+=1
            if m.by[at]['operands'] or m.succ[at]:raise ModelError('helper ret form')
            returned=m.pop()
            if returned!=marker or m.regs['ecx']!=ecx:raise ModelError('helper marker/ECX')
            return {'caller_esp':m.regs['esp'],'returned_marker':returned,'regs':m.regs,'probe_addresses':m.probes,'site_visits':dict(m.visits),'steps':n+1}
        at=m.step(at)
    raise ModelError('helper step bound')

def caller(c,h,w,invented,open_return=0x11111111,write_return=128,close_return=0,length_clobber=None,output_clobber=False,direction=0,flat_segments=True,max_steps=512):
    if type(invented) is not bytes or len(invented)!=127 or type(direction) is not int or direction!=0 or flat_segments is not True:raise ModelError('caller invented copy preconditions')
    if any(type(v) is not int or not 0<=v<=0xffffffff for v in (open_return,write_return,close_return)):raise ModelError('invented stub return domain')
    mem=Storage();mem.fill(GLOBAL,invented);mem.put(S,4,MARKER)
    regs={'eax':0,'ecx':0x2468ace0,'edx':0,'esi':0x12345678,'edi':0x87654321,'esp':S};m=Machine(c['instruction_shapes'],c['bounded_edges'],0x40020,regs,mem)
    at=m.root;calls=[];captures={};requested=None;transform=None;request_bytes=None;close_seen=False
    for n in range(max_steps):
        r=m.by[at];mn=r['mnemonic'];ops=r['operands'];captures[at]=regs['esp']-S
        if mn=='ret':
            m.visits[at]+=1
            if ops or m.succ[at] or m.pop()!=MARKER or regs['esp']!=S+4:raise ModelError('caller normal return')
            return {'return_value':regs['eax'],'calls':calls,'close_stub_seen':close_seen,'request_slots':requested,'request_bytes':request_bytes,
              'transform':transform,'entry_relative_stack_before_sites':captures,'caller_site_visits':dict(m.visits),'steps':n+1,'original_io_executed':False}
        if mn=='call':
            m.visits[at]+=1
            if len(m.succ[at])!=1:raise ModelError('caller continuation')
            cont=m.succ[at][0];target=ops[0]['constant']-BASE;calls.append(at)
            if at==0x40025 and target==0x49160:
                old=regs['esp'];m.push(BASE+cont);hr=helper(h['instruction_shapes'],h['bounded_edges'],regs['eax'],mem,regs['esp'],regs['ecx'],BASE+cont)
                regs.update(hr['regs']);captures['helper_delta']=regs['esp']-old
            elif at==0x4005a and target==0x47010:
                args=[mem.get(regs['esp']+4*i,4) for i in range(6)];ip,count,seed,op,lp,cap=args
                if args!=[S-4128,127,0,S-4000,S-4132,4000]:raise ModelError('caller transform geometry')
                result=WriterModel(mem.data(ip,count),seed,cap).run(w['instruction_shapes'],w['bounded_edges'])
                mem.fill(ip,result['mutated_input']);mem.fill(op,result['output']);mem.put(lp,4,result['output_length'])
                transform={'slots':args,'output_length':result['output_length'],'length_cell':lp,'output_address':op,'output':result['output']}
                regs['eax']=op;regs['ecx']=0xdeadbeef;regs['edx']=0xabababab
            elif at==0x40069 and target==0x487ba:
                regs['eax']=open_return;regs['ecx']=0xdeadbeef;regs['edx']=0xabababab
                if length_clobber is not None:mem.put(S-4132,4,length_clobber)
                if output_clobber:mem.put(S-4000,1,mem.get(S-4000,1)^255)
            elif at==0x40090 and target==0x48bbc:
                requested=[mem.get(regs['esp']+4*i,4) for i in range(4)];buf,unit,count,obj=requested
                if not 0<=count<=4000:raise ModelError('invented write request bound')
                request_bytes=mem.data(buf,unit*count);regs['eax']=write_return
            elif at==0x400ac and target==0x4856c:close_seen=True;regs['eax']=close_return
            else:raise ModelError('unsupported explicit call abstraction')
            at=cont;continue
        if mn in ('rep movsd','movsw','movsb'):
            m.visits[at]+=1;size={'rep movsd':4,'movsw':2,'movsb':1}[mn];repeat=regs['ecx'] if mn=='rep movsd' else 1
            if not 0<=repeat<=31:raise ModelError('invented repeat bound')
            for _ in range(repeat):mem.put(regs['edi'],size,mem.get(regs['esi'],size));regs['edi']+=size;regs['esi']+=size
            if mn=='rep movsd':regs['ecx']=0
            if len(m.succ[at])!=1:raise ModelError('copy fallthrough')
            at=m.succ[at][0];continue
        at=m.step(at)
    raise ModelError('caller step bound')
