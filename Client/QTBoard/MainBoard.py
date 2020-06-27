import json,sys,time,os,threading
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from QTBoard.BaseBoard import *
from QTBoard.ItemCalBoard import ItemCalBoard
from QTBoard.MessageManageBoard import MessageManageBoard
from QTBoard.AddFriendBoard import AddFriendBoard
from QTWidget.UserInfoWidget import UserInfoWidget
from QTWidget.FriendInfoWidget import FriendInfoWidget
from QTWidget.TitleWidget import TitleWidget
from cbProtocol import CommunicationProtocol
from Config import *

class listenThread(QThread):
	updateFrendListSignal=pyqtSignal()
	updateUserListSignal=pyqtSignal()
	updateMesBoard=pyqtSignal()
	def __init__(self,parent,sock):
		super().__init__()
		self.socket=sock
		self.parent=parent
	def run(self):
		while True:
			Data=CommunicationProtocol.recv(self.socket)
			if Data:
				self.processData(Data)
			else:
				print('接收到错误数据包，结束')
				sock.close()
				break
	def processData(self,data):
		if data[0]==PackTypeClient.UserInfo:
			print('数据包为用户信息:')
			self.parent.userdata=data[1][0]
			with open('myphoto.jpg','wb') as f:
				f.write(self.parent.userdata['photo'])
			self.updateFrendListSignal.emit()
			self.parent.widget_userinfo.data=self.parent.userdata
			self.parent.widget_userinfo.update()
		if data[0]==PackTypeClient.Heart:
			pass
		if data[0]==PackTypeClient.SearchUserData:
			print('数据包为搜索的用户数据:')
			if self.parent.addFriendBoard:
				self.parent.addFriendBoard.data=data[1]
				self.updateUserListSignal.emit()
		if data[0]==PackTypeClient.PutMesOfFriendRequest:
			print('数据包为好友请求消息:')
			print(data)
			self.parent.messageManageBoard.data=data[1]
			self.updateMesBoard.emit()
			self.updateUserListSignal.emit()

class operation:
	def __init__(self,sock,topBoard):
		self.socket=sock
		self.topBoard=topBoard
	def getSearchData(self,tag):
		print('尝试搜索[%s]相关数据'%tag)
		if len(tag)>0:
			if tag[0]=='#':
				id_=tag[1:]
				if  not id_.isdigit():
					self.topBoard.popUpMessage('用户ID只能为数字')
					return
		else:
			self.topBoard.popUpMessage('关键字不能为空')
			return
		message=CommunicationProtocol(PackTypeServer.SearchUser,(tag,))
		if message.send(self.socket):
			print('获取搜索用户数据的请求发出成功')
		else:
			self.topBoard.popUpMessage('搜索失败,请检查网络状态后再尝试')
	def addFriend(self,id_):
		message=CommunicationProtocol(PackTypeServer.AddFriend,(id_,))
		if message.send(self.socket):
			self.topBoard.popUpMessage('好友请求发送成功!等待对方验证')
		else:
			self.topBoard.popUpMessage('好友请求发送失败,请检查网络状态后再尝试')
	def getMesFriendRequest(self):
		message=CommunicationProtocol(PackTypeServer.GetMesOfFriendRequest)
		if message.send(self.socket):
			print('发送[获取好友请求消息]请求成功')
			return True
		else:
			print('发送[获取好友请求消息]请求失败')
			return False
	def responseFriendRequest(self,mesID,ans):
		message=CommunicationProtocol(PackTypeServer.FriendRequestResponse,(mesID,ans))
		if message.send(self.socket):
			print('回应好友请求成功')
			return True
		else:
			print('回应好友请求失败')
			return False
class MainBoard(BaseBoard):
	def __init__(self,sock=None):
		super().__init__()
		self.initAttr()
		self.initUI()
		self.initSystemTray()
		if sock:
			self.socket=sock
			self.initUser()
	def initAttr(self):
		self.HEIGHT=700
		self.WIDTH=300
		self.addFriendBoard=None
		self.messageManageBoard=None
		self.socket=None
	def initUI(self):
		#创建控件
		self.widget_title=TitleWidget(self,(300,30))
		self.widget_userinfo=UserInfoWidget(self)
		self.list_friend=QListWidget()#好友列表控件
		self.button_tool_addFriend=QPushButton()
		self.button_tool_messageManage=QPushButton()
		self.button_function_itemCal=QPushButton()
		#创建布局
		
		self.layout_main=QVBoxLayout()#主布局为垂直
		self.layout_userinfo=QHBoxLayout()#用户信息为水平布局
		self.layout_friend=QVBoxLayout()#好友列表为垂直布局
		self.layout_tools=QHBoxLayout()
		self.layout_function=QHBoxLayout()

		self.layout_tools.setSpacing(0)
		#设置控件属性

		

		self.setStyleSheet('MainBoard{background:url(Data/img/mainBackground.jpg) no-repeat}')
		self.button_tool_addFriend.setIcon(QIcon('Data/img/addFriend.png'))#setStyleSheet("border-image:url(Data/img/itemCal.png)")
		self.button_tool_addFriend.setStyleSheet('QPushButton{background:transparent} QPushButton:hover{background:rgba(200,200,200,0.5);border:0px solid black}')
		self.button_tool_addFriend.setIconSize(QSize(25,25))
		self.button_tool_addFriend.setToolTip("添加好友")
		self.button_tool_messageManage.setIcon(QIcon('Data/img/message.png'))#setStyleSheet("border-image:url(Data/img/itemCal.png)")
		self.button_tool_messageManage.setStyleSheet('QPushButton{background:transparent} QPushButton:hover{background:rgba(200,200,200,0.5);border:0px solid black}')
		self.button_tool_messageManage.setIconSize(QSize(25,25))
		self.button_tool_messageManage.setToolTip("查看系统消息")

		self.list_friend.setStyleSheet('QListWidget{background:rgba(255,255,255,0.3)}')

		self.button_function_itemCal.setIcon(QIcon('Data/img/itemCal.png'))#setStyleSheet("border-image:url(Data/img/itemCal.png)")
		self.button_function_itemCal.setStyleSheet('background:transparent')
		self.button_function_itemCal.setIconSize(QSize(25,25))
		self.button_function_itemCal.setToolTip("打开我的世界材料计算程序")
		#为布局添加控件和布局
		
		# self.layoutAddWidget(self.layout_title,QWidget(),size=(260,20))
		# self.layoutAddWidget(self.layout_title,self.button_title_min,size=(20,20))
		# self.layoutAddWidget(self.layout_title,self.button_title_close,size=(20,20))
		
		self.layoutAddWidget(self.layout_userinfo,self.widget_userinfo)
		self.layoutAddWidget(self.layout_tools,QWidget(),size=(210,25),alignment=Qt.AlignLeft)
		self.layoutAddWidget(self.layout_tools,self.button_tool_messageManage,size=(35,35),alignment=Qt.AlignLeft)
		self.layoutAddWidget(self.layout_tools,self.button_tool_addFriend,size=(35,35),alignment=Qt.AlignLeft)
		self.layoutAddWidget(self.layout_friend,self.list_friend)
		self.layoutAddWidget(self.layout_function,self.button_function_itemCal,size=(25,25),alignment=Qt.AlignRight)
		
		self.layoutAddWidget(self.layout_main,self.widget_title)
		self.layout_main.addLayout(self.layout_userinfo)
		self.layout_main.addLayout(self.layout_tools)
		self.layout_main.addLayout(self.layout_friend)
		self.layout_main.addLayout(self.layout_function)
		#为控件连接事件消息
		self.widget_title.initEvent(self.close,self.minEvent)
		self.button_tool_messageManage.clicked.connect(self.event_Button_messageManage)
		self.button_tool_addFriend.clicked.connect(self.event_Button_addFriend)
		self.button_function_itemCal.clicked.connect(self.event_Button_itemCal)
		self.list_friend.itemDoubleClicked.connect(self.doubleClickedFriend)

		self.layout_main.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self.layout_main)
		self.setWindowFlags( Qt.FramelessWindowHint| Qt.Tool)
		# self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
		self.setFixedSize(self.WIDTH,Config.BOARD[0]+self.HEIGHT);
		self.setWindowTitle('云鸟') 
		icon = QIcon()
		icon.addPixmap(QPixmap("data/img/tt.ico"), QIcon.Normal, QIcon.Off)
		self.setWindowIcon(icon)

		self.show()
	def doubleClickedFriend(self,event):
		print('双机')
		print(event,dir(event))
		print(dir(event.listWidget().currentItem()))
	def initSystemTray(self):
		self.mSysTrayIcon = QSystemTrayIcon(self)
		icon = QIcon("data/img/tt.ico")
		self.mSysTrayIcon.setIcon(icon)
		self.mSysTrayIcon.setToolTip("云鸟")
		self.mSysTrayIcon.activated.connect(self.onActivated)
		self.mSysTrayIcon.show()
	def initUser(self):
		if self.socket:
			self.operation=operation(self.socket,self)
			self.Listener=listenThread(self,self.socket)#threading.Thread(target=self.Listener_action,args=(self.socket,))
			# self.Listener.setDaemon(True)
			self.Listener.start()
			print('开启服务端信息监听')
			self.Listener.updateFrendListSignal.connect(self.friendListUpdate)

	def friendListUpdate(self):
		self.list_friend.clear()
		if len(self.userdata['friendlist'])>0:
			for i in self.userdata['friendlist']:
				print('创建一个好友控件:',i['id'],i['name'],i['certification'])
				newitem=FriendInfoWidget(self,i)
				listitem=QListWidgetItem()
				listitem.setSizeHint(QSize(220,50))
				self.list_friend.addItem(listitem)
				self.list_friend.setItemWidget(listitem,newitem)

		else:
			newitem=QLabel('交一个朋友吧')
			newitem.setAlignment(Qt.AlignCenter)
			listitem=QListWidgetItem()
			listitem.setSizeHint(QSize(250,20))
			self.list_friend.addItem(listitem)
			self.list_friend.setItemWidget(listitem,newitem)
	def minEvent(self):
		self.hide()
		
	def onActivated(self, reason):
		# if reason == self.mSysTrayIcon.Trigger:
		if self.isHidden():
			# self.setWindowFlags(Qt.WindowStaysOnTopHint|Qt.FramelessWindowHint| Qt.Tool)
			# self.setWindowFlags(Qt.FramelessWindowHint| Qt.Tool)
			self.activateWindow()
			self.show()
		else:
			self.hide()
		
		
		# self.raise_()

	def closeEvent(self,event):
		exit(0)
	def event_Button_itemCal(self):
		self.itemCalBorad=ItemCalBoard(self,self)
	def event_Button_addFriend(self):
		if self.addFriendBoard:
			if self.addFriendBoard.isHidden():
				self.addFriendBoard.resetPosition()
				self.addFriendBoard.show()
				self.addFriendBoard.activateWindow()
			else:
				self.addFriendBoard.hide()
		else:
			self.addFriendBoard=AddFriendBoard(self,self)

	def event_Button_messageManage(self):
		if self.messageManageBoard:
			if self.messageManageBoard.isHidden():
				self.messageManageBoard.resetPosition()
				self.messageManageBoard.show()
				self.messageManageBoard.activateWindow()
			else:
				self.messageManageBoard.hide()
		else:
			self.messageManageBoard=MessageManageBoard(self,self)