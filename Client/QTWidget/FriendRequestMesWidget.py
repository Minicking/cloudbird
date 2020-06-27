from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
class FriendRequestMesWidget(QWidget):
	def __init__(self,parent=None,data=None):
		super().__init__()
		self.data=data#(消息ID,请求者数据(ID,名称,认证状态),请求发起时间)
		self.parent=parent
		self.initUI()

	def initUI(self):
		#创建控件
		qss='''
			QPushButton{border:1px solid rgba(255,255,255,1);font-size:9px;color:black} 
			QPushButton:hover{border:1px solid rgba(0,0,0,0);font-size:9px;color:red}
		'''
		self.label_text=QLabel("<b>%s</b>(#%d)请求加你为好友"%(self.data[1][1],self.data[1][0]))
		self.label_date=QLabel("%s"%self.data[2])
		self.label_date.setAlignment(Qt.AlignCenter)
		self.label_date.setStyleSheet("font-size:10px;color:#888")
		if self.data[1][2]==0:
			self.label_certicication=QLabel('未认证')
			self.label_certicication.setStyleSheet('color:red;font-size:10px;font-weight:800')
		else:
			self.label_certicication=QLabel('已认证')
			self.label_certicication.setStyleSheet('color:green;font-size:10px;font-weight:800')
		self.button_agree=QPushButton('同意')
		self.button_refuse=QPushButton('拒绝')
		self.setStyleSheet(qss)
		self.button_agree.setCursor(QCursor(Qt.PointingHandCursor))
		self.button_refuse.setCursor(QCursor(Qt.PointingHandCursor))

		# self.label_text.setStyleSheet('border:1px solid red')
		# self.label_certicication.setStyleSheet('border:1px solid red')
		# self.label_date.setStyleSheet('border:1px solid red')
		# self.button_agree.setStyleSheet('border:1px solid red')
		# self.button_refuse.setStyleSheet('border:1px solid red')
		#创建布局

		layout_main=QHBoxLayout()#主布局为水平布局
		layout_left=QVBoxLayout()#主左区域为垂直布局
		layout_right=QVBoxLayout()#主右区域为垂直布局
		layout_left_top=QHBoxLayout()#主左上区域为水平布局
		layout_main.setContentsMargins(0, 0, 0, 0)
		layout_left.setContentsMargins(0, 0, 0, 0)
		layout_right.setContentsMargins(0, 0, 0, 0)
		layout_left_top.setContentsMargins(0, 0, 0, 0)

		self.parent.layoutAddWidget(layout_left_top,self.label_text,size=(155,20))
		self.parent.layoutAddWidget(layout_left_top,self.label_certicication,size=(35,20))
		layout_left.addLayout(layout_left_top)
		self.parent.layoutAddWidget(layout_left,self.label_date,size=(180,10))

		self.parent.layoutAddWidget(layout_right,self.button_agree,size=(30,15))
		self.parent.layoutAddWidget(layout_right,self.button_refuse,size=(30,15))
		layout_main.addLayout(layout_left)
		layout_main.addLayout(layout_right)

		self.setLayout(layout_main)
		#为控件绑定事件
		self.button_agree.clicked.connect(self.agree_Event)
		self.button_refuse.clicked.connect(self.refuse_Event)
	def agree_Event(self):
		print('点击同意好友请求',self.data)
		self.parent.topBoard.operation.responseFriendRequest(self.data[0],1)
	def refuse_Event(self):
		print('点击拒绝好友请求',self.data)
		self.parent.topBoard.operation.responseFriendRequest(self.data[0],0)
	# def addEvent(self):
	# 	print('发起对用户',self.data,'的添加好友请求')
	# 	data=self.parent.topBoard.widget_userinfo.data
	# 	if data['id']==self.data[0]:
	# 		print('发起人和目标者为同一人,不可进行好友申请')
	# 		self.parent.topBoard.popUpMessage('不可对自己发送好友申请')
	# 		return
	# 	self.parent.topBoard.operation.addFriend(self.data[0])