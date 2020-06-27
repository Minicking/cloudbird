'''
在主窗口进行添加好友操作时创建的用户搜索窗口
'''
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from QTBoard.BaseBoard import *
from QTWidget.AddFriendListItem import AddFriendListItem
class AddFriendBoard(DiaBaseBoard):
	def __init__(self,parent=None,topBoard=None):
	    super().__init__(parent,topBoard)
	    self.WIDTH=270
	    self.HEIGHT=420
	    self.data=None
	    self.initUI()
	def resetPosition(self):
		qr=self.frameGeometry()
		cp=self.parent.geometry().center()
		# cp.setY(cp.y()-150)
		qr.moveCenter(cp)
		self.move(qr.topLeft())
	def initUI(self):
		self.topBoard.Listener.updateUserListSignal.connect(self.userListUpdate)


		#定义布局
		layout_main=QVBoxLayout()
		layout_search=QHBoxLayout()
		#定义控件
		self.edit_search=QLineEdit()
		button_search=QPushButton()
		self.list_user=QListWidget()
		#定义属性

		self.edit_search.setPlaceholderText("输入用户名或#id进行用户搜索")
		# layout_main.setContentsMargins(0, 0, 0, 0)
		#定义样式
		self.edit_search.setStyleSheet('border-radius:7px;border:1px solid #888')
		button_search.setIcon(QIcon('Data/img/search.jpg'))#setStyleSheet("border-image:url(Data/img/itemCal.png)")
		button_search.setStyleSheet('background:transparent')
		button_search.setIconSize(QSize(25,25))
		button_search.setToolTip("添加好友")
		# button_offline.setStyleSheet("QPushButton{border:0px} QPushButton:hover{color:#555}")
		button_search.setCursor(QCursor(Qt.PointingHandCursor))

		#为布局添加控件和布局
		# layout_main.addSpacing(30)
		self.layoutAddWidget(layout_search,self.edit_search,size=(200,25))
		self.layoutAddWidget(layout_search,button_search,size=(50,25),alignment=Qt.AlignLeft)
		layout_main.addLayout(layout_search)
		self.layoutAddWidget(layout_main,self.list_user)
		self.setLayout(layout_main)
		#为控件绑定事件
		button_search.clicked.connect(self.search_Event)

		icon = QIcon()
		icon.addPixmap(QPixmap("data/img/tt.ico"), QIcon.Normal, QIcon.Off)
		self.setWindowIcon(icon)
		self.setGeometry(500,500,self.WIDTH,self.HEIGHT)  

		self.resetPosition()
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.setWindowFlags( Qt.FramelessWindowHint| Qt.Tool)
		
		self.setMinimumSize(self.WIDTH,self.HEIGHT)
		self.setMaximumSize(self.WIDTH,self.HEIGHT)
		self.setWindowTitle('添加好友') 
		self.installEventFilter(self)
		self.userListUpdate()
		self.show()
		self.activateWindow()

	def userListUpdate(self):
		print('调用刷新搜索结果')
		self.list_user.clear()
		if self.data and len(self.data)>0:
			if self.data[0]:
				friendlist=self.topBoard.widget_userinfo.data['friendlist']
				friendlistID=[]
				for i in friendlist:
					friendlistID.append(i['id'])
				for i in self.data:
					newitem=AddFriendListItem(self,i)#QLabel(str(i))
					if newitem.data[0] in friendlistID:
						newitem.button_add.setText('已添加')
						newitem.button_add.setStyleSheet('QPushButton{background:rgb(230,230,230);color:black;border-radius:5px}')
						newitem.button_add.setEnabled(False)
					elif newitem.data[0]==self.topBoard.widget_userinfo.data['id']:
						newitem.button_add.setText('自己')
						newitem.button_add.setStyleSheet('QPushButton{background:rgb(230,230,230);color:black;border-radius:5px}')
						newitem.button_add.setEnabled(False)
					listitem=QListWidgetItem()
					listitem.setFlags(Qt.NoItemFlags)
					listitem.setSizeHint(QSize(220,20))
					self.list_user.addItem(listitem)
					self.list_user.setItemWidget(listitem,newitem)
				return
			else:
				newitem=QLabel('无匹配结果')
		else:
			newitem=QLabel('未搜索')
		newitem.setAlignment(Qt.AlignCenter)
		listitem=QListWidgetItem()
		listitem.setSizeHint(QSize(200,20))
		self.list_user.addItem(listitem)
		self.list_user.setItemWidget(listitem,newitem)
	def eventFilter(self, obj, event):
	    if event.type() == QEvent.WindowDeactivate:
	        # self.close()  #点击其他程序窗口，会关闭该对话框
	        self.hide()
	        return True
	    else:
	        return super(AddFriendBoard, self).eventFilter(obj, event)
	def search_Event(self):
		self.topBoard.operation.getSearchData(self.edit_search.text())
