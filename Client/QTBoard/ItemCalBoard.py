'''
通过主窗口的功能栏可以打开,用来计算物品合成数据的窗口,可以通过这个窗口打开合成物品配方窗口DataBoard,
还可以打开适用于东方大陆的自动答题功能
'''
import json,sys,time,os,threading
from PyQt5.QtWidgets import *#QListWidgetItem,QListWidget,QComboBox,QFileDialog,QDialogButtonBox,QDialog,QMainWindow,QGridLayout,QTextEdit,QLineEdit,QWidget, QMessageBox, QApplication,QLabel,QPushButton,QHBoxLayout,QVBoxLayout,QMenu,QAction
from PyQt5.QtCore import *# Qt,QTimer,QObject,pyqtSignal,QBasicTimer
from PyQt5.QtGui import *#QPainter, QColor, QFont,QPen,QIntValidator,QDoubleValidator,QPixmap,QIcon
sys.path.append('./')
sys.path.append('../')
from Function import autoAns
from Config import *
from QTBoard.DataBoard import *
from QTBoard.ModifyBoard import *
from QTBoard.BaseBoard import *
class ItemCalBoard(BaseBoard):
	def __init__(self,parent=None,topBoard=None):#sock=None):
		topBoard=self
		super(ItemCalBoard,self).__init__(parent,topBoard)
		print('初始化UI...')
		self.autoAns=autoAns.AutoAns(r'D:\MCLDownload\Game\.minecraft\logs\latest.log')
		self.initUI()
		print('面板绘制完毕')
		try:
			self.Cal=synthetic()
		except Exception as e:
			self.display([DisplayMessage(text="读取物品数据文件错误，请检查数据文件"),DisplayMessage(text=str(e))])
			print('读取错误',e)
		else:
			self.display([DisplayMessage(text="程序初始化完成")])
		
	def display(self,messageList):
		for i in messageList:
			newLabel=i
			listitem=QListWidgetItem()
			if i.type==0:
				listitem.setSizeHint(QSize(Config.WIDTH-50,50))
			self.display_list.addItem(listitem)
			self.display_list.setItemWidget(listitem,newLabel)
	def ToolMenu_AddOption(self,title,option,action):
		newOption=QAction(title,self)
		option.addAction(newOption)
		newOption.triggered.connect(action)
	
	def initUI(self):
		self.dataBoard=None
		#开始初始化UI部分
			#创建UI控件
		print('创建控件')
		self.label_title=QLabel("<p style='color:rgb(0,0,0);font-size:20px;font-weight:800;text-align:center'>物品合成材料计算</p>")
		self.label_input_name=QLabel("需要合成的物品名称")
		self.label_input_num=QLabel("需要合成的物品数量")
		self.label_input_price=QLabel("预计出售的单位价格")
		self.edit_input_name=QLineEdit()
		self.edit_input_num=QLineEdit()
		self.edit_input_price=QLineEdit()
		self.button_mate=QPushButton("材料")
		self.button_cal=QPushButton("计算")
		print('创建布局')
		layout_main=QVBoxLayout()
		layout_top_1=QHBoxLayout()
		layout_top_2=QHBoxLayout()
		layout_top_3=QHBoxLayout()
		layout_bottom=QHBoxLayout()
		self.display_list=QListWidget()
		print('为布局添加控件')
		self.layoutAddWidget(layout_main,self.label_title,size=(Config.WIDTH,50))
		self.layoutAddWidget(layout_top_1,self.label_input_name,size=(150,30))
		self.layoutAddWidget(layout_top_1,self.edit_input_name,size=(Config.WIDTH-150,30))
		self.layoutAddWidget(layout_top_2,self.label_input_num,size=(150,30))
		self.layoutAddWidget(layout_top_2,self.edit_input_num,size=(150,30))
		self.layoutAddWidget(layout_top_2,self.button_mate,size=(Config.WIDTH-300,30))
		self.layoutAddWidget(layout_top_3,self.label_input_price,size=(150,30))
		self.layoutAddWidget(layout_top_3,self.edit_input_price,size=(150,30))
		self.layoutAddWidget(layout_top_3,self.button_cal,size=(Config.WIDTH-300,30))
		self.layoutAddWidget(layout_bottom,self.display_list,size=(Config.WIDTH,Config.HEIGHT-100))
		layout_main.addLayout(layout_top_1)
		layout_main.addLayout(layout_top_2)
		layout_main.addLayout(layout_top_3)
		layout_main.addLayout(layout_bottom)
		print('应用当前窗口布局')
		self.setLayout(layout_main)
		print('应用完毕')
		self.ToolMenu_options_1=self.menuBar().addMenu('选项')
		self.ToolMenu_options_2=self.menuBar().addMenu('功能')
		self.ToolMenu_options_3=self.menuBar().addMenu('其他')
		self.ToolMenu_options_4=self.menuBar().addMenu('用户')
		self.ToolMenu_AddOption('选择数据文件',self.ToolMenu_options_1,self.click_option_openDataFile)
		self.ToolMenu_AddOption('打开答案获取',self.ToolMenu_options_2,self.click_option_autoAns)
		self.ToolMenu_AddOption('打开自动答题',self.ToolMenu_options_2,self.click_option_autoInput)
		self.ToolMenu_AddOption('查看所有物品数据',self.ToolMenu_options_2,self.click_option_itemList)
		self.ToolMenu_AddOption('软件说明',self.ToolMenu_options_3,self.click_option_instruction)
		self.ToolMenu_AddOption('作者相关',self.ToolMenu_options_3,self.click_option_author)
			#设置控件属性
		self.edit_input_num.setValidator(QIntValidator(1,9999))
		self.edit_input_price.setValidator(QDoubleValidator(0,999999999,2))
		self.button_cal.setToolTip("查询此物品合成所需要的所有材料和其他数据。")
		self.button_mate.setToolTip("查询可由此物品合成的所有物品。")
			#给控件绑定事件
		self.button_cal.clicked.connect(self.button_CalEvent)
		self.button_mate.clicked.connect(self.button_MateEvent)
		#UI初始化完成
		icon = QIcon()
		icon.addPixmap(QPixmap("data/img/tt.ico"), QIcon.Normal, QIcon.Off)
		self.setWindowIcon(icon)
		self.setGeometry(0, 0,Config.BOARD[1]+Config.BOARD[3]+Config.WIDTH,Config.BOARD[0]+Config.BOARD[2]+Config.HEIGHT )        
		qr=self.frameGeometry()
		cp=QDesktopWidget().availableGeometry().center()      
		qr.moveCenter(cp)
		self.move(qr.topLeft())
		self.setMinimumSize(380,573)
		self.setMaximumSize(380,573)
		self.setWindowTitle('物品合成材料计算(版本:%s)'%Config.VERSION) 
		self.show()
		print(self.width(),self.height())
	
	def click_option_autoInput(self):
		sender=self.sender()
		self.autoAns.Input=not self.autoAns.Input
		if self.autoAns.Input:
			self.popUpMessage('1、当问题出现时，自动将答案输入到聊天框中进行答题。\n2、在自动答题前会有一个短暂的声音提示，当听到提示时请迅速关闭聊天框，停止所有操作，等待自动答题结束。\n3、生效需先打开答案获取功能\n4、如此功能不生效，请关闭游戏登录器重新启动。\n【建议挂机时使用此功能。】')
			sender.setText('关闭自动答题')
		else:
			sender.setText('打开自动答题')
	def click_option_autoAns(self):
		sender=self.sender()
		if self.autoAns.stat:
			self.autoAns.stop()
			sender.setText('打开答案获取')
		else:
			self.popUpMessage('当问题出现时，自动获取答案，并将答案复制到剪切板上，只需要立即打开聊天框按下ctrl+V即可快速答题。\n【此功能需要打开游戏窗口】')
			self.autoAns.run()
			sender.setText('关闭答案获取')
	def click_option_openDataFile(self):
		fname=QFileDialog.getOpenFileName(self,'选择数据文件',Config.workDir,'Excel files(*.cb)')
		if fname[0]:
			Config.dataFile=fname[0]
			try:
				self.Cal.initItemList()
			except Exception as e:
				self.popUpMessage('选择的文件为不可用数据文件')
			else:
				self.popUpMessage('数据文件更换成功[%s]'%Config.dataFile)
	def click_option_login(self):
		print('登录')
	def click_option_logout(self):
		print('退出登录')
	def click_option_itemList(self):
		if self.dataBoard:
			self.dataBoard.close()
			self.dataBoard=None
		else:
			self.dataBoard=DataBoard(self,self.topBoard)
	
	def click_option_instruction(self):
		self.popUpMessage("此软件是为了在玩我的世界的大型服务器时，方便计算各类物品的制作材料以及材料用途、成本花费、利润之类的数据而开发的。当然实际可以用于更多的地方，只要是包括复杂的物品材料合成的场景下都可适用。默认状态下内置了服务器【东方大陆】内的部分物品数据。可通过自行添加合成表进行数据扩充。",'软件说明')
	def click_option_author(self):
		self.popUpMessage(["<b style='color:rgb(255,100,100)'>作者</b>：%s"%Config.AUTHOR,"<b style='color:rgb(255,100,100)'>QQ</b>:505826682"],'作者相关')
	def button_MateEvent(self):
		self.display_list.clear()
		name=self.edit_input_name.text()
		if name!='':
			l=[DisplayMessage(text='可由[<b style="color:rgb(255,100,100)">%s</b>]作为材料制作的所有物品如下所示：'%name)]
			for i in self.Cal.itemList:
				if self.Cal.itemList[i]['formula']!=None:
					for j in self.Cal.itemList[i]['formula']:
						if j['name']==name:
							l.append(DisplayMessage(1,i,i))
							break
			if len(l)==1:
				l=[DisplayMessage(text='此物品不可合成任何物品，可能是合成表数据不完整或是物品不存在')]
		else:
			l=[DisplayMessage(text='不可查询空数据')]
		self.display(l)
	def button_CalEvent(self):
		self.display_list.clear()
		try:
			name=self.edit_input_name.text()
			num=int(self.edit_input_num.text())
			price=self.edit_input_price.text()
			if price!='':
				price=float(price)
			else:
				price=None
		except Exception as e:
			self.display([DisplayMessage(text="不合法的输入")])
			print(e)
		else:
			# try:
			r=self.Cal.run(name,num,price)
			self.display(r)
			# except Exception as e:
			# 	self.display([DisplayMessage(text='不可进行合成')])
			# 	print('不可合成：',e)

