import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QKeySequence, QPixmap
from PyQt5.QtCore import Qt, QEvent


class FindWdgt(QDialog):
    Internal_Widget_Height = 30
    def __init__(self, List, parent=None):
        super(FindWdgt, self).__init__(parent)
        self.setup_Widgets(List)
        self.setup_SinglConnection()
        self.setup_Layout()
        self.setup_Appearence()
        self.setup_cfg()

    def setup_cfg(self):
        self.installEventFilter(self)
        self.hide()


    def setup_Appearence(self):

        # self.setWindowIcon(QtGui.QIcon(FindIcon_Path))#设置窗口图标
        self.setWindowFlags( Qt.FramelessWindowHint| Qt.Tool) #使用QT.Popup会QLineEdit导致无法输入中文
        self.setStyleSheet('QDialog{background-color: rgb(255,162,108);font-size:40px}')
    def setup_Widgets(self, List):
        self.Find_LineEdit  = QLineEdit(self)
        self.IconLabel      = QLabel(self)
        self.ExitBtn        = QPushButton( "退出", self)
        self.Completer      = QCompleter(List)

        self.ExitBtn.setFixedSize(QtCore.QSize(60, self.Internal_Widget_Height))

        # self.IconLabel.setPixmap(QPixmap(FindPNG_Path))#设置label显示图片

        #设置QLineEdit字体格式
        self.Find_LineEdit.setPlaceholderText("输入搜索内容")
        self.Find_LineEdit.setFixedSize(QtCore.QSize(300, self.Internal_Widget_Height))
        self.Find_LineEdit.setCompleter(self.Completer)
        self.Find_LineEdit.setFont(QtGui.QFont( "微软雅黑" , 13) )

    def setup_Layout(self):
        """
        设置布局
        """
        self.HBoxLayout     = QHBoxLayout(self)

        self.HBoxLayout.addWidget(self.IconLabel)
        self.HBoxLayout.addWidget(self.Find_LineEdit)
        self.HBoxLayout.addWidget(self.ExitBtn)
        self.HBoxLayout.setContentsMargins(7, 7, 7, 7)#...(int left, int top, int right, int bottom)
        self.HBoxLayout.setSpacing(2)

        self.setLayout(self.HBoxLayout)
    def setup_SinglConnection(self):
        """
        信号连接
        """
        self.ExitBtn.clicked.connect(self.close)

    def eventFilter(self, obj, event):
        """
        事件过滤
        """
        if event.type() == QEvent.WindowDeactivate:
            # print("WindowDeactivate")
            self.close()  #点击其他程序窗口，会关闭该对话框
            return True
        else:
            return super(FindWdgt, self).eventFilter(obj, event)

    def Show_Handler(self):
        self.show()
        self.activateWindow()#激活窗口，这样在点击母窗口的时候，eventFilter里会捕获到WindowDeactivate事件，从而关闭搜索窗口
        self.Find_LineEdit.setFocus()
        self.Find_LineEdit.clear()

if __name__ == '__main__':

    app         = QtWidgets.QApplication(sys.argv)
    List        = ['1', '111', '1234', '22', '345', '678']
    widget      = QWidget()
    Find        = FindWdgt(List, widget)
    Btn         = QPushButton("点击弹出", widget)
    Btn.clicked.connect(Find.Show_Handler)
    Btn.resize(QtCore.QSize(100, 50))
    widget.resize(QtCore.QSize(300, 150))
    widget.show()
    sys.exit(app.exec_())
