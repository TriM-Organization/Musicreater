"""音·创的日志消息处理"""
# 诸葛亮与八卦阵帮忙修改语法 日期：---2022年1月19日
# 统计：致命（三级）错误：0个；警告（二级）错误：0个；语法（一级）错误：9个

# 对开发者说的话：
#
# 请不要修改这里的日志，日志是给开发者和专业人士看的
# 而不是给普通用户看的，因此，没必要使用开发者自己也
# 不习惯的日志系统，比如说，之前诸葛亮与八卦阵 (bgArray)
# 用了 logging 库来改写我原来的日志支持，但是我反
# 而找不到我想要的信息了，所以，日志系统给我们开发者
# 自己看得好就可以了昂，真的别改了。而且，诸葛八卦改
# 了之后并没有多好，喵喵喵，所以我就换回来了。我知道
# logging 库比较常用，而且功能也好，但是我们毕竟没
# 这个必要，就别用那个库了昂，球球了~ 
#                              ——金羿 Eilles
#                                2022 03 09

# To ALL the developers who will change this part:
#
# Please do NOT change anything in this file!
# The log file is only for developers or
# someone who knows a lot about our program
# to see, but not the common users. So it 
# is NOT NECESSARY to use a logging system
# that we do not familiar or we do not like.
# Take bgAray “诸葛亮与八卦阵” as a example, 
# he once change this `log.py` into 
# logging-library-based log support system.
# But after the change had done, I could NOT
# find useful infomation according to the 
# log file... So use this file but not to 
# make changes PLEASE!!! I know some libraries
# like logging is usually better than the 
# simple system in this file and it is normal
# to use but, I think it is not necessery,
# so PLEASE DO NOT USE OTHER LIBs TO 
# OVERWRITE MY LIBRARY, THANKS. 
#                              ——Eilles 金羿
#                                03/09/2022



import datetime,os

#载入日志功能
StrStartTime = str(datetime.datetime.now()).replace(':', '_')[:-7]
'''字符串型的程序开始时间'''


def log(info:str = '',level : str = 'INFO', isPrinted:bool = False):
    '''将信息连同当前时间载入日志
    :param info : str
        日志信息
    :param level : str['INFO','WARRING','ERROR','CRASH']
        信息等级
    :param isPrinted : bool
        是否在控制台打印
    
    :return bool
        表示是否完成任务'''

    try:

        if not os.path.exists('./log/'):
            os.makedirs('./log/')
        
        outputinfo = f'{str(datetime.datetime.now())[11:19]}-[{level}] {info}'

        with open('./log/'+StrStartTime+'.msct.log', 'a',encoding='UTF-8') as f:
            f.write(outputinfo+'\n')
        
        if isPrinted:
            print(outputinfo)
        
        return True
    except:
        return False
