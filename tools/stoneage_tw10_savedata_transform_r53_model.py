"""Restricted numerical instruction-shape model for invented fixtures only.

No binary loader, native execution, file input, original save evaluation, or
production decoder API. Memory regions/arguments are fabricated and disjoint.
"""
from collections import Counter

INPUT=0x10000000
OUTPUT=0x20000000
OUTLEN=0x30000000
ENTRY_ESP=0x40001000
ROOT=0x47160
MAX_COUNT=4000

class ModelError(ValueError):pass

def signed(value,bits=32):
    value&=(1<<bits)-1
    return value-(1<<bits) if value&(1<<(bits-1)) else value

def signed_divide(dividend,divisor,bits=32):
    if divisor==0:raise ModelError('division by zero')
    q=abs(dividend)//abs(divisor)
    if (dividend<0)!=(divisor<0):q=-q
    if not -(1<<(bits-1))<=q<(1<<(bits-1)):raise ModelError('quotient overflow')
    return q,dividend-q*divisor

ALIASES={name:(parent,shift,width) for parent,names in {
    'eax':('eax','ax','al','ah'),'ebx':('ebx','bx','bl','bh'),
    'ecx':('ecx','cx','cl','ch'),'edx':('edx','dx','dl','dh'),
    'esi':('esi','si'),'edi':('edi','di'),'ebp':('ebp','bp'),'esp':('esp','sp')}.items()
    for name,shift,width in [(n,8 if n.endswith('h') and len(n)==2 else 0,32 if n==parent else 8 if len(n)==2 and n[-1] in 'lh' else 16) for n in names]}

def check_invented(data):
    if type(data) is not bytes or not 2<=len(data)<=MAX_COUNT:raise ModelError('invented fixture count must be 2..4000')

class NumericModel:
    def __init__(self,invented,seed=0):
        check_invented(invented)
        if type(seed) is not int or not -(1<<31)<=seed<(1<<31):raise ModelError('seed domain')
        self.initial=bytes(invented);self.n=len(invented)
        self.regs={'eax':0,'ecx':0,'edx':0,'esp':ENTRY_ESP,'ebx':0x12345678,'ebp':0x87654321,'esi':0x23456789,'edi':0x76543210}
        self.saved={r:self.regs[r] for r in ('ebx','ebp','esi','edi')}
        self.regions=[('input',INPUT,bytearray(invented)),('output',OUTPUT,bytearray([0xa5]*(self.n-1))),('outlen',OUTLEN,bytearray(4)),('stack',ENTRY_ESP-128,bytearray(256))]
        self.flags=None;self.writes=[];self.visits=Counter();self.branches=Counter()
        for offset,value in [(0,0x55555555),(4,INPUT),(8,self.n),(12,seed),(16,OUTPUT),(20,OUTLEN)]:self.memory(ENTRY_ESP+offset,4,value,record=False)
    def register(self,name,value=None):
        if name not in ALIASES:raise ModelError('register scope')
        parent,shift,bits=ALIASES[name];mask=(1<<bits)-1
        if value is None:return (self.regs[parent]>>shift)&mask
        self.regs[parent]=(self.regs[parent]&~(mask<<shift))|((value&mask)<<shift)
        self.regs[parent]&=0xffffffff
    def memory(self,address,width,value=None,record=True,site=None):
        if width not in (1,2,4):raise ModelError('memory width')
        for name,start,data in self.regions:
            if start<=address and address+width<=start+len(data):
                offset=address-start
                if value is None:return int.from_bytes(data[offset:offset+width],'little')
                if name=='input':raise ModelError('invented input alias/write')
                data[offset:offset+width]=(value&((1<<(8*width))-1)).to_bytes(width,'little')
                if record:self.writes.append({'site_rva':site,'region':name,'offset':offset,'width_bytes':width})
                return
        raise ModelError('invented memory range')
    def address(self,op):
        g=op.get('geometry') or {};disp=g.get('relative_field_offset')
        if g.get('segment_register') is not None or type(disp) is not int:raise ModelError('address geometry')
        base=self.register(g['base_register']) if g.get('base_register') else 0
        index=self.register(g['index_register']) if g.get('index_register') else 0
        return (base+index*g.get('index_scale',1)+disp)&0xffffffff
    def operand(self,op,value=None,site=None):
        if op['kind']=='register':return self.register(op['register'],value)
        if op['kind']=='immediate' and value is None:return op['constant']
        if op['kind']=='memory':return self.memory(self.address(op),op['width_bytes'],value,site=site)
        raise ModelError('operand scope')
    def arithmetic_flags(self,a,b,result,bits,subtract=False):
        mask=(1<<bits)-1;sign=1<<(bits-1);a&=mask;b&=mask;result&=mask
        overflow=bool(((a^b)&(a^result)&sign) if subtract else ((~(a^b))&(a^result)&sign))
        self.flags={'zf':result==0,'sf':bool(result&sign),'of':overflow}
    def logic_flags(self,result,bits):
        result&=(1<<bits)-1;self.flags={'zf':result==0,'sf':bool(result&(1<<(bits-1))),'of':False}
    def condition(self,m):
        if self.flags is None:raise ModelError('undefined model flags')
        z,s,o=(self.flags[k] for k in ('zf','sf','of'))
        return {'je':z,'jne':not z,'jle':z or s!=o,'jl':s!=o,'jge':s==o,'jns':not s}[m]
    def run(self,rows,edges,max_steps=1000000):
        if type(max_steps) is not int or not 1<=max_steps<=1000000:raise ModelError('step bound')
        by={r['site_rva']:r for r in rows};succ={a:[] for a in by}
        if len(by)!=len(rows) or ROOT not in by or len(rows)>256:raise ModelError('model inventory')
        for a,b in edges:
            if a not in by or b not in by:raise ModelError('model edge')
            succ[a].append(b)
        at=ROOT
        for step in range(max_steps):
            r=by[at];m=r['mnemonic'];ops=r['operands'];self.visits[at]+=1
            if m=='ret':
                if ops or succ[at] or self.register('esp')!=ENTRY_ESP or any(self.regs[k]!=v for k,v in self.saved.items()):raise ModelError('normal-return model')
                if self.memory(OUTLEN,4)!=self.n-1:raise ModelError('invented output length')
                output=next(data for name,start,data in self.regions if name=='output')
                initial=next(data for name,start,data in self.regions if name=='input')
                if bytes(initial)!=self.initial:raise ModelError('invented input changed')
                covered={w['offset'] for w in self.writes if w['region']=='output' and w['width_bytes']==1}
                if covered!=set(range(self.n-1)):raise ModelError('invented output coverage')
                return {'output':bytes(output),'output_length':self.n-1,'steps':step+1,'site_visits':dict(self.visits),'branch_outcomes':dict(self.branches),'writes':self.writes}
            elif m=='mov':self.operand(ops[0],self.operand(ops[1]),at)
            elif m=='lea':self.operand(ops[0],self.address(ops[1]),at)
            elif m=='push':
                if len(ops)!=1 or ops[0]['width_bytes']!=4:raise ModelError('stack width')
                value=self.operand(ops[0]);self.register('esp',self.register('esp')-4);self.memory(self.register('esp'),4,value,site=at)
            elif m=='pop':
                if len(ops)!=1 or ops[0]['width_bytes']!=4:raise ModelError('stack width')
                value=self.memory(self.register('esp'),4);self.register('esp',self.register('esp')+4);self.operand(ops[0],value,at)
            elif m=='cdq':
                if ops:raise ModelError('CDQ form')
                self.register('edx',-1 if signed(self.register('eax'))<0 else 0)
            elif m=='idiv':
                if len(ops)!=1 or ops[0]['width_bytes']!=4:raise ModelError('division width')
                numerator=signed((self.register('edx')<<32)|self.register('eax'),64);q,rem=signed_divide(numerator,signed(self.operand(ops[0])))
                self.register('eax',q);self.register('edx',rem);self.flags=None
            elif m=='imul':
                if len(ops)==1 and ops[0]['width_bytes']==1:self.register('ax',signed(self.register('al'),8)*signed(self.operand(ops[0]),8))
                elif len(ops)==2 and all(o['width_bytes']==4 for o in ops):self.operand(ops[0],signed(self.operand(ops[0]))*signed(self.operand(ops[1])),at)
                else:raise ModelError('multiply form')
                self.flags=None
            elif m in ('xor','and','or','sub','cmp','test'):
                a,b=self.operand(ops[0]),self.operand(ops[1]);bits=ops[0]['width_bytes']*8
                value={'xor':lambda:a^b,'and':lambda:a&b,'or':lambda:a|b,'sub':lambda:a-b,'cmp':lambda:a-b,'test':lambda:a&b}[m]()
                if m in ('sub','cmp'):self.arithmetic_flags(a,b,value,bits,True)
                else:self.logic_flags(value,bits)
                if m not in ('cmp','test'):self.operand(ops[0],value,at)
            elif m in ('inc','dec'):
                a=self.operand(ops[0]);bits=ops[0]['width_bytes']*8;value=a+(1 if m=='inc' else -1)
                self.arithmetic_flags(a,1,value,bits,m=='dec');self.operand(ops[0],value,at)
            elif m=='not':self.operand(ops[0],~self.operand(ops[0]),at)
            elif m in ('je','jne','jle','jl','jge','jns'):
                target=ops[0]['constant']-0x400000;other=[b for b in succ[at] if b!=target]
                if target not in succ[at] or len(other)!=1:raise ModelError('branch geometry')
                taken=self.condition(m);self.branches[(at,taken)]+=1;at=target if taken else other[0];continue
            else:raise ModelError('unsupported numeric mnemonic '+m)
            if len(succ[at])!=1:raise ModelError('fallthrough geometry')
            at=succ[at][0]
        raise ModelError('model step limit')

def seed_zero_reference(invented,seed=0):
    """Conditional independent formula; invented fixtures only, no file input."""
    check_invented(invented)
    if type(seed) is not int or seed!=0:raise ModelError('reference restricted to seed zero')
    key=invented[0];out=[]
    for j,value in enumerate(invented[1:]):
        source_index=j+1;v=(value-((source_index*source_index)%7)*key)&255
        if j%5==0 or j%2==0:v^=255
        out.append(v)
    return bytes(out)

def seed_zero_fixture_inverse(invented_output,key):
    """Invented fixture generator, not a historical write-path assertion."""
    if type(invented_output) is not bytes or not 1<=len(invented_output)<MAX_COUNT or type(key) is not int or not 0<=key<=255:raise ModelError('fixture inverse domain')
    out=[key]
    for j,value in enumerate(invented_output):
        v=value^255 if j%5==0 or j%2==0 else value
        out.append((v+(((j+1)*(j+1))%7)*key)&255)
    return bytes(out)
