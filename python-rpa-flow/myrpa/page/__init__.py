from functools import wraps
import asyncio
import logutil
async def input_text_clear(page, xid):
    logutil.log('正在清空input框内字符')
    await page.evaluate(f'document.getElementById("{xid}").value = ""')

def retry_on_exception(times, delay=1, exceptions=(Exception,)):

    def decorator(func):
        params = {'times': 3, '_timeout': 5000}
        @wraps(func)
        async def wrapper(*args, **kwargs):
            #print(f"参数是:{args}")
            '''
            if params.get('times', 3):
                times = params['times']
            if params.get('_timeout', 5000):
                #args[3] = params['_timeout']
                new_args = list(args)
                new_args[3] = params['_timeout']
            '''
            for _ in range(times):
                try:
                    return await func(*args, **kwargs)
                except exceptions as ex:
                    print(f'Retrying due to {str(ex)}')
                    await asyncio.sleep(delay)
            #return await func(*args, **kwargs)
            print('All retries failed! Stop execution')
            return False
        def set_param(param, value):
            params[param] = value
        wrapper.set_param = set_param
        return wrapper
    return decorator