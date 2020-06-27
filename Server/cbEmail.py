from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from Config import Config
import threading
class Email:
	def __init__(self,Config=None):
		try:
			self.smtp=SMTP_SSL(host=Config.email_host)
			self.smtp.login(user=Config.email_sender,password=Config.email_password)
		except Exception as e:
			print('email初始化失败',e)
		self.sender=Config.email_sender
		self.password=Config.email_password
	def __str__(self):
		return "sender:%s\npassword:%s"%(self.sender,self.password)
	def __del__(self):
		self.smtp.close()
	def _thread_send(self,data,Type):
		if Type==0:
			msg = MIMEText("您接收到了来自云鸟的注册验证码<div style='color:red;font-size:15px;display:inline'>%s</div>，请于5分钟内使用,过期失效。"%(data['confirm']),'HTML',_charset="utf8")
		msg["Subject"] = "云鸟"
		msg["from"] = self.sender
		msg["to"] = data['target']
		self.smtp.sendmail(from_addr=self.sender,to_addrs=data['target'], msg=msg.as_string())
	def send(self,data,Type=0):
		'''
		type：0 验证码信息 data={'target':目标邮箱,'confirm':计算得到的验证码}
		type：1 @信息      data={'target':目标邮箱,'text':用户A@了你：内容}
		'''
		thread=threading.Thread(target=self._thread_send,args=(data,Type))
		thread.start()
		return True
if __name__ == '__main__':
	e=Email(Config)
	e.send({'target':'1018842028@qq.com','confirm':'ecja'},0)
	# a=bin(5)
	# print(a,type(a))