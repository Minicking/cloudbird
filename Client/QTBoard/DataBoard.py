'''
	物品数据面板类,通过物品合成计算程序窗口进行打开,
	在里面可以进行合成物品的配方修改添加删除操作.
'''
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from QTBoard.DataBoard import *
from QTBoard.ModifyBoard import *
from QTBoard.BaseBoard import *
from QTWidget.ListItem_itemData import *
class DataBoard(BaseBoard):
	def __init__(self,parent=None,topBoard=None):
		super(DataBoard,self).__init__(parent,topBoard)
		self.HEIGHT=500
		self.WIDTH=560
		self.data=None
		self.initUI()
	def initUI(self):
		#创建控件
		self.list_widget=QListWidget()
		self.comboBox=QComboBox()
		self.button_addItem=QPushButton("添加新物品")
		data={}
		for i in self.parent.Cal.itemList:
			item=self.parent.Cal.itemList[i]
			if item['level'] in data:
				data[item['level']].append(item['name'])
			else:
				data[item['level']]=[item['name']]
		self.data=data
		self.createItemLevelList()
		self.searchBox=QLineEdit()
		self.searchBox.setPlaceholderText("搜索")
		#创建布局
		self.layout_main=QVBoxLayout()
		#为布局添加控件和布局
		self.layoutAddWidget(self.layout_main,self.comboBox,size=(self.WIDTH-40,30))
		self.layoutAddWidget(self.layout_main,self.searchBox,size=(self.WIDTH-40,30))
		self.layoutAddWidget(self.layout_main,self.list_widget,size=(self.WIDTH-40,self.HEIGHT-150))
		self.layoutAddWidget(self.layout_main,self.button_addItem,alignment=Qt.AlignRight)
		#为控件连接事件消息
		self.comboBox.currentIndexChanged.connect(self.selectChange)
		self.searchBox.textChanged.connect(self.searchChange)
		self.button_addItem.clicked.connect(self.button_addItem_Event)
		self.setLayout(self.layout_main)
		self.setGeometry(self.parent.x()+self.parent.width(), self.parent.y()+30,Config.BOARD[1]+Config.BOARD[3]+self.WIDTH,Config.BOARD[0]+Config.BOARD[2]+self.HEIGHT )        
		self.setMinimumSize(Config.BOARD[1]+Config.BOARD[3]+self.WIDTH,Config.BOARD[0]+Config.BOARD[2]+self.HEIGHT )
		self.setMaximumSize(Config.BOARD[1]+Config.BOARD[3]+self.WIDTH,Config.BOARD[0]+Config.BOARD[2]+self.HEIGHT )
		self.setWindowTitle('物品列表') 
		self.show()
	def closeEvent(self,event):
		self.parent.dataBoard=None
		self.parent.Cal.writeDataFile()
	def selectChange(self,index):
		self.list_widget.clear()
		if index>0:
			count=0
			for i in self.data[index]:
				data=self.parent.Cal.itemList[i]
				self.displayItem(data)
				count+=1
	def createItemLevelList(self):
		self.comboBox.clear()
		self.comboBox.addItem("无")
		for i in range(len(self.data)):
			self.comboBox.addItem("%d级物品[%d个]"%(i+1,len(self.data[i+1])))
	def displayItem(self,data):
		newitem=ListItem_itemData(data,self.parent)#self.createItem(data)
		listitem=QListWidgetItem()
		listitem.setSizeHint(QSize(300,50))
		self.list_widget.addItem(listitem)
		self.list_widget.setItemWidget(listitem,newitem)
	def searchChange(self,text):
		self.list_widget.clear()
		if text!='':
			count=0
			for i in self.data:
				for j in self.data[i]:
					if text in j:
						data=self.parent.Cal.itemList[j]
						self.displayItem(data)
						count+=1
			if count==0:
				self.list_widget.addItem("无符合关键词的物品")
		else:
			self.list_widget.addItem("无关键词")
	def button_addItem_Event(self):
		print('创建新物品')
		data=ModifyBoard(None,self,self.topBoard).data
		print(data)
		flag=True
		if data:
			for i in self.parent.Cal.itemList:
				if i == data['name']:
					self.popUpMessage('此物品已存在，无法重复添加')
					flag=False
					break
			if flag:
				maxLevel=0
				if data['formula']:
					for i in data['formula']:
						if self.parent.Cal.itemList[i['name']]['level']>maxLevel:
							maxLevel=self.parent.Cal.itemList[i['name']]['level']
				data['level']=maxLevel+1
				print('判断新物品的等级为%d'%data['level'])
				self.parent.Cal.itemList[data['name']]=data
				if data['level'] in self.data:
					self.data[data['level']].append(data['name'])
				else:
					self.data[data['level']]=[data['name']]
				self.createItemLevelList()
				self.searchBox.setText(data['name'])
				self.popUpMessage('新物品[%s(%d级)]添加成功'%(data['name'],data['level']))