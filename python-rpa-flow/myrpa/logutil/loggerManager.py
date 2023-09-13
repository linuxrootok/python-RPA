# coding=utf-8
import sys
import time
import logging
import logging.handlers
import os
from . import define
from . import handler

s_log_dir = 'logs'

class Logger(object):
	"""
	日志封装
	log_name直接对应目录文件
	@example login 		===>login/login.log 
			 login.net 	===>login/net/net.log
	"""
	def __init__(self, log_name):
		self._log_name = log_name
		self._logger = logging.getLogger(self._log_name)
		self._filename = None

	def config(self):
		if not s_log_dir:
			raise Exception('you need specify log directory!')
		
		log_dir = os.path.abspath(s_log_dir)
		if not os.path.exists(log_dir):
			os.mkdir(log_dir)

		if not self._log_name:
			raise Exception('logger has no name!')

		#steam handler
		fmt = logging.Formatter(define.FORMAT)
		if self._log_name == define.CONSOLE_LOGGER and True:
			stream_handler = logging.StreamHandler(sys.stdout)
			stream_handler.setFormatter(fmt)
			self._logger.addHandler(stream_handler)
		elif True:
			stream_handler = logging.StreamHandler(sys.stdout)
			stream_handler.setFormatter(fmt)
			self._logger.addHandler(stream_handler)

		dirs = self._log_name.split('.')
		path = log_dir
		for _dir in dirs:
			path = os.path.join(path, _dir)
			if not os.path.exists(path):
				os.mkdir(path)
		self._filename = os.path.join(path,'%s%s'%(
			dirs[len(dirs)-1], define.SUFFIX))
				
		#time rotate file handler
		# file_handler = logging.handlers.TimedRotatingFileHandler(
		# 	self._filename, when='h', interval=1)
		file_handler = handler.HourlyFileHandler(self._filename)
		file_handler.setFormatter(fmt)
		self._logger.addHandler(file_handler)
		self._logger.setLevel(logging.DEBUG)

	def get_logger(self):
		return self._logger

class LoggerManager(object):
	def __init__(self):
		self._logger_map = {}

	def get_logger(self, log_name):
		logger = self._logger_map.get(log_name, None)
		if not logger:
			logger = Logger(log_name)
			logger.config()
			self._logger_map[log_name] = logger
		return logger.get_logger()

if '_logger_mng' not in globals():
	_logger_mng = LoggerManager()

def get_logger_manager():
	global _logger_mng
	return _logger_mng