


import threading


class NewThread(threading.Thread):
    '''新建一个进程来运行函数，函数运行完毕后可以使用.getResult方法获取其返回值'''
    def __init__(self, func, args=()):
        super(NewThread, self).__init__()
        self.func = func
        self.args = args
    def run(self):
        self.result = self.func(*self.args)
    def getResult(self):
        threading.Thread.join(self)  # 等待线程执行完毕
        try:
            return self.result
        except Exception:
            return None

#
# ————————————————
# 版权声明：上面的类NewThread修改自CSDN博主「星火燎愿」的原创文章中的内容，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/xpt211314/article/details/109543014
# ————————————————
#