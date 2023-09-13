import asyncio
import time

import yaml
from pyppeteer import launch
from jinja2 import Template
from . import retry_on_exception
import logutil
from yml import PATH_YML

stop = False

async def execute_actions(page, actions, data, timeout=5000):
    global stop

    element = None
    mark = None
    desc = None

    for action in actions:
        if stop:
            break
        try:
            await asyncio.sleep(0.5)
            element, mark, desc, stop = await execute_action(page, action, data, timeout)
            logutil.log('browser', f"正在运行的阶段:{mark},注释:{desc},控件:{element},是否停止：{stop}")
            if not element:
                print('stopping execution')
            if stop:
                logutil.log('browser', f"配置要求到此结束，给出操作结果")
                break
            else:
                logutil.log('browser', f"go on ...")
        except TypeError:
            print('没有找到控件')
            if stop:
                return None, mark, desc
    return element, mark, desc

async def run(page, event, data):
    res = None
    with open(PATH_YML+'/'+event+'.yaml', encoding='utf-8') as file:
        config = yaml.safe_load(file)
        res = await execute_actions(page, config['actions'], data)
    return res


#@retry_on_exception(10, exceptions=(TimeoutError,))
@retry_on_exception(3)
async def execute_action(page, action, data, _timeout=5000):
    global stop
    element = None
    mark = None
    desc = None

    if action['type'] in ('input', 'click'):
        if action.get('selector', None):
            action['selector'] = Template(action['selector']).render(data)

        if action.get('selector_type') == 'xpath':
            await page.waitForXPath(action['selector'], timeout=_timeout)
        else:
            await page.waitForSelector(action['selector'], timeout=_timeout)

        # TODO 有些页面要等待导航时间处理
        #await page.waitForNavigation({'waitUntil': 'domcontentloaded'})
        await asyncio.sleep(1)
    if action['type'] == 'input':
        if action.get('selector_type') == 'xpath':
            elements = await page.xpath(action['selector'])
            if elements:
                element = elements[0]
                #logutil.log('browser', f"需要替换的模板内容：{action['text']}, 准备的实际内容为:{data}")
                try:
                    input_text = Template(action['text']).render(data)
                    await element.type(input_text)
                except Exception as e:
                    logutil.log('browser', f"模板错误信息:{e}")
                #await element.type(action['text'])
        else:
            element = await page.querySelector(action['selector'])
            await page.type(action['selector'], action['text'])

        mark = action.get('mark', 'input')
        desc = action.get('desc', '无注释')


    elif action['type'] == 'click':
        if action.get('selector_type') == 'xpath':
            action['selector'] = Template(action['selector']).render(data)
            elements = await page.xpath(action['selector'])
            if elements:
                element = elements[0]
                await element.click()
        else:
            element = await page.querySelector(action['selector'])
            await page.click(action['selector'])

        mark = action.get('mark', 'click')
        desc = action.get('desc', '无注释')
        stop = action.get('stop', False)

    elif action['type'] == 'navigator':
        logutil.log('browser', f"导航中")
        element = page
        url = action.get('url', None)
        await page.goto(url,{'waitUntil':'load'})
        #await page.waitForNavigation({'waitUntil': 'domcontentloaded'})

        mark = action.get('mark', 'navigator')
        desc = action.get('desc', '页面跳转')

    elif action['type'] == 'runjs':
        element = page
        action['script'] = Template(action['script']).render(data)
        await page.evaluate(action['script'])

        mark = action.get('mark', 'if')
        desc = action.get('desc', '无注释')

    elif action['type'] == 'upload':
        logutil.log('browser', f"正在上传资源文件:{action['file']}")
        try:
            if action.get('selector_type') == 'xpath':
                elements = await page.xpath(action['selector'])
                if elements:
                    element = elements[0]
                    #await element.type('')
                    await element.uploadFile(action['file'])
            else:
                element = await page.querySelector(action['selector'])
                await element.uploadFile(action['file'])
        except Exception as e:
            logutil.log('browser', f"上传资源时有错误:{e}")

        mark = action.get('mark', 'if')
        desc = action.get('desc', '无注释')
        await asyncio.sleep(1)

    elif action['type'] == 'if':
        value = 0 
        await asyncio.sleep(0.5)
        if action['condition'].get('selector_type') == 'xpath':
            await page.waitForXPath(action['condition']['selector'], timeout=1000)
            elements = await page.xpath(action['condition']['selector'])
            if elements:
                element = elements[0]
                value = 1
            else:
                value = 0
        else:
            await page.waitForSelector(action['condition']['selector'], timeout=_timeout)
            element = await page.querySelector(action['condition']['selector'])

        page_property = await element.getProperty(action['condition']['property'])
        value = await page_property.jsonValue()

        mark = action['condition'].get('mark', 'if')
        desc = action['condition'].get('desc', '无注释')
        stop = action['condition'].get('stop', False)

        logutil.log('browser', f"{mark}:查找到的数据值：{value}")
        if value == action['condition']['value']:
            #execute_action.set_param('times', 2)
            #execute_action.set_param('_timeout', 800)
            await execute_actions(page, action['then'], data, 1000)
        else:
            #execute_action.set_param('times', 1)
            if 'else' in action:
                await execute_actions(page, action['else'], data, 1000)

    return element, mark, desc, stop
