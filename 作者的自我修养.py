
from os import system
from sys import platform

if platform == "linux":
    system("python3 -m pip install -r ./requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/")
elif platform == "win32":
    system("pip install -r ./requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/")
