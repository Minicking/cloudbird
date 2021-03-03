'''
所有有关于客户端以及用户的操作
'''
from base.cbProtocol import CommunicationProtocol
from Config import Config, PackTypeClient, PackTypeServer, messageManageType, StimulusType
from Operation import operation


class ClientOperation:
    def __init__(self, server, sock, addr, db, email):
        self.server = server
        self.sock = sock
        self.addr = addr
        self.db = db
        self.data = None
        self.email = email
        self.uploadCount = 0  # 用户上传的数据量
        self.downloadCount = 0  # 用户下载的数据量
        self.stat = True  # 客户端状态 True为正常,False为已断开
    def getUserPhoto(self, id_):
        try:
            with open(r'resource\photo\%d.jpg' % id_, 'rb') as f:
                data = f.read()
        except Exception as e:
            print('头像文件读取失败，返回默认头像数据')
            with open(r'resource\photo\default.jpg', 'rb') as ff:
                data = ff.read()
        return data

    def getUserInfo(self, id_):
        try:
            count, r = self.db.selectFromWhere('user', 'id=%d' % id_)
            if count > 0:
                l = dict(zip(
                    ['id', 'name', 'account', 'password', 'email', 'regDate', 'lastDate', 'lastIP', 'certification'],
                    r[0]))
                return l
            else:
                return None
        except Exception as e:
            print('获取用户信息时出现错误')
            return None

    def getFriendListDate(self):  # 获取用户自身基本信息与好友基本信息列表,用以发送给客户端进行主界面显示
        friendlist = self.db.selectFromWhere('friend', 'owner=%d' % self.data['id'])
        print('得到的好友列表:', friendlist)
        self.data['photo'] = self.getUserPhoto(self.data['id'])
        self.data['friendlist'] = []
        for i in friendlist[1]:
            info = self.db.selectFromWhere('user', 'id=%d' % i[2])
            info = {'id': info[1][0][0], 'name': info[1][0][1], 'certification': info[1][0][8],
                    'photo': self.getUserPhoto(info[1][0][0])}
            self.data['friendlist'].append(info)

    def waitLogin(self):
        loginData = CommunicationProtocol.recv(self.sock)
        if loginData and loginData[0] == PackTypeServer.Login:
            print('登录数据获取成功')
            account = loginData[1][0]
            password = loginData[1][1]
            print('开始进行用户数据验证')
            count, r = self.db.selectFromWhere('user', 'account=\'%s\' and password=\'%s\'' % (account, password))
            print('用户个人信息:', r)
            if count <= 0:
                return False
            else:
                self.data = dict(zip(
                    ['id', 'name', 'account', 'password', 'email', 'regDate', 'lastDate', 'lastIP', 'certification',
                     'referrer', 'login'],
                    r[0]))
                return self.login()
        else:
            print(loginData)
            print('获取到了错误的登录信息')
            return False

    def login(self):
        count, r = self.db.selectColumnFromWhere('user', 'login', 'id=%d' % self.data['id'])
        if count > 0:
            loginstat = r[0]
            if loginstat == False:
                print('未登录状态,修改为登录状态')
                if self.db.update('user', {'id': self.data['id'], 'login': True}):
                    print('修改成功,登录完成')
                    return True
                else:
                    print('修改失败,登录失败')
                    return False
            else:
                print('已登录状态,登录失败')
                return False

    def logout(self):
        if self.stat:
            if self.db.update('user', {'id': self.data['id'], 'login': False}):
                self.stat=False
                print('登出成功')
            else:
                print('登出失败')
        else:
            print('已登出,不做重复数据修改')
    def processPack(self, data):
        print('开始处理数据:', data)
        dataType = data[0]
        data = data[1]
        if dataType == PackTypeServer.SearchUser:
            print('接收到的包为请求搜索用户数据')
            tag = data[0]
            if operation.PushFriendSearchResult(self, tag):
                print('响应完成')
        if dataType == PackTypeServer.AddFriend:
            print('接收到的包为添加好友请求')
            print('检查是否符合添加要求')
            if self.data['id'] == data[0]:
                print('发起人和目标者为同一人,不可进行好友申请')
                return
            count, r = self.db.selectFromWhere('friendrequest',
                                               "requester=%d and target=%d" % (self.data['id'], data[0]))
            if count > 0:
                print('此请求已存在')
                return
            count, r = self.db.selectFromWhere('friend', "owner=%d and target=%d" % (self.data['id'], data[0]))
            if count > 0:
                print('已经是好友,不可重复申请')
                return
            print('检查通过,存入好友请求数据到数据库')
            if self.db.insertTo('friendrequest',
                                {'requester': self.data['id'], 'target': data[0], 'requestDate': self.db.getNowTime()}):
                print('存入成功')
            else:
                print('存入失败')
        if dataType == PackTypeServer.GetMesOfFriendRequest:
            print('接收到的包为获取好友请求的消息')
            if operation.PushFriendRequestList(self):
                print('响应成功')
        if dataType == PackTypeServer.FriendRequestResponse:
            print('接收到的包为回应好友请求')
            count, r = self.db.selectFromWhere('friendrequest', "id=%d" % data[0])
            if count > 0:
                print('回应内容:', data)
                if r[0][2] == self.data['id']:
                    print('没毛病,做出回应')
                    if data[1] == 1:
                        print('接受好友请求')
                        self.db.insertTo('friend',
                                         {'owner': r[0][1], 'target': r[0][2], 'addDate': self.db.getNowTime()})
                        self.db.insertTo('friend',
                                         {'owner': r[0][2], 'target': r[0][1], 'addDate': self.db.getNowTime()})
                        self.getFriendListDate()
                        operation.PushUserInfo(self)
                        for i in self.server.clientList:
                            print(i.data['id'], r[0][1])
                            if i.data['id'] == r[0][1]:
                                print('告诉请求者请求对方接受了好友请求,刷新他的面板')
                                i.getFriendListDate()
                                operation.PushUserInfo(i)

                                break
                    else:
                        print('拒绝好友请求')
                    self.db.deleteFromWhere('friendrequest', "id=%d" % data[0])
                    print('删除请求数据成功')
                    if operation.PushFriendRequestList(self):
                        print('响应成功')

                else:
                    print('不可对不是自己的好友请求做出回应')

    def close(self):
        self.logout()
        print('关闭', self.sock, '的连接,在此期间的收发数据:\n上传至服务器:%fmb\n从服务器下载:%fmb' % (
            self.uploadCount / 1024 / 1024, self.downloadCount / 1024 / 1024))
        self.sock.close()
