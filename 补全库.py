
from os import system

if platform == "linux":
    system("python3 -m pip install -r ./Musicreater/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/")
elif platform == "win32":
    system("pip install -r ./Musicreater/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/")
