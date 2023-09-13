# coding=utf-8
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
from . import loggerManager
from . import define
import logging
from . import timeUtil
import datetime

MAX_CACHE_COUNT = 100  # 最大缓存日志条数
MAX_FLUSH_TIME = 1000  # 最大写入时间间隔ms
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

if '_log_queue' not in globals():
    _log_queue = multiprocessing.Queue()
    _log_cache = []
    _last_flush_time = 0

if '_executor' not in globals():
    _executor = ThreadPoolExecutor(max_workers=1)

if 'started' not in globals():
    started = False

if '_print' not in globals():
    _print = True            # 设置为False则显示控制台，线上应该为True


def log(log_name, content, report=True):
    log_info = {
        'log_name': log_name,
        'content': content,
        'report': report,
    }
    log_all = {
        'log_name': "all",
        'content': log_name+"|"+content,
        'report': report,
    }
    # flush_logs(log_info)
    flush_logs(log_all)


def console(content, report=True):
    show_console = True
    if not _print:
        print(content)
        return None
    if not show_console:
        return None
    log_info = {
        'log_name': define.CONSOLE_LOGGER,
        'content': content,
        'report': report,
    }
    if not started:
        print(content)
    flush_logs(log_info)


def flush_logs(log_info):
    global _log_cache
    global _log_queue
    global _last_flush_time
    now = datetime.datetime.now()
    # log_info['time'] = datetime.datetime.strftime(
    #                         now, DATETIME_FORMAT)
    log_info['time'] = str(now)
    _log_cache.append(log_info)
    now = timeUtil.mill_second()
    if len(_log_cache) >= MAX_CACHE_COUNT or \
            (now - _last_flush_time) >= MAX_FLUSH_TIME:
        # 缓存部分再一次刷入,减少锁的消耗
        _log_queue.put_nowait(_log_cache)
        _last_flush_time = now
        _log_cache = []


def _log_worker(queue):
    global _log_queue
    while True:
        try:
            logs = _log_queue.get()
            for log_info in logs:
                log_name = log_info.get('log_name', None)
                content = log_info.get('content', None)
                time = log_info.get('time', None)
                report = log_info.get('report', False)
                if not log_name or not content or not time:
                    continue
                loggerManager.get_logger_manager() \
                    .get_logger(log_name).debug("%s|%s" % (time, content))
        except Exception as e:
            pass


# def _log_worker(queue):
#     while True:
#         try:
#             global _log_queue
#             print("log size:", _log_queue.qsize())
#             log_info = _log_queue.get_nowait()
#             log_name = log_info.get('log_name', None)
#             content = log_info.get('content', None)
#             if not log_name or not content:
#                 continue
#             loggerManager.get_logger_manager()\
#                 .get_logger(log_name).debug(content)
#         except Exception as e:
#             print("heheh")

def start():
    global started
    global _executor
    global _log_queue
    started = True
    _executor.submit(_log_worker, (_log_queue,))
    console("log start!")
