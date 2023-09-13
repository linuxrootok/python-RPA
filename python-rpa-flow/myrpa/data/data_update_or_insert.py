import logutil
from dbutil.db_action import fetch_account, update_account_all, insert_account
async def handle_data(data, is_actived):

    project_id = data.get('projectNo','')
    company_id = data.get('companyId','')


    post_username = data.get('username','')
    post_password = data.get('password','')

    # 是否进行更新　过滤一下　0为不更新，１为更新
    is_update = 1

    # status 0为更新　其他为新增
    status = 0

    account_id = 0
    last_insert_id = 0
    # 判断是否存在记录
    res = fetch_account(project_id, company_id) 
    if res:
        username = res[0][6]
        password = res[0][7]
        
        if all((username == post_username, password == post_password)):
            is_update = 0

        else:
            logutil.log('browser', f"帐启名和密码一致，不做更新，更新ID将显示为0")


    logutil.log('browser', f"数据库获取到的数据:{res}")
    #　如果存在，更新它
    if res:
        if is_update:
            account_id = res[0][0]
            update_account_all(account_id, data, is_actived)
            return status, account_id
        else:
            return status, account_id
    else:
        # 不存在，插入数据
        data['status'] = is_actived

        last_insert_id = insert_account(data)
        status = 1
        return status, last_insert_id