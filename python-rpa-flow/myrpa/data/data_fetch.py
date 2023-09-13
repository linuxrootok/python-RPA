import requests
#from dbutil.db_action import insert_account
from req.req_get_account import run
from config.config import api_get_account_url, api_set_account_url

async def get_account_via_api(data):
    # 请求API 获取数据后贮存
    #requests.post(api)
    '''
    account = 'zhonghuohua'
    password = 'Aa123456*'

    '''
    print(f"传递给登录页面的数据:{data}")

    '''
    data = {"key": "value"}
    res = await run(api_get_account_url, data)
    print(f"现在请求的API的url是:{api_get_account_url}")
    print(res)

    '''
    # 伪代码
    #　正式运行时　account, password从res变量中获取
    # acoount,password = res

    #　入库
    #insert_account(res)

    account = data['username']
    password = data['password']

    # 返回用户名密码
    return [account, password]