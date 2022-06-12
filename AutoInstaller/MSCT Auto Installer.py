# -*- coding: utf-8 -*-


# 音·创 开发交流群 861684859
# Email EillesWan2006@163.com W-YI_DoctorYI@outlook.com EillesWan@outlook.com
# 版权所有 金羿("Eilles Wan") & 诸葛亮与八卦阵("bgArray") & 鸣凤鸽子("MingFengPigeon")
# 若需转载或借鉴 请依照 Apache 2.0 许可证进行许可


"""
音·创自动安装器 (Musicreater Auto Installer)
对音·创的自动安装提供支持的独立软件
Musicreater Auto Installer (音·创自动安装器)
A software that used for installing Musicreater automatically

   Copyright 2022 all the developers of Musicreater

   Licensed under the Apache License, Version 2.0 (the 'License');
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an 'AS IS' BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

# 代码写的并非十分的漂亮，还请大佬多多包涵；本软件源代码依照Apache软件协议公开


# 下面为正文


from sys import platform
from platform import architecture
import urllib.request
import zipfile
from os import system as srun
from os import walk, rename, remove, path, chdir, listdir
from shutil import rmtree, move


if platform == "win32":

    nowpath = __file__[: len(__file__) - __file__[len(__file__) :: -1].index('\\')]

    if srun('python -V'):

        print('\033[7m{}\033[0m'.format("正在下载python\nDownloading Python"))

        try:
            urllib.request.urlretrieve(
                "https://www.python.org/ftp/python/3.8.10/python-3.8.10.exe"
                if architecture()[0] == "32bit"
                else "https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe",
                "./pythonInstaller.exe",
            )
            # urllib.request.urlretrieve("https://www.python.org/ftp/python/3.8.10/python-3.8.10.exe","./pythonInstaller.exe")
        except Exception as E:
            input(str(E) + "\n自动下载失败，按下回车取消")
            exit()

        print('正在安装python\nInstalling Python')

        # open('install.bat','w').write(f'.\\pythonInstaller.exe /passive InstallAllUsers=0 TargetDir="{nowpath}python38" DefaultJustForMeTargetDir="{nowpath}python38" AssociateFiles=0 CompileAll=1 PrependPath=0 Shortcuts=0 Include_doc=0 Include_launcher=0 InstallLauncherAllUsers=0 Include_test=0 Include_tools=0')

        srun(
            f'.\\pythonInstaller.exe /passive InstallAllUsers=1 AssociateFiles=1 CompileAll=1 PrependPath=1 Shortcuts=1 Include_doc=0 Include_exe=1 Include_pip=1 Include_lib=1 Include_tcltk=1 Include_launcher=1 InstallLauncherAllUsers=1 Include_test=0 Include_tools=0'
        )

        remove('./pythonInstaller.exe')

    # print('\033[7m{}\033[0m'.format("正在下载pip安装工具\nDownloading get-pip tool"))

    # try:
    #     urllib.request.urlretrieve(
    #         "https://bootstrap.pypa.io/get-pip.py", "./python38/get-pip.py"
    #     )
    # except Exception as E:
    #     input(str(E) + "\n自动下载失败，按下回车取消")
    #     exit()

    # print('\033[7m{}\033[0m'.format("正在下载pip\nDownloading pip"))

    # chdir('./python38')
    # srun(r'".\python.exe get-pip.py')

    # print('\033[7m{}\033[0m'.format('正在安装pip\nInstalling pip'))

    # for dire in listdir('./Lib/site-packages/'):
    #     move('./Lib/site-packages/'+dire,'./'+dire)

    # print('\033[7m{}\033[0m'.format("完成！"))

    # chdir('../')

    try:
        choseurl = int(
            input(
                '\033[7m{}\033[0m'.format(
                    """请选择 音·创 下载源,默认为0
Please choose a download source of Musicreater(default 0)
[0] 私有服务器<暂无> | Private Server<Haven't been built>
[1] Gitee
[2] Github\n:"""
                )
            )
        )
    except Exception as E:
        print('\033[7m{}\033[0m'.format(str(E) + "\n将使用默认源\nUsing default source"))
        choseurl = 0

    myurl = ""
    Giteeurl = "https://gitee.com/EillesWan/Musicreater/repository/blazearchive/master.zip?Expires=1647771436&Signature=%2BkqLHwmvzScCd4cPQDP0LHLpqeZUxOrOv17QpRy%2FTzs%3D"
    Githuburl = (
        "https://codeload.github.com/EillesWan/Musicreater/zip/refs/heads/master"
    )

    url = (
        myurl
        if choseurl == 0
        else Giteeurl
        if choseurl == 1
        else Githuburl
        if choseurl == 2
        else myurl
    )

    print('\033[7m{}\033[0m'.format("正在下载音·创\nDownloading Musicreater"))

    try:
        urllib.request.urlretrieve(url, "./master.zip")
    except Exception as E:
        input('\033[0{}\033[0m'.format(str(E) + "\n自动下载失败，按下回车取消"))
        exit()

    print('\033[7m{}\033[0m'.format("安装音·创\nInstalling Musicreater"))

    zipfile.ZipFile("./master.zip", "r").extractall()

    remove("./master.zip")

    try:
        rmtree("./Musicreater")
    except:
        pass

    rename("./Musicreater-master/", "./Musicreater/")

elif platform == 'linux':
    srun("sudo apt-get install python3")
    srun("sudo apt-get install python3-pip")
    srun("sudo apt-get install git")
    try:
        choseurl = int(
            input(
                '\033[0{}\033[0m'.format(
                    """请选择 音·创 下载源,默认为1
Please choose a download source of Musicreater(default 1)
[1] Gitee
[2] Github\n:"""
                )
            )
        )
    except Exception as E:
        print(str(E) + "\n将使用默认源\nUsing default source")
        choseurl = 1

    url = (
        "https://gitee.com/EillesWan/Musicreater.git"
        if choseurl == 1
        else "https://github.com/EillesWan/Musicreater.git"
        if choseurl == 2
        else "https://gitee.com/EillesWan/Musicreater.git"
    )
    srun(f"sudo git clone {url}")


print('\033[7m{}\033[0m'.format("编译音·创\nCompiling Musicreater"))

if platform == "linux":
    srun("python3 -O -m compileall -b ./Musicreater/")
elif platform == "win32":
    srun("python -O -m compileall -b ./Musicreater/")

for parent, dirnames, filenames in walk("./Musicreater"):
    for filename in filenames:
        if filename[-3:] == ".py":
            fn = path.join(parent, filename)
            remove(fn)
            print(f"删除文件 {fn}")
    for dirname in dirnames:
        if dirname == "__pycache__":
            pn = path.join(parent, dirname)
            rmtree(pn)
            print(f"删除目录 {pn}")


print(
    '\033[7m{}\033[0m'.format(
        """您可以开始使用音·创了
我们将在后台为您安装各项支持库
您可以运行Musicreater文件夹中的Musicreater.pyc文件来运行音·创

You can use Musicreater now,
We will setup the libraries ineed for you in background,
You can now open Musicreater.PYC in the directory of ./Musicreater to run Musicreater
"""
    )
)


if platform == "linux":
    srun("python3 -m pip install -r ./Musicreater/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/")
elif platform == "win32":
    srun("pip install -r ./Musicreater/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/")
