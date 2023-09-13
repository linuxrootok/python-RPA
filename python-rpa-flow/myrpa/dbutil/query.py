#-*-coding:utf-8-*-

import re
from common import *
from baseobj import *
from . import config
import logutil
import dbutil
import serverConfig
from pymysql.converters import escape_string   # escape_string函数用来转义json类型数据
from copy import deepcopy
import json

class Query(object):
    """
    查询数据库表，插入最新数据
    """
    def __init__(self, data):
        self._data = data
        self._db = dbutil.gdDBSQL
        self._id_project = None
        self._id_gate = None
        self._gate_name = None
        self._id_company = None
        self._id_team = None
        self._id_class = None
        self._project_no = self._data.get("projectNo", "0")
        self._gate_no    = self._data.get("gateNo", "0")
        self._idcard    = self._data.get("idcard", "0")
        self._id_user = None
    
    def gate_no(self):
        sql = "SELECT * FROM `tbl_gate_producer` WHERE `gate_no` = '%s';" % (self._data.get("gateNo", "0"))
        tab_data = self._db.execute_sql(sql)
        
        if not tab_data:
            return False
        else:
            self._id_gate = tab_data[0][0]
            self._gate_name = tab_data[0][2]
        return True

    def gate_name(self):
        return self._gate_name

    def project_no(self):
        self.gate_no()
        sql = "SELECT * FROM `tbl_project` WHERE `gate_no` = '%s' and `project_no` = '%s' LIMIT 0,10;" % (self._data.get("gateNo", "0"), self._data.get("projectNo", "0"))
        tab_data = self._db.execute_sql(sql)
        if not tab_data:
            return False
        else:
            self._id_project = tab_data[0][0]
        return True

    def project_name(self):
        pass

    def company_no(self):
        if not self.project_no():
            return False
        if not self._id_project:
            return False
        sql = "SELECT * FROM `tbl_sub_company` WHERE `project_id` = '%s' and `sub_company` = '%s' and `is_create` = 1 LIMIT 0,10;" % (self._id_project, self._data.get("subCompany", "0"))
        tab_data = self._db.execute_sql(sql)
        if not tab_data:
            return False
        else:
            self._id_company = tab_data[0][0]
        return True

    def team_no(self, is_create=1):
        if not self.company_no():
            return False
        if not self._id_company:
            return False
        if is_create == 1:
            sql = "SELECT * FROM `tbl_team` WHERE `sub_company_id` = '%s' and `team` = '%s' and `is_create` in (1, 2) LIMIT 0,10;" % (self._id_company, self._data.get("subCompany", "0"))
        elif is_create == 2:
            sql = "SELECT * FROM `tbl_team` WHERE `sub_company_id` = '%s' and `team` = '%s' and `is_create` in (2) LIMIT 0,10;" % (self._id_company, self._data.get("subCompany", "0"))
        tab_data = self._db.execute_sql(sql)
        if not tab_data:
            return False
        else:
            self._id_team = tab_data[0][0]
        return True

    def class_no(self):
        if not self.team_no():
            return False
        if not self._id_team:
            return False
        sql = "SELECT * FROM `tbl_class` WHERE `team_id` = '%s' and `class` = '%s' and `is_create` = 1 LIMIT 0,10;" % (self._id_team, self._data.get("subClass", "0"))
        tab_data = self._db.execute_sql(sql)
        if not tab_data:
            return False
        else:
            self._id_class = tab_data[0][0]
        return True

    def insert_company(self):
        sql = "SELECT * FROM `tbl_sub_company` WHERE `project_id` = '%s' and `sub_company` = '%s' LIMIT 0,10;" % (self._id_project, self._data.get("subCompany", "0"))
        tab_data = self._db.execute_sql(sql)
        if tab_data:
            return True

        create_time = datetime_str()
        
        sql = "INSERT INTO `tbl_sub_company` (`project_id`, `sub_company`, `is_create`, `create_time`) VALUES (%d, '%s', %d, '%s');" \
            %(self._id_project, self._data.get("subCompany", "0"), 0, create_time)
        
        tab_data = self._db.execute_commit(sql)
        if tab_data == True:
            return True
        return False
    
    def update_company(self):
        update_time = datetime_str()
        
        sql = "UPDATE `tbl_sub_company` SET `is_create` = 1,`update_time`='%s' WHERE `project_id` = '%s' and `sub_company` = '%s';" \
            %(update_time, self._id_project, self._data.get("subCompany", "0"))
        
        tab_data = self._db.execute_commit(sql)
        self.company_no()
        if tab_data == True:
            return True
        return False

    def insert_team(self):
        sql = "SELECT * FROM `tbl_team` WHERE `sub_company_id` = '%s' and `team` = '%s' LIMIT 0,10;" % (self._id_company, self._data.get("subCompany", "0"))
        tab_data = self._db.execute_sql(sql)
        if tab_data:
            return True

        create_time = datetime_str()

        if not self._id_company:
            return False
        
        sql = "INSERT INTO `tbl_team` (`sub_company_id`, `team`, `is_create`, `create_time`) VALUES (%d, '%s', %d, '%s');" \
            %(self._id_company, self._data.get("subCompany", "0"), 0, create_time)
        
        tab_data = self._db.execute_commit(sql)
        if tab_data == True:
            return True
        return False
    
    def update_team(self, status):
        '''status: 
            0 = 创建失败
            1 = 创建成功
            2 = 队伍入场成功
        '''
        update_time = datetime_str()
        
        sql = "UPDATE `tbl_team` SET `is_create` = '%s',`update_time`='%s' WHERE `sub_company_id` = '%s' and `team` = '%s';" \
            %(status, update_time, self._id_company, self._data.get("subCompany", "0"))
        
        tab_data = self._db.execute_commit(sql)
        self.team_no()
        if tab_data == True:
            return True
        return False

    def insert_class(self):
        sql = "SELECT * FROM `tbl_class` WHERE `team_id` = '%s' and `class` = '%s' LIMIT 0,10;" % (self._id_team, self._data.get("subClass", "0"))
        tab_data = self._db.execute_sql(sql)
        if tab_data:
            return True
        
        create_time = datetime_str()
        
        sql = "INSERT INTO `tbl_class` (`team_id`, `class`, `is_create`, `create_time`) VALUES (%d, '%s', %d, '%s');" \
            %(self._id_team, self._data.get("subClass", "0"), 0, create_time)
        
        if not self._id_team:
            return False
        
        tab_data = self._db.execute_commit(sql)
        if tab_data == True:
            return True
        return False
    
    def update_class(self):
        '''更新班组'''
        update_time = datetime_str()
        
        sql = "UPDATE `tbl_class` SET `is_create` = 1,`update_time`='%s' WHERE `team_id` = '%s' and `class` = '%s';" \
            %(update_time, self._id_team, self._data.get("subClass", "0"))
        
        tab_data = self._db.execute_commit(sql)
        self.class_no()
        if tab_data == True:
            return True
        return False

    def user_no(self, is_create=1):
        '''查询用户'''
        if not self.class_no():
            return False
        sql = "SELECT * FROM `tbl_user` WHERE `project_no` = '%s' and `gate_no` = '%s' and `idcard` = '%s' and `is_create` = %d LIMIT 0,10;" % (self._project_no, self._gate_no, self._idcard, is_create)
        tab_data = self._db.execute_sql(sql)
        
        if not tab_data:
            return False
        else:
            self._id_user = tab_data[0][0]
        return True

    def insert_user(self):
        '''插入用户'''
        sql = "SELECT * FROM `tbl_user` WHERE `project_no` = '%s' and `gate_no` = '%s' and `idcard` = '%s' LIMIT 0,10;" % (self._project_no, self._gate_no, self._idcard)
        tab_data = self._db.execute_sql(sql)
        if tab_data:
            return True
        
        create_time = datetime_str()
        project_no = self._data.get("projectNo", "0")
        project_name = self._data.get("projectName", "0")
        gate_no = self._data.get("gateNo", "0")
        gate_name = self._data.get("gateName", "0")
        username = self._data.get("username", "0")
        idcard = self._data.get("idcard", "0")
        
        sql = "INSERT INTO `tbl_user` (`project_no`, `project_name`, `gate_no`, `gate_name`,`username`, `idcard`, `is_create`, `create_time`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', 0, '%s');" \
            %(project_no, project_name, gate_no, gate_name, username, idcard, create_time)
        
        tab_data = self._db.execute_commit(sql)
        if tab_data == True:
            return True
        return False

    def update_user(self, is_create=1):
        '''更新用户'''
        update_time = datetime_str()
        project_no = self._data.get("projectNo", "0")
        project_name = self._data.get("projectName", "0")
        gate_no = self._data.get("gateNo", "0")
        gate_name = self._data.get("gateName", "0")
        username = self._data.get("username", "0")
        idcard = self._data.get("idcard", "0")
        
        sql = "UPDATE `tbl_user` SET `is_create` = %d,`update_time`='%s' WHERE `project_no` = '%s' and `gate_no` = '%s' and `idcard` = '%s';" \
            %(is_create, update_time, project_no, gate_no, idcard)
        
        tab_data = self._db.execute_commit(sql)
        if tab_data == True:
            return True
        return False
    

def load_action_user_table(data):
    '''判断列表有没有工人数据'''
    dbHandler = dbutil.gdDBSQL
    idcard = data.get('idcard', '0')
    action = data.get('action', '0')
    project_no = data.get('projectNo', '0')
    gate_no = data.get('gateNo', '0')

    sql = f"SELECT * FROM `tbl_gate_add_user` WHERE `project_no` = '{project_no}' and `gate_no` = '{gate_no}' and `idcard` = '{idcard}' \
        and `action` = '{action}' and `action_status` not in ('1') LIMIT 0,10;"
    tab_data = dbHandler.execute_sql(sql)
    if not tab_data:
        return False
    else:
        data["qId"] = tab_data[0][0]
    return data

def insert_action_user_table(data):
    '''在表中插入一条工人数据'''
    dbHandler = dbutil.gdDBSQL
    create_time = datetime_str()
    username = data.get('username', '0')
    idcard = data.get('idcard', '0')
    action = data.get('action', '0')
    project_no = data.get('projectNo', '0')
    project_name = data.get('projectName', '0')
    gate_no = data.get('gateNo', '0')
    gate_name = data.get('gateName', '0')
    json_nfo = json.dumps(data)

    sql = f"INSERT INTO `tbl_gate_add_user` (`project_no`, `project_name`, `gate_no`, `gate_name`,`username`, `idcard`, `action`, `action_status`, `action_running`, `browser`, `send`, `times`, `create_time`, `info`) VALUES \
        ('{project_no}', '{project_name}', '{gate_no}', '{gate_name}', '{username}', '{idcard}', '{action}', '0', '0', '0', '0', 0, '{create_time}',"
    
    sql_2 = "'{json1}');"
    
    sql = sql + sql_2
    
    sql = sql.format(json1=escape_string(json_nfo)) 
    tab_data = dbHandler.execute_commit(sql)
    if tab_data == True:
        return True
    return False

def insert_user_info(data):
    '''在表中插入一条工人信息'''
    dbHandler = dbutil.gdDBSQL
    create_time = datetime_str()
    username = data.get('username', '0')
    idcard = data.get('idcard', '0')
    action = data.get('action', '0')
    project_no = data.get('projectNo', '0')
    project_name = data.get('projectName', '0')
    gate_no = data.get('gateNo', '0')
    gate_name = data.get('gateName', '0')
    json_nfo = json.dumps(data)

    sql = f"INSERT INTO `tbl_user_info` (`project_no`, `project_name`, `gate_no`, `gate_name`,`username`, `idcard`, `action`, `create_time`, `info`) VALUES \
        ('{project_no}', '{project_name}', '{gate_no}', '{gate_name}', '{username}', '{idcard}', '{action}','{create_time}',"
    
    sql_2 = "'{json1}');"
    
    sql = sql + sql_2

    
    sql = sql.format(json1=escape_string(json_nfo)) 

    tab_data = dbHandler.execute_commit(sql)
    if tab_data == True:
        return True
    return False


def load_action_user_info():
    '''取出工人数据，判断列表有没有工人数据'''
    dbHandler = dbutil.gdDBSQL
    project_no = serverConfig.PROJECT_NO
    gate_no = serverConfig.GATE_NO
    data = {}
    times = 10

    sql = f"SELECT * FROM `tbl_gate_add_user` WHERE `project_no` = '{project_no}' and `gate_no` = '{gate_no}' \
        and `action_status` not in ('1') and `action_running` not in ('1') and `times` <= {times} ORDER BY id ASC LIMIT 0,10;"
    
    tab_data = dbHandler.execute_sql(sql)
    if not tab_data:
        return False
    
    qData = list(deepcopy(tab_data[0]))
    
    data['id']           = qData[0]
    data['project_no']   = qData[1]
    data['project_name'] = qData[2]
    data['gate_no']      = qData[3]
    data['gate_name']    = qData[4]
    data['username']     = qData[5]
    data['idcard']       = qData[6]
    data['action']       = qData[7]
    data['action_status']  = qData[8]
    data['action_running'] = qData[9]
    data['browser']      = qData[10]
    data['send']         = qData[11]
    data['times']        = qData[12]
    data['info']         = json.loads(qData[13])
    data['flow']         = qData[14]
    data['create_time']  = qData[15]
    data['update_time']  = qData[16]
    return data

def update_action_user_status(data, status, count=False):
    '''更新工人动作的状态'''
    dbHandler = dbutil.gdDBSQL
    id = data.get('id', None)
    times = data.get('times', 1)
    if count:
        times = data.get('times', 1)+1
    else:
        times = data.get('times', 1)

    if not id:
        return False

    sql = f"UPDATE `tbl_gate_add_user` SET `action_running` = '{status}',`times` = {times} WHERE `id` = {id}"
    
    tab_data = dbHandler.execute_commit(sql)
    if tab_data == True:
        return True
    return False
# data 2, 1
def update_user_results(data, status, action_status):
    '''更新工人最后的动作的状态
    status:1=运行中, 2=运行完毕
    action_status:1=成功, 2=失败, 3=异常
    '''
    dbHandler = dbutil.gdDBSQL
    id = data.get('id', None)
    if not id:
        return False

    sql = f"UPDATE `tbl_gate_add_user` SET `action_running` = '{status}',`action_status` = '{action_status}' WHERE `id` = {id};"
    
    tab_data = dbHandler.execute_commit(sql)
    if tab_data == True:
        return True
    return False
