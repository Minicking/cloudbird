'''
用来显示某一个函数运行所花费的时间的装饰器
'''
import time, threading


def timing(func):
    def start(*args, **kwargs):
        time1 = time.time()
        r = func(*args, **kwargs)
        time2 = time.time()
        print("%s(%s,%s),运行结束，用时%f" %
              (func.__name__, args, kwargs, time2 - time1))
        return r

    return start


if __name__ == '__main__':

    @timing
    def a(t):
        x = 0
        for i in range(t):
            x += 1
        return x

    print(a(10000000))
