import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QSystemTrayIcon
from PyQt5.QtGui import QIcon
class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()
    
    def initUi(self):
        self.resize(400, 300)
        self.setWindowTitle("微信公众号：学点编程吧；www.xdbcb8.com；最小化到右下脚")
        pb_min = QPushButton("最小化到右下脚", self)
        pb_min.move(200, 150)
        pb_min.clicked.connect(self.pbMin)
        
    def pbMin(self):
        self.hide()
        self.mSysTrayIcon = QSystemTrayIcon(self)
        icon = QIcon("zan.png")
        self.mSysTrayIcon.setIcon(icon)
        self.mSysTrayIcon.setToolTip("我在这里哦！")
        self.mSysTrayIcon.activated.connect(self.onActivated)
        self.mSysTrayIcon.show()
    def onActivated(self, reason):
        if reason == self.mSysTrayIcon.Trigger:
            self.show()
            self.mSysTrayIcon.hide()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())