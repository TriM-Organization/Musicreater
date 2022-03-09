# -*- coding: utf-8 -*-
'''音·创的GUI窗口界面显示库
:若要使用其他界面显示，请详见：
:开发说明|指南'''


import tkinter as tk
import tkinter.simpledialog as sdialog
import tkinter.filedialog as fdialog
from msctLib.log import log


DEFAULTBLUE = (0, 137, 242)
WEAKBLUE = (0, 161, 231)
LIGHTBLUE = (38, 226, 255)
RED = (255, 52, 50)
PURPLE = (171, 112, 255)
GREEN = (0, 255, 33)
WHITE = (242, 244, 246)
BLACK = (18, 17, 16)




class disp:

    # 正在修改，没改完
    def __init__(self,root:tk.Tk = tk.Tk(),debug:bool = False,title:str = '',
                 geometry : str = '0x0', iconbitmap : tuple = ('',''), menuWidget:dict = {},
                 wordView : str = '音·创 Musicreater', ) -> None:
        '''传入root参数为窗口根，kwgs详见开发说明|指南'''

        self.root = root

        self.FUNCLIST = {
            'title' : self.setTitle,
            'geometry': self.setGeometry,
            'iconbitmap': self.setIcon,
            'menu': self.setMenu,
            'widget': self.setWidget,
        }
        '''注：此处为引导传参，若传参错误且debug模式关闭则不会有任何反馈'''

        for func,args in kwgs:
            if func in self.FUNCLIST.keys():
                if type(args) == type([]):
                    self.FUNCLIST[func](*args)
                if type(args) == type({}):
                    self.FUNCLIST[func](**args)
                else:
                    self.FUNCLIST[func](args)
            elif debug:
                raise KeyError(f'无法定位函数{func}')

    def setTitle(self,title:str = '',debug : bool = False) -> None:
        '''设置窗口标题'''
        self.root.title = title
        if debug:
            
    
    def setGeometry(self,geometry) -> None:
        '''设置窗口大小'''
        self.root.geometry(geometry)
    
    def setIcon(self,*icon) -> None:
        '''设置窗口图标'''
        self.root.iconbitmap(*icon)
    
    def setMenu(self,**kwgs) -> None:
        '''设置根菜单'''
        if not kwgs:
            return self.RootMenu
        self.RootMenu = {}
        self.mainMenuBar = tk.Menu(self.root)
        for menuName,menuCmd in kwgs.items():
            menu = tk.Menu(self.mainMenuBar,tearoff=0)
            for cmdName,cmdFunc in menuCmd.items():
                if cmdName:
                    menu.add_command(label = cmdName, command = cmdFunc)
                else:
                    menu.add_separator()
            self.mainMenuBar.add_cascade(label=menuName,menu=menu)
            self.RootMenu[menuName] = menu
        self.root.config(menu=self.mainMenuBar)
    
    def addMenu(self,menuRoot:str = '',menuLabel:str = '',menuCommand:str = None):
        '''增加一个菜单项'''
        if menuRoot in self.RootMenu.keys:
            if menuLabel:
                self.RootMenu[menuRoot].add_command(label = menuLabel, command = menuCommand)
            else:
                self.RootMenu[menuRoot].add_separator()
        else:
            menu = tk.Menu(self.mainMenuBar,tearoff=False)
            if menuLabel:
                menu.add_command(label = menuLabel, command = menuCommand)
            else:
                menu.add_separator()
            self.mainMenuBar.add_cascade(label=menuRoot,menu=menu)
            self.RootMenu[menuRoot] = menu

        
    
    def setWidget(self,**kwgs) -> None:
        self._wordviewBar = tk.Label(self.root)
        pass

    def setWordView(self, **kwgs) -> None:
        for key,value in kwgs.items():
            self._wordviewBar[key] = value




class ProgressBar:

    def __init__(self,root:tk.Tk = tk.Tk(),style:tuple = (DEFAULTBLUE,BLACK,WHITE),
                 type : bool = False, info : str = '', debug:bool = False) -> None:
        '''建立一个进度条或者加载等待界面
        :param root : tk.Tk
            建立进度条的根窗口
        :param style : tuple
            设置主题颜色，第一个参数为进度条或者等待转圈圈的颜色，第二个参数为前景色，第三个是背景色
        :param type : bool
            类型，为 False 时为进度条，为 True 时为等待板
        :param info : str
            显示的附加信息
        :param debug : bool
            是否输出日志到控制台'''
        self.root = root