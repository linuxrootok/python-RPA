import datetime
import time,random
import asyncio
import json
import random
from config.config import ELE_TIMEOUT

import logutil

def test():
    print('test')


# 输出带时间戳的log日志
def print_dt(ss):
    t = str(datetime.datetime.now()) + '|print_dt|'
    t = t+str(ss)
    print(t)

async def step_des(timeout, des, data={}):
    if not data:
        des = des + ",等待 %s 秒......" % str(timeout)
    else:
        username = str(data.get("username", "默认名字"))
        idcard = str(data.get("idcard", "0"))
        des = f"{username}|{idcard}|" + des + "|等待 %s 秒......" % str(timeout)
    print_dt(des)
    logutil.log("step", des)
    await asyncio.sleep(float(timeout))

# 选择frame
async def select_frame(page, name):
    frame_list = page.frames #获取所有frame
    for frame in frame_list:
        if name == await frame.title():
            return frame


async def while_on_page_get_element(page, xpath=[], times=1, data={}, remark="", timeout=0.1):
    '''检查控件函数'''
    num = 0
    ele = None
    title = None
    # print(await page.title())
    while num<=times:
        num += 1
        await step_des(timeout, f"RPAWaitForXPath|步骤|{remark}|等待{str(xpath)}元素", data)
        for i,v in enumerate(xpath):
            await step_des(0.0, f"RPAWaitForXPath|步骤|{remark}|等待{v}元素", data)
            cache_title = page.url
            await step_des(0.0, f"page|标题|{cache_title}", data)
            # await page.waitForNavigation()
            # await page.waitForNavigation(waitUntil='networkidle0')
            if not title:
                title = cache_title
                ele = await page.xpath(v)
                if ele:
                    return ele
            elif title == cache_title:
                ele = await page.xpath(v)
                if ele:
                    return ele
            else:
                return ele

    return ele

async def page_get_element_error(page, xpath=[], times=1, data={}, remark=""):
    ele = await while_on_page_get_element(page, xpath, times, data, remark)
    if not ele:
        raise Exception(f"Exception|没有找到控件|{remark}|{str(xpath)}|{str(times)}")

#点击元素事件模拟
async def click_element(page, xpath, text=None, frame=None, check=0, before_delay=0.5, after_delay=0.1, offset=0, descript='',mark='', data={}):

    #print(f'offset:{offset}')
    if before_delay != '0.0':
        await step_des(before_delay, f'{mark}|{descript}|等待{xpath}元素', data)

    myObj = page
    if frame and frame != 'index':
        _page = await select_frame(page, frame)
        if not check:
            await page_get_element_error(_page, [xpath], ELE_TIMEOUT, data, mark)
        element = await _page.xpath(xpath)
        myObj = _page
    else:
        if not check:
            await page_get_element_error(page, [xpath], ELE_TIMEOUT, data, mark)
        element = await page.xpath(xpath)

    if check:

        await step_des(0.0, '因为需要检测DOM，准备切换分支')
        if element:
            await step_des(0.0, f'{mark}检测结果:(是) {descript}', data)
            return [True,myObj,offset]
        else:
            await step_des(0.0, f'{mark}检测结果:(否) {descript}', data)
            sign = -1 if offset < 0 else 1  
            reversed_num = int(str(abs(offset))[::-1])  
            reversed_num *= sign 
            return [False,myObj,reversed_num]
    
    if offset >= 0:
        await element[offset].click()
        await step_des(0.0, f'点击编号是：{mark}, 描述: {descript}', data)
        if text:
            await element[offset].type(text, {'delay': random.randint(10, 20)})
            await step_des(0.0, f'输入编号是：{mark}, 描述: {descript}', data)
        else:
            pass
    else:

        if offset == -1:
            if text:
                await element[0].uploadFile(text)
            else:
                await step_des(0.0, f'上传图片结果: 请重新生成YAML配置文件-by Tyler', data)
        elif offset % 11 == 0:
            if text:
                await myObj.evaluate(text)
            else:
                await step_des(0.0, f'运行脚本: 请重新生成YAML配置文件-by Tyler', data)
        else:
            await element[0].click()
            await step_des(0.0, f'点击编号是：{mark}, 描述：{descript}', data)
            if text:
                await element[0].type(text, {'delay': random.randint(10, 20)})
                await step_des(0.0, f'输入编号是：{mark}, 描述：{descript}', data)

    await step_des(1, f'{descript}')

    if after_delay != '0.0':
        await step_des(after_delay, f'{mark}已处理:{descript}选项', data)
    return [False, myObj, offset]