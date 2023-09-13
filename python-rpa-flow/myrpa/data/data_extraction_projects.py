import json
import requests
from .config import PROJECT_DATA_PATH

import urllib3
urllib3.disable_warnings()

import logutil

def save_to_file(data):
    """将数据保存到文件"""
    with open(PROJECT_DATA_PATH, 'w') as f:
        f.write(str(data))

async def extract_data_projects(page, myData):
    pageCookies = await page.cookies()
    #logutil.log('browser',f"cookies => {pageCookies}")

    session_id = [d['value'] for d in pageCookies if d['name'] == 'jeesite.session.id'][0]
    
    #logutil.log('browser',f"seeion_id is {session_id}")
    cookies = {
        'jeesite.session.id': session_id,
        'loginType': '1',
        'formLayerModel': 'true',
        'pageSize': '12',
        'currentMenuCode': '1421809497242624000',
    }
    #logutil.log('browser',f"project数据获取时的cookies: {cookies}")
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'jeesite.session.id=7196c4423ed1487ca8aa90272d46ab62; loginType=1; formLayerModel=true; pageSize=12; currentMenuCode=1421812060734119936',
        'Origin': 'https://gzsm.org.cn',
        'Referer': 'https://gzsm.org.cn/js/a/smz/smzProjectAdmin/listProject',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {}

    data = {
        'key': '',
        #'adminId': '129506',
        'loginCode': '',
        'director': '',
        'jobType': '',
        'pageNo': '',
        'pageSize': '',
        'orderBy': '',
    }

    response = requests.post('https://gzsm.org.cn/js/a/smz/smzProjectAdmin/listProjectData?detailsType=', params=params, cookies=cookies, headers=headers, data=data)


    # 从响应中提取数据
    #data = extract_data(response.text)      
    # 保存到文件
    #save_to_file(response.text)

    #logutil.log()
    

    #　返回此数据给班组数据采集
    project_ids = None
    data_projects = json.loads(response.text)
    if data_projects.get('message', None) == None:



        project_ids = [item['projectId'] for item in data_projects['list'] if item['projectName'] == myData['govSysProjectName']]
        project_names = [item['projectName'] for item in data_projects['list']]
        
    return project_ids,project_names