'''
在主窗口打开的消息面板,所有系统消息都在此处查看,例如好友申请消息,系统广播消息
'''
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from QTBoard.BaseBoard import DiaBaseBoard
from QTWidget.AddFriendListItem import AddFriendListItem
from QTWidget.FriendRequestMesWidget import FriendRequestMesWidget
from Config import MessageManageType


class MessageManageBoard(DiaBaseBoard):
	def __init__(self,parent=None,topBoard=None):
		super().__init__(parent,topBoard)
		self.WIDTH = 270
		self.HEIGHT = 420
		self.data = None  #记录消息管理面板中的数据,格式:(消息类型,消息1,消息2......)
		self.clickState = 0
		self.initUI()
	def resetPosition(self):
		qr=self.frameGeometry()
		cp=self.parent.geometry().center()
		# cp.setY(cp.y()-150)
		qr.moveCenter(cp)
		self.move(qr.topLeft())
	def initUI(self):
		#连接自定义消息
		self.topBoard.Listener.updateMesBoard.connect(self.mesListUpdate)
		#定义布局
		layout_main=QVBoxLayout()
		layout_menu=QHBoxLayout()
		#定义控件
		self.button_sysMes=QPushButton()#系统通知按钮
		self.button_addFriendMes=QPushButton()#好友请求按钮
		self.list_message=QListWidget()#消息内容列表
		#定义属性
		# layout_main.setContentsMargins(0, 0, 0, 0)
		#定义样式
		# self.edit_search.setStyleSheet('border-radius:7px;border:1px solid #888')
		self.button_sysMes.setIcon(QIcon('Data/img/sysMes.png'))#setStyleSheet("border-image:url(Data/img/itemCal.png)")
		self.button_sysMes.setStyleSheet('background:transparent')
		self.button_sysMes.setIconSize(QSize(20,20))
		self.button_sysMes.setToolTip("系统消息")
		self.button_addFriendMes.setIcon(QIcon('Data/img/friendRequestMes.png'))#setStyleSheet("border-image:url(Data/img/itemCal.png)")
		self.button_addFriendMes.setStyleSheet('background:transparent')
		self.button_addFriendMes.setIconSize(QSize(20,20))
		self.button_addFriendMes.setToolTip("好友请求")
		# button_offline.setStyleSheet("QPushButton{border:0px} QPushButton:hover{color:#555}")
		self.button_sysMes.setCursor(QCursor(Qt.PointingHandCursor))
		self.button_sysMes.setStyleSheet("padding:10px;background:rgba(255,255,255,0)")
		self.button_addFriendMes.setCursor(QCursor(Qt.PointingHandCursor))
		self.button_addFriendMes.setStyleSheet("padding:10px;background:rgba(255,255,255,0)")


		#为布局添加控件和布局
		# layout_main.addSpacing(30)
		self.layoutAddWidget(layout_menu,QWidget(),size=(200,30),alignment=Qt.AlignRight)
		
		self.layoutAddWidget(layout_menu,self.button_addFriendMes,size=(30,30),alignment=Qt.AlignRight)
		self.layoutAddWidget(layout_menu,self.button_sysMes,size=(30,30),alignment=Qt.AlignRight)
		layout_main.addLayout(layout_menu)
		self.layoutAddWidget(layout_main,self.list_message)
		self.setLayout(layout_main)
		#为控件绑定事件
		self.button_addFriendMes.clicked.connect(self.clicked_addFriendMes_Event)
		self.button_sysMes.clicked.connect(self.clicked_sysMes_Event)

		icon = QIcon()
		icon.addPixmap(QPixmap("data/img/tt.ico"), QIcon.Normal, QIcon.Off)
		self.setWindowIcon(icon)
		self.setGeometry(500,500,self.WIDTH,self.HEIGHT)  

		self.resetPosition()
		# self.setAttribute(Qt.WA_TranslucentBackground)
		self.setWindowOpacity(0.8)
		self.setStyleSheet("messageManageBoard{border-radius:10px;border:1px solid black}")
		self.setWindowFlags( Qt.FramelessWindowHint| Qt.Tool)

		self.setMinimumSize(self.WIDTH,self.HEIGHT)
		self.setMaximumSize(self.WIDTH,self.HEIGHT)
		self.setWindowTitle('消息管理') 
		self.installEventFilter(self)
		# self.userListUpdate()
		self.show()
		self.activateWindow()
	def clicked_addFriendMes_Event(self):
		print('点击好友请求消息')
		if self.topBoard.operation.getMesFriendRequest():
			self.clickState=MessageManageType.FriendRequestMes
			self.button_addFriendMes.setStyleSheet("background:rgba(210,210,210,0.8);border:0px")
			self.button_sysMes.setStyleSheet("background:rgba(255,255,255,0)")

	def clicked_sysMes_Event(self):
		print('点击系统消息')
		self.clickState=MessageManageType.SysMes
		self.button_addFriendMes.setStyleSheet("background:rgba(255,255,255,0)")
		self.button_sysMes.setStyleSheet("background:rgba(210,210,210,0.8);border:0px")
	def mesListUpdate(self):
		self.list_message.clear()
		if self.data[0]==MessageManageType.SysMes:
			pass
		elif self.data[0]==MessageManageType.FriendRequestMes:
			if self.data and len(self.data)>1:
				for i in self.data[1:]:
					# x=(5,(2,'老王asdfdasfasdf',1),'2020-6-21 2:37:55')
					newitem=FriendRequestMesWidget(self,i)
					listitem=QListWidgetItem()
					listitem.setSizeHint(QSize(230,30))
					self.list_message.addItem(listitem)
					self.list_message.setItemWidget(listitem,newitem)
			else:
				newitem=QLabel('暂无任何好友请求')
				newitem.setAlignment(Qt.AlignCenter)
				listitem=QListWidgetItem()
				listitem.setSizeHint(QSize(200,20))
				self.list_message.addItem(listitem)
				self.list_message.setItemWidget(listitem,newitem)
			newitem=QLabel('<b>点击消息按钮刷新</b>')
			newitem.setStyleSheet("font-size:10px;color:#777")
			newitem.setAlignment(Qt.AlignCenter)
			listitem=QListWidgetItem()
			listitem.setSizeHint(QSize(200,12))
			self.list_message.addItem(listitem)
			self.list_message.setItemWidget(listitem,newitem)
	def eventFilter(self, obj, event):
	    if event.type() == QEvent.WindowDeactivate:
	        # self.close()  #点击其他程序窗口，会关闭该对话框
	        self.hide()
	        return True
	    else:
	        return super(MessageManageBoard, self).eventFilter(obj, event)
	# def search_Event(self):
	# 	self.topBoard.operation.getSearchData(self.edit_search.text())
