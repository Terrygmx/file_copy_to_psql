from file_name_parser import *
from cycle_date_addup import addup
from psql_copy import *
from logger import *
import shutil,os


@log_function_call(logger)
def trigger_file_handler(file,cycle_date,mapping, conn):
    cur = conn.cursor()
    if mapping.if_add_date=='0':
        new_file_name = addup(file, cycle_date,mapping)
    else:
        new_file_name = file
    try:
        #conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur.execute("BEGIN")
        copy_into_psql(new_file_name, mapping.tb_name, cur, sep=mapping.de)
        insert_into_psql(mapping.type, mapping.tb_name, cycle_date, cur)
        cur.execute("COMMIT")
        if not os.path.exists('/data/CP2/data/whitelist_copy_to_cpdb_bak'):
            os.makedirs('/data/CP2/data/whitelist_copy_to_cpdb_bak')
        
        shutil.move(file,'/data/CP2/data/whitelist_copy_to_cpdb_bak/')
        
        conn.commit()
        logger.info(f'入库成功, 文件挪到 /data/CP2/data/whitelist_copy_to_cpdb_bak/{new_file_name}')
    except Exception as e:
        cur.execute("ROLLBACK")
        if not os.path.exists('/data/CP2/data/whitelist_copy_to_cpdb_err'):
            os.makedirs('/data/CP2/data/whitelist_copy_to_cpdb_err')
        
        shutil.move(file,'/data/CP2/data/whitelist_copy_to_cpdb_err/')
        logger.error(f'入库错误： {e}, 文件挪到 /data/CP2/data/whitelist_copy_to_cpdb_err/{new_file_name}')
    finally:
        cur.close()
        
        
"""
    python3 file_handler.py table_mappings_new.csv ./
"""
        
if __name__=='__main__':
    import sys,re
    if len(sys.argv)<3:
        print(f'请输入数据表映射文件路径，和入库文件路径目录')
        sys.exit(1)
    mappings = load_mappings(sys.argv[1])
    conn = psycopg2.connect('postgresql://cpuser:cpuser@192.168.94.74:10300/cptest')
    #print(mappings)
    
    for p in sys.argv[2:]:
        if not os.path.exists(p) or not os.path.isdir(p):
            #print(f'路径不存在或不是目录： ${p}')
            logger.error(f'路径不存在或不是目录：{p}')
            continue
        for file in [os.path.join(p,f) for f in os.listdir(p) if os.path.isfile(os.path.join(p,f))]:
            for mapping in mappings:
                if mapping.pattern in file.lower():
                    match = re.search('20[2-9]\d[01]\d[0-3]\d', file)
                    if match:
                        logger.info(f'文件在配置表中找到，开始处理： ${file}')
                        cycle_date = match.group(0)
                        
                        try:
                            trigger_file_handler(file,cycle_date,mapping,conn)
                            #logger.info(f"文件 '{file}' 处理完成，移动到/data/CP2/data/whitelist_copy_to_cpdb_bak/目录")
                        except Exception as e:
                            logger.error(f"入库文件'{file}'失败！错误：", exc_info=True)
                        break
    conn.close()
