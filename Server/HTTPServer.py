import socket,random,threading,hashlib,time,sys,os
sys.path.append('../../')
sys.path.append('../')
from multiprocessing import Process
from cbEmail import Email
from Config import Config
from myLib.mydb import mysqldb as mydb
class log:
    def __init__(self):
        self.data=''
    def out(self,text,filename):
        nowTime=time.localtime()
        nowTime="[%s-%s-%s %s:%s:%s]"%(nowTime.tm_year,nowTime.tm_mon,nowTime.tm_mday,nowTime.tm_hour,nowTime.tm_min,nowTime.tm_sec)
        self.data+=''+nowTime+text
        if len(self.data.encode('utf-8'))>0:
            # print('日志缓存已满,写入到文件中')
            print(self.data)
            with open('log/%s.txt'%filename,'a',encoding='utf-8') as f:
                f.write(self.data)
                self.data=''
class HTTPStatus:
    def __init__(self,_type,content=None):
        self.response_headers = "Server: CB HTTP Server\r\n"
        if _type=='成功':#成功
            self.response_start_line = "HTTP/1.1 200 成功\r\n"
            self.response_body = '成功'

        elif _type=='拒绝':#拒绝请求(被服务器禁止,如IP被封锁)
            self.response_start_line = "HTTP/1.1 403 请求被拒绝\r\n"
            self.response_body = '被服务器拒绝访问'

        elif _type=='未授权':#拒绝请求(被服务器禁止,如IP被封锁)
            self.response_start_line = "HTTP/1.1 401 权限不足\r\n"
            self.response_body = '权限不足'

        elif _type=='失败':#拒绝请求(被服务器禁止,如IP被封锁)
            self.response_start_line = "HTTP/1.1 202 请求失败\r\n"
            self.response_body = content

        elif _type=='参数错误':#错误访问(有对应请求头,但参数不合法)
            self.response_start_line = "HTTP/1.1 405 参数错误\r\n"
            self.response_body = '参数错误'

        elif _type=='请求头错误':#错误访问(无请求头)
            self.response_start_line = "HTTP/1.1 417 错误的请求\r\n"
            self.response_body = '非法请求'

        elif _type=='服务器错误':#服务器错误(当服务器处理出现错误)
            self.response_start_line = "HTTP/1.1 500 服务器出现错误\r\n"
            self.response_body = '服务器发生错误'

        elif _type=='请求不存在':#不存在的请求(服务器不存在的请求类型)
            self.response_start_line = "HTTP/1.1 400 不存在的请求类型\r\n"
            self.response_body = '不支持的请求类型'

        self.response = self.response_start_line + self.response_headers + "\r\n" + self.response_body
class HTTPProcess:
    def __init__(self,data,db):
        self.db=db
        data=data.replace('\r','')
        data=data.split('\n')
        a1=data[0].index(' ')+1
        a2=data[0].index(' ',a1+1)
        self.method=data[0][:a1-1]
        self.protocol=data[0][a2+1:]
        self.url=data[0][a1:a2]
        a1=self.url.index('?')
        self.interface=self.url[1:a1]
        parameterStr=self.url[a1+1:]
        self.parameter={}
        i=0
        while i<len(parameterStr):
            a1=parameterStr.index('=',i)
            key=parameterStr[i:a1]
            i=a1+1
            try:
                a2=parameterStr.index('&',i)
            except Exception as e:
                value=parameterStr[i:]
                a2=9999999
            else:
                value=parameterStr[i:a2]
            i=a2+1
            self.parameter[key]=value
        self.header={}
        data.remove(data[0])
        for i in data:
            i=i.replace(' ','')
            if i!='':
                index=i.index(':')
                key=i[:index]
                value=i[index+1:]
                self.header[key]=value
    def sendConfirmCodeEmail(self,email,confirmcode):
        e=Email(Config)
        print('Emai组件数据:')
        print(str(e))
        print(email,confirmcode)
        e.send({'target':email,'confirm':confirmcode},0)
    def createConfirmCode(self):
        return "".join(random.sample('zyxwvutsrqponmlkjihgfedcba1234567890',5))
    def getRightConfirm(self,email):
        return hashlib.md5(email.encode('utf-8')).hexdigest()[::3]
    def checkRequestCondition(self,type_):
        if type_=='getconfirmcode':
            return self.method=='GET' and 'confirm' in self.header and 'email' in self.parameter
        if type_=='register':
            return self.method=='GET' and 'confirm' in self.header and 'account' in self.parameter and 'password' in self.parameter and 'email' in self.parameter and 'confirmcode' in self.parameter
    def process(self):
        print('请求的基础数据:')
        print(str(self))
        print('[1]进入处理请求流程:')
        if self.interface == 'getconfirmcode':
            print('[2]此请求为获取验证码')
            if self.checkRequestCondition('getconfirmcode'):
                print('[3]数据合理性检查通过')
                if self.header['confirm']==self.getRightConfirm(self.parameter['email']):
                    print('[4]身份码合法,开始进行验证码入库操作')
                    confirmcode=self.createConfirmCode()
                    existID=self.db.exist('confirmcode',{'email':self.parameter['email']})
                    index=-1
                    if existID==False:
                        print('[5]此邮箱对应的验证码不在数据库内,进行创建操作')
                        if self.db.insertTo('confirmcode',{'email':self.parameter['email'],'code':confirmcode,'regDate':self.db.getNowTime()}):
                            print('[6]验证码数据创建成功')
                            index=7
                        else:
                            self.result=HTTPStatus('服务器错误')
                            print('[6]验证码数据创建失败')
                    else:
                        print('[5]此邮箱对应的验证码已在数据库内,进行更新操作')
                        if self.db.update('confirmcode',{'id':existID,'code':confirmcode,'regDate':self.db.getNowTime()}):
                            print('[6]更新成功')
                            index=7
                        else:
                            print('[6]更新失败')
                            self.result=HTTPStatus('服务器错误')
                    if index>0:
                        self.result=HTTPStatus('成功')
                        print('[%d]发送验证码邮件:'%index,self.parameter['email'],confirmcode)
                        self.sendConfirmCodeEmail(self.parameter['email'],confirmcode)
                else:
                    print('[4]身份码不合法,此请求权限不够,返回NoPermissions')
                    self.result=HTTPStatus('未授权')
                return
            else:
                print('[3]数据合理性检查不通过')
                self.result=HTTPStatus('参数错误')
        if self.interface == 'register':
            print('[2]此请求为用户注册')
            if self.checkRequestCondition('register'):
                print('[3]数据合理性检查通过')
                if self.db.exist('user',{'account':self.parameter['account']}):
                    print('[4]账号已被使用,注册失败')
                    self.result=HTTPStatus('失败','账号已被使用')
                else:
                    if self.db.exist('user',{'email':self.parameter['email']}):
                        print('[4]邮箱已被使用,注册失败')
                        self.result=HTTPStatus('失败','邮箱已被使用')
                    else:
                        print('[4]账号或邮箱可被使用')
                        if self.db.exist('confirmcode',{'email':self.parameter['email']}):
                            print('[5]邮箱验证码已在数据库内')
                            count,r=self.db.selectFromWhere('confirmcode','email=\'%s\''%(self.parameter['email']))
                            code=r[0][2]
                            if code==self.parameter['confirmcode']:
                                print('[6]验证码匹配成功')
                                if self.db.insertTo('user',{'name':'新用户','account':self.parameter['account'],'password':self.parameter['password'],'email':self.parameter['email'],'regDate':self.db.getNowTime(),'lastDate':self.db.getNowTime(),'lastIP':self.header['Host'][:self.header['Host'].index(':')]}):
                                    print('[7]新的用户数据插入成功')
                                    self.result=HTTPStatus('成功')
                                else:
                                    print('[7]新的用户数据插入失败')
                                    self.result=HTTPStatus('服务器错误')
                            else:
                                print('[6]验证码匹配失败')
                                self.result=HTTPStatus('失败','验证码错误')
                        else:
                            print('[5]邮箱验证码未数据库内,失败')
                            self.result=HTTPStatus('失败','邮箱未进行验证或已过期')
            else:
                print('[3]数据合理性检查不通过,返回参数错误')
                self.result=HTTPStatus('参数错误')
            return
    def __str__(self):
        s='请求方法:'+self.method+'\n'
        s+='请求URL:'+self.url+'\n'
        s+='请求接口'+self.interface+'\n'
        s+='请求参数'+str(self.parameter)+'\n'
        s+='请求协议版本:'+self.protocol+'\n'
        s+='请求头:\n'
        for i in self.header:
            s+='%s:%s\n'%(i,self.header[i])
        return s
class HTTPServer:
    def __init__(self):
        self.log=log()

        self.server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('',20203))
        self.process=Process(target=self.start,args=())
        self.process.start()
    def start(self):
        self.db=mydb('127.0.0.1','root','123456','cb')
        self.server_socket.listen()
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.log.out("[%s, %s]用户连接上了" % client_address,'httplog')
            clientProcess = threading.Thread(target=self.clientProcess, args=(client_socket,))
            clientProcess.start()
    
    def clientProcess(self,client_sock):
        request_data = client_sock.recv(1024).decode('utf-8')
        print('数据接受完成,开始处理数据')
        process=HTTPProcess(request_data,self.db)
        process.process()
        self.log.out('请求响应:%s'%process.result.response_start_line,'httplog')
        client_sock.send(bytes(process.result.response, "utf-8"))
        client_sock.close()

if __name__ == "__main__":
    server=HTTPServer()
    server.start()