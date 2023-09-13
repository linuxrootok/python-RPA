import os
import random
from . import crop, get_code
import asyncio
from .config import codeXpath, inputXpath, errorXpath, passwordXpath, retryTime, delayTime, xid
#from browser.Browser import Browser, Page

from common import input_backspace
from page import input_text_clear

from logutil.exceptions import log_exception
import logutil

myPath = os.path.dirname(__file__)

async def input_code(Page):

    for i in range(0, retryTime):
        logutil.log('browser', f"验证码尝试，当前次数:{i+1}")
        try:
            await asyncio.sleep(3)
            picPath = await crop(Page, codeXpath, f"{myPath}/code.png")
            code = await get_code(picPath)

            await asyncio.sleep(2)
            validCodeObj = await Page.xpath(inputXpath)
            await input_backspace(Page, inputXpath, 'clear input code')
            #await input_text_clear(Page, xid)

            await validCodeObj[0].type(code, {'delay': random.randint(10, 20)})

            await asyncio.sleep(1)
            passwordXpathObj = await Page.xpath(passwordXpath)
            await passwordXpathObj[0].click()

            #await asyncio.sleep(100000)
            await asyncio.sleep(delayTime)

            #verifyObj = await Page.xpath(errorXpath)
            #logutil.log("验证码出错控件监测结果：{verifyObj}")

            await asyncio.sleep(2)
            if (await Page.xpath(errorXpath)):
                logutil.log('browser', f"验证码不通过，第{i+1}次尝试...")
                continue
            else:
                break

        except Exception as e:
            logutil.log('browser', f"错误:{e}")