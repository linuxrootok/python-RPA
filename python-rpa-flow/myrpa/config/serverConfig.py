# !/usr/bin/env python
# -*- coding:utf-8 -*-# 

import platform

# 服务端口
SERVER_PORT = 33008

# 服务端地址
SERVER_ADDR = 'http://127.0.0.1'

API_RPA_CENTER = ''

# 获取项目进、出场基本信息
API_GET_PROJECT_BASIC = API_RPA_CENTER+'/rpa/center/getProjectInfo'

# 获取项目出、进场详细信息
API_GET_PROJECT_DATA = API_RPA_CENTER+'/rpa/center/pullRouteData'

# 获取项目方登录谁信息[用户名密码]
API_GET_PROJECT_AUTH = ''
#　反馈地址，RPA操作结果
API_FEEDBACK_ROUTE = 'http://10.1.18.16:6012/rpa/route/rpaResultCallback'

################

API_FEEDBACK_DATA_SYNC = ''

# 请求传输班组信息
API_SET_CLASS_URL = ''

# 前台启动-False，后台启动-True
BROWSER_HEADLESS = False

# 数据库配置
if '6.1.7601' == platform.version():
    # 数据库配置(本地)
    host         = ""
    username     = "rpa" 
    password     = ""  
    port         = 63753 
    database     = "rpa"
else:
    host         = ""
    username     = "rpa" 
    password     = ""  
    port         = 3306 
    database     = "rpa"