#-*-coding:utf-8-*-
'''
python操作mysql数据库基本类封装 - cxl283的博客 - CSDN博客  
https://blog.csdn.net/cxl283/article/details/73521831

python操作mysql数据库基本类封装 - cxl283的博客 - CSDN博客  
https://blog.csdn.net/cxl283/article/details/73521831

python -m pip install websockets -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com
python -m pip install --upgrade pip -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com
python3 -m pip install --upgrade pip -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com
'''

import re
import common
from base.baseobj import *
import pymysql as mdb
from dbutils.pooled_db import PooledDB, SharedDBConnection
from config import serverConfig
import logutil

host       = serverConfig.host
username   = serverConfig.username 
password   = serverConfig.password 
port       = serverConfig.port
database   = serverConfig.database

@Singleton
class MysqldbHelper(object):
	"""
	操作mysql数据库，基本方法
	"""
	def __init__(self , host, username, password, port, database):
		self.host = host
		self.username = username
		self.password = password
		self.database = database
		self.port = port
		self.con = None
		self.cur = None
		self.pool = PooledDB(mdb, 1, host=self.host, user=self.username, passwd=self.password, db=self.database, port=self.port, charset="utf8") # 5为连接池里的最少连接数
		self.con = self.pool.connection()
		self.cur = self.con.cursor()
		# try:
		# 	self.con = mdb.connect(host=self.host, user=self.username, passwd=self.password, port=self.port, db=self.database, charset="utf8")
		# 	# 所有的查询，都在连接 con 的一个模块 cursor 上面运行的
		# 	self.cur = self.con.cursor()
		# except:
		# 	logutil.log("error","DataBase connect error,please check the db config.")
		# 	raise "DataBase connect error,please check the db config."

	def __exit__(self, type, value, trace):
		self.cursor.close()
		self.conn.close()

	def refresh_db(self):
		#刷新数据库信息,否则只会拿到旧的数据
		#self.con.connect()
		self.con = self.pool.connection()
		self.cur = self.con.cursor()
		pass

	def close(self):
		"""
		关闭数据库连接

		"""
		self.cur.close()
		self.con.close()

	def get_version(self):
		"""获取数据库的版本号

		"""
		self.refresh_db()
		self.cur.execute("SELECT VERSION()")
		data = self.get_one_data()
		logutil.log("sql",str(data))
		return data

	def get_one_data(self):
		"""
		取得上个查询的结果，是单个结果
		"""
		data = self.cur.fetchone()
		return data

	def execute_commit(self,sql=''):
		"""执行数据库sql语句，针对更新,删除,事务等操作失败时回滚
		"""
		self.refresh_db()
		logutil.log("sql",sql)
		last_insert_id = 0
		try:
			self.cur.execute(sql)
			self.cur.execute("select last_insert_id();")
			last_insert_id = self.cur.fetchone()
			self.con.commit()
		except (mdb.Error) as e:
			self.con.rollback()
			error = 'MySQL execute failed! ERROR (%s): %s' %(e.args[0],e.args[1])
			logutil.log("error",error)
			return error
		return last_insert_id

	def execute_sql(self,sql=''):
		"""执行sql语句，针对读操作返回结果集

			args：
				sql  ：sql语句
		"""
		common.print_dt('sql == %s' % sql)
		self.refresh_db()
		try:
			self.cur.execute(sql)
			records = self.cur.fetchall()
			return records
		except (mdb.Error) as e:
			error = 'MySQL execute failed! ERROR (%s): %s' %(e.args[0],e.args[1])
			logutil.log("error",error)
			return error
############################################################################
	# def select(self, tablename, cond_dict='', order='', fields='*'):
	# 	"""查询数据

 # 			args：
	# 			tablename  ：表名字
	# 			cond_dict  ：查询条件
	# 			order      ：排序条件

	# 		example：
	# 			print mydb.select(table)
	# 			print mydb.select(table, fields=["name"])
	# 			print mydb.select(table, fields=["name", "age"])
	# 			print mydb.select(table, fields=["age", "name"])
	# 	"""
	# 	consql = ' '
	# 	if cond_dict!='':
	# 		for k, v in cond_dict.items():
	# 			consql = consql+k + '=' + v + ' and'
	# 	consql = consql + ' 1=1 '
	# 	if fields == "*":
	# 		sql = 'select * from %s where ' % tablename
	# 	else:
	# 		if isinstance(fields, list):
	# 			fields = ",".join(fields)
	# 			sql = 'select %s from %s where ' % (fields, tablename)
	# 		else:
	# 			raise "fields input error, please input list fields."
	# 	sql = sql + consql + order
	# 	print 'select: == ' + sql
	# 	print type(self.execute_sql(sql)[0])
	# 	return self.execute_sql(sql)
############################################################################
	#介于什么之间
	def between_and(self, tablename, cond_dict='', order='', fields='*'):
		"""查询数据

 			args：
				tablename  ：表名字
				cond_dict  ：查询条件
				order      ：排序条件

			example：
				print mydb.select(table)
				print mydb.select(table, fields=["name"])
				print mydb.select(table, fields=["name", "age"])
				print mydb.select(table, fields=["age", "name"])
		"""
		self.refresh_db()
		consql = ' '
		if cond_dict!='':
			for k, v in cond_dict.items():
				consql = consql + k + ' between ' + v[0] + ' and ' + v[1] 
		consql = consql
		if fields == "*":
			sql = 'select * from %s where ' % tablename
		else:
			if isinstance(fields, list):
				fields = ",".join(fields)
				sql = 'select %s from %s where ' % (fields, tablename)
			else:
				raise "fields input error, please input list fields."
		sql = sql + consql + order
		#print ('select: == ' + sql)
		#print type(self.execute_sql(sql)[0])
		return self.execute_sql(sql)
		#SELECT * FROM `amber1`.`sign_in1` WHERE `logintime` BETWEEN '2018-11-17 09:09:52' AND '2018-11-19 17:10:57' LIMIT 0, 1000

	def insert_many(self, table, attrs, values):
		"""插入多条数据
			args：
				tablename  ：表名字
				attrs        ：属性键
				values      ：属性值

			example：
				table='test_mysqldb'
				key = ["id" ,"name", "age"]
				value = [[101, "liuqiao", "25"], [102,"liuqiao1", "26"], [103 ,"liuqiao2", "27"], [104 ,"liuqiao3", "28"]]
				mydb.insert_many(table, key, value)
		"""
		self.refresh_db()
		self.con = self.pool.connection()
		self.cur = self.con.cursor()
		values_sql = ['%s' for v in attrs]
		attrs_sql = '('+','.join(attrs)+')'
		values_sql = ' values('+','.join(values_sql)+')'
		sql = 'insert into %s'% table
		sql = sql + attrs_sql + values_sql
		try:
			for i in range(0,len(values),20000):
				self.cur.executemany(sql,values[i:i+20000])
				self.con.commit()
			return ("success")
		except (mdb.Error) as e:
			self.con.rollback()
			error = 'insert_many executemany failed! ERROR (%s): %s' %(e.args[0],e.args[1])
			error = error + " === " + table
			logutil.log("error",error)
			common.print_dt (error)
			return error

if "gdDBSQL" not in globals():
	gdDBSQL = MysqldbHelper(host, username, password, port, database)

def db_select(sql=''):
	global gdDBSQL
	common.print_dt("gdDBSQL.get_version() == %s" % gdDBSQL.get_version())
	print(gdDBSQL.execute_sql(sql))
	print(gdDBSQL.execute_commit("UPDATE `gh_building`.`tb_login` SET `gh_value` = '777' WHERE `id` = 2;"))

async def db_check_active():
	global gdDBSQL
	logutil.log("sql","检查数据库活跃链接")
	gdDBSQL.get_version()
