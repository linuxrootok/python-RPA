import random
import asyncio

#from .config import userInputXpath, passInputXpath, validcodeXpath, loginXpath, loginSuccessedTitle
from .config import loginObj
import logutil

#from dbutil.db_action import insert_account, fetch_account
from page.page_check_and_retry import check_xpath_exists

async def goto_page(Page, url, project_id):
    if url:
        print(f"直接跳转")
        await Page.goto(url)
    else:
        print(f"查询url后进行跳转")
        url = loginObj.get(project_id).get('loginUrl')
        await Page.goto(url)
    #return page
    if project_id == 'ZJ001':
        await asyncio.sleep(2)
    if project_id == 'ZJ002':
        await asyncio.sleep(10)

async def extract_content(page):
    content = await page.content()
    return content

#@check_xpath_exists('//*[@id="btnSubmit"]')
async def input_and_login(page, data, account, password, project_id):

    #from .config import loginObj
    print(f"project_id 是:{project_id}")
    currentLoginObj = loginObj.get(project_id, 'index')

    userInputXpath = currentLoginObj.get('userInputXpath')
    passInputXpath = currentLoginObj.get('passInputXpath')
    validcodeXpath = currentLoginObj.get('validcodeXpath')
    loginXpath = currentLoginObj.get('loginXpath')

    
    #data = {}
    #　写入数据
    last_insert_id = 0 

    #　这里是主动拉取api的数据 需要判断过后才能入库，不启用
    '''
    if data.get('is_cron_new', None) == None:
        last_insert_id = insert_account(data)
    '''

    #get account and password
    #account, password = fetch_account()[0]
    #print(f"account: {account}")
    #print(f"password: {password}")
    try:    
        usernameObj = await page.xpath(userInputXpath)
        passwordObj = await page.xpath(passInputXpath)
        
        await usernameObj[0].type(account, {'delay': random.randint(10, 20)})
        await passwordObj[0].type(password, {'delay': random.randint(10, 20)})
        #code = input('please enter validcode : ')

        #验证码　先不启用　
        #validcodeObj = await page.xpath(validcodeXpath)
        #await validcodeObj[0].type(str(code))
        
        #点击登录
        await asyncio.sleep(1)
        logonObj = await page.xpath(loginXpath)
        await logonObj[0].click()
        cookies = await page.cookies()
        print(cookies)
        #return cookies[0]['value'], last_insert_id
    except Exception as e:
        pass
        
    return last_insert_id

async def is_login_successed(page, project_id):

    #from .config import loginObj
    await asyncio.sleep(1)
    is_in = False
    title = await page.title()
    print(f"标题是：{title}")
    currentLoginObj = loginObj.get(project_id, None)
    if title == currentLoginObj.get('loginSuccessedTitle', None):
        is_in = True
        if currentLoginObj.get('loginSuccessedMark', None):
            logutil.log('browser',f"验证节点[个人中心]是否存在　")
            pageCookies = await page.cookies()
            logutil.log('browser', f"网站cookie is:{pageCookies}")
            await asyncio.sleep(1)
            page.waitForXPath(currentLoginObj['loginSuccessedMark'], timeout=10000)
            logutil.log('browser',f"验证节点[个人中心]是否存在　完成")
            elements = await page.xpath(currentLoginObj['loginSuccessedMark'])

            if not elements:
                is_in = False

            logutil.log('browser', f"额外验证了登录是否成功:{is_in}, 查找到的节点是:{elements}")
    return is_in

async def do_logout(page, project_id):
    from .config import loginObj
    await page.goto(loginObj[project_id]['logoutUrl']) 
