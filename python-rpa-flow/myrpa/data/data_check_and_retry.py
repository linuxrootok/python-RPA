import json
import asyncio
from functools import wraps
from .data_noneError import NoneError
import logutil

def check_data_retry(max_retry=5, retry_interval=1):

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            print(args)
            for i in range(max_retry):
                # Wait for the element to appear on the page
                task = asyncio.create_task(func(*args, **kwargs))
                await asyncio.wait_for(task, timeout=3000)
                
                # Check if data exists and return True if it does
                res = task.result()
                #print(f"装饰体内的获取结果:{res},类型:{type(res)}") 
                if res:
                    if res['code'] == 200:
                        return res
                await asyncio.sleep(retry_interval)
            
            # If data does not exist after max_retry attempts, raise an error
            print(f"获取数据尝试第 {i+1} 次")
            logutil.log('browser', f"获取数据尝试第 {i+1} 次")
            raise NoneError(f'RPA jobs {args[2]} data is empty now!')
        
        return wrapper
    
    return decorator
