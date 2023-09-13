import aiohttp
import logutil

class AsyncHttpRequest:
    def __init__(self, url):
        self.url = url

    async def get(self, params=None, headers=None):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.url, params=params, headers=headers, ssl=False) as response:
                    return await response.text()
            except aiohttp.ClientError as e:
                print(f"Error during GET request to {self.url}: {e}")
                logutil.log('console', f"Error during GET request to {self.url}: {e}")
                return None

    async def post(self, data=None, headers=None):
        res = ''
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.url, data=data, headers=headers, ssl=False) as response:
                    status, res = (response.status, await response.text())
                    return status, res
            except aiohttp.ClientError as e:
                print(f"Error during POST request to {self.url}: {e}")
                logutil.log('console', f"Error during GET request to {self.url}: {e}")
                return None