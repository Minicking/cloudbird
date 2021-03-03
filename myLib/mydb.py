'''
自己使用的一个基于pymysql的数据库类，方便自己操作数据库
带有一个线程锁,默认状态下只有一个只有一个游标可以使用
'''
import pymysql,time
import threading
def CheckMySQL(func):
	def catch(*args,**kwargs):
		count=0
		while True:
			try:
				r=func(*args,**kwargs)
			except Exception as e:
				print('有问题,试图重连',e)
				count+=1
				args[0].lock.release()
				args[0].connectMySQL()
			else:
				break
			if count>10:
				print('重连失败')
				break
		if count>0:
			print('重连次数：',count)
		return r
	return catch
class mysqldb:
	def __init__(self,host,username,password,library):
		self.host=host
		self.username=username
		self.password=password
		self.library=library
		self.connectMySQL()
		self.lock=threading.Lock()
	def getNowTime(self):
		nowTime=time.localtime()
		nowTime="%s-%s-%s %s:%s:%s"%(nowTime.tm_year,nowTime.tm_mon,nowTime.tm_mday,nowTime.tm_hour,nowTime.tm_min,nowTime.tm_sec)
		return nowTime
	def connectMySQL(self):
		self.db=pymysql.connect(self.host,self.username,self.password,self.library)
	def __del__(self):

		self.db.close()
	@CheckMySQL
	def executeSQL(self,sql):
		self.lock.acquire()
		cursor=self.db.cursor()
		try:
			for i in sql:
				cursor.execute(i)
		except Exception as e:
			print('ERROR:executeSQL:',e)
			self.db.rollback()
			cursor.close()
			self.lock.release()
			return False
		else:
			self.db.commit()
			cursor.close()
			self.lock.release()
			return True
	@CheckMySQL
	def selectFrom_all(self,table):
		self.lock.acquire()
		cursor=self.db.cursor()
		result=cursor.execute('select * from %s'%table)
		self.db.commit()
		cursor.close()
		self.lock.release()
		return result,cursor.fetchall()
	@CheckMySQL
	def deleteFromWhere(self,table,condition):
		self.lock.acquire()
		cursor=self.db.cursor()
		if condition=="":
			sql='delete from %s;'%(table)
		else:
			sql='delete from %s where %s;'%(table,condition)
		result=cursor.execute(sql)
		self.db.commit()
		cursor.close()
		self.lock.release()
	@CheckMySQL
	def selectFromWhere(self,table,condition):
		self.lock.acquire()
		cursor=self.db.cursor()
		if condition=="":
			sql='select * from %s;'%(table)
		else:
			sql='select * from %s where %s;'%(table,condition)
		result=cursor.execute(sql)
		self.db.commit()
		cursor.close()
		self.lock.release()
		return result,cursor.fetchall()#数量、结果列表
	@CheckMySQL
	def selectColumnFromWhere(self,table,col,condition):
		self.lock.acquire()
		cursor=self.db.cursor()
		if condition=="":
			sql='select %s from %s;'%(col,table)
		else:
			sql='select %s from %s where %s;'%(col,table,condition)
		count=cursor.execute(sql)
		self.db.commit()
		cursor.close() 
		result=[]
		for i in cursor.fetchall():
			result.append(i[0])
		self.lock.release()
		return count,result#数量、结果列表
	def exist(self,table,data):
		'''
		判断table表内是否含有符合要求的数据
		data{'字段':数据,'字段':数据....}多个字段 只要一个符合
		'''
		where=''
		for i in data:
			if where=='':
				if type(data[i])==str:
					where='%s=\'%s\''%(i,data[i])
				else:
					where='%s=%s'%(i,data[i])
			else:
				if type(data[i])==str:
					where+='or %s=\'%s\''%(i,data[i])
				else:
					where+='or %s=%s'%(i,data[i])
		# print(table,where)
		result=self.selectFromWhere(table,where)
		# print('exist:',result)
		if result[0]>0:
			return result[1][0][0]
		else:
			return False
	def update(self,table,data):
		'''
		更新数据，必须有一个id作为主键指向需要修改的目标数据
		'''
		sql=''
		idkey=None
		for i in data:
			if 'id' not in i:
				if sql=='':
					if type(data[i])==str:
						sql="%s='%s'"%(i,data[i])
					else:
						sql="%s=%s"%(i,data[i])
				else:
					if type(data[i])==str:
						sql+=",%s='%s'"%(i,data[i])
					else:
						sql+=",%s=%s"%(i,data[i])
			else:
				idkey=i
		if idkey:
			sql="update %s set "%table+sql+" where %s=%s;"%(idkey,data[idkey])
			return self.executeSQL([sql])
			
		else:
			return False
	@CheckMySQL
	def insertTo(self,table,data):
		#data---{'列名':数据`````````}
		part1=table+'('
		part2='('
		for i in data:
			part1+=i+','
			part2+='\''+str(data[i]).replace("\\","\\\\").replace("'","\\\'").replace("\"","\\\"").replace("--","- -")+'\','
		part1=part1[:len(part1)-1]+')'
		part2=part2[:len(part2)-1]+')'
		self.lock.acquire()
		cursor=self.db.cursor()
		try:
			cursor.execute('insert into %s value %s'%(part1,part2))
		except Exception as e:
			print('执行插入出错',e)
			self.lock.release()
			self.db.rollback()
			return None
		else:
			self.db.commit()
		insertID=cursor.lastrowid
		cursor.close()
		self.lock.release()
		return insertID
if __name__ == '__main__':
	tdb=mysqldb('127.0.0.1','root','123456','cb')
	r,s=tdb.selectColumnFromWhere('user','name','login=0')
	print(r)
	print(s)