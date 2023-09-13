from .asyncHttpRequest import AsyncHttpRequest
#from config.config import api_get_account_url, api_set_account_url

async def run(url, data):
    #url = api_get_account_url
    request = AsyncHttpRequest(url)
    #response = await request.get()
    #print(response)

    #data = {"key": "value"}
    headers = {"Content-Type": "application/json"}
    response = await request.post(data=data, headers=headers)
    #print(response)
    return response
