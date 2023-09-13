#coding=utf-8
import logging
import time

class HourlyFileHandler(logging.FileHandler):
    """
    文件名以当前时间命名,粒度为一小时
    """
    def __init__(self, filename, mode='a', encoding="utf-8", delay=False):
        self._cur_filename = ''
        logging.FileHandler.__init__(self, filename, mode, encoding, delay)

    #override
    def emit(self, record):
        #当前文件与当前时间对不上,关闭文件,重新根据当前时间创建文件
        try:
            if self._cur_filename != self.timed_filename():
                self.close()
            logging.FileHandler.emit(self, record) 
        except Exception:
            self.handleError(record)

    #override
    def _open(self):
        self._cur_filename = self.timed_filename()
        return open(self._cur_filename, self.mode, 
                encoding=self.encoding)

    def timed_filename(self):
        current_time = int(time.time())
        time_tuple = time.localtime(current_time)
        filename = self.baseFilename + '.' + \
            time.strftime("%Y-%m-%d-%H", time_tuple)
        return filename