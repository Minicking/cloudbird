import sys,socket,pickle,struct
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# from QTBoard.DataBoard import *
# from QTBoard.ListItem_itemData import *
# from QTBoard.ModifyBoard import *
from QTBoard.RegisterBoard import *
from QTBoard.BaseBoard import *
from QTWidget.TitleWidget import TitleWidget
from Config import *
from cbProtocol import CommunicationProtocol
class currentConfig:
	WIDTH=400
	HEIGHT=300
class LoginBoard(DiaBaseBoard):
	def __init__(self,parent=None,topBoard=None):
	    super().__init__(parent,topBoard)
	    self.success=False
	    self.socket=None
	    self.initUI()
	def initUI(self):
		#定义布局
		layout_main=QHBoxLayout()
		layout_right=QVBoxLayout()
		layout_right_button=QHBoxLayout()
		layout_main.setContentsMargins(0, 0, 0, 0)
		layout_right.setContentsMargins(0, 0, 0, 0)
		layout_right_button.setContentsMargins(0, 0, 0, 0)
		# layout_right_button.setContentsMargins(0,0,0,0)
		#定义控件
		self.widget_title=TitleWidget(self,(220,30))
		label_img_background=QLabel()
		self.edit_account=QLineEdit('tangzifan')
		self.edit_password=QLineEdit('123456')
		button_login=QPushButton('登录')
		button_regist=QPushButton('注册')
		button_offline=QPushButton('离线登录')
		#定义属性
		label_img_background.setPixmap(QPixmap('data/img/background.jpg'))
		label_img_background.setScaledContents(True)
		self.edit_account.setPlaceholderText("账号/邮箱")
		self.edit_password.setPlaceholderText("密码")
		self.edit_password.setEchoMode(QLineEdit.Password)
		layout_main.setContentsMargins(0, 0, 0, 0)
		#定义样式
		button_login.setStyleSheet("QPushButton{border:0px} QPushButton:hover{color:#555}")
		button_regist.setStyleSheet("QPushButton{border:0px} QPushButton:hover{color:#555}")
		# button_offline.setStyleSheet("QPushButton{border:0px} QPushButton:hover{color:#555}")
		self.edit_account.setStyleSheet("border-radius:7px;border:1px solid #888")
		self.edit_password.setStyleSheet("border-radius:7px;border:1px solid #888")
		button_offline.setStyleSheet("QPushButton:hover{color:black;} QPushButton{color:#aaa} ")
		
		button_offline.setCursor(QCursor(Qt.PointingHandCursor))
		button_login.setCursor(QCursor(Qt.PointingHandCursor))
		button_regist.setCursor(QCursor(Qt.PointingHandCursor))
		#为布局添加控件和布局
		self.layoutAddWidget(layout_right,self.widget_title,size=(260,30),alignment=Qt.AlignLeft)
		layout_right.addSpacing(40)
		self.layoutAddWidget(layout_right,self.edit_account,size=(150,25))
		layout_right.addSpacing(40)
		self.layoutAddWidget(layout_right,self.edit_password,size=(150,25))
		layout_right.addSpacing(50)
		self.layoutAddWidget(layout_right_button,button_login)
		self.layoutAddWidget(layout_right_button,button_regist)
		layout_right.addLayout(layout_right_button)
		layout_right.addSpacing(10)
		self.layoutAddWidget(layout_right,button_offline,size=(60,20))
		layout_right.addSpacing(20)
		self.layoutAddWidget(layout_main,label_img_background,size=(150,currentConfig.HEIGHT))
		# layout_main.addSpacing(50)
		layout_main.addLayout(layout_right)


		self.setLayout(layout_main)
		#为控件绑定事件
		self.widget_title.initEvent(self.close,self.minEvent)
		button_login.clicked.connect(self.button_login_Event)
		button_regist.clicked.connect(self.button_register_Event)
		button_offline.clicked.connect(self.button_offline_Event)

		
		self.setWindowFlags( Qt.FramelessWindowHint)
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
		self.setWindowTitle('登录') 
		self.exec_()
	def minEvent(self):
		self.showMinimized( )
	def connectServer(self):
		curSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		try:
			curSocket.connect(Config.ServerAddr)
		except Exception as e:
			print('连接失败',e)
			return False
		else:
			print('连接成功')
			return curSocket
	def login(self):
		account=self.edit_account.text()
		password=self.edit_password.text()
		curSocket=self.connectServer()
		successTag=False
		if curSocket:
			print('连上服务器，开始传输登录数据')
			message=CommunicationProtocol(PackTypeServer.Login,(account,password))
			if message.send(curSocket):
				print('数据发送成功，等待确认登录信息')
				confirmData=CommunicationProtocol.recv(curSocket)
				if confirmData and confirmData[0]==PackTypeClient.LoginConfirm:
					print('登录确认信息为：',confirmData)
					print(confirmData[1][0],type(confirmData[1][0]))
					if confirmData[1][0]==b'\x01':
						print('修改success为True')
						self.success=True
						self.socket=curSocket
						self.close()
					else:
						self.popUpMessage('登录失败(账号密码错误)')
				else:
					self.popUpMessage('登录失败(错误的验证信息)')
			else:
				self.popUpMessage('无法将登录信息发送至服务器，请稍后再试。')
			if not self.success:
				curSocket.close()
		else:
			self.popUpMessage('无法与服务器进行连接，请稍后再试。')
		
	def button_login_Event(self):
		self.login()
	def button_register_Event(self):
		register=RegisterBoard(self)
	def button_offline_Event(self):
		print('离线登录')
		self.success=True
		self.close()
