"""提供对于音创系列的日志"""
# 诸葛亮与八卦阵帮忙修改语法 日期：---2022年1月19日
# 统计：致命（三级）错误：0个；警告（二级）错误：0个；语法（一级）错误：9个

import logging
import os
import datetime
import sys

StrStartTime = str(datetime.datetime.now()).replace(':', '_')[:-7]
time = StrStartTime

main_path = './log/'

position = main_path + time

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler(position + ".logger")
print(position + ".logger")

handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

logger.addHandler(handler)
logger.addHandler(console)

print("using Timbre_resources_package_generator_lib \n --made by 诸葛亮与八卦阵")
print(sys.path[0].replace("nmcsup\\logger", "log\\"))

# import logger

# 载入日志功能
StrStartTime = str(datetime.datetime.now()).replace(':', '_')[:-7]
# logger.setting(StrStartTime)
"""字符串型的程序开始时间"""


def log(info: str = '', isPrinted: bool = False, isLoggerLibRecord: bool = True):
    # isLoggerLibRecord: 是否同时在logger库中记录
    """将信息连同当前时间载入日志"""
    if not os.path.exists('./log/'):
        os.makedirs('./log/')
    with open('./log/' + StrStartTime + '.msct.log', 'a', encoding='UTF-8') as f:
        f.write(str(datetime.datetime.now())[11:19] + '	' + info + '\n')
    if isPrinted:
        print(str(datetime.datetime.now())[11:19] + '	' + info)
    if isLoggerLibRecord:
        logger.info(info)
