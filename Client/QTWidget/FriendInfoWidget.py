from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
class FriendInfoWidget(QWidget):
	def __init__(self,parent=None,data=None):
		super().__init__()
		self.data=data
		self.parent=parent
		self.initUI()
		self.update()
	def initUI(self):
		#创建控件
		self.label_photo=QLabel()
		self.label_name=QLabel()
		self.label_certicication=QLabel()#官方认证标识
		#创建布局
		layout_main=QHBoxLayout()
		#为控件设置属性
		# self.label_photo.setStyleSheet('border:1px solid red')
		self.label_name.setStyleSheet('font-size:12px;')
		# self.label_certicication.setStyleSheet('border:1px solid red')

		self.label_photo.setScaledContents(True)
		self.label_certicication.setScaledContents(True)
		self.parent.layoutAddWidget(layout_main,self.label_photo,size=(40,40),alignment=Qt.AlignCenter- Qt.AlignVCenter|Qt.AlignHCenter)
		self.parent.layoutAddWidget(layout_main,self.label_name,size=(85,20),alignment=Qt.AlignHCenter)
		self.parent.layoutAddWidget(layout_main,self.label_certicication,size=(35,15),alignment=Qt.AlignHCenter)
		self.setLayout(layout_main)
	def update(self):
		self.label_photo.setPixmap(QPixmap.fromImage(QImage.fromData(self.data['photo'])))
		self.label_name.setText(self.data['name'])
		if self.data['certification']==1:
			self.label_certicication.setText('已认证')
			self.label_certicication.setStyleSheet('color:green;font-size:10px;font-weight:800')
		else:
			self.label_certicication.setText('未认证')
			self.label_certicication.setStyleSheet('color:red;font-size:10px;font-weight:800')
