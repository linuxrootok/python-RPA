#-*-coding:utf-8-*-

from datetime import datetime
import re
#from common import *
#from baseobj import *
#from . import config
import logutil
import dbutil
#import serverConfig
from pymysql.converters import escape_string   # escape_string函数用来转义json类型数据


def insert_account(data):
    dbHandler = dbutil.gdDBSQL
    print('准备插入数据')
    


    now = datetime.now()
    formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")

    project_id = data.get('projectNo','')
    project_name = data.get('projectName','')
    gate_code = data.get('gateNo','')
    gate_name = data.get('gateName','')
    account = data.get('username','')
    password = data.get('password','')

    backend_url = data.get('sysLoginUrl','')
    system_name = data.get('govSysProjectName','')
    main_contractor = data.get('mainContractor','')

    company_id = data.get('companyId','')
    company_id = data.get('companyId','')
    status = data.get('status', 0)


    '''插入用户'''
    sql = f"INSERT INTO `tbl_account` (`project_no`, `project_name`, `gate_no`, `gate_name`,`username`, `password`, `sys_login_url`, `gov_sys_project_name`, `create_time`, `update_time`, `status`, `main_contractor`, `company_id`) VALUES ('{project_id}', '{project_name}', '{gate_code}', '{gate_name}','{account}', '{password}','{backend_url}','{system_name}', '{formatted_date_time}', '{formatted_date_time}', '{status}', '{main_contractor}', '{company_id}')"

    insert_id = dbHandler.execute_commit(sql)

    if insert_id:
        print(f"最后插入数据的ID:{insert_id}")

    else:
        print(f"插入数据没有成功:{insert_id}")
     
    return insert_id

def fetch_account(project_no=0, company_id=0):
    dbHandler = dbutil.gdDBSQL
    sqlExt = ''    
    if all((project_no, company_id)):
        sqlExt = f" AND project_no='{project_no}' and company_id='{company_id}'"
    
    sql = f"SELECT * FROM tbl_account WHERE (gate_no, update_time) IN (SELECT gate_no, MAX(update_time) FROM tbl_account WHERE status=1 {sqlExt} GROUP BY project_no, company_id) ;"

    logutil.log('browser', f"查询数据匹配sql语句:{sql}")
    account = dbHandler.execute_sql(sql)
    #print(account)
    return account

def update_account(account_id):
    dbHandler = dbutil.gdDBSQL

    sql_updata = f"UPDATE `tbl_account` SET `status`='1' WHERE `id`='{account_id}';"
    dbHandler.execute_commit(sql_updata)

    sql_select = f"select status from `tbl_account` where id='{account_id}';"
    account = dbHandler.execute_sql(sql_select)
    #account = dbHandler.get_one_data()
    print(f"account数据更新后: {account}")
    return account

# TODO 更新数据
def update_account_all(account_id, data, status):
    dbHandler = dbutil.gdDBSQL

    
    now = datetime.now()
    formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")

    project_id = data.get('projectNo','')
    project_name = data.get('projectName','')
    gate_code = data.get('gateNo','')
    gate_name = data.get('gateName','')
    account = data.get('username','')
    password = data.get('password','')

    backend_url = data.get('sysLoginUrl','')
    system_name = data.get('govSysProjectName','')
    main_contractor = data.get('mainContractor','')

    company_id = data.get('companyId','')


    sql_updata = f"UPDATE `tbl_account` SET `project_no`='{project_id}', `project_name`='{project_name}', `gate_no`= '{gate_code}', `gate_name`='{gate_name}', `username`='{account}', `password`='{password}', `sys_login_url`='{backend_url}', `gov_sys_project_name`='{system_name}', `main_contractor`='{main_contractor}', `status`='{status}',`company_id`='{company_id}',`update_time`='{formatted_date_time}' WHERE `id`='{account_id}'"

    dbHandler.execute_commit(sql_updata)

    return True


def load_action_user_table(data):
    '''判断列表有没有工人数据'''
    dbHandler = dbutil.gdDBSQL
    

