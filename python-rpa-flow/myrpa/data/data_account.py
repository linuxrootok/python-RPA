from dbutil.db_action import fetch_account, update_account

async def get_data_account():
    account_array = fetch_account()

    data = {
        #"companyName": account_array[0][],
        "sysLoginUrl": account_array[0][9],
        #"gateName": account_array[0][],
        #"companyId": account_array[0][],
        "password": account_array[0][7],
        #"mainContractor": account_array[0][],
        #"projectNo": account_array[0][],
        "is_cron_new": True,
        #"callbackUrl": account_array[0][],
        #"govSysProjectName": account_array[0][],
        "gateNo": "ZJ001",
        "govSysProjectName": account_array[0][10],
        "username": account_array[0][6]
    } 
    return data

async def update_status_account(account_id):
    update_account(account_id)