# -*- coding: utf-8 -*-


# 音·创 开发交流群 861684859
# Email EillesWan2006@163.com W-YI_DoctorYI@outlook.com EillesWan@outlook.com
# 版权所有 金羿("Eilles Wan") & 诸葛亮与八卦阵("bgArray") & 鸣凤鸽子("MingFengPigeon")
# 若需转载或借鉴 请依照 Apache 2.0 许可证进行许可


"""
音·创启动器 (Musicreater Launcher)
对音·创的自动安装以及相应版本选择提供支持的工具
Musicreater Launcher (音·创启动器)
A tool that used for installing Musicreater automatically

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


# 下面为正文


import os
import shutil
import threading
import time
import urllib.request
from platform import architecture
from sys import platform

from git import Repo


def downloadPython():
    if os.system('python -V'):
        print('\033[7m{}\033[0m'.format("正在下载python\nDownloading Python"))
        try:
            urllib.request.urlretrieve(
                "https://www.python.org/ftp/python/3.8.10/python-3.8.10.exe"
                if architecture()[0] == "32bit"
                else "https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe",
                "./pythonInstaller.exe",
            )
        except Exception as E:
            input(str(E) + "\n自动下载失败，按下回车取消 | Download failed, press enter to cancel")
            exit()

        print('正在安装python\nInstalling Python')

        os.system(
            f'.\\pythonInstaller.exe /passive InstallAllUsers=1 AssociateFiles=1 CompileAll=1 PrependPath=1 Shortcuts=1 Include_doc=0 Include_exe=1 Include_pip=1 Include_lib=1 Include_tcltk=1 Include_launcher=1 InstallLauncherAllUsers=1 Include_test=0 Include_tools=0'
        )

        os.remove('./pythonInstaller.exe')


def downloadPkgVer():
    Repo.clone_from(
        'https://gitee.com/EillesWan/Musicreater.git',
        './MusictraterPkgver',
        branch='pkgver',
    )


def installLibraries(
    libraries: list, indexs: str = 'https://pypi.tuna.tsinghua.edu.cn/simple'
):
    """安装全部开发用库"""
    if platform == 'win32':
        for i in libraries:
            print("安装库 | Installing Librory：" + i)
            os.system(f"python -m pip install {i} -i {indexs}")
    elif platform == 'linux':
        os.system("sudo apt-get install python3-pip")
        for i in libraries:
            print("安装库 | Installing Librory：" + i)
            os.system(f"sudo python3 -m pip install {i} -i {indexs}")


def __mian__():
    if platform == 'win32':
        import wx

        # 主窗口类
        class MainFrame(wx.Frame):
            def __init__(self, parent, title):
                wx.Frame.__init__(
                    self, id=wx.ID_ANY, parent=parent, title=title, size=(350, 200)
                )

                self.buttonMainVer = wx.Button(
                    self, -1, "音·创主版本\nMSCT main", pos=(50, 20), size=(100, 50)
                )

                self.button_pkgver = wx.Button(
                    self, -1, "音·创库版本\nPkgver", pos=(180, 20), size=(100, 50)
                )

                self.Bind(wx.EVT_BUTTON, self.mainVer, self.buttonMainVer)
                self.buttonMainVer.SetDefault()

                self.Bind(wx.EVT_BUTTON, self.pkgVer, self.button_pkgver)
                self.button_pkgver.SetDefault()

                self.textlabel = wx.StaticText(self, -1, "就绪\nReady", pos=(50, 100))

                self.Show(True)

            def mainVer(self, event):
                wx.MessageBox(
                    "音·创主版本尚在开发过程中，敬请期待！\nThe main version of Musicreater is now developing, please stay tuned...",
                    "提示 | Tips",
                    wx.OK | wx.ICON_INFORMATION,
                )

            def pkgVer(self, event):
                wx.MessageBox(
                    "音·创库版本是一项支持库，本程序仅提供下载，具体使用请见下载后的文件，谢谢！\nThis program is only available for download of pkgver, please see the downloaded file for specific use, thank you!",
                    "提示 | Tips",
                    wx.OK | wx.ICON_INFORMATION,
                )
                self.textlabel.SetLabel("正在检测Python环境\nChecking Python environment")
                time.sleep(1)
                downloadPython()
                self.textlabel.SetLabel("正在下载音·创库版本\nChecking Musicreater Pkgver")
                time.sleep(1)
                downloadPkgVer()
                self.textlabel.SetLabel("正在安装所需依赖库\nInstalling required libraries")
                time.sleep(1)
                installLibraries(
                    [
                        'brotli',
                        'mido',
                    ]
                )
                self.textlabel.SetLabel("完成！\nOK!")
                time.sleep(1)
                os.remove('./MusictraterPkgver/.gitignore')
                shutil.rmtree('./MusictraterPkgver/.git')
                self.Show(False)
                self.Destroy()
                exit()

        app = wx.App(False)
        frame = MainFrame(None, "音·创 启动器 | MSCT Launcher")
        app.MainLoop()
    elif platform == 'linux':
        pass


if __name__ == '__main__':
    __mian__()
