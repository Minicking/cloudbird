from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
class TitleWidget(QWidget):
	def __init__(self,parent=None,size=(300,30)):
		super().__init__()
		self.size=size
		self.parent=parent
		self.stat=False#鼠标状态 False为松开状态 True为按下状态
		self.initUI()
	def initEvent(self,fun_close,fun_min):
		self.button_close.clicked.connect(fun_close)
		self.button_min.clicked.connect(fun_min)
	def initUI(self):
		qss="""
			
			QPushButton{background:transparent;}
			QPushButton:hover{border:0px solid black;background:rgb(170,170,170);}
			TitleWidget{background:rgba(255,255,255,0.2);}
		"""
		#创建控件
		self.button_close=QPushButton()
		self.button_min=QPushButton()

		self.button_min.setIcon(QIcon('Data/img/titleMin.png'))
		self.button_min.setStyleSheet('')
		self.button_min.setIconSize(QSize(self.size[1]-10,self.size[1]-10))
		self.button_min.setContentsMargins(0,0,0,0)
		self.button_min.setToolTip("最小化")

		self.button_close.setIcon(QIcon('Data/img/titleClose.png'))
		self.button_close.setIconSize(QSize(self.size[1]-10,self.size[1]-10))
		self.button_close.setContentsMargins(0,0,0,0)
		self.button_close.setToolTip("关闭")
		#创建布局
		self.layout_main=QHBoxLayout()
		#为控件绑定事件
		
		self.layout_main.setContentsMargins(0, 0, 0, 0)
		self.parent.layoutAddWidget(self.layout_main,QWidget(),size=(self.size[0]-2*self.size[1],self.size[1]))
		self.layout_main.addSpacing(0)
		self.parent.layoutAddWidget(self.layout_main,self.button_min,size=(self.size[1],self.size[1]),alignment=Qt.AlignLeft)
		self.parent.layoutAddWidget(self.layout_main,self.button_close,size=(self.size[1],self.size[1]),alignment=Qt.AlignLeft)
		
		
		self.setLayout(self.layout_main)
		self.setStyleSheet(qss)
		# print('尺寸:',self.size())
	def mousePressEvent(self,event):
		self.stat=True
		QPoint()
		a=self.parent.pos()
		b=event.globalPos()
		self.offset=QPoint(b.x()-a.x(),b.y()-a.y())
		print('按下时鼠标与控件的相对位置:',self.offset)

	def mouseReleaseEvent(self,event):
		self.stat=False
	def mouseMoveEvent(self,event):
		if self.stat:
			curPos=event.globalPos()
			x=curPos.x()-self.offset.x()
			y=curPos.y()-self.offset.y()
			self.parent.move(x,y)
	def paintEvent(self, event):
        # 以下几行代码的功能是避免在多重传值后的功能失效
		opt = QStyleOption()
		opt.initFrom(self)
		p = QPainter(self)
		self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)