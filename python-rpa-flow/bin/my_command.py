import requests, json, sys

import argparse

import urllib3
urllib3.disable_warnings()

def _getData(mark):
    #print(f"命令参数是: {mark}")    
    data = {
        "companyName": "广州诗尼曼家居股份有限公司",
        "sysLoginUrl": "https://gzsm.org.cn/js/a/login",
        "gateName": "广州市建设领域管理应用信息平台",
        "companyId": 1002352,
        "password": "Aa123456*",
        "mainContractor": 1,
        "projectNo": "2305231750021897734",
        #"is_cron": False,
        "is_cron_new": True,
        "callbackUrl": "https://dev-szjg-api-web.cwdsp.com/v1/craftsman/project/check3rdAccountAndPassword",
        "govSysProjectName": "欧昊集团总部大楼地下室及东塔项目",
        "gateNo": "ZJ001",
        "projectName": "新年分包项目一v1001T8",
        "username": "zhonghuohua"
    }
    #data['is_cron'] = False
    if mark == 'restart':
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        url = 'https://dev-szjg-rpa-account.cwdsp.com/restart'
        response = requests.post(url, data=json.dumps(data), headers=headers, verify=False)
        print(response.content)
        sys.exit()

    if mark == 'check':

        data['is_cron_new'] = False

    if mark == 'fetch':

        data['is_cron_new'] = True

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    url = 'https://dev-szjg-rpa-account.cwdsp.com/accountVerify'
    response = requests.post(url, data=json.dumps(data), headers=headers, verify=False)
    print(response.content)

def getData():
    parser = argparse.ArgumentParser()
    parser.add_argument('arg1', help='first argument')
    #parser.add_argument('arg2', help='second argument')
    args = parser.parse_args()

    _getData(args.arg1)
