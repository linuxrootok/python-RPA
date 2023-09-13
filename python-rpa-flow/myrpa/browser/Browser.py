import asyncio
from pyppeteer import launch
from page.page_operations import goto_page, extract_content
from hook.hook_point import run_hook_point
from config.config import chromeExePath, lunchParam
#from base.baseobj import Singleton
from logutil.exceptions import log_exception
import logutil

Browser = None
Page = None

#@Singleton
async def init_browser():
    global Browser, Page

    while True:
        try:
            #Browser = await launch(headless=False,executablePath="C:/Users/Administrator/AppData/Local/Google/Chrome/Application/chrome.exe")
            Browser = await launch(lunchParam)
            Page = (await Browser.pages())[0]

            # 添加headers
            headers = {
                'Accept-Encoding': 'gzip' # 使用gzip压缩让数据传输更快
            }
            await Page.setExtraHTTPHeaders(headers)
            #page过滤器
            await run_hook_point("page_object_ready", data={'page':Page, 'browser':Browser})

            # 检测浏览器是否正常
            #await Page.waitForNavigation({'timeout': 15000})
            #break
            is_running = await Page.waitForFunction('navigator.userAgent')
            print(is_running)
            if is_running:
                #queue.put(Browser)
                break

        except Exception as e:
            logutil.log('browser',f"检测到浏览器异常: {e}")
            print("正在尝试重新启动浏览器...")
            if Browser:
                await Browser.close()
                Browser = None
                Page = None
            await asyncio.sleep(5)
    return Browser, Page

async def check():
    global Browser, Page
    await asyncio.sleep(10)
    while True:
        try:
            await Page.waitForFunction('1+1') 
            print('页面可访问,浏览器未关闭')
            logutil.log('browser',f"关闭浏览器后，当前页面个数：{len(await Browser.pages())}")
        except Exception as e:
            print(f'页面不可访问,浏览器可能已关闭:{e}')
            #await init_browser()
            loop = asyncio.get_event_loop()
            task = loop.create_task(init_browser())
            task2 = loop.create_task(check())
            loop.run_until_complete(asyncio.gather(task))
            #break
        await asyncio.sleep(10)
#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#task2 = loop.create_task(check())
#loop.run_until_complete(asyncio.gather(task,task2))

#loop = asyncio.get_event_loop()
#task = loop.create_task(init_browser())
#loop.run_until_complete(asyncio.gather(task))
