# coding=utf-8
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import dbutil
from browser.Browser import Browser, Page

scheduler = AsyncIOScheduler()

# 采用date的方式，在特定时间里执行一次，2秒后执行动作
# scheduler.add_job(operation.user_action, 'date', run_date=timedelta_seconds(2), args=[data, TAX_USER_REGISTER_TIMEOUT, start_time])


# 每天晚上23点59分关闭浏览器
#scheduler.add_job(Browser.Browser.close, 'cron', hour='23', minute='58')

# 间隔60秒，定时检查数据库连接池活跃连接
#scheduler.add_job(dbutil.db_check_active, 'interval', seconds=2)

def start():
    '''启动定时器'''
    scheduler.start()