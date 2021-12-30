"""
音·创(Musicreater)是由金羿(W-YI)开发的一款《我的世界》基岩版音乐生成辅助软件
"""


# W-YI 金羿
# QQ 2647547478
# 音·创 开发交流群 861684859
# Email EillesWan2006@163.com W-YI_DoctorYI@outlook.com
# 版权所有 Team-Ryoun 金羿
# 若需转载或借鉴 请附作者


#  代码写的并非十分的漂亮，还请大佬多多包涵；本软件源代码依照Apache软件协议公开


import sys

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from musicreater.Cmd_Msct import *
from musicreater.msctspt.bugReporter import version

from musicreater.resources.ChineseLang import LANGUAGE



__version__ = version.version[1]+version.version[0]
__author__ = 'W-YI （金羿）'





if sys.platform == 'win32':
    os.chdir(__file__[:len(__file__)-__file__[len(__file__)::-1].index('\\')])
    log("更新执行位置，当前文件位置"+__file__)
else:
    try:
        os.chdir(__file__[:len(__file__) -
                 __file__[len(__file__)::-1].index('/')])
    except:
        pass
    log("其他平台："+sys.platform+"更新执行位置，当前文件位置"+__file__)






class Musicreater(toga.App):
    '''音·创 本体\n
    W-YI 金羿\n
    QQ 2647547478\n
    音·创 开发交流群 861684859\n
    Email EillesWan2006@163.com W-YI_DoctorYI@outlook.com\n
    版权所有 Team-Ryoun 金羿\n
    若需转载或借鉴 请附作者\n
    '''

    

    def startup(self):
        
        
        # Start to draw the window

        main_box = toga.Box(style=Pack(direction=COLUMN))

        self.noticeLabel = toga.Label('MSCT >>>',style=Pack(padding=(0, 5)))

        self.inputBox = toga.TextInput(style=Pack(flex=1))
        #dispImage = toga.ImageView("./resources/oddevenmatrix.png")

        cmd_box = toga.Box(style=Pack(direction=ROW, padding=5))

        cmd_box.add(self.noticeLabel)
        cmd_box.add(self.inputBox)
        # cmd_box.add(dispImage)

        button = toga.Button(
            LANGUAGE['main']['run'],
            on_press=self.showMessage,
            style=Pack(padding=5)
        )
        

        main_box.add(cmd_box)
        main_box.add(button)
        

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

        self.main_window.info_dialog('',"{} {} —— {} {}".format(__author__,LANGUAGE['main']['name'],LANGUAGE['main']['version'],__version__))

        self.nowWorkPath = os.path.split(os.path.realpath(__file__))[0]


    def showMessage(self, widget):

        strcmd = self.inputBox.value
        
        cmd = strcmd.lower().split(' ')

        if cmd[0] == 'exit':
            if exitapp(cmd[1:]) == False:
                self.main_window.info_dialog('',LANGUAGE['command']['FormatError'])
        elif cmd[0] == 'save':
            if saveProject(cmd[1:]) == False:
                self.main_window.info_dialog('',LANGUAGE['command']['FormatError'])
        elif cmd[0] == 'load':
            if loadMusic(cmd[1:]) == False:
                self.main_window.info_dialog('',LANGUAGE['command']['FormatError'])
        elif cmd[0] == 'chdir':
            self.main_window.info_dialog('',LANGUAGE['command']['NotAvailable'])
            return
            nowWorkPath = os.path.realpath(cmd[1])
            os.chdir(nowWorkPath)
        elif cmd[0] == 'build':
            if funBuild(cmd[1:]) == False:
                self.main_window.info_dialog('',LANGUAGE['command']['FormatError'])
        else:
            return
            os.system(strcmd)
        


def main():
    return Musicreater()
