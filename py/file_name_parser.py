"""
    dwi_shazha_leiji_phone_no_value_dd.20231015.csv__c427bbf0_0a6b_4dac_8387_8c6e9846c91f
    beijing.DM_PUB_LOW_RISK_RESULT_DS.20231015.0.dat
"""
import os,sys
class TableMapping():
    def __init__(self, line):
        arr=line.strip().split('\t')
        if len(arr)<4: return None
        (self.pattern, self.tb_name, self.type, self.if_add_date, self.de)= arr
        
    def __repr__(self):
        return f"TableMapping({self.pattern},{self.tb_name},{self.type}, {self.if_add_date}, {self.de}"
            
            
            
def load_mappings(conf_file='conf/table_mappings.csv'):
    if not os.path.isfile(conf_file):  
            print(f'配置文件未找到：{conf_file}')
            sys.exit(1)
    mappings=[]
    with open(conf_file, 'r') as f:
        for line in f.readlines():
            tm=TableMapping(line.lower())
            if tm:
                mappings.append(tm)
                
    return mappings
    
if __name__=='__main__':
    import sys,re
    if len(sys.argv)<3:
        print(f'请输入数据表映射文件路径，和入库文件路径目录')
        os.exit(1)
    mappings = load_mappings(sys.argv[1])
    #print(mappings)
    for p in sys.argv[2:]:
        if not os.path.exists(p) or not os.path.isdir(p):
            print(f'路径不存在或不是目录： ${p}')
            continue
        for file in [os.path.join(p,f.lower()) for f in os.listdir(p) if os.path.isfile(f)]:
            for mapping in mappings:
                if mapping.pattern in file:
                    match = re.search('\d{8}', file)
                    if match:
                        cycle_date = match.group(0)
                        #todo
                        trigger_file_handler(file,cycle_date,mapping)
                        break