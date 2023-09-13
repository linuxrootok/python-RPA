import asyncio
import aiohttp
import os

from data import is_file_valid

async def download_file(file_url, file_path, is_check=True):
    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as response:
            if response.status == 200:
                file_name = os.path.basename(file_url)
                file_path = os.path.join(file_path, file_name)

                if not is_file_valid(file_path):
                    with open(file_path, 'wb') as file:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            file.write(chunk)

                return file_name, file_path

            else:
                return None, None

# 调用示例
'''
file_url = 'http://bcdoing.com/nfcppp/template.yaml'
file_path = PATH_DATA_UPLOADS
file_name, full_path = asyncio.run(download_file(file_url, file_path))

if file_name and full_path:
    print(f"文件 {file_name} 下载成功，保存在 {full_path}")
else:
    print("文件下载失败")
'''
