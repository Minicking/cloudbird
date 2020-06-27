import sys,socket,pickle,struct,re,requests,hashlib
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from QTBoard.BaseBoard import *
from Config import *
from cbProtocol import CommunicationProtocol
class currentConfig:
	WIDTH=300
	HEIGHT=300
class ConfirmButton(QPushButton):
	def __init__(self,parent,text):
		super().__init__(text)
		self.clicked.connect(self.clickedEvent)
		self.parent=parent
		self.timer=None
	def clickedEvent(self):
		print('触发点击')
		email=self.parent.edit_email.text()
		l=re.compile('[0-9a-z]+@[0-9a-z]+\.com').findall(email)
		if l==[]:
			self.parent.popUpMessage("不是一个可用的邮箱")
			return 
		try:
			x=requests.get('http://%s:%d/getconfirmcode?email=%s'%(Config.HTTPAddr[0],Config.HTTPAddr[1],email),headers={'confirm':hashlib.md5(email.encode('utf-8')).hexdigest()[::3]})
		except Exception as e:
			self.parent.popUpMessage('无法获取验证码,请检查网络状态与软件是否为最新版本.错误代码:101 %s'%str(e))
		else:
			r=self.parent.processHttpResponse(x)
			if r==True:
				self.setEnabled(False)
				self.waitTime=60
				self.setText('邮件已发送(%d)'%self.waitTime)
				if not self.timer:
					self.timer=QBasicTimer()
				self.timer.start(1000,self)
			else:
				self.parent.popUpMessage(r[1])
	def timerEvent(self,e):
		self.waitTime-=1
		if self.waitTime>0:
			self.setText('邮件已发送(%d)'%self.waitTime)
		else:
			self.setEnabled(True)
			self.waitTime=0
			self.setText('获取验证码')
			self.timer.stop()
class RegisterBoard(DiaBaseBoard):
	def __init__(self,parent=None,topBoard=None):
	    super().__init__(parent,topBoard)
	    self.success=False
	    self.socket=None
	    self.initUI()
	def processHttpResponse(self,response):
		if response.status_code==200:
			return True
		elif response.status_code==202:
			print(dir(response))
			return (False,'请求失败:%s'%response.text)
		elif response.status_code==403:
			return (False,'请求出现错误,请检查软件是否为最新版本.错误代码:102')
		elif response.status_code==500:
			return (False,'服务器出现错误.错误代码:103')
		elif response.status_code==404:
			return (False,'因为您被判为恶意用户,服务器拒绝您的请求.错误代码:104')
		elif response.status_code==405:
			return (False,'非法的访问请求.错误代码:105')

	def initUI(self):
		#定义布局
		layout_main=QHBoxLayout()
		layout_right=QVBoxLayout()
		layout_confirm=QHBoxLayout()
		layout_right_button=QHBoxLayout()
		#定义控件
		# label_img_background=QLabel()
		self.edit_account=QLineEdit('tangzifan')
		self.edit_name=QLineEdit('云中鸟')
		self.edit_password=QLineEdit('123456')
		self.edit_repassword=QLineEdit('123456')
		self.edit_email=QLineEdit('547250643@qq.com')
		self.edit_confirmcode=QLineEdit()
		self.button_register=QPushButton('确认注册')
		self.button_back=QPushButton('返回')
		self.button_getconfirmcode=ConfirmButton(self,'获取验证码')
		#定义属性
		# label_img_background.setPixmap(QPixmap('data/img/background.jpg'))
		# label_img_background.setScaledContents(True)
		self.edit_account.setPlaceholderText("账号")
		self.edit_password.setPlaceholderText("密码")
		self.edit_repassword.setPlaceholderText("重复输入密码")
		self.edit_email.setPlaceholderText("邮箱")
		self.edit_confirmcode.setPlaceholderText('验证码')
		self.edit_password.setEchoMode(QLineEdit.Password)
		self.edit_repassword.setEchoMode(QLineEdit.Password)
		layout_main.setContentsMargins(0, 0, 0, 0)
		layout_right_button.setContentsMargins(0, 0, 0, 0)
		#定义样式
		# self.setStyleSheet("QPushButton{border:0px} QPushButton:hover{color:#555;border:1px solid #ddd}")
		self.setStyleSheet("QLineEdit{border-radius:7px;border:1px solid #888}")
		# self.button_register.setStyleSheet("background:rgb(150,150,150)")
		# self.button_back.setStyleSheet("background:rgb(150,150,150)")
		# self.edit_account.setStyleSheet("border-radius:7px;border:1px solid #888")
		# self.edit_password.setStyleSheet("border-radius:7px;border:1px solid #888")

		self.button_back.setCursor(QCursor(Qt.PointingHandCursor))
		self.button_register.setCursor(QCursor(Qt.PointingHandCursor))
		#为布局添加控件和布局
		self.layoutAddWidget(layout_right,self.edit_account,size=(150,25))
		self.layoutAddWidget(layout_right,self.edit_password,size=(150,25))
		self.layoutAddWidget(layout_right,self.edit_repassword,size=(150,25))
		self.layoutAddWidget(layout_right,self.edit_email,size=(150,25))
		self.layoutAddWidget(layout_confirm,self.edit_confirmcode,size=(100,25))
		self.layoutAddWidget(layout_confirm,self.button_getconfirmcode,size=(110,25))
		layout_right.addLayout(layout_confirm)
		self.layoutAddWidget(layout_right_button,self.button_register)
		# layout_right_button.addSpacing(30)
		self.layoutAddWidget(layout_right_button,self.button_back)
		layout_right.addLayout(layout_right_button)
		# self.layoutAddWidget(layout_right,button_offline,size=(60,20))
		# self.layoutAddWidget(layout_main,label_img_background,size=(150,currentConfig.HEIGHT))
		layout_main.addSpacing(50)
		layout_main.addLayout(layout_right)
		layout_main.addSpacing(50)

		self.setLayout(layout_main)
		#为控件绑定事件
		self.button_register.clicked.connect(self.event_button_register)
		# self.button_getconfirmcode.clicked.connect(self.event_button_getconfirmcode)
		# button_offline.clicked.connect(self.button_offline_Event)

		icon = QIcon()
		icon.addPixmap(QPixmap("data/img/tt.ico"), QIcon.Normal, QIcon.Off)
		self.setWindowIcon(icon)
		self.setGeometry(500,500,currentConfig.WIDTH,currentConfig.HEIGHT)  
		qr=self.frameGeometry()
		cp=QDesktopWidget().availableGeometry().center()      
		qr.moveCenter(cp)
		self.move(qr.topLeft())
		self.setMinimumSize(currentConfig.WIDTH,currentConfig.HEIGHT)
		self.setMaximumSize(currentConfig.WIDTH,currentConfig.HEIGHT)
		self.setWindowTitle('注册') 
		self.exec_()
	def event_button_register(self):
		account=self.edit_account.text()
		password=self.edit_password.text()
		password_re=self.edit_repassword.text()
		email=self.edit_email.text()
		confirmcode=self.edit_confirmcode.text()
		if password!=password_re:
			self.popUpMessage("两次密码不一致")
			return
		l=re.compile('[0-9a-z]+@[0-9a-z]+\.com').findall(email)
		if l==[]:
			self.popUpMessage("不是一个可用的邮箱")
			return
		if len(account)<6:
			self.popUpMessage("账号太短、最小长度为6个字符")
			return
		elif len(account)>15:
			self.popUpMessage("账号太长、最大长度为15个字符")
			return
		if len(password)>20:
			self.popUpMessage("密码太长、最大长度为20个字符")
			return
		elif len(password)<6:
			self.popUpMessage("密码太短、最小长度为6个字符")
			return
		print('数据合法，向服务器发送注册请求')
		try:
			x=requests.get('http://%s:%d/register?account=%s&password=%s&email=%s&confirmcode=%s'%(Config.HTTPAddr[0],Config.HTTPAddr[1],account,password,email,confirmcode),headers={'confirm':hashlib.md5(email.encode('utf-8')).hexdigest()[::3]})
		except Exception as e:
			self.popUpMessage('服务器出现错误,暂时无法进行访问,请稍后再试')
		else:
			r=self.processHttpResponse(x)
			if r==True:
				self.popUpMessage('注册成功')
				self.parent.edit_account.setText(account)
				self.parent.edit_password.setText(password)
				self.close()
			else:
				self.popUpMessage(r[1])