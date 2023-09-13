import os
browserDataPath = os.path.dirname(__file__)
userDataDir = browserDataPath+'/'+'user_data_dir3'
#chromeExePath = 'C:/Users/Administrator/AppData/Local/Google/Chrome/Application/chrome2.exe'
chromeExePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
from .serverConfig import BROWSER_HEADLESS
lunchParam = {
    'ignoreHTTPSErrors': True,
    'autoClose': False,
    'headless': BROWSER_HEADLESS, 
    'devtools': False, 
    "handleSIGINT": True,
    "handleSIGTERM": True,
    "handleSIGHUP": True, 
    'args': ["--log-level=3", "--disable-gpu", "--disable-infobars", '-–incognito'],
    'dumpio': True, 
    'autoClose': False, 
    'defaultViewport': {'width': 1366, 'height': 768},
    'ignoreDefaultArgs': ["--enable-automation"], 
    'userDataDir': userDataDir,
    #'executablePath':chromeExePath
}
#身份认证,指定身份排队
idcard = {'id':0}

#session value
session_value = 0

#goto base 开关
gotobase_on = True


base_url = {
    'index': '', 
    'ZJ001': '', 
    '10001': '',

    '10002': '',
    '10003': '',
    '10004': '',
}

#并发开关 限制浏览器在执行当前任务流程时 其他流程请求将收到busy状态提醒(filter_on=False)
filter_on = False 
filter_array = ['data_filter_ready']

filter_idcard_on = False
filter_idcard_array = ['data_filter_idcard_ready']

extract_on = True
extract_array = ['extract_data_ready']



#EVENT
# 寻找控件的最长时间(每次的粒度为0.1)，100次则是10秒
ELE_TIMEOUT = 100
EVENT_CALL_LATER_TIMEOUT_FLASH = 1
EVENT_CALL_LATER_TIMEOUT = 2


'''API'''
# 请求帐号信息以作登录验证
api_get_account_url = ''

# 请求设置帐号状态，可用或不可用
api_set_account_url = 'https://test'

# 请求传输班组信息
api_set_class_url = ''


# 请求班组信息，依据不同的项目
api_get_class_url = ''


# 数据同步模块

# 每次同步间隔时间
TIME_WAIT_SYNC = 60
