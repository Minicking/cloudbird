import os,sys,json,pickle,chardet
from PyQt5.QtWidgets import QLabel,QMenu,QAction
from PyQt5.QtCore import Qt
class Config:
	WIDTH=350
	HEIGHT=450
	BOARD=(0,0,0,0)
	VERSION='1.0.0'
	AUTHOR='云中鸟'
	workDir=os.path.dirname(sys.argv[0])
	dataFile=workDir+r'\Data\data.cb'
	ServerAddr=('127.0.0.1',20202)
	HTTPAddr=('127.0.0.1',20203)
	# ServerAddr=('47.103.200.210',25565)
class StimulusType:
	GetUserInfo=1#刺激客户端发起获取用户基本信息请求
class MessageManageType:
	SysMes=1
	FriendRequestMes=2
class PackTypeClient:#客户端接收的包 服务器发送的包
	Heart=1
	LoginConfirm=2
	UserInfo=3
	FriendList=4
	SearchUserData=5
	PutMesOfFriendRequest=6
class PackTypeServer:#服务器接收的包 客户端发送的包
	Login=1
	SearchUser=2
	AddFriend=3
	GetMesOfFriendRequest=4
	FriendRequestResponse=5
class DisplayMessage(QLabel):
	'''
	{'type':0/1,'text':'abc','name':'石英'}
	type:0 普通说明类消息
	     1 可点击类物品消息
	'''
	def __init__(self,Type=0,text=None,name=None):
		super().__init__(text)
		self.type=Type
		self.setWordWrap(True)
		if self.type==1:
			self.name=name
		self.setContextMenuPolicy(Qt.CustomContextMenu)
		self.customContextMenuRequested.connect(self.rightMenuShow)
	def rightMenuShow(self,pos):
		if self.type==1:
			self.popMenu=QMenu()
			self.button_1=QAction('暂无操作',self)
			self.popMenu.addAction(self.button_1)
			self.button_1.triggered.connect(self.button_1_Event)
			self.popMenu.exec_(self.mapToGlobal(pos))
	def button_1_Event(self):
		pass
	def mousePressEvent(self,event):
		if event.button()==Qt.LeftButton:
			if self.type==1:
				mainwindow=self.parent().parent().parent().parent()
				if mainwindow.dataBoard:
					mainwindow.dataBoard.searchBox.setText(self.name)
class synthetic:
	def __init__(self):
		print('初始化合成表中...')
		self.itemList={}
		self.result={}
		self.initItemList()
		self.resultList=[]
	def run(self,targetName,num=1,price=0):
		self.clear()
		if targetName in self.itemList:
			if self.calculate(self.itemList[targetName]['formula'],num)==-1:
				return self.resultList
			self.resultList.append(DisplayMessage(text='【%s】为【%d】级物品，制造【%d】个需要消耗的材料如下所示：\n'%(targetName,self.itemList[targetName]['level'],num)))
			self.resultList.append(DisplayMessage(text="<p style='color:rgb(150,150,150)'>使用说明：先将所有1级材料集齐，然后一级一级根据下面的显示来制作出更高级的材料,最后拿到所有背包剩余的材料就可以制造出你需要的最终成品了。</p>\n"))
			self.resultList
			index=1
			level=0
			countCost=0.0
			for i in self.result:
				if self.result[i]['number']>0:
					if self.result[i]['level']>level:
						level=self.result[i]['level']
						index=1
						self.resultList.append(DisplayMessage(text="\n<b style='color:#9B30FF;'>%d级</b>材料"%(level)))
					if self.result[i]['level']==1:
						cost=self.itemList[i]['cost']*self.result[i]['number']
						countCost+=cost 
						self.resultList.append(DisplayMessage(1,"<b style='color:#009ACD;'>%d</b>:[<nobr style='color:#53868B;'>%s</nobr>]%d个(<b style='color:#CD6889;'>%d组+%d个</b>) 溢出%d个,<b style='color:#EE9A00;'>价值：%.2f功勋</b>\n"%(index,i,self.result[i]['number'],(self.result[i]['number']*self.itemList[i]['number'])//64,self.result[i]['number']*self.itemList[i]['number']-(self.result[i]['number']*self.itemList[i]['number'])//64*64,self.result[i]['overflow'],cost),i))
					else:
						self.resultList.append(DisplayMessage(1,"<b style='color:#009ACD;'>%d</b>:[<nobr style='color:#53868B;'>%s</nobr>]%d次合成(最终会出现<b style='color:#CD6889;'>%d组+%d</b>个)   溢出%d个\n"%(index,i,self.result[i]['number'],(self.result[i]['number']*self.itemList[i]['number'])//64,self.result[i]['number']*self.itemList[i]['number']-(self.result[i]['number']*self.itemList[i]['number'])//64*64,self.result[i]['overflow']),i))
					index+=1
			self.resultList.append(DisplayMessage(text="[<b style='color:#CD6889;'>最终成本花费</b>：<b>%.2f</b>功勋]"%countCost))
			if price:
				self.resultList.append(DisplayMessage(text="[<b style='color:#CD6889;'>售价为</b><b>%.2f</b>功勋]"%float(price*num)))
				self.resultList.append(DisplayMessage(text="[<b style='color:#CD6889;'>利润为</b><b>%.2f</b>功勋]"%float(price*num-countCost)))
		else:
			self.resultList.append(DisplayMessage(text='此物品不存在于合成表中'))
		return self.resultList
	def calculate(self,formula,count):
		if formula:
			for i in formula:
				needNum=i['number']*count#为了完成此次合成，当前这个物品i['name']的所需数量
				overflowPool=self.result[i['name']]['overflow']
				if overflowPool>=needNum:#判断当前材料的溢出区的存货是否足够使用
					self.result[i['name']]['overflow']-=needNum#如果有存货则优先使用存货,溢出池中的数量对应进行减少
					needNum=0
				else:
					needNum-=overflowPool
					self.result[i['name']]['overflow']=0
				makeNum=needNum//self.itemList[i['name']]['number']
				if makeNum*self.itemList[i['name']]['number']<needNum:
					makeNum+=1
				overflowNum=makeNum*self.itemList[i['name']]['number']-needNum
				self.result[i['name']]['number']+=makeNum
				self.result[i['name']]['overflow']+=overflowNum
				if self.itemList[i['name']]['level']>1:
					self.calculate(self.itemList[i['name']]['formula'],makeNum)
		else:
			self.resultList.append(DisplayMessage(text='1级物品无法合成'))
			return -1
	def clear(self):
		self.resultList=[]
		self.initResult()
	def initResult(self):
		self.result={}
		for i in self.itemList:
			item=self.itemList[i]
			self.result[item['name']]=({'number':0,'overflow':0,'level':item['level'],'cost':item['cost']})
	def initItemList(self):#通过文件读取数据
		self.readDataFile()
	def writeDataFile(self):
		with open(Config.dataFile,'wb') as f:
			line=pickle.dump(self.itemList,f)
	def readDataFile(self):
		with open(Config.dataFile,'rb') as f:
			self.itemList=pickle.load(f)
		self.initResult()