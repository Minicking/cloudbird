'''
一个基于有道云的翻译类，可以进行文本翻译，可自动识别语言。
'''
import sys
import uuid
import requests
import hashlib
import time,json
from imp import reload

import time
class Translation:
	def __init__(self):
		reload(sys)
		self.YOUDAO_URL = 'https://openapi.youdao.com/api'
		self.APP_KEY = '11bf04851fab41b8'
		self.APP_SECRET = 'brpt4BYgxp2g6N5ehRepGNZfroXMIiiw'


	def encrypt(self,signStr):
	    hash_algorithm = hashlib.sha256()
	    hash_algorithm.update(signStr.encode('utf-8'))
	    return hash_algorithm.hexdigest()


	def truncate(self,q):
	    if q is None:
	        return None
	    size = len(q)
	    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


	def do_request(self,data):
	    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
	    return requests.post(self.YOUDAO_URL, data=data, headers=headers)


	def post(self,text):
		data = {}
		data['from'] = 'auto'
		data['to'] = 'auto'
		data['signType'] = 'v3'
		curtime = str(int(time.time()))
		data['curtime'] = curtime
		salt = str(uuid.uuid1())
		signStr = self.APP_KEY + self.truncate(text) + salt + curtime + self.APP_SECRET
		sign = self.encrypt(signStr)
		data['appKey'] = self.APP_KEY
		data['q'] = text
		data['salt'] = salt
		data['sign'] = sign
		response = self.do_request(data)
		contentType = response.headers['Content-Type']
		# if contentType == "audio/mp3":
		# 	millis = int(round(time.time() * 1000))
		# 	filePath = "合成的音频存储路径" + str(millis) + ".mp3"
		# 	fo = open(filePath, 'wb')
		# 	fo.write(response.content)
		# 	fo.close()
		# else:
		# 	con=response.content
		# 	result=json.loads(response.content)
		# 	return result
		result=json.loads(response.content)
		return result
	def translate(self,text):
		r=self.post(text)
		if r['errorCode']=='0':
			return r['translation'][0]
		return r['errorCode']
if __name__ == '__main__':
	a=Translation()
	x=a.translate("哈哈")
	print(x,type(x))