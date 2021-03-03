'''
一个可以捕获函数异常的装饰器，捕获的同时会将异常写在错误日志中，并记录详细错误信息。需要事先在被捕获的函数源文件目录下创建一个错误日志文件夹
'''
import time,threading
def catchError(func):
	def catch(*args,**kwargs):
		try:
			r=func(*args,**kwargs)
		except Exception as e:
			s="""函数名：%s\n函数地址：%s\n参数:%s----%s\n错误日志：%s\n"""%(func.__name__,str(func),str(args),str(kwargs),str(e))
			nowTime=time.localtime()
			nowTime="%s-%s-%s %s:%s:%s"%(nowTime.tm_year,nowTime.tm_mon,nowTime.tm_mday,nowTime.tm_hour,nowTime.tm_min,nowTime.tm_sec)
			with open('错误日志/%s错误日志.txt'%threading.current_thread().name,'a',encoding='utf-8') as f:
				f.write(nowTime+"-------"+s+'\n')
		else:
			return r
	return catch