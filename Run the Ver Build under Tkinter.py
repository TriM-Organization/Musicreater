# -*- coding: utf-8 -*-
import os,shutil
from sys import platform





print("更新执行位置...")
if platform == 'win32':
    try:
        os.chdir(__file__[:len(__file__)-__file__[len(__file__)::-1].index('\\')]+'src\\')
        print("更新执行位置，当前文件位置"+__file__)
    except:
        pass
else:
    try:
        os.chdir(__file__[:len(__file__)-__file__[len(__file__)::-1].index('/')]+'src/')
    except:
        pass
    print("其他平台："+platform+"更新执行位置，当前文件位置"+__file__)
print('完成！')







try:
    import toga,amulet
except:
    print("You'd better install the libraries of this app\nNow, we're helping you with this.")
    from src.musicreater.msctspt.bugReporter import version
    version.installLibraries(version)






if platform == 'win32':
    os.system("python ./Musicreater.py")
elif platform == 'linux':
    os.system("python3 ./Musicreater.py")






try:
    if os.path.exists("./log/"):
        shutil.rmtree("./log/")
    if os.path.exists("./logs/"):
        shutil.rmtree("./logs/")
    if os.path.exists("./cache/"):
        shutil.rmtree("./cache/")
except:
    print("无法清除日志及临时文件")