import os
import asyncio
from ocrutil import yunMa

myPath = os.path.dirname(__file__)

# 局部对象截图
async def crop(Page, xpath, picName):
    pic = await Page.xpath(xpath) 
    await pic[0].click()
    await asyncio.sleep(1) 
    picPath = picName
    await pic[0].screenshot({"path": picPath})
    #await step_des(3, "正在保存验证码截图信息")
    await asyncio.sleep(5) 
    return picPath
    

async def get_code(picPath):
    res = yunMa.check_verify(picPath)
    #await step_des(1, "正在等待返回验证码字串")
    print(f"验证码字串是:{res}")
    return res  
     
