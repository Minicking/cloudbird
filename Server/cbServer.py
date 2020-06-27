import os, sys, time, socket, threading, struct, pickle
from cbEmail import Email
sys.path.append('../../')
sys.path.append('../')
from cbProtocol import CommunicationProtocol
from myLib.mydb import mysqldb as mydb
from Config import Config, PackTypeClient, PackTypeServer, messageManageType, StimulusType
from HTTPServer import HTTPServer
from Operation import operation
from ClientOperation import ClientOperation
class Server:
    def __init__(self):
        print("初始化:初始化服务器....")
        print("初始化:服务器端口设定...")
        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Socket.bind(("0.0.0.0", Config.PORT))
        print("初始化:初始化监听线程...")
        self.Listener = threading.Thread(target=self.Listener, args=())
        print("初始化:数据库开启...")
        self.db = mydb('127.0.0.1', 'root', '123456', 'cb')  # pymysql.connect("localhost","root","123456","tTalk")
        print("初始化:初始化客户端池...")
        self.clientList = []
        print('初始化心跳线程...')
        self.heartThread = threading.Thread(target=self.heartThread_run, args=())
        print('初始化Http服务器')
        self.HTTPServer = HTTPServer()
        print("初始化:邮件处理系统...")
        self.email = Email(Config)
        print("初始化:重置登录状态")
        self.resetLoginStat()
        print('初始化完成,服务器运行中---------------------------------------------------------')
    def resetLoginStat(self):
        self.db.executeSQL(["update user set login=0"])
    def heartThread_run(self):
        while True:
            faillist = []
            for i in self.clientList:
                if not i.stat or not CommunicationProtocol(PackTypeClient.Heart, (b'\x01',)).send(i.sock):
                    faillist.append(i)
                    print('%s出现问题,断开连接并移除客户端池' % i.data['name'])
            for i in faillist:
                i.close()
                self.clientList.remove(i)
            time.sleep(10)

    def Listener(self):
        while True:
            try:
                sock, addr = self.Socket.accept()
            except Exception as e:
                print('接收客户端连接时出现错误:', e)
            else:
                print("来自%s的用户与服务器进行了连接！" % (str(addr)))
                client_thread = threading.Thread(target=self.clientListener, args=(sock, addr))  # 把sock 加入线程内
                client_thread.start()  # 启动线程

    def clientListener(self, sock, addr):
        print('监听来自', addr, '的用户')
        client = ClientOperation(self, sock, addr, self.db, self.email)
        succssTag = False
        if client.waitLogin():
            print('登录成功,发送确认验证信息给客户端')
            self.clientList.append(client)
            if operation.SendConfirmResult(client,True):
                succssTag = True
                client.getFriendListDate()
                if not operation.PushUserInfo(client):
                    succssTag = False
            else:
                client.close()
                print('登录验证信息发送失败,断开连接')
        else:
            print('登录失败,发送拒绝验证信息给客户端')
            operation.SendConfirmResult(client, False)
            client.close()
        while succssTag:
            Data = CommunicationProtocol.recv(sock)
            print('接收到来自客户端的请求:', Data)
            if Data:
                client.uploadCount += Data[2]
                client.processPack(Data)
            else:
                print('接收到错误数据包，结束')
                client.close()
                return

    def run(self):
        self.Socket.listen()
        self.Listener.start()
        self.heartThread.start()


if __name__ == '__main__':
    s = Server()
    s.run()
