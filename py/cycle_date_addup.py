import os
from logger import *



@log_function_call(logger)
def addup(file,cycle_date,mapping):
    
    p,f=os.path.split(file)
    addup_path = os.path.join(p ,'addup')
    if not os.path.exists(addup_path):
        os.makedirs(addup_path)
    de=mapping.de
    if not de: de = ','
    to_write = os.path.join(p ,'addup', f)
    with open(to_write,'w',buffering=2048) as w:
        with open(file,'r', buffering=2048) as f:
            for line in f.readlines():
                w.write(line.strip() + f'{de}{cycle_date}\n')
                
    return to_write
                
                
if __name__=='__main__':
    import sys
    addup(sys.argv[1],'2023-10-19')