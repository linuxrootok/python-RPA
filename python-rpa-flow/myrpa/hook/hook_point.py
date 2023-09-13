import logging
import asyncio

from page.page_operations import goto_page, extract_content, input_and_login, is_login_successed, do_logout

from data.data_validation import validate_data
from data.data_storage import store_data
from data.data_extraction_classes import extract_data_classes
from data.data_extraction_projects import extract_data_projects
from data.data_filter import filter_data
from data.data_filter import filter_data_idcard
from data.data_fetch import get_account_via_api
from data.data_notify import notify_data, feedback, feedback_data_center

#from data.data_account import get_data_account, update_status_account

#from data.data_update_or_insert import handle_data

from screenshot.screenshot_event import input_code

from page import page_event


from page.config import loginObj
from config.config import base_url 

async def run_hook_point(name, *args, **kwargs):

    logging.info(f"Hook point: {name}")
    project_id = kwargs['data'].get('project_id', None)
    data = kwargs['data'].get('data', None)
    Page = kwargs['data'].get('page', None)

    if name == "page_object_ready":
        await goto_page(kwargs["data"]['page'], base_url['index'], '')

    if name == "data_validattion_ready":
        await validate_data(kwargs["data"])
        await store_data(kwargs["data"])

    if name == "data_filter_ready":
        return await filter_data(kwargs["data"])

    if name == "data_filter_idcard_ready":
        return await filter_data_idcard(kwargs["data"])

    # 验证码
    if name == 'screenshot_event_ready':
        from page.config import loginObj
        # only do this for having captcha 
        projects = loginObj.get(project_id)
        if projects:
            if projects.get('is_captcha'):
                await input_code(kwargs["data"]['page'])
        else:
            print(f"似乎此管理页面不需要验证码")
    
    #获取account帐号
    if name == 'data_event_ready':
        return await get_account_via_api(kwargs["data"]["data"])

    if name == 'page_login_ready':
        # TODO 此处需要增加判断是否自动退出了页面,又或者一直处于已经登录成功后的状态[则不需要再次登录，引起异常]

        try:
            res = await input_and_login(kwargs["data"]['page'], kwargs["data"]['data'],  kwargs["data"]['account'], kwargs["data"]['password'], kwargs["data"]['project_id'])
        except ValueError:
            print('反复查找控件，无结果!')
            
        await asyncio.sleep(3)
        if res != 0:
            return res[0]

    # 验证登录结果
    if name == 'page_event_post_ready':
        await asyncio.sleep(2)
        return await is_login_successed(kwargs["data"]['page'], kwargs["data"]['project_id'])

    # 登出
    if name == 'page_event_logout_ready':
        await do_logout(kwargs["data"]['page'], kwargs["data"]['project_id'])

    #　回调1
    if name == 'data_feedback_ready':
        #if kwargs['data']['data']['is_cron'] == False:
        #if kwargs['data']['data']['is_cron_new'] == False:
        if kwargs['data']['data'].get('is_cron_new', None) == None:
            return await feedback(kwargs["data"]['data'], kwargs["data"]['res'])

        else:
            return '[标识]=>这里是定时任务，不需要回调后端通知01,班组数据将在下一个回调'

    #　回调3=>给数据中心
    if name == 'data_feedback_center_ready':
        if kwargs['data']['data'].get('is_cron_new', None) == None:
            return await feedback_data_center(kwargs["data"]['data'], kwargs["data"]['res'])

        else:
            return '[标识]=>这里是定时任务，不需要回调后端通知01,班组数据将在下一个回调'

    # 定时任务数据
    if name == 'data_account_ready':
        if kwargs['data']['data'].get('is_cron_new', None):
            return await get_data_account()
        else:
            return None

    # page事件流
    if name == 'page_event_flow_ready':

        if not kwargs['data'].get('is_login', None):
            # 未登录
            return await page_event.run(Page, 'front-'+project_id, data)
        else:
            # 已登录
            return await page_event.run(Page, 'backend-'+project_id, data)
        return True,None,None