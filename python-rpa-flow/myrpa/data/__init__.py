import os
PATH_DATA = os.path.dirname(__file__)
PATH_DATA_UPLOADS = os.path.dirname(__file__)+'/uploads'

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"目录 {directory} 不存在，已创建")
    else:
        print(f"目录 {directory} 已存在")

def is_file_valid(file_path):
    if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
        return True
    else:
        return False

async def get_event_source(sourceUrl, idCard, timeOut):

    res = (None,None)
    loop = asyncio.get_event_loop()

    sourceUrl = 'http://bcdoing.com/nfcppp/template.yaml'
    sourcePath = PATH_DATA_UPLOADS+'/'+str(idCard)
    ensure_directory_exists(sourcePath)
    task = loop.create_task(download_file(sourceUrl, sourcePath))
    await asyncio.wait_for(task, timeout=timeOut)
    logutil.log('browser', f"任务结果: {task.result()}")
    res = task.result()
    if not res[0]:
        logutil.log('browser', f"缺少出入场数据，操作将会终止")
    return res

async def traslate_data(data):
    key = 'reqData'
    res = json.loads(data.get(key))      
    return res
