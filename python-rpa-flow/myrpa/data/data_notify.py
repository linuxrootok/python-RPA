import json
from req.req_get_account import run
import logutil
from config.serverConfig import API_FEEDBACK_DATA_SYNC

async def notify_data():
    pass

async def feedback(data, res):
    print(f"准备请求的data:{data}")
    #api_feedback_url = 'https://dev-szjg-api-web.cwdsp.com/v1/craftsman/project/check3rdAccountAndPassword'

    api_feedback_url = data['callbackUrl']


    if res['code'] == 200:
        statusCode = 1
    elif res['code'] in (500,501):
        statusCode = 2
    elif res['code'] == 502: 
        statusCode = 0

    status = {
        'projectNo': data['projectNo'],
        'companyId': data['companyId'],
        'mainContractor': data['mainContractor'],
        'accountCheckStatus': statusCode,
        'accountCheckDesc': res['msg']
    }
    logutil.log('browser', f"准备接口１请求第三方的数据是:{status}")

    result = await run(api_feedback_url, json.dumps(status))
    return result
    logutil.log('browser', f"接口１反馈结果请求后的响应:{result}")

async def feedback_data_center(data, res):

    print(f"准备请求的data:{data}")
    #api_feedback_url = 'https://dev-szjg-api-web.cwdsp.com/v1/craftsman/project/check3rdAccountAndPassword'

    api_feedback_url = API_FEEDBACK_DATA_SYNC

    statusCode = None
    msg = ''

    if res['code'] == 200:
        statusCode = 1
        msg = '成功'
    else:
        statusCode = 0
        msg = '失败'

    #elif res['code'] in (500,501):
        #statusCode = 2
    #elif res['code'] == 502: 
        #statusCode = 0


    # 更新状态及结果
    data['status'] = statusCode
    data['msg'] = msg


    logutil.log('console', f"[接口3]===>准备请求第三方的数据是:{data}")

    result = await run(api_feedback_url, json.dumps(data))
    return result
    logutil.log('console', f"[接口3]<===反馈结果请求后的响应:{data}")

    