import datetime
import sys, subprocess
from quart import Quart, jsonify
from core.core_handler import handle_core, handle_except
import asyncio
#import scheduled
import logutil
from config.serverConfig import SERVER_PORT
import pyppeteer

app = Quart(__name__)
asyncio.get_event_loop().set_debug(True)

@app.route('/', methods=['GET'])
@app.route('/home/', methods=['GET'])
@app.route('/index', methods=['GET'])
async def index():
    return jsonify({'code': 200, 'msg':'Service is good now', 'data':''})

@app.route('/api', methods=['POST'])
@app.route('/accountVerify', methods=['POST'])
async def api_handle_task():
    try:
        return await handle_core()
    except Exception as e:
        print(f"出错了:{e}")
        return 'error'

@app.route('/task', methods=['POST'])
async def my_task():
    await run_task()

@app.route('/restart', methods=['POST'])
async def restart_task():
    await handle_except()
    return 'My browser has been restart'

@app.errorhandler(Exception)
async def error_500(error):
    """这个handler可以catch住所有的abort(500)和raise exeception."""
    response = dict(status=0, message="500 Error")
    logutil.console("=== errorhandler == %s" % error)
    ret = {
    "state": "exception",
    "content": "中间出错",
    "response": str(response)
    }
    # 清空列表
    t = "%s == clear 报错时间500" % (str(datetime.datetime.now()))
    logutil.log('browser', t)
    
    return jsonify(ret)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # 启动 日志 模块
    logutil.start()
    # 启动 定时器 模块

    # 自循环生产者协程
    from data import data_fetch_request as dfr
    #import get_event_data

    #loop = asyncio.get_event_loop()
    
    #request_data = {'src':'Tyler'}
    request_data = {}
    #loop.create_task(dfr.get_event_data('', request_data))

    try:
        app.run(host='0.0.0.0', port=SERVER_PORT, debug=False, use_reloader=False, loop = loop)
    except Exception as e:
        logutil.log('browser', f"主循环出错信息:{e}")