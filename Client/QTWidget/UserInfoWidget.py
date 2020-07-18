from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from myLib.ImageProcess import ImageProcess
class UserInfoWidget(QWidget):
	def __init__(self,parent=None,data=None):
		super().__init__()
		self.data=data
		self.parent=parent
		self.initUI()
	def initUI(self):
		#创建控件
		self.label_photo=QLabel()
		self.label_name=QLabel()
		self.label_certicication=QLabel()#官方认证标识
		#创建布局
		layout_main=QHBoxLayout()
		#为控件设置属性
		# self.label_photo.setStyleSheet('border:1px solid red')
		self.label_name.setStyleSheet('font-size:15px;font-weight:800')
		# self.label_certicication.setStyleSheet('border:1px solid red')

		self.label_photo.setScaledContents(True)
		self.label_certicication.setScaledContents(True)
		self.parent.layoutAddWidget(layout_main,self.label_photo,size=(50,50))
		self.parent.layoutAddWidget(layout_main,self.label_name,size=(100,50))
		self.parent.layoutAddWidget(layout_main,self.label_certicication,size=(50,20))
		self.setLayout(layout_main)

	def update(self):
		# self.label_photo.setPixmap(QPixmap.fromImage(QImage.fromData(self.data['photo'])))
		Image=ImageProcess()
		Image.readBytes(self.data['photo'])
		Image.toCicle()
		self.label_photo.setPixmap(QPixmap.fromImage(Image.toQImage()))
		self.label_name.setText(self.data['name'])
		if self.data['certification']==1:
			self.label_certicication.setText('已认证')
			self.label_certicication.setStyleSheet('color:green;font-size:12px;font-weight:800')
		else:
			self.label_certicication.setText('未认证')
			self.label_certicication.setStyleSheet('color:red;font-size:12px;font-weight:800')
