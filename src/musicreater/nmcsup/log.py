"""提供对于音创系列的日志"""

import datetime,os

#载入日志功能
StrStartTime = str(datetime.datetime.now()).replace(':', '_')[:-7]
'''字符串型的程序开始时间'''


def log(info:str = '',isPrinted:bool = True):
    '''将信息连同当前时间载入日志'''
    if not os.path.exists('./log/'):
        os.makedirs('./log/')
    with open('./log/'+StrStartTime+'.msct.log', 'a',encoding='UTF-8') as f:
        f.write(str(datetime.datetime.now())[11:19]+'	'+info+'\n')
    if isPrinted:
        print(str(datetime.datetime.now())[11:19]+'	'+info)
