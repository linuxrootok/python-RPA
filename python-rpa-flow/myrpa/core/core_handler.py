import traceback
import os, sys
import importlib
import asyncio
from quart import request, jsonify
import time
from browser.Browser import Browser, Page, init_browser
from pyppeteer.launcher import connect

from page.page_operations import goto_page, extract_content
#from data.data_extraction import extract_data

from hook.hook_point import run_hook_point

from config.config import idcard, base_url, EVENT_CALL_LATER_TIMEOUT
from config.config import filter_on, filter_idcard_on, gotobase_on
from config.config import filter_array, filter_idcard_array

from config.config import chromeExePath, lunchParam
from pyppeteer import launch

from event.event_flow import event_test,event_go

from data.data_convert import convert_data

from logutil.exceptions import log_exception
import logutil
#from dbutil.db_action import insert_account, fetch_account

logutil.log('browser', "test")

timeout = 3 
IS_BUSY = False
IS_LOGIN = False
PROJECT_ID = None
USER_NAME = None
USER_PASSWORD = None

async def run_browser_once():
    global Browser, Page

    Browser,Page = await init_browser()

def set_browser_idle(n, loop):
    global IS_BUSY
    IS_BUSY = False 

    logutil.log('browser','设置浏览器为空闲[完成]')

def my_allback(n, loop):
    global IS_BUSY
    logutil.log('browser','my_allback has been ran')    

def my_call_later(n, loop):
    logutil.log('browser','my_call_later has been ran!')

async def handle_except():
    global Browser, Page
    try:
        await Page.close()
        await Browser.close()
        Browser = await launch(lunchParam)
        Page = (await Browser.pages())[0]
    except Exception as e:
        logutil.log('browser',"关闭浏览器异常：{e}")
    finally:
        pass

async def sync_data():
    pass

async def sub_coroutine(page):

    for i in range(10):

        print(f"子协程:{time.time()}")
        #title = await page.evaluate('document.querySelector("title").textContent')
        #print(f"title: {title}")
        #if title == "Google":
            #return True

        await asyncio.sleep(1)

    return False

async def handle_core():
    global idcard
    global PROJECT_ID
    global USER_NAME
    global USER_PASSWORD
    global IS_BUSY
    global IS_LOGIN
    global Browser, Page

    try:
        # 验证的数据ID,将会被写入，然后可能会更新
        lastInsertId = 0

        if not Browser : 
            logutil.log('browser', f"浏览器尚未启动")
            await run_browser_once()
        else:
            logutil.log('browser', f"浏览器已启动")


            #　有一种情况，浏览器被干掉
            if (await Browser.pages() == 0):
                try:
                    await Browser.close()     
                except Exception as e:
                    logutil.log('browser', f"浏览器被不明物体干掉了!{e}")
                await run_browser_once()

        returnData = {'code':500, 'msg':'verify fail', 'data':''}

        # 转换数据格式
        #originData = await request.get_json()
        #data = await convert_data(originData)

        data = await request.get_json()
        logutil.log('browser',f"初始的data:{data}")

        pid = data.get('gateNo', 'index')
        src_username = data.get('username', None)
        src_password = data.get('password', None)  

        if not PROJECT_ID:
            PROJECT_ID = pid
            src_username = data.get('username', None)
            src_password = data.get('password', None) 

        logutil.log('browser', f"当前的PROJECT_ID：{PROJECT_ID} != {pid}") 
        logutil.log('browser', f"当前的USER_NAME：{USER_NAME} != {src_username}") 
        logutil.log('browser', f"当前的USER_PASSWORD：{USER_PASSWORD} != {src_password}") 
        pageCookies = await Page.cookies()
        logutil.log('browser', f"cookie is:{pageCookies}")
        # 如果不是连续的同样后台，即需要预先退出当前可能的后台管理页面
        if any((PROJECT_ID != pid, USER_NAME != src_username, USER_PASSWORD != src_password)):
            logutil.log('browser',f"执行退出后台管理系统,退出操作")
            IS_LOGIN = False
            await run_hook_point('page_event_logout_ready', data={'page':Page,'project_id':PROJECT_ID})

        if pid:
            PROJECT_ID = pid 
            USER_NAME = data.get('username', None)
            USER_PASSWORD = data.get('password', None)

        #数据格式验证 开始
        try:
            await run_hook_point("data_validattion_ready", data=data)
        except Exception as e:
            logutil.log('browser','data error')
        #数据格式验证 结束

        #过滤器 身份认证 开始
        if filter_idcard_on:
            if not idcard['id']:
                idcard['id'] = data['idcard']
            for fn in filter_idcard_array: 
                logutil.log('browser',"当前运行的过滤器是: {fn}")
                is_available = await run_hook_point(fn, data=data)
                if is_available:
                    IS_BUSY = False
                else:
                    returnData['code'] = 502
                    returnData['msg'] = 'Browser is busy now'
                    returnData['data'] = ''
                    #return jsonify({'code': 502, 'msg':'Browser is busy now', 'data':''})
        #过滤器 身份认证 结束 

        #提取数据，贮存 开始
        #content = await extract_content(Page)
        #myData = await extract_data(content)
        await run_hook_point("data_extract_ready", data={'page':Page})
        #提取数据，贮存 结束

        #filter data start
        #检查过滤器开关 开始
        print(filter_array)
        if filter_on:
            for fn in filter_array: 
                logutil.log('browser',"当前运行的过滤器是: {fn}")
                is_available = await run_hook_point(fn, data=data)
                if is_available:
                    IS_BUSY = False
                else:
                    #return jsonify({'status': 'busy'})
                    #return jsonify({'code': 502, 'msg':'Browser is busy now', 'data':''})
                    returnData['code'] = 502
                    returnData['msg'] = 'Browser is busy now'
                    returnData['data'] = ''

        #检查过滤器开关 结束
        #filter data end 

        if IS_BUSY:
            returnData['code'] = 502
            returnData['msg'] = 'Browser is busy now'
            returnData['data'] = ''

        IS_BUSY = True

        #try:
        pageNum = len(await Browser.pages())

        if pageNum == 0:
            logutil.log('browser',"页面当前个数为0")
            Browser = await launch(lunchParam)
            Page = (await Browser.pages())[0]
            IS_BUSY = False
        
        pageNum = len(await Browser.pages())    
        if pageNum > 1:
            for i in range(pageNum-1):
                await (await Browser.pages())[i].close()
        pageNum = len(await Browser.pages())        
        if  pageNum == 1:
            Page = (await Browser.pages())[0]
        logutil.log('browser',f"页面个数:{len(await Browser.pages())}")
        logutil.log('browser','进入主体区域')

        # 在这里使用Pyppeteer执行任务
        await asyncio.sleep(1)
        #event_test()
        if gotobase_on:
            #　旧的维护一套多项目+密码的字典(舍弃)
            #await goto_page(Page, base_url.get(PROJECT_ID, 'index'), PROJECT_ID)

            # 新的方案　采用data参数传递
            #await goto_page(Page, data.get('sysLoginUrl', None), PROJECT_ID)
            await goto_page(Page, None, PROJECT_ID)

            await asyncio.sleep(1)

        # 测试子协程
        print(f"子协程准备开始:{int(time.time())}")

        task1 = asyncio.create_task(sub_coroutine(Page))
        task1_result = None
        try:
            task1_result = await asyncio.wait_for(task1, timeout=3)
            print(f"子协程正在运行:{time.time()}")
        except asyncio.TimeoutError:
            print("The task took too long, cancelling.")
            task1.cancel()  
            try:
                await task1  
            except asyncio.CancelledError:
                pass  

        print('验证结果：', task1_result)

        print(f"项目ID为:{PROJECT_ID}")

        try:    
            await run_hook_point('screenshot_event_ready', data={'page':Page, 'project_id': PROJECT_ID})

        except Exception as e:
            logutil.log('browser', f"截图至登录阶段错误:{e}")

        account, passwd = await run_hook_point('data_event_ready', data={'data':data})

        # TODO 请求JAVA端获取项目下网站的登录信息
        await run_hook_point('data_get_auth_ready', data={'data':data})

        if not IS_LOGIN:
            #　执行登录操作
            lastInsertId = await run_hook_point('page_login_ready', data={'data':data, 'page':Page, 'account':account, 'password': passwd, 'project_id':PROJECT_ID})

            # 验证是否登录成功
            IS_LOGIN = await run_hook_point('page_event_post_ready', data={'page':Page ,'project_id':PROJECT_ID})
            logutil.log('browser',f"登录结果:{IS_LOGIN}")

        if IS_LOGIN:
            returnData['code'] = 200
            returnData['msg'] = 'verify success'

        else:
            returnData['code'] = 500
            returnData['msg'] = 'verify fail, username or password is wrong!'

        # TODO处理页面事件

        print('准备运行页面事件')
        #res = await run_hook_point('page_event_flow_ready', data={'page':Page ,'project_id':PROJECT_ID})
        # 如果没有登录成功，由直接跳过page事件
        if IS_LOGIN:
            loop = asyncio.get_event_loop()
            task2 = asyncio.create_task(run_hook_point('page_event_flow_ready', data={'data':data, 'page':Page ,'project_id':PROJECT_ID, 'is_login': IS_LOGIN}))
            try:
                await asyncio.wait_for(task2, timeout=180)
            except asyncio.exceptions.TimeoutError:
                logutil.log('browser', f"页面处理结果超时")
                print('操作页面失败')

                returnData['code'] = 504
                returnData['msg'] = 'event timeout!'
                return jsonify(returnData)


            print(f"页面事件运行结束.{task2.result()}")
            logutil.log('browser', f"页面处理结果：{task2.result()}")

            if task2.result()[0]:
                print('操作页面成功')
                logutil.log('browser', '操作页面成功')
                returnData['code'] = 200
                returnData['msg'] = 'success'
            else:
                print('操作页面失败')
                logutil.log('browser', '操作页面元素动作失败')
                returnData['code'] = 500
                returnData['msg'] = 'fail'

            await asyncio.sleep(5)

        '''
        logutil.log('browser', f"入库前的数据判断:登录结果:{IS_LOGIN},验证网站项目存在与否:{is_actived}")
        if all((IS_LOGIN, is_actived)):
            updateStatus,accountID  = await run_hook_point("data_update_or_insert_account_ready", data={'data':data, 'is_actived':is_actived} )
            if updateStatus:

                logutil.log('browser',f"数据已同步完成，方式为:新增,ID:{accountID}")
            else:

                logutil.log('browser',f"数据已同步完成,　方式为:更新ID:{accountID}")

        else:
            logutil.log('browser',f"数据登录并验证项目名称存在失败")

        '''

        '''#  回调3=>中心数据
         
        feekbackMsg = await run_hook_point('data_feedback_center_ready', data={'data':data, 'res': returnData})
        print(f"请求反馈后给我的响应:{feekbackMsg}")
        logutil.log('console',f"[接口3]请求反馈后给我的响应:{feekbackMsg}")

        # 退出操作
        await run_hook_point('page_event_logout_ready', data={'page':Page,'PROJECT_ID':PROJECT_ID})
        '''


        # 回调1=>给JAVA后端API
        '''
        if all((IS_LOGIN, returnData['code'] == 200)):
            feekbackMsg = await run_hook_point('data_feedback_ready', data={'data':data, 'res': returnData})
            print(f"请求反馈后给我的响应:{feekbackMsg}")
            logutil.log('browser',f"请求反馈后给我的响应:{feekbackMsg}")
        '''

        # 更新登录成功后的数据状态        
        '''
        if all((IS_LOGIN, returnData['code'] == 200, lastInsertId)):
            # 获取最后插入数据的ID
            logutil.log('browser', f"正在处理修改帐号状态")
            await run_hook_point('data_status_ready', data={'status':1, 'lastInsertId':lastInsertId})
        '''

    except ConnectionError:
        logutil.log('browser','与浏览器断开了连接')
        IS_BUSY = False

    except Exception as e:
        traceback.print_exc()
        logutil.log('browser',f"发生异常,原因: {e}")
        await Page.close()
        await Browser.close()

        Browser = await launch(lunchParam)
        Page = (await Browser.pages())[0]
        IS_BUSY = False

    finally:
        #Browser.process.kill()
            #loop = asyncio.get_event_loop()
            #loop.call_later(EVENT_CALL_LATER_TIMEOUT, set_browser_idle, 1, loop) 
        #else:
            #IS_BUSY = False

        idcard['id'] = 0
        if EVENT_CALL_LATER_TIMEOUT:
            logutil.log('browser','设置浏览器为空闲[执行中]')
            IS_BUSY = False
            logutil.log('browser','设置浏览器为空闲[已完成]')

    return jsonify(returnData)