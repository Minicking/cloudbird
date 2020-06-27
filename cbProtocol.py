
import struct,ctypes,binascii,sys,os,time,pickle
# sys.path.append('../../')
# from myLib.timing import timing
class DataType:
	Int=1
	Str=2
	Float=3
	Bytes=4
	Struct=5
class CommunicationProtocol:
	'''
	通讯协议类规则
	1:一个完整数据包,根据类别包含所有需要的信息,且数据包包含两个部分,一个8字节长度的数据包头和一个任意长度的数据包体
	2:完整的数据包定义规则:
		数据包头:1-4字节:数据包类型(如登录信息 私聊信息 添加好友)
				5-8字节:数据包体的字节数
		数据包体:数据包体由多个不同的数据段组成,其中每个数据段的规则如下:
				1字节:数据段的类型(如整数 字符串 结构体 实数 二进制)
				2-5字节:数据段的实际长度L
				之后L个字节为实际数据内容

	'''
	def __init__(self,type_,data=None):
		'''
			type_:数据包类型:如登录 私聊 添加好友
			data:数据包内的数据,为数据本身
			示例: CommunicationProtocol(PackTypeServer.Login,('tangzifan','123456'))
		'''
		self.type=type_
		self.data=None
		if data:
			if type(data)==tuple:
				self.data=data
			else:
				self.data=(data,)

	@staticmethod
	def showBinary(data):
		return binascii.hexlify(data)
	@staticmethod
	def unpack(data):
		'''
			将数据包体的内容解包
		'''
		r=[]
		maxLength=len(data)
		index=0
		while index<maxLength:
			type_= dataType=struct.unpack('b',data[index:index+1])[0]
			index+=1
			if type_==DataType.Int:
				content=struct.unpack('I',data[index:index+4])[0]
				index+=4
			elif type_==DataType.Float:
				content=struct.unpack('f',data[index:index+4])[0]
				index+=4
			elif type_==DataType.Str:
				length=struct.unpack('I',data[index:index+4])[0]
				index+=4
				content=data[index:index+length].decode('utf-8')
				index+=length
			elif type_==DataType.Bytes:
				length=struct.unpack('I',data[index:index+4])[0]
				index+=4
				content=data[index:index+length]
				index+=length
			elif type_==DataType.Struct:
				length=struct.unpack('I',data[index:index+4])[0]
				index+=4
				content=pickle.loads(data[index:index+length])
				index+=length
			else:
				return False
			r.append(content)
		return r
	def getPack(self):
		r=[]
		packBody=None
		#数据包体的获取
		if self.data:
			for i in self.data:
				dt=type(i)
				if dt==int:
					dataType=struct.pack('b',DataType.Int)
					rule=struct.Struct('I')
					dataContent=ctypes.create_string_buffer(rule.size)
					rule.pack_into(dataContent,0,i)
					dataPack=dataType+dataContent
				elif dt==str:
					dataType=struct.pack('b',DataType.Str)
					dataContent=i.encode("utf-8")
					dataLength=struct.pack('I',len(dataContent))
					dataPack=dataType+dataLength+dataContent

				elif dt==float:
					dataType=struct.pack('b',DataType.Float)
					rule=struct.Struct('f')
					dataContent=ctypes.create_string_buffer(rule.size)
					rule.pack_into(dataContent,0,i)
					dataPack=dataType+dataContent
				elif dt==bytes:
					dataType=struct.pack('b',DataType.Bytes)
					dataContent=i
					dataLength=struct.pack('I',len(dataContent))
					dataPack=dataType+dataLength+dataContent
				else:
					dataType=struct.pack('b',DataType.Struct)
					dataContent=pickle.dumps(i)
					dataLength=struct.pack('I',len(dataContent))
					dataPack=dataType+dataLength+dataContent
				r.append(dataPack)
			
			for i in r:
				if packBody:
					packBody+=i
				else:
					packBody=i
		
		#数据包头的获取
		headType=struct.pack('I',self.type)
		packLength=struct.pack('I',len(packBody)) if packBody else struct.pack('I',0)
		packHead=headType+packLength
		return (packHead,packBody)
	@staticmethod
	def recv(sock):
		try:
			head=sock.recv(8)
			packType=struct.unpack('I',head[:4])[0]
			packLength=struct.unpack('I',head[4:])[0]
			if packLength>0:
				body=sock.recv(packLength)
				datalist=CommunicationProtocol.unpack(body)
			else:
				datalist=None
		except Exception as e:
			print('recv错误:',e)
			return False
		else:
			return (packType,datalist,8+packLength)
	def send(self,sock):
		L=self.getPack()
		length=len(L[0])+(len(L[1]) if L[1] else 0)
		try:
			sock.send(L[0])
			if L[1]:
				sock.send(L[1])
		except Exception as e:
			return False
		else:
			return length
if __name__ == '__main__':
	t=CommunicationProtocol(1,(223,5.56,b'\x02\x12\x35','tangzdsfaifanfsdfsdafsdwofuckyou',{'fuck':'me','end':123}))
	L=t.getPack()
	print('数据包头:',L[0])
	print('数据包体:',L[1])
	print(t.unpack(L[1]))

