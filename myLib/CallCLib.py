'''
通过这个类可以直接调用用C写的库,只需提供C文件将自动编译,每次初始化时都会重新编译得到最新的库
'''
from ctypes import cdll
import sys, os
# sys.path.append('../')
# from myLib.timing import timing


class CallCLib:
    def __init__(self, cpath):
        s = self.cmdOrder('gcc -fPIC -shared %s.c -o %s.so' % (cpath, cpath))
        if s:
            self.lib = cdll.LoadLibrary(cpath + '.so')
        else:
            print('文件%s.c编译失败或编译结果.so文件不可用' % cpath)
            self.lib = None

    def cmdOrder(self, order):
        with os.popen(order, 'r') as f:
            r = f.read()
            print(r, len(r), type(r))
            if r == '':
                r = True
            return r
        return False


if __name__ == '__main__':
    t = CallCLib(r'D:\WorkSpace\python\Cpython\c1')
    if t.lib:
        print(dir(t.lib.t1))
        print(t.lib.t1(1, 2))
