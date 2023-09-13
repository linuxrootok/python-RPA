import asyncio
import aiohttp
import json
import sys

from req.asyncHttpRequest import AsyncHttpRequest
from config.serverConfig import API_GET_PROJECT_BASIC, API_GET_PROJECT_DATA, API_FEEDBACK_ROUTE, API_GET_PROJECT_AUTH, SERVER_ADDR, SERVER_PORT
from .data_convert import convert_data
from config.config import TIME_WAIT_SYNC
import logutil
from .data_noneError import NoneError
from .data_check_and_retry import check_data_retry
from data import PATH_DATA_UPLOADS, ensure_directory_exists
from .data_file_download import download_file
from data import get_event_source, traslate_data

# 获取项目基础参数
@check_data_retry(5)
async def get_project_event(url, req_data, remark='获取数据'):
    logutil.log('browser', f'测试中...')
    request = AsyncHttpRequest(url)
    headers = {"Content-Type": "application/json"}
    status = 0
    res = None
    resDict = None
    try:
        status, res = await request.post(data=json.dumps(req_data), headers=headers)
    except Exception as e:
        logutil.log('browser', f"网络错误:{e}")
    if status != 200:
        logutil.log('browser', f"请求API无法到达!大概是网络有问题")
    if res:
        resDict = json.loads(res)
    return resDict

async def get_event_data(url, req_data):

    data = {
        'companyId': None,
        'projectName': None,
        'sysCode': None,
        'orderNo': None,
    }
    logutil.log("console",f"协程运行中")
    res = None
    while True:
        logutil.log('browser', f"第一步,重新获取基本数据")
        try:
            res = await get_project_event(API_GET_PROJECT_BASIC, req_data, '获取初始数据')
            # TODO 这里可能要处理记录的company_id和project_no 
            print(res)
            infoData = res.get('data', None)
            print(infoData)
            if infoData:
                data['companyId'] = infoData['companyId']
                data['projectName'] = infoData['projectName']
                data['sysCode'] = infoData['sysCode']
                data['orderNo'] = infoData['orderNo']
            else:
                await asyncio.sleep(3)
                continue
            #await asyncio.sleep(1000000)
        except NoneError:
            logutil.log('browser', f'获取的数据为空!')
            continue
        logutil.log('browser', f"获取到的基础数据：{res},类型:{type(res)}")
        # 获取进/出场数据详细
        download_status = [True]
        for k,v in data.items():
            if v == None:
                logutil.log('browser', f"准备的参数不全，无法继续执行，正在返回循环体重试上一个步骤")
                continue
        req_data = data
        if req_data.get('projectName', None):
            del(req_data['projectName'])
        logutil.log('browser', f"正在准备进出场数据的请求:{req_data}")
        is_main_loop = False
        await asyncio.sleep(1)
        enter_data = req_data
        while True:
            logutil.log('browser', f"第二步，正在收集进出场数据的请求")
            try:
                res = await get_project_event(API_GET_PROJECT_DATA, enter_data, '获取进出场数据')
                logutil.log('browser', f"获取到的进出场数据:{res},类型:{type(res)}")
                # TODO预处理接口获取的数据
                _eventData = res.get('data', None)
                if _eventData:
                    feedbackId = _eventData.get('id', None)
                    logutil.log('browser', f"收集到进出场数据:{_eventData},类型:{type(_eventData)}")
                    if isinstance(_eventData, str):
                        _data = json.loads(_eventData)
                    elif isinstance(_eventData, dict):
                        _data = _eventData
                    else:
                        logutil.log('browser', f"出入场获取到的数据类型错误")    
                    resDict = await traslate_data(_data)
                    logutil.log('browser', f"出入场所需的实际数据.{resDict}")    
                    idCard = resDict.get('idcard', None)
                    for k,v in resDict.items():
                        if k in 'Path':
                            has_failed = False
                            for x in range(3):
                                srcName, srcPath = get_event_source(v, idCard)
                                if not all((srcName, srcPath)):
                                    download_status.append(False)
                                    has_failed = True
                                    continue
                                else:
                                    if has_failed:
                                        download_status.pop()
                                        download_status.append(True)
                                    break
                else:
                    logutil.log('browser', f"进出场数据为空")
                    break
                # 获取登入后台管理的用户名密码
                req_data = {}
                projectNo = data.get('projectNo', None)
                companyId = str(data.get('companyId', None))
                req_data = {
                    'projectNo': projectNo, 
                    'companyId': companyId,
                }
                try:
                    logutil.log('browser', f"开始获取用户名和密码！")
                    authData = None
                    username = None
                    password = None
                    res = await get_project_event(API_GET_PROJECT_AUTH, req_data, '获取认证数据')
                    authData = res.get('data', None)
                    if authData:
                        username = authData.get('username', None)
                        password = authData.get('password', None)
                    if all((authData, username, password)):
                        data['username'] = username
                        data['password'] = password
                        break
                    else:
                        logutil.log('browser', f"用户名和密码没有获取到,RPA将无法正常工作！")
                        continue
                except NoneError:
                    logutil.log('browser', f'获取的登录认证数据为空!') 
                    break 

                # 加入用户名和密码两项数据即可让RPA服务正常工作
                logutil.log('browser', f"开始验证是否有获取到用户名和密码")
                if all((data.get('username', None), data.get('password', None))):
                    logutil.log('browser', f"用户名和密码都有")
                    request = AsyncHttpRequest(f"{SERVER_ADDR}:{SERVER_PORT}")
                    headers = {"Content-Type": "application/json"}
                    response = await request.post(data=json.dumps(data), headers=headers)
                    resDict = json.loads(response)
                    logutil.log('browser', f"调用RPA本地接口结果: {resDict}")
                    # 回调反馈接口
                    data = {
                        "id": feedbackId,
                        "code": "200" if resDict[0] else "500",
                        "msg": "成功" if resDict[0] else "失败"
                    }
                    request = AsyncHttpRequest(API_FEEDBACK_ROUTE)
                    headers = {"Content-Type": "application/json"}
                    try:
                        status, res = await request.post(data=json.dumps(data), headers=headers)
                        if status == 200:
                            logutil.log('browser', f"请求回调反馈后的数据{res}和状态:{status}") 
                        else:
                            logutil.log('browser', f"回调反馈结果失败")

                    except Exception as ex:
                        logutil.log('browser', f"回调反馈结果错误:{ex}")
                else:
                    logutil.log('browser', f"用户名/密码缺少!!!")

            except Exception as e:
                print(f'获取出进场数据阶段出错,{e}')
                break
            except NoneError:
                logutil.log('browser', f'获取的进出场数据为空!,重新开始') 
                is_main_loop = True
                break
            if not all(download_status):
                logutil.log('browser', f'部分资源文件下载出错!') 
                break
            else:
                break
        if is_main_loop:
            logutil.log('browser', f'因为取的进出场数据为空!,重新开始') 
            continue
