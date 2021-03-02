import time, sys
class ConstError(Exception):
    pass

class Enum:
    '''
    Gender = Enum('male', 'female')
    user_gender = Gender.male
    '''
    def __init__(self,*args):
        self.data = {}
        self.index = 0
        for ii in args:
            self.data[ii] = self.index
            self.index += 1

    def __getattr__(self, key):

        return self.data[key]

    def __str__(self):
        return str(self.data)


class Const(dict):

    '''
    c = Const()
    c.A = 1
    c['B'] = 2
    print(c.A, c['A'], c.B, c['B'])
    '''

    def __setattr__(self, key, val):

        if key in self:
            raise ConstError

        self[key] = val

    def __getattr__(self, key):

        return self[key]

    def __contains__(self, key):
        return key in self.values()


class Uitl:
    def __init__(self, config):
        self.config = config

    def log(self, text):
        now = time.localtime()
        now_time = r'{}:{}:{}'.format(now.tm_hour, now.tm_min, now.tm_sec)
        now_date = r'{}-{}-{}'.format(now.tm_year, now.tm_mon,now.tm_mday)
        if self.config.log_path:
            path = r'../{}-{}.log'.format(self.config.log_path, now_date)
            with open(path, 'a+') as f:
                f.write(r"[{}]:{}\n".format(now_time, text))
        print(r"[{}]:{}".format(now_time, text))

if __name__ == '__main__':
    sys.path.append('../')
    for i in sys.path:
        print(i)
    from Config import Config
    a = Uitl(Config)
    a.log('wocao')