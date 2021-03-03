class Config:
    # # PORT=8888
    # PORT = 20202
    # email_host = 'smtp.qq.com'
    # email_sender = '505826682@qq.com'
    # email_password = 'fapgpyuhuagcbjbh'
    # log_path = 'log/debug'

    def __init__(self, env = 'dev'):
        self.Port = 20202
        self.email_host = 'smtp.qq.com'
        self.email_sender = '505826682@qq.com'
        self.email_password = 'fapgpyuhuagcbjbh'
        self.log_path = 'log/debug'
        self.mysql_host = 'www.minicking.com'
        self.mysql_account = 'root'
        self.mysql_password = 'tzfminicking1997'
        if env == 'online':
            pass


class StimulusType:
    GetUserInfo = 1  #刺激客户端发起获取用户基本信息请求


class messageManageType:  #消息管理面板中消息的类型
    SysMes = 1  #系统消息
    FriendRequestMes = 2  #好友请求消息


class PackTypeClient:  #客户端接收的包 服务器发送的包
    Heart = 1
    LoginConfirm = 2
    UserInfo = 3
    FriendList = 4
    SearchUserData = 5
    PutMesOfFriendRequest = 6


class PackTypeServer:  #服务器接收的包 客户端发送的包
    Login = 1
    SearchUser = 2
    AddFriend = 3
    GetMesOfFriendRequest = 4
    FriendRequestResponse = 5
