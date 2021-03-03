import sys, psutil
# sys.path.append('./')
# sys.path.append('../../')
from PyQt5.QtWidgets import QApplication
from QTBoard.ItemCalBoard import ItemCalBoard
from QTBoard.LoginBoard import LoginBoard
from QTBoard.MainBoard import MainBoard


#进程列表获取
# proc_dict={}
# proc_name=set()
# for proc in psutil.process_iter(attrs=['pid','name']):
# 	proc_dict[proc.info['pid']]=proc.info['name']
# 	proc_name.add(proc.info['name'])
# for i in proc_dict:
# 	print(i,proc_dict[i])
class cbClient:
    def __init__(self):
        self.login = LoginBoard()
        #窗口获取
        # winclass='Qt5QWindowIcon'
        # winname='登录'#'物品合成材料计算(版本:1.0.0)'
        # hwnd=win32gui.FindWindow(winclass,winname)
        # print(hwnd)
        if self.login.success:
            print('进入主界面')
            if self.login.socket:
                print('登录进入')
                self.win = MainBoard(
                    sock=self.login.socket)  #Window(sock=self.login.socket)
            else:
                print('离线进入')
                self.win = MainBoard()  #Window()

        else:
            print('登录失败')
            exit(0)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	print('111')
	x = cbClient()
	print('gogogo')
	sys.exit(app.exec_())
