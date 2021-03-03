'''
    图片处理库
    1、toCicle方法:将任意图片转为带透明通道的圆形图片,如果长宽不一致则会以短边为基准切割,可以将二进制图片数据直接转化或者将文件形式的图片进行转化
    2、重载的+运算符:将两张图片合成为一张,要求两张图片必须大小一致且通道数一致
    3、setScale方法(width,height)：将图片的大小修改为宽width,长height
    说明：可以通过toQImage直接将img转为PyQt5支持的QImage对象
'''
import numpy as np
import cv2,sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PIL import Image
# import timing
# 图像处理，获取图片最大内接圆，其他区域置为透明
class ImageProcess:
    def __init__(self):

        self.path=None
        self.img=None#numpy格式的array数据
        self.stat={}
    def getStat(self):
        rows, cols, channel = self.img.shape
        self.stat={'rows':rows,'cols':cols,'channel':channel}
    def save(self,name):
        if self.img.all()!=None:
            if self.stat['channel']==3:
                end='jpg'
            else:
                end='png'
            print('haha:',cv2.COLOR_BGRA2RGBA,cv2.COLOR_RGB2BGR,cv2.COLOR_BGR2RGB)
            print(self.img.shape)
            self.img=cv2.cvtColor(self.img,cv2.COLOR_BGRA2RGBA)
            print(self.img.shape)
            # channels="RGBA"
            # img = Image.fromarray(self.img,channels[:self.stat['channel']])
            print('储存:','%s.%s'%(name,end))
            cv2.imwrite('%s.%s'%(name,end),self.img)
        return True
    def show(self):
        channels="RGBA"
        img = Image.fromarray(self.img,channels[:self.stat['channel']])
        img.show()
    def setScale(self,width,height):
        self.img=cv2.resize(self.img,(height,width),interpolation=cv2.INTER_CUBIC)
        self.getStat()
    def cv_imread(self):
        # cv_img=cv2.imdecode(np.fromfile(self.path,dtype=np.uint8),-1)
        cv_img=cv2.imread(self.path,cv2.IMREAD_UNCHANGED)
        print('读取:',cv_img.shape)
        # imdecode读取的是rgb，如果后续需要opencv处理的话，需要转换成bgr，转换后图片颜色会变化
        if cv_img.shape[2]==4:
            cv_img=cv2.cvtColor(cv_img,cv2.COLOR_RGBA2BGRA)
        else:
            cv_img=cv2.cvtColor(cv_img,cv2.COLOR_RGB2BGR)
        return cv_img
    def openImg(self,path):
        self.path=path
        self.img=self.cv_imread()
        print('fuck',self.img.shape)
        rows, cols, channel = self.img.shape
        self.stat={'rows':rows,'cols':cols,'channel':channel}
        return self
    def readBytes(self,data):
        self.img=cv2.imdecode(np.fromstring(data, np.uint8),cv2.IMREAD_COLOR)
        rows, cols, channel = self.img.shape
        rows, cols, channel = self.img.shape
        self.stat={'rows':rows,'cols':cols,'channel':channel}
        return self
    def toCicle(self):
        # cv2.IMREAD_COLOR，读取BGR通道数值，即彩色通道，该参数为函数默认值
        # cv2.IMREAD_UNCHANGED，读取透明（alpha）通道数值
        # cv2.IMREAD_ANYDEPTH，读取灰色图，返回矩阵是两维的
        # img = cv2.imread(input_img, cv2.IMREAD_UNCHANGED)
        
        if self.stat['rows']>self.stat['cols']:
            rows_a=(self.stat['rows']-self.stat['cols'])//2
            rows_b=rows_a+self.stat['cols']
            cols_a=0
            cols_b=self.stat['cols']
            bc=self.stat['cols']
        else:
            rows_a=0
            rows_b=self.stat['rows']
            cols_a=(self.stat['cols']-self.stat['rows'])//2
            cols_b=cols_a+self.stat['rows']
            bc=self.stat['rows']
        # 创建一张4通道的新图片，包含透明通道，初始化是透明的
        img_new = np.zeros((bc,bc,4),np.uint8)
        print("%d-%d"%(rows_a,rows_b))
        print("%d-%d"%(cols_a,cols_b))
        img_new[:,:,0:3] = self.img[rows_a:rows_b,cols_a:cols_b,0:3]

        # 创建一张单通道的图片，设置最大内接圆为不透明，注意圆心的坐标设置，cols是x坐标，rows是y坐标
        img_circle = np.zeros((bc,bc,1),np.uint8)
        img_circle[:,:,:] = 0  # 设置为全透明
        img_circle = cv2.circle(img_circle,(bc//2,bc//2),int(bc//2),(255),-1) # 设置最大内接圆为不透明

        # 图片融合
        img_new[:,:,3] = img_circle[:,:,0]
        self.img=img_new
        self.getStat()
        return img_new
    def __add__(self,t):
        print(self.stat)
        print(t.stat)
        if self.stat==t.stat:
            nt=ImageProcess()
            nt.img=cv2.add(self.img,t.img)
            nt.getStat()
            return nt
        return None
        
    # cv2与matplotlib的图像转换，cv2是bgr格式，matplotlib是rgb格式
    def img_convert(self):
        # 灰度图片直接返回
        if len(self.img.shape) == 2:
            return self.img
        # 3通道的BGR图片
        elif len(self.img.shape) == 3 and self.img.shape[2] == 3:
            b, g, r = cv2.split(self.img)
            return cv2.merge((r, g, b))
        # 4通道的BGR图片
        elif len(self.img.shape) == 3 and self.img.shape[2] == 4:
            b, g, r, a = cv2.split(self.img)
            return cv2.merge((r, g, b, a))
        # 未知图片格式
        else:
            return self.img
    def toQImage(self):
        '''
            将ImageProcess类处理得到的图片数据(numpyArray类型)转为PyQt5支持的QImage类型
        '''
        return Image.fromarray(np.uint8(self.img)).toqimage()
# 主函数
if __name__ == "__main__":
    t=ImageProcess()
    t.openImg('img/1.jpg')
    t.show()
    t.toCicle()
    t.save('mylove')
    tt=ImageProcess()
    tt.openImg('mylove.png')
    tt.show()
    # img=toCicle(r'D:\WorkSpace\python\云鸟\Server\resource\photo\10.jpg')
    # img=Image.fromarray(np.uint8(t.toCicle()))

    