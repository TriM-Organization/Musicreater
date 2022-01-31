"""提供对于音创系列的日志"""
# 诸葛亮与八卦阵帮忙修改语法 日期：---2022年1月19日
# 统计：致命（三级）错误：0个；警告（二级）错误：0个；语法（一级）错误：9个

import logging
import os
import datetime

StrStartTime = str(datetime.datetime.now()).replace(':', '_')[:-7]
time = StrStartTime

main_path = './log/'

position = main_path + time

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

if not os.path.exists('./log/'):
    os.makedirs('./log/')

# try:
# handler = logging.FileHandler(position + ".logger")
# except FileNotFoundError:
# os.makedirs('./log/')
handler = logging.FileHandler(position + ".logger")
print(position + ".logger")

handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

logger.addHandler(handler)
logger.addHandler(console)

# import logger

# 载入日志功能
StrStartTime = str(datetime.datetime.now()).replace(':', '_')[:-7]
# logger.setting(StrStartTime)
"""字符串型的程序开始时间"""


def log(info: str = '', isWrite: bool = True, isPrinted: bool = False, isLoggerLibRecord: bool = True):
    """
    info: 信息
    isPrinted: 是否print（仅限金羿log，python官方的logging照常输出）
    isLoggerLibRecord: 是否同时在logger库中记录
    isWrite: 是否write（仅限金羿log，python官方的logging照常输出）
    """
    """将信息连同当前时间载入日志"""
    # 致后来的开发者：请让金羿的log存在吧，不然他自己都看不懂你们写了什么了
    # 我指的是程序内部
    # ——金羿
    if not os.path.exists('./log/'):
        os.makedirs('./log/')
    if isWrite:
        with open('./log/' + StrStartTime + '.msct.log', 'a', encoding='UTF-8') as f:
            f.write(str(datetime.datetime.now())[11:19] + '	' + info + '\n')
    if isPrinted:
        print(str(datetime.datetime.now())[11:19] + '	' + info)
    if isLoggerLibRecord:
        logger.info(info)


def end():
    logging.disable(logging.INFO)
    logging.shutdown()
