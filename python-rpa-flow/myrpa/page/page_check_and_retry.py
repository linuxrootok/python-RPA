import asyncio
from functools import wraps
from pyppeteer import launch
from pyppeteer.errors import ElementHandleError

def check_xpath_exists(xpath, max_retry=3, retry_interval=1):

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            page = args[0]
            
            for i in range(max_retry):
                try:
                    # Wait for the element to appear on the page
                    await page.waitForXPath(xpath, timeout=2000)
                    
                    # Check if element exists and return True if it does
                    element = await page.xpath(xpath)
                    if element:
                        return await func(*args, **kwargs)
                    
                except ElementHandleError:
                    # If element does not exist, catch the error                    # and retry after interval
                    await asyncio.sleep(retry_interval)
            
            # If element does not exist after max_retry attempts, raise an error
            raise ValueError(f"Element '{xpath}' not found on page.")
        
        return wrapper
    
    return decorator
