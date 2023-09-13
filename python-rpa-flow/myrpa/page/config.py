'''login测试帐号,仅作测试，实际不用'''
username = 'zhonghuohua'
password = 'Aa123456*'

#　登录输入框xpath
loginObj = {
    'index':{
        'loginUrl':'https://gzsm.org.cn/js/a/login',
        'userInputXpath':'//*[@id="username"]',
        'passInputXpath':'//*[@id="password"]',
        'validcodeXpath':'//*[@id="validCode"]',
        'loginXpath'    :'//*[@id="btnSubmit"]',
        'logoutUrl': 'https://gzsm.org.cn/js/a/logout',
        'loginSuccessedTitle':'广州市建设领域管理应用信息平台',
        'loginDelay': 2,
        'is_captcha': True,
    },
    # 住建
    'ZJ001':{
        'loginUrl':'https://gzsm.org.cn/js/a/login',
        'userInputXpath':'//*[@id="username"]',
        'passInputXpath':'//*[@id="password"]',
        'validcodeXpath':'//*[@id="validCode"]',
        'loginXpath'    :'//*[@id="btnSubmit"]',
        'logoutUrl': 'https://gzsm.org.cn/js/a/logout',
        'loginSuccessedTitle':'广州市建设领域管理应用信息平台',
        'loginDelay': 2,
        'is_captcha': True,
    },
    # 九象
    'ZJ002':{
        'loginUrl':'http://jiuxiang.9xsmart.com/?code=tmNZIG#/home/index',
        'userInputXpath':'//*[@id="app"]/div/div/div[2]/form/div[1]/div/div[1]/input',
        'passInputXpath':'//*[@id="app"]/div/div/div[2]/form/div[2]/div/div[1]/input',
        'validcodeXpath':'',
        'loginXpath'    :'//*[@id="app"]/div/div/div[2]/form/div[3]/div/button/span',
        'loginSuccessedTitle':'智慧工地',
        'loginSuccessedMark':'//*[@id="app"]/div/div[1]/div[1]/div',
        'logoutUrl': 'https://smart-oauth.9xsmart.com/logout?redirect_uri=http://jiuxiang.9xsmart.com',
        'loginDelay': 10,
        'is_captcha': False,
    },

    'ZJ003':{
        'loginUrl':'https://gzsm.org.cn/js/a/login',
        'userInputXpath':'//*[@id="username"]',
        'passInputXpath':'//*[@id="password"]',
        'validcodeXpath':'',
        'loginXpath'    :'//*[@id="wrap"]/div/div[2]/div[2]/div/input',
        'loginSuccessedTitle':'泥蜂管理系统',
        'logoutUrl': 'https://www.nifengss.com/zgz/a/logout',
        'loginDelay': 10,
        'is_captcha': True,
    },
    'ZJ004':{
        'loginUrl':'https://gzsm.org.cn/js/a/login',
        'userInputXpath':'//*[@id="app"]/div/div/div[2]/form/div[1]/div/div[1]/input',
        'passInputXpath':'//*[@id="app"]/div/div/div[2]/form/div[2]/div/div[1]/input',
        'validcodeXpath':'',
        'loginXpath'    :'//*[@id="app"]/div/div/div[2]/form/div[3]/div/button/span',
        'loginSuccessedTitle':'智慧工地',
        'loginDelay': 10,
        'is_captcha': True,
    },
    'ZJ005':{
        'loginUrl':'https://gzsm.org.cn/js/a/login',
        'userInputXpath':'//*[@id="app"]/div/div/div[2]/form/div[1]/div/div[1]/input',
        'passInputXpath':'//*[@id="app"]/div/div/div[2]/form/div[2]/div/div[1]/input',
        'validcodeXpath':'',
        'loginXpath'    :'//*[@id="app"]/div/div/div[2]/form/div[3]/div/button/span',
        'loginSuccessedTitle':'智慧工地',
        'loginDelay': 10,
        'is_captcha': True,
    },
}
