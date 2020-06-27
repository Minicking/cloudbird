from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
class AddFriendListItem(QWidget):
	def __init__(self,parent=None,data=None):
		super().__init__()
		self.data=data
		self.parent=parent
		self.initUI()

	def initUI(self):
		#创建控件
		self.label_name=QLabel(self.data[1])
		if self.data[2]==0:
			self.label_certicication=QLabel('未认证')
			self.label_certicication.setStyleSheet('color:red;font-size:10px;font-weight:800')
		else:
			self.label_certicication=QLabel('已认证')
			self.label_certicication.setStyleSheet('color:green;font-size:10px;font-weight:800')

		self.button_add=QPushButton('添加')
		#创建布局
		layout_main=QHBoxLayout()
		layout_main.setContentsMargins(0, 0, 0, 0)
		#为控件设置属性
		self.label_name.setStyleSheet('font-size:12px')
		self.button_add.setStyleSheet('QPushButton{border:0px;color:white} QPushButton:hover{background:rgb(230,230,230);color:black;border-radius:5px}')
		self.button_add.setCursor(QCursor(Qt.PointingHandCursor))

		self.label_certicication.setScaledContents(True)
		#为控件绑定事件
		self.button_add.clicked.connect(self.addEvent)

		self.parent.layoutAddWidget(layout_main,self.label_name,size=(120,20))
		self.parent.layoutAddWidget(layout_main,self.label_certicication,size=(50,20))
		self.parent.layoutAddWidget(layout_main,self.button_add,size=(50,20))
		self.setLayout(layout_main)
	def addEvent(self):
		print('发起对用户',self.data,'的添加好友请求')
		data=self.parent.topBoard.widget_userinfo.data
		if data['id']==self.data[0]:
			print('发起人和目标者为同一人,不可进行好友申请')
			self.parent.topBoard.popUpMessage('不可对自己发送好友申请')
			return
		self.parent.topBoard.operation.addFriend(self.data[0])