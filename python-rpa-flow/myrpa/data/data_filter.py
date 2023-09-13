from config.config import idcard
async def filter_data(data):
    """过滤数据，必需返回布尔值"""
    print('DATA FILTER RUNNING')
    return True

async def filter_data_idcard(data):
    """过滤数据，必需返回布尔值"""
    logutil.log('browser',f"idcard is: {idcard} ")
    print('DATA CARDID FILTER RUNNING')
    if idcard['id'] == data['idcard']:
        return True
    else:
        return False