"""Independent compact relation for invented zero-seed writer inputs only."""
def reference(invented,capacity=4000):
    if type(invented) is not bytes or not 0<=len(invented)<=3999 or type(capacity) is not int or not 0<=capacity<=4000:raise ValueError('invented writer reference domain')
    n=len(invented)
    if capacity<n+1:return {'output':invented[:capacity],'mutated_input':invented,'output_length':capacity,'key':None,'capacity_fallback':True}
    if n==0:raise ValueError('zero count reaches a division by zero')
    key=sum(invented)&255
    changed=bytes(v^(255 if j%5==0 or j%2==0 else 0) for j,v in enumerate(invented))
    output=bytes([key])+bytes((v+(((j+1)*(j+1))%7)*key)&255 for j,v in enumerate(changed))
    return {'output':output,'mutated_input':changed,'output_length':n+1,'key':key,'capacity_fallback':False}
