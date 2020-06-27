'''
	修改物品数据的面板类
	添加物品也是调用这个类，不提供构造参数就行了。
'''
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from QTBoard.BaseBoard import *
class ModifyBoard_Item(QLabel):#修改物品面板类中合成表内的物品类
	def __init__(self,data,topBoard,parent,itemname):
		super().__init__("%s×%d"%(data['name'],data['number']))
		self.data=data
		self.itemname=itemname
		self.topBoard=topBoard
		self.parent=parent
		self.setContextMenuPolicy(Qt.CustomContextMenu)
		self.customContextMenuRequested.connect(self.rightMenuShow)
	def rightMenuShow(self,pos):
		self.popMenu=QMenu()
		self.button_Modify=QAction('修改数据',self)
		self.button_Delete=QAction('删除物品',self)
		self.popMenu.addAction(self.button_Modify)
		self.popMenu.addAction(self.button_Delete)
		self.button_Modify.triggered.connect(self.button_Modify_Event)
		self.button_Delete.triggered.connect(self.button_Delete_Event)
		self.popMenu.exec_(self.mapToGlobal(pos))
	def button_Modify_Event(self):
		print('尝试修改')
		item=ModifyBoard_SelectItem(self,self.topBoard).result
		print('添加材料：',item)
		if item:
			if item[0]==self.itemname:
				self.parent.popUpMessage('不能以自身为合成材料')
			else:
				self.setText("%s×%d"%(item[0],item[1]))
				self.data['name'],self.data['number']=item[0],item[1]
	def button_Delete_Event(self):
		print('删除被点击的材料',self.data)
		print(self.parent.data)
		self.parent.data['formula'].remove(self.data)
		print(self.parent.data)
		self.parent.createFormulaList()
class ModifyBoard_SelectItem(DiaBaseBoard):#打开一个物品选择面板，从所有物品中选择一个
	def __init__(self,parent,topBoard):
		super().__init__(parent,topBoard)
		self.result=None
		self.closeTag=True
		self.initUI()
	def initUI(self):
		#定义控件
		self.selectLevel=QComboBox(self)
		self.searchBox=QLineEdit(self)
		self.list_widget=QListWidget(self)
		self.label_num=QLabel('数量',self)
		self.edit_num=QLineEdit('1',self)
		self.button_confirm=QPushButton("确认",self)
		#定义属性
		self.edit_num.setValidator(QIntValidator(1,9999))
		self.searchBox.setPlaceholderText('搜索')
		#添加数据
		self.data=self.topBoard.dataBoard.data
		for i in self.data:
			self.selectLevel.addItem("%d级装备[%d个]"%(i,len(self.data[i])))
		for i in self.data[1]:
			data=self.topBoard.Cal.itemList[i]
			self.displayItem(data)
		#定义布局
		layout_main=QVBoxLayout()
		layout_num=QHBoxLayout()
		#为布局添加控件与布局
		self.layoutAddWidget(layout_main,self.selectLevel,size=(120,20))
		self.layoutAddWidget(layout_main,self.searchBox,size=(120,20))
		self.layoutAddWidget(layout_main,self.list_widget,size=(120,200))
		self.layoutAddWidget(layout_num,self.label_num)
		self.layoutAddWidget(layout_num,self.edit_num,size=(50,20))
		layout_main.addLayout(layout_num)
		self.layoutAddWidget(layout_main,self.button_confirm,size=(40,20))
		#定义事件
		self.selectLevel.currentIndexChanged.connect(self.selectChange)
		self.button_confirm.clicked.connect(self.button_confirm_Event)
		self.searchBox.textChanged.connect(self.searchChange)
		self.setLayout(layout_main)
		self.setGeometry(self.topBoard.x()+self.topBoard.width(),self.topBoard.y()+35,170,320)        
		self.setMinimumSize(170,320)
		self.setMaximumSize(170,320)
		self.setWindowTitle('选择物品') 
		self.exec_()
	def displayItem(self,data):
		newitem=QLabel(data['name'])
		listitem=QListWidgetItem()
		listitem.setSizeHint(QSize(100,20))
		self.list_widget.addItem(listitem)
		self.list_widget.setItemWidget(listitem,newitem)
	def selectChange(self,index):
		self.list_widget.clear()
		index+=1
		for i in self.data[index]:
			data=self.topBoard.Cal.itemList[i]
			self.displayItem(data)
	def button_confirm_Event(self):
		r=self.list_widget.currentItem()
		widget=self.list_widget.itemWidget(r)
		if widget:
			self.result=(widget.text(),int(self.edit_num.text()))
		self.closeTag=False
		self.close()
	def searchChange(self,text):
		self.list_widget.clear()
		if text!='':
			count=0
			for i in self.data:
				for j in self.data[i]:
					if text in j:
						self.displayItem(self.topBoard.Cal.itemList[j])
						count+=1
			if count==0:
				self.list_widget.addItem("无符合关键词的物品")
		else:
			self.list_widget.addItem("无关键词")
	def closeEvent(self,event):
		if self.closeTag:
			print('关闭，不做物品选择')
class ModifyBoard(DiaBaseBoard):
	def __init__(self,data=None,parent=None,topBoard=None):
		super().__init__(parent,topBoard)
		print('test:',self.parent,self.topBoard)
		if data:
			self.data=data
			self.createTag=False
		else:
			self.data={'name':'新建物品','level':1,'formula':None,'number':1,'cost':1.0}
			self.createTag=True
		self.closeTag=True
		self.initUI()
	def initUI(self):
		#定义布局
		layout_main=QVBoxLayout()
		layout_main_top_1=QHBoxLayout()#装载物品名称
		layout_main_top_2=QHBoxLayout()#装载成本、单次合成数量
		layout_main_bottom=QVBoxLayout()#装载合成表显示框
		self.layout_bottom_itemlist=QVBoxLayout()
		#定义控件
		label_name=QLabel('物品名称(%d级)'%self.data['level'])
		if self.createTag:
			self.edit_name=QLineEdit(self.data['name'])
		else:
			self.edit_name=QLabel(self.data['name'])
		self.edit_name.setStyleSheet("border:1px solid black;")
		label_price=QLabel('成本')
		self.edit_price=QLineEdit(str(self.data['cost']))
		label_num=QLabel('合成产生数量')
		self.edit_num=QLineEdit(str(self.data['number']))
		self.display_formula=QWidget()
		self.display_formula.setObjectName('display_formula')
		self.button_confirm=QPushButton("确认")
		#定义属性
		self.display_formula.setStyleSheet("QWidget#display_formula{border: 1px solid rgb(0,0,0);}")
		self.edit_num.setValidator(QIntValidator(1,9999))
		self.edit_price.setValidator(QDoubleValidator(0,999999999,2))
		#为布局添加控件与布局
		self.layoutAddWidget(layout_main_top_1,label_name,size=(85,30))
		self.layoutAddWidget(layout_main_top_1,self.edit_name,size=(215,30))
		self.layoutAddWidget(layout_main_top_2,label_price,size=(25,30))
		self.layoutAddWidget(layout_main_top_2,self.edit_price,size=(105,30))
		self.layoutAddWidget(layout_main_top_2,label_num,size=(80,30))
		self.layoutAddWidget(layout_main_top_2,self.edit_num,size=(90,30))
		self.layoutAddWidget(layout_main_bottom,self.display_formula,size=(300,300))
		self.display_formula.setLayout(self.layout_bottom_itemlist)
		self.createFormulaList()
		self.layoutAddWidget(layout_main_bottom,self.button_confirm)
		layout_main.addLayout(layout_main_top_1)
		layout_main.addLayout(layout_main_top_2)
		layout_main.addLayout(layout_main_bottom)
		self.setLayout(layout_main)
		#定义事件
		self.button_confirm.clicked.connect(self.button_confirm_Event)
		self.setGeometry(self.topBoard.x()+self.topBoard.width(),self.topBoard.y()+35,300,300)        
		self.setMinimumSize(380,470)
		self.setMaximumSize(380,470)
		self.setWindowTitle('新建物品' if self.createTag else '修改数据') 
		self.exec_()
	def createFormulaList(self):
		#清空layout内所有widget
		for i in range(self.layout_bottom_itemlist.count()):
			print('fuck:',i,self.layout_bottom_itemlist.count())
			self.layout_bottom_itemlist.itemAt(i).widget().deleteLater()
		button_add=QPushButton("添加材料",self)
		if self.data['formula']:
			for i in self.data['formula']:
				nlabel=ModifyBoard_Item(i,self.topBoard,self,self.data['name'])
				nlabel.setStyleSheet('border:1px solid black;')
				self.layoutAddWidget(self.layout_bottom_itemlist,nlabel,alignment=Qt.AlignLeft,size=(280,20))
			self.layoutAddWidget(self.layout_bottom_itemlist,button_add,size=(280,20))
			self.layoutAddWidget(self.layout_bottom_itemlist,QWidget(),alignment=Qt.AlignLeft,size=(280,300-20-30*len(self.data['formula'])))
			
		else:
			self.layoutAddWidget(self.layout_bottom_itemlist,QLabel("无"),alignment=Qt.AlignLeft,size=(280,30))
			self.layoutAddWidget(self.layout_bottom_itemlist,button_add,size=(280,20))
			self.layoutAddWidget(self.layout_bottom_itemlist,QWidget(),alignment=Qt.AlignLeft,size=(280,250))
		button_add.clicked.connect(self.button_add_Event)
	def button_confirm_Event(self):
		self.data['name']=self.edit_name.text()
		self.data['number']=int(self.edit_num.text())
		self.data['cost']=float(self.edit_price.text())
		self.closeTag=False
		self.close()
	def button_add_Event(self):
		print('弹出选择物品框')
		item=ModifyBoard_SelectItem(self,self.topBoard).result
		print(self.data,item)
		
		print('选择了%s'%str(item))
		print(self.data)
		if item:
			if item[0] == self.data['name']:
				self.popUpMessage('不能以自身为制作材料')
				return
			flag=True
			if not self.data['formula']:
				self.data['formula']=[]
			for i in self.data['formula']:
				if i['name']==item[0]:
					print('此材料已存在于合成表中，不可重复添加')
					flag=False
					break
			if flag:
				self.data['formula'].append({'name':item[0],'number':item[1]})
		self.createFormulaList()
	def closeEvent(self,event):
		if self.closeTag:
			self.data=None
			print('关闭，不做修改物品')
		else:
			print('修改完成')