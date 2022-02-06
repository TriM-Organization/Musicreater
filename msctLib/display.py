# -*- coding: utf-8 -*-
'''音·创的GUI界面显示库
:若要使用其他界面显示，请详见：
:开发说明|指南'''


import tkinter as tk
import tkinter.simpledialog as sdialog
import tkinter.filedialog as fdialog

root = tk.Tk()

class disp:

    def __init__(self,root:tk.Tk = root,debug:bool = False,**kwgs) -> None:
        '''传入root参数为窗口根，kwgs详见开发说明|指南'''

        self.root = root

        self.FUNCLIST = {
            'title' : self.setTitle,
            'geometry': self.setGeometry,
            'iconbitmap': self.setIcon,
        }
        '''注：此处为引导传参，若传参错误且debug模式关闭则不会有任何反馈'''

    def setTitle(self,title:str = '') -> None:
        self.root.title = title
    
    def setGeometry(self,geometry) -> None:
        self.root.geometry(geometry)
    
    def setIcon(self,*icon) -> None:
        self.root.iconbitmap(*icon)
    
    def setMenu(self,**kwgs) -> None:
        menus = []
        mainMenuBar = tk.Menu(self.root)
        for menuName,menuCmd in kwgs.items():
            menu = tk.Menu(mainMenuBar,tearoff=0)
            for cmdName,cmdFunc in menuCmd.items():
                if cmdName:
                    menu.add_command(label = cmdName, command = cmdFunc)
                else:
                    menu.add_separator()
            mainMenuBar.add_cascade(label=menuName,menu=menu)
            menus.append(menu)