#-*-coding:utf-8-*-	
import functools
import time

# 单例模式
def Singleton(cls):
	"""
	单例模式
	@Singleton
	class MyClass(object):
		pass
	"""
	cls.__ori_new__ = cls.__new__
	cls.__ori_ini__ = cls.__init__

	@functools.wraps(cls.__new__)
	def _replace_new(_cls, *args, **kwargs):
		if not hasattr(_cls, '__singleton_instance__'):
			# print('create instance ', _cls)
			instance = _cls.__ori_new__(_cls)
			instance.__ori_ini__(*args, **kwargs)
			setattr(_cls, '__singleton_instance__', instance)

		return getattr(_cls, '__singleton_instance__')

	# 替换cls.__new__
	cls.__new__ = staticmethod(_replace_new)
	# 替换cls.__init__保证多次实例化对象__init__只会在对象第一次创建的时候被调用一次
	cls.__init__ = lambda self, *args, **kwargs: None

	return cls



if __name__ == '__main__':
	pass