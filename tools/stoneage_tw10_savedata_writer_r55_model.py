"""Restricted writer instruction-shape model on fabricated arrays only.

No binary/file loader, original payload, native CALL, or original execution.
R53's read model remains unchanged. Its arithmetic helpers are reused explicitly.
"""
from collections import Counter
from tools.stoneage_tw10_savedata_transform_r53_model import (NumericModel,ModelError,signed,signed_divide,INPUT,OUTPUT,OUTLEN,ENTRY_ESP)
ROOT=0x47010
MAX_COUNT=3999

class WriterModel(NumericModel):
    def __init__(self,invented,seed=0,capacity=4000):
        if type(invented) is not bytes or not 0<=len(invented)<=MAX_COUNT:raise ModelError('writer invented count 0..3999')
        if type(seed) is not int or not -(1<<31)<=seed<(1<<31):raise ModelError('writer seed domain')
        if type(capacity) is not int or not 0<=capacity<=4000:raise ModelError('writer capacity domain')
        self.initial=bytes(invented);self.n=len(invented);self.capacity=capacity
        self.regs={'eax':0,'ecx':0x13579bdf,'edx':0,'esp':ENTRY_ESP,'ebx':0x12345678,'ebp':0x87654321,'esi':0x23456789,'edi':0x76543210}
        self.saved={r:self.regs[r] for r in ('ebx','ebp','esi','edi')}
        self.regions=[('inout',INPUT,bytearray(invented)),('output',OUTPUT,bytearray([0xa5]*capacity)),('outlen',OUTLEN,bytearray(4)),('stack',ENTRY_ESP-128,bytearray(256))]
        self.flags=None;self.writes=[];self.visits=Counter();self.branches=Counter()
        for offset,value in [(0,0x55555555),(4,INPUT),(8,self.n),(12,seed),(16,OUTPUT),(20,OUTLEN),(24,capacity)]:self.memory(ENTRY_ESP+offset,4,value,record=False)
    def condition(self,m):
        if m=='jg':
            if self.flags is None:raise ModelError('undefined model flags')
            return not self.flags['zf'] and self.flags['sf']==self.flags['of']
        return super().condition(m)

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
                length=self.memory(OUTLEN,4);want=min(self.n+1,self.capacity)
                if length!=want:raise ModelError('invented writer output length')
                output=next(data for name,start,data in self.regions if name=='output')
                mutated=next(data for name,start,data in self.regions if name=='inout')
                covered={w['offset'] for w in self.writes if w['region']=='output' and w['width_bytes']==1}
                if covered!=set(range(want)):raise ModelError('invented writer output coverage')
                if self.capacity<self.n+1 and bytes(mutated)!=self.initial:raise ModelError('capacity branch mutated input')
                return {'output':bytes(output[:length]),'mutated_input':bytes(mutated),'output_length':length,'steps':step+1,'site_visits':dict(self.visits),'branch_outcomes':dict(self.branches),'writes':self.writes,'returned_ecx':self.register('ecx')}
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
            elif m in ('xor','and','or','add','sub','cmp','test'):
                a,b=self.operand(ops[0]),self.operand(ops[1]);bits=ops[0]['width_bytes']*8
                value={'xor':lambda:a^b,'and':lambda:a&b,'or':lambda:a|b,'add':lambda:a+b,'sub':lambda:a-b,'cmp':lambda:a-b,'test':lambda:a&b}[m]()
                if m in ('add','sub','cmp'):self.arithmetic_flags(a,b,value,bits,m!='add')
                else:self.logic_flags(value,bits)
                if m not in ('cmp','test'):self.operand(ops[0],value,at)
            elif m in ('inc','dec'):
                a=self.operand(ops[0]);bits=ops[0]['width_bytes']*8;value=a+(1 if m=='inc' else -1)
                self.arithmetic_flags(a,1,value,bits,m=='dec');self.operand(ops[0],value,at)
            elif m=='not':self.operand(ops[0],~self.operand(ops[0]),at)
            elif m=='jmp':
                target=ops[0]['constant']-0x400000
                if succ[at]!=[target]:raise ModelError('unconditional branch geometry')
                at=target;continue
            elif m in ('je','jne','jle','jl','jge','jg','jns'):
                target=ops[0]['constant']-0x400000;other=[b for b in succ[at] if b!=target]
                if target not in succ[at] or len(other)!=1:raise ModelError('branch geometry')
                taken=self.condition(m);self.branches[(at,taken)]+=1;at=target if taken else other[0];continue
            else:raise ModelError('unsupported numeric mnemonic '+m)
            if len(succ[at])!=1:raise ModelError('fallthrough geometry')
            at=succ[at][0]
        raise ModelError('model step limit')
