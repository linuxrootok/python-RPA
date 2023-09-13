import asyncio
import json
import requests
from .config import CLASS_DATA_PATH
from req.req_get_account import run
from config.config import api_get_class_url
from config.serverConfig import API_SET_CLASS_URL

from logutil.exceptions import log_exception
import logutil

def save_to_file(data):
    """将数据保存到文件"""
    with open(CLASS_DATA_PATH, 'w') as f:
        f.write(str(data))

async def extract_data_classes(page, project_ids, src_data):
    pageCookies = await page.cookies()
    #logutil.log('browser',f"cookie is {pageCookies}")

    session_id = [d['value'] for d in pageCookies if d['name'] == 'jeesite.session.id'][0]

    #logutil.log('browser',f"seeion_id is {session_id}")
    cookies = {
        'jeesite.session.id': session_id,
        'loginType': '1',
        'formLayerModel': 'true',
        'pageSize': '',
        'currentMenuCode': '1421809497242624000',
        'pageNo': '1',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'jeesite.session.id=70ba6f0c352644ecabd79220f284c095; loginType=1; formLayerModel=true; pageSize=12; currentMenuCode=1421809497242624000; pageNo=1',
        'Origin': 'https://gzsm.org.cn',
        'Referer': 'https://gzsm.org.cn/js/a/smz/smzTeam/list',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    # 枚举所有project_id下所有的班组信息
    for project_id in project_ids:
        data = {
            'state': '',
            'projectId': project_id,
            'key': '',
            'pageNo': '1',
            'pageSize': '50',
            'orderBy': '',
        }

        response = requests.post(api_get_class_url, cookies=cookies, headers=headers, data=data)

        # 从响应中提取数据
        #data = extract_data(response.text)      
        # 保存到文件
        #save_to_file(response.text)

        logutil.log('browser', f"发送给接口2从网站上获取到的班组数据:{response.text}")

        #　转发此数据给接口
        data_class = json.loads(response.text)
        if data_class.get('message', None) == None:


            data_class['szCompanyId'] = src_data['companyId'] 
            data_class['szProjectNo'] = src_data['projectNo'] 

            logutil.log('browser', f"url={API_SET_CLASS_URL}|准备发送班组数据:{data_class}")
            res = await run(API_SET_CLASS_URL, json.dumps(data_class))
            logutil.log('browser',f"res类型:{type(res)}")
            logutil.log('browser',f"请求德恩的ＡＰＩ返回:{res}")

            logutil.log('console', res)
            result_dict = json.loads(res)
            if result_dict.get('code', 0) == 200:
                logutil.log('browser',f"推送班级信息成功了")
                logutil.log('console', '推送班组信息成功！')

        await asyncio.sleep(1)

