# !/usr/bin/env python
# -*- coding:utf-8 -*-# 
import datetime
import time,random,os,requests
import asyncio
import json
import random

from async_retrying import retry
from pyppeteer.frame_manager import Frame
from pyppeteer.page import Page
from string import Template

import logutil
from config import serverConfig



def template_substitute(text, data):
    '''字符串模板替换'''
    return Template(text).safe_substitute(data)

# 输出带时间戳的log日志
def print_dt(ss):
    t = str(datetime.datetime.now()) + '|print_dt|'
    t = t+str(ss)
    print(t)

# 时间转成字符串
def datetime_to_string(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

# 获取当前时间
def datetime_str():
    dt = datetime.datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def png_time_name():
    '''当前时间作为图片名'''
    dt = datetime.datetime.now()
    return dt.strftime("%Y-%m-%d-%H-%M-%S")

# 获取后几秒的时间
def timedelta_seconds(num):
    now_time=datetime.datetime.now()
    return (now_time+datetime.timedelta(minutes = + num/60)).strftime("%Y-%m-%d %H:%M:%S")

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

def log_action(des, data={}):
    if data:
        username = str(data.get("username", "默认名字"))
        idcard = str(data.get("idcard", "0"))
        des = f"{username}|{idcard}|" + des
    logutil.log("action", des)

def is_between(start_at, end_at) -> bool:
    """
    判断当前时间是否在指定时间之间
    例如：指定时间段为[09:00:00, 18:00:00]若当前时间是 2021年8月16日17:53:45 ,判断是否在这个时间段,返回 True
    另外：若指定时间段为[22:00:00, 02:00:00]若当前时间是 2021年8月16日23:00:00 ,同样返回 True
    :param start_at:
    :param end_at:
    :return bool:
    """
    startAtStr = str(start_at).strip()
    endAtStr = str(end_at).strip()
    if len(startAtStr) > 0 and len(endAtStr) > 0:
        startAt = time.strftime("%Y-%m-%d") + " " + startAtStr
        endAt = time.strftime("%Y-%m-%d") + " " + endAtStr
        startAtTime = int(time.mktime(time.strptime(startAt, '%Y-%m-%d %H:%M:%S')))
        endtAtTime = int(time.mktime(time.strptime(endAt, '%Y-%m-%d %H:%M:%S')))
        nowTime = int(time.time())
        if startAtTime < endtAtTime:
            return startAtTime <= nowTime <= endtAtTime
        else:
            tomorrowDate = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')  # 明天的日期
            endAt = tomorrowDate+" "+endAtStr
            endtAtTime = int(time.mktime(time.strptime(endAt, '%Y-%m-%d %H:%M:%S')))
            return startAtTime <= nowTime <= endtAtTime
    return False


# 选择frame
async def select_frame(page, name):
    frame_list = page.frames #获取所有frame
    for frame in frame_list:
        if name == await frame.title():
            return frame

# 返回信息
def message(status, msg, project_no='0', project_name='0'):
    ret = {
            "status": status,
            "msg": msg,
            "project_no": str(project_no),
            "project_name": str(project_name)
        }
    return ret

# 返回信息，带上耗时
def message_dt(status='init', msg='msg', data={}):
    idcard = data.get("idcard", "0")
    username = data.get("username", "0")
    start = data.get("start", 0)

    ret = {
            "status": status,
            "msg": msg,
            "username": username,
            "idcard": idcard,
            "start": str(datetime.datetime.now()),
            "time": "耗时="+str(time.time() - start),
        }
    return ret

# 返回二维码信息
def message_code(status='init', msg='msg', data={}):
    idcard = data.get("idcard", "0")
    username = data.get("username", "0")
    start = data.get("start", 0)
    qrCode = data.get("content", None)

    ret = {
            "status": status,
            "msg": msg,
            "username": username,
            "idcard": idcard,
            "start": str(datetime.datetime.now()),
            "time": "耗时="+str(time.time() - start),
            "qrCode": qrCode,
        }
    return ret

async def while_on_page_get_element(page, xpath=[], times=1, data={}, remark="", timeout=1):
    '''检查控件函数'''
    num = 0
    ele = None
    while num<=times:
        num += 1
        await step_des(timeout, f"RPAWaitForXPath|步骤|{remark}|等待{str(xpath)}元素", data)
        for i,v in enumerate(xpath):
            await step_des(0.0, f"RPAWaitForXPath|步骤|{remark}|等待{v}元素", data)
            ele = await page.xpath(v)
            if ele:
                return ele
    return ele

async def page_get_element_error(page, xpath=[], times=1, data={}, remark="", timeout=1):
    ele = await while_on_page_get_element(page, xpath, times, data, remark, timeout)
    if not ele:
        raise Exception(f"Exception|没有找到控件|{remark}|{str(xpath)}|{str(times)}")
    return ele

#点击元素事件模拟
async def click_element(page, xpath, text=None, frame=None, check=0, before_delay=0.5, after_delay=0.1, offset=0, descript='',mark='', data={}):

    #print(f'offset:{offset}')
    if before_delay != '0.0':
        await step_des(before_delay, f'{mark}等待{xpath}元素', data)

    myObj = page
    if frame and frame != 'index':
        _page = await select_frame(page, frame)
        if not check:
            await page_get_element_error(_page, [xpath], serverConfig.ELE_TIMEOUT, data, mark)
        element = await _page.xpath(xpath)
        myObj = _page
    else:
        if not check:
            await page_get_element_error(page, [xpath], serverConfig.ELE_TIMEOUT, data, mark)
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
        if text:
            await element[offset].type(text, {'delay': random.randint(10, 20)})
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
            if text:
                await element[0].type(text, {'delay': random.randint(10, 20)})

    await step_des(1, f'{descript}')

    if after_delay != '0.0':
        await step_des(after_delay, f'{mark}已处理:{descript}选项', data)
    return [False, myObj, offset]

#清空input控件value
async def input_backspace(page, xpath, descript=''):
    input_element = await page.xpath(xpath)
    await input_element[0].click()
    await page.keyboard.down('Control')
    await page.keyboard.press('A')
    await page.keyboard.up('Control')
    await page.keyboard.press('Backspace')
    if descript:
        await step_des(0.0, descript)

#frame下的输入控件输入text
async def type_text(page, xpath, text, frame=None):
    myObj = page
    if frame and frame != 'index':
        _page = await select_frame(page, frame)
        myObj = _page

    await page.type(xpath, text, {'delay': random.randint(10, 20)})

    await step_des(3, f'页面{frame}输入框{xpath}输入了{text}内容')



    return [False, myObj]

async def page_clear_input(page, element):
    '''清空输入框'''
    await element.click()
    await page.keyboard.down('Control')
    await page.keyboard.press('A')
    await page.keyboard.up('Control')
    await page.keyboard.press('Backspace') 

def get_code():
    '''测试-获取验证码'''
    with open("config.json", 'r') as load_f:
        load_dict = json.load(load_f)
        print_dt(load_dict)
    return load_dict["verify"]

def write_cache_json(path, data):
    '''写入json文件'''
    with open(path, 'w') as f:
        json.dump(data, f)

def load_cache_json(path):
    '''读取json文件'''
    with open(path, 'r') as f:
        v = json.load(f)
        return v



def save_local_jpg(url='https://ghosstest.oss-cn-beijing.aliyuncs.com/1d4a13090e.png'):
    '''下载图片,保存本地图片'''
    root =  os.getcwd() # 获取当前路径
    face = os.path.join(root, 'picture/face')
    path = os.path.join(face,  url.split('/')[-1]) 
    print_dt(path)
    if not os.path.exists(face):
        os.mkdir(face)

    if os.path.exists(path):
        os.remove(path)
        print_dt('文件已存在，删除文件，删除成功')
        time.sleep(5)

    r = requests.get(url)
    
    with open(path,'wb') as f:
        f.write(r.content)
        f.close()
        print_dt('文件保存成功')
    return path