import sys,os,time,datetime,threading
import subprocess
import win32con
import win32api
import win32clipboard as wincld
import time,random
import winsound

key_map = {
    "0": 49, "1": 50, "2": 51, "3": 52, "4": 53, "5": 54, "6": 55, "7": 56, "8": 57, "9": 58,
    "A": 65, "B": 66, "C": 67, "D": 68, "E": 69, "F": 70, "G": 71, "H": 72, "I": 73, "J": 74,
    "K": 75, "L": 76, "M": 77, "N": 78, "O": 79, "P": 80, "Q": 81, "R": 82, "S": 83, "T": 84,
    "U": 85, "V": 86, "W": 87, "X": 88, "Y": 89, "Z": 90, "ENTER":13, "CTRL":17
}

 
 
def key_down(key):
    """
    函数功能：按下按键
    参    数：key:按键值
    """
    key = key.upper()
    vk_code = key_map[key]
    win32api.keybd_event(vk_code,win32api.MapVirtualKey(vk_code,0),0,0)
 
 
def key_up(key):
    """
    函数功能：抬起按键
    参    数：key:按键值
    """
    key = key.upper()
    vk_code = key_map[key]
    win32api.keybd_event(vk_code, win32api.MapVirtualKey(vk_code, 0), win32con.KEYEVENTF_KEYUP, 0)
 
def key_press(key):
    """
    函数功能：点击按键（按下并抬起）
    参    数：key:按键值
    """
    key_down(key)
    time.sleep(1)
    key_up(key)
def copy2clip(txt):
    cmd='echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)
class message:
	def __init__(self,s):
		self.type=None
		try:
			self.time=datetime.datetime.strptime(s[1:9],'%H:%M:%S')
		except Exception as e:
			self.time=None
		else:
			try:
				a=s.index('[CHAT]')+6
			except Exception as e:
				self.text=None
				self.question=None
			else:
				self.text=s[a:]
				if self.text[:10]==' [!] 最快输入 ':
					try:
						self.question=self.text[10:self.text.index('正确')]
					except Exception as e:
						self.question=self.text[10:self.text.index('的玩家')]
						self.type=1
					else:
						self.type=0
				else:
					self.question=None
	def ans(self):
		if self.question:
			return eval(self.question)
		else:
			return None

class AutoAns:
	def __init__(self,filepath):
		self.filename=filepath
		self.lasttime=datetime.datetime.strptime('00:00:00','%H:%M:%S')
		self.stat=False
		self.Input=False
	def log(self,s):
		print(s)
		nowTime=time.localtime()
		nowTime="[%s-%s-%s %s:%s:%s]"%(nowTime.tm_year,nowTime.tm_mon,nowTime.tm_mday,nowTime.tm_hour,nowTime.tm_min,nowTime.tm_sec)
		with open('auto.txt','a',encoding='utf-8') as f:
			f.write(nowTime+s+'\n')
	def tail(self,file, taillines=500, return_str=True, avg_line_length=None):
	    """avg_line_length:每行字符平均数,
	    return_str:返回类型，默认为字符串，False为列表。
	    offset:每次循环相对文件末尾指针偏移数"""
	    with open(file, errors='ignore',encoding='ansi') as f:
	        if not avg_line_length:
	            f.seek(0, 2)
	            f.seek(f.tell() - 3000)
	            avg_line_length = int(3000 / len(f.readlines())) + 10
	        f.seek(0, 2)
	        end_pointer = f.tell()
	        offset = taillines * avg_line_length
	        if offset > end_pointer:
	            f.seek(0, 0)
	            lines = f.readlines()[-taillines:]
	            return "".join(lines) if return_str else lines
	        offset_init = offset
	        i = 1
	        while len(f.readlines()) < taillines:
	            location = f.tell() - offset
	            f.seek(location)
	            i += 1
	            offset = i * offset_init
	            if f.tell() - offset < 0:
	                f.seek(0, 0)
	                break
	        else:
	            f.seek(end_pointer - offset)
	        lines = f.readlines()
	        if len(lines) >= taillines:
	            lines = lines[-taillines:]

	        return "".join(lines) if return_str else lines
	def autoInput(self,s):
		copy2clip(s)
		key_press('t')
		time.sleep(0.05)
		key_down('ctrl')
		time.sleep(0.05)
		key_down('v')
		time.sleep(0.05)
		key_up('ctrl')
		time.sleep(0.05)
		key_up('v')
		time.sleep(0.05)
		key_press('enter')
		self.log('回答完成')
	def lateAction(self,action,s,late):
		nowtime=time.localtime(time.time()).tm_hour
		winsound.Beep(600,100)
		if nowtime>2 and nowtime<7:
			e=random.randint(3,7)
			self.log('夜间答题额外多等%d秒'%e)
			time.sleep(late+e)
		else:
			self.log('白天答题正常时间')
			time.sleep(late+0.1)
		action(s)
	def loop(self,auto):
		self.log('开启答案获取')
		while self.stat:
			s=self.tail(self.filename,5,False)
			for i in s:
				mes=message(i)
				if mes.time:
					if mes.time>self.lasttime:
						if mes.question:
							self.log("%s"%mes.question)
							if mes.type==0:
								ans=str(int(mes.ans()))
								if self.Input:
									self.lateAction(self.autoInput,ans,1+0.02*len(mes.question))
							elif mes.type==1:
								if self.Input:
									self.lateAction(self.autoInput,mes.question,1+0.1*len(mes.question))
							self.lasttime=mes.time
			time.sleep(0.1)	
		self.log('关闭答案获取')
		self.a=None
	def stop(self):
		self.stat=False
	def run(self):
		self.stat=True
		self.a=threading.Thread(target=self.loop,args=(True,))
		self.a.setDaemon(True)
		self.a.start()

		# self.a.join()
			