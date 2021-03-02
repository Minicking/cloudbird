'''
服务器的所有数据发送都从这里进行调用
'''
import os, sys, time, socket, threading, struct, pickle
# sys.path.append('../../')
# sys.path.append('../')
from Config import Config, PackTypeClient, PackTypeServer, messageManageType
from cbProtocol import CommunicationProtocol

class operation:
    @staticmethod
    def PushFriendSearchResult(client, tag):
        print('开始搜索关于[%s]的用户数据' % tag)
        if tag[0] == '#':
            print('进行ID搜索')
            tag = tag[1:]
            count, r = client.db.selectFromWhere('user', "id=%s" % tag)
        else:
            count, r = client.db.selectFromWhere('user', "name like '%%%s%%'" % tag)
        print('得到%d条搜索结果' % count)
        if count > 0:
            l = []
            for i in r:
                l.append((i[0], i[1], i[8]))
            l = tuple(l)
        else:
            l = None
        s = CommunicationProtocol(PackTypeClient.SearchUserData, l).send(client.sock)
        client.downloadCount += s
        if s:
            print('推送搜索用户结果成功')
            return True
        else:
            print('推送搜索用户结果失败')
            return False

    @staticmethod
    def PushFriendRequestList(client):
        count, r = client.db.selectFromWhere('friendrequest', "target=%d" % (client.data['id']))
        l = [messageManageType.FriendRequestMes]
        if count > 0:
            for i in r:
                userinfo = client.getUserInfo(i[1])
                l.append((i[0], (userinfo['id'], userinfo['name'], userinfo['certification']), i[3]))
        s = CommunicationProtocol(PackTypeClient.PutMesOfFriendRequest, tuple(l)).send(client.sock)
        client.downloadCount += s
        if s:
            print('推送好友请求消息成功')
            return True
        else:
            print('推送好友请求消息失败')
            return False

    @staticmethod
    def PushUserInfo(client):
        s = CommunicationProtocol(PackTypeClient.UserInfo, client.data).send(client.sock)
        client.downloadCount += s
        if s:
            print('推送用户基本信息成功')
            return True
        else:
            print('推送用户基本信息失败')
            return False

    @staticmethod
    def SendConfirmResult(client, result):
        '''
        参数说明:client:连接进来的客户端对象(CLientOperation)
                result:验证结果,True或者False
        '''
        s = CommunicationProtocol(PackTypeClient.LoginConfirm, (b'\x01' if result else b'\x00',)).send(client.sock)
        client.downloadCount += s
        if s:
            print('验证信息%s发送成功' % str(result))
            return True
        else:
            print('验证信息%s发送失败' % str(result))
            return False
