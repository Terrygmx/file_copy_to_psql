import psycopg2
from logger import *


@log_function_call(logger)
def copy_into_psql(file, tb_name, cur, sep=','):
    if not sep: sep = ','
    copy_sql = f"copy cmsi.{tb_name} from stdin delimiter as '{sep}'"
    with open(file, 'r') as f:
        cur.copy_expert(sql=copy_sql, file=f)
#        conn.commit()
#        cur.close()
        #logger.info(f'FINISH: {copy_sql}')
        
@log_function_call(logger)
def insert_into_psql(type, tb_name, cycle_date, cur):
    #cur = conn.cursor()
    insert_sql = f"INSERT INTO bedim.af_white_list_cycle_date (table_db_name, table_name, cycle_date, table_type) \
    VALUES('cmsi', '{tb_name}', '{cycle_date}', {type})\
    on conflict (table_db_name, table_name) \
    do update set cycle_date = {cycle_date};"
    cur.execute(insert_sql)
    #conn.commit()
    #cur.close()
    #logger.info(f'FINISH: {insert_sql}')
        
        
if __name__ == '__main__':
    conn = psycopg2.connect('postgresql://cpuser:cpuser@192.168.94.74:10300/cptest')
