'''
	用于物品数据面板DataBoard中的物品数据类
'''
import sys,copy
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Config import *
# from QTBoard.DataBoard import *
# from QTBoard.ListItem_itemData import *
from QTBoard.ModifyBoard import *
class ListItem_itemData(QWidget):
	def __init__(self,data,mainboard):
		super().__init__()
		self.data=data
		self.mainboard=mainboard
		layout_main=QHBoxLayout()#整体布局为横向布局
		layout_main.addStretch(0)
		self.name=QLabel(data['name'])
		self.name.resize(80,35)
		self.level=QLabel(str(data['level'])+'级')
		self.level.resize(20,35)
		layout_right=QVBoxLayout()#右边为纵向布局
		nt=QLabel('合成表')
		nt.setAlignment(Qt.AlignCenter)
		self.mainboard.layoutAddWidget(layout_right,nt,size=(400,15))
		self.layout_right_down=QHBoxLayout()#右下为横向布局
		if data['formula']:
			w=400/len(data['formula'])
			for i in data['formula']:
				nt=QLabel("%s*%d"%(i['name'],i['number']))
				nt.setAlignment(Qt.AlignCenter)
				self.mainboard.layoutAddWidget(self.layout_right_down,nt,size=(w,20))
		else:
			nt=QLabel("无")
			nt.setAlignment(Qt.AlignCenter)
			self.mainboard.layoutAddWidget(self.layout_right_down,nt,size=(400,20))
		layout_right.addLayout(self.layout_right_down)
		#按照顺序添加控件
		self.mainboard.layoutAddWidget(layout_main,self.name,Qt.AlignLeft,size=(100,40))
		self.mainboard.layoutAddWidget(layout_main,self.level,Qt.AlignLeft,size=(30,40))
		layout_main.addLayout(layout_right)
		self.setLayout(layout_main)
		self.setContextMenuPolicy(Qt.CustomContextMenu)
		self.customContextMenuRequested.connect(self.rightMenuShow)
	
	def rightMenuShow(self,pos):
		self.popMenu=QMenu()
		self.button_Cal=QAction('计算合成信息',self)
		self.button_Make=QAction('查询可合成物品',self)
		self.button_Modify=QAction('修改物品数据',self)
		self.button_Delete=QAction('删除此物品',self)
		self.popMenu.addAction(self.button_Cal)
		self.popMenu.addAction(self.button_Make)
		self.popMenu.addAction(self.button_Modify)
		self.popMenu.addAction(self.button_Delete)
		self.button_Cal.triggered.connect(self.button_Cal_Event)
		self.button_Make.triggered.connect(self.button_Make_Event)
		self.button_Modify.triggered.connect(self.button_Modify_Event)
		self.button_Delete.triggered.connect(self.button_Delete_Event)
		self.popMenu.exec_(self.mapToGlobal(pos))
	def button_Cal_Event(self):
		self.mainboard.edit_input_name.setText(self.data['name'])
		self.mainboard.edit_input_num.setText('1')
		self.mainboard.button_CalEvent()
	def button_Make_Event(self):
		self.mainboard.edit_input_name.setText(self.data['name'])
		self.mainboard.button_MateEvent()
	def updateItemInfo(self,item):
		for i in self.mainboard.Cal.itemList:
			if self.mainboard.Cal.itemList[i]['formula']:
				flag=False
				for j in self.mainboard.Cal.itemList[i]['formula']:
					if j['name']==item:
						flag=True
						break
				if flag:
					# 更新物品的等级
					maxLevel2=0
					for k in self.mainboard.Cal.itemList[i]['formula']:
						if self.mainboard.Cal.itemList[k['name']]['level']>maxLevel2:
							maxLevel2=self.mainboard.Cal.itemList[k['name']]['level']
					maxLevel2+=1
					print('物品%s的等级应更新为%d'%(i,maxLevel2))
					oldLevel=self.mainboard.Cal.itemList[i]['level']
					self.mainboard.Cal.itemList[i]['level']=maxLevel2
					# 更新物品在dataBoard中所在的级别位置
					self.mainboard.dataBoard.data[oldLevel].remove(i)
					print('将%s从%d添加到%d物品中'%(i,oldLevel,self.mainboard.Cal.itemList[i]['level']))
					if self.mainboard.Cal.itemList[i]['level'] not in self.mainboard.dataBoard.data:
						self.mainboard.dataBoard.data[self.mainboard.Cal.itemList[i]['level']]=[i]
					else:
						self.mainboard.dataBoard.data[self.mainboard.Cal.itemList[i]['level']].append(i)
					self.updateItemInfo(i)
	def button_Modify_Event(self):
		print('修改此物品数据',self.data)
		data=ModifyBoard(copy.deepcopy(self.data),self,self.mainboard).data
		print('得到的修改数据：',data)
		if not data:
			print('取消修改')
		else:
			self.data['formula']=data['formula']
			self.data['number']=data['number']
			self.data['cost']=data['cost']
			print('修改完成')
			#清空layout内所有widget
			for i in range(self.layout_right_down.count()):
				print(i,self.layout_right_down.count())
				self.layout_right_down.itemAt(i).widget().deleteLater()
			#将更新后的合成表数据显示出来
			if data['formula']:
				w=400/len(data['formula'])
				for i in data['formula']:
					nt=QLabel("%s*%d"%(i['name'],i['number']))
					# nt.setStyleSheet('border:1px solid black;')
					nt.setAlignment(Qt.AlignCenter)
					self.mainboard.layoutAddWidget(self.layout_right_down,nt,size=(w,20))
			else:
				nt=QLabel("无")
				nt.setAlignment(Qt.AlignCenter)
				self.mainboard.layoutAddWidget(self.layout_right_down,nt,size=(400,20))
			#更新被修改物品的等级
			maxLevel=0
			if data['formula']:
				for i in data['formula']:
					if self.mainboard.Cal.itemList[i['name']]['level']>maxLevel:
						maxLevel=self.mainboard.Cal.itemList[i['name']]['level']
			if maxLevel+1!=data['level']:
				oldLevel=data['level']
				self.mainboard.Cal.itemList[data['name']]['level']=maxLevel+1
				self.data['level']=maxLevel+1
				self.name.setText(data['name'])
				self.level.setText(str(data['level'])+'级')
				print('将%s从%d级物品中移除'%(data['name'],oldLevel))
				self.mainboard.dataBoard.data[oldLevel].remove(data['name'])
				print('将%s从%d添加到%d物品中'%(data['name'],oldLevel,self.data['level']))
				self.mainboard.dataBoard.data[self.data['level']].append(data['name'])
				#更新所有合成涉及到被修改物品的物品的等级
				self.updateItemInfo(data['name'])
				self.mainboard.dataBoard.createItemLevelList()
				self.mainboard.dataBoard.searchBox.setText('')
				self.mainboard.dataBoard.searchBox.setText(data['name'])
	def button_Delete_Event(self):
		reply=QMessageBox.question(self,'提示',"是否确定要删除此物品?",QMessageBox.Yes|QMessageBox.No)
		if reply==QMessageBox.Yes:
			print('确认删除')
			flag=True
			for i in self.mainboard.Cal.itemList:
				item=self.mainboard.Cal.itemList[i]
				if item['formula']:
					for j in item['formula']:
						if j['name']==self.data['name']:
							self.mainBoard.popUpMessage('此物品包含于其他物品的合成表中，无法删除。')
							flag=False
							break
				if flag==False:
					break
			if flag:
				self.mainboard.Cal.itemList.pop(self.data['name'])
				for i in self.mainboard.dataBoard.data:
					if self.data['name'] in self.mainboard.dataBoard.data[i]:
						print('数据面板：从%d级物品中去除%s'%(i,self.data['name']))
						self.mainboard.dataBoard.data[i].remove(self.data['name'])
						index=i
						break
				if self.mainboard.dataBoard.data[index]==[]:
					self.mainboard.dataBoard.data.pop(index)
				self.mainboard.dataBoard.createItemLevelList()
				self.mainBoard.popUpMessage('删除[%s]成功！'%self.data['name'])
