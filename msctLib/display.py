# -*- coding: utf-8 -*-
'''音·创的GUI窗口界面显示库
:若要使用其他界面显示，请详见：
:开发说明|指南'''


import tkinter as tk
import tkinter.simpledialog as sdialog
import tkinter.filedialog as fdialog
from msctLib.log import log


DEFAULTBLUE = (0, 137, 242)
# 0089F2

WEAKBLUE = (0, 161, 231)
LIGHTBLUE = (38, 226, 255)
# 26E2FF

RED = (255, 52, 50)
PURPLE = (171, 112, 255)
GREEN = (0, 255, 33)
WHITE = (242, 244, 246)
BLACK = (18, 17, 16)


backgroundColor = WHITE
frontgroundColor = BLACK
loadingColor = DEFAULTBLUE
errorColor = RED
okColor = GREEN
tipsColor = PURPLE

# 注：UI界面字体、代码字体
fontPattern = ('DengXian Light', 'Fira Code')


class disp:
    '''音·创 的基本Tk窗口显示库'''

    def __init__(
        self,
        root: tk.Tk = tk.Tk(),
        debug: bool = False,
        title: str = '音·创',
        geometry: str = '0x0',
        iconbitmap: tuple = ('', ''),
        menuWidget: dict = {},
        wordView: str = '音·创 Musicreater',
        buttons: list = [],
        settingBox: list = [],
        notemap: list = [],
        infobar:str = '就绪',
    ) -> None:
        '''使用参数建立基本的 音·创 窗口
        :param root 根窗口
        :param debug 是否将日志输出到控制台
        :param title 窗口标题
        wordview: str #言论部分显示的字样
        button: list = [ # 操作按钮部分
            dict = {
                按钮名称 : tuple(按钮图标,执行函数)
            },
        ],
        settingbox: list = [ # 设置部分显示的字样及其对应的设置函数
            (
                设置名称:str,
                值类型:tuple,
                显示内容:str,
                设置操作函数:<function>,
            )
        ],
        map: list = [ # 一首曲目的音符数据
            音符数据
        ]
        :param infobar 显示信息用
        '''

        # 载入参量 注意！图标将不被载入参数
        self.__root = root
        '''窗口根'''

        self.title = title
        '''窗口标题'''

        self.menuWidgets = menuWidget
        '''菜单设定项'''

        self.wordView = wordView
        '''言·论'''

        self.buttons = buttons
        '''快捷功能按钮'''

        self.settingBox = settingBox
        '''设置框'''

        self.notemap = notemap
        '''音符列表'''

        self.infoBar = infobar
        '''信息显示版'''



        self.debug = debug
        '''是否打开调试模式'''

        self.setTitle()
        self.setGeometry(geometry)
        self.setIcon(*iconbitmap)

        self.setMenu()

        self.initWidget()

    # =========================================================
    # 设定函数部分
    # =========================================================

    def setTitle(self) -> None:
        '''设置窗口标题'''
        self.__root.title = self.title
        if self.debug:
            log(f"设置窗口标题{self.title}")

    def setGeometry(self,geometry:str = '0x0') -> None:
        '''设置窗口大小'''
        self.__root.geometry(geometry)
        if self.debug:
            log(f"设置窗口大小{geometry}")

    def setIcon(
        self, bitmap: str = './musicreater.ico', default: str = ''
    ) -> None:
        '''设置窗口图标
        注意，default参数仅在Windows下有效，其意为将所有没有图标的窗口设置默认图标
        如果在非Windows环境使用default参数，一个Error将被升起'''
        if not self.debug:
            try:
                if default:
                    self.__root.iconbitmap(bitmap, default)
                    log(f'设置图标为{bitmap}，默认为{default}')
                else:
                    self.__root.iconbitmap(bitmap)
                    log(f'设置图标为{bitmap}')
                return True
            except Exception as e:
                log(str(e), 'ERROR')
                return False
        else:
            self.__root.iconbitmap(bitmap, default)
            return

    def setMenu(self) -> None:
        '''设置根菜单'''
        if not self.menuWidgets:
            # 如果传入空参数则返回当前菜单
            try:
                return self.RootMenu
            except Exception as E:
                if self.debug:
                    raise E
                else:
                    log('无法读取菜单信息', 'WARRING')
        # 如果不是空参数则新建菜单
        self.RootMenu = {}
        self.mainMenuBar = tk.Menu(self.__root)
        for menuName, menuCmd in self.menuWidgets.items():
            # 取得一个菜单名和一堆菜单函数及其显示名称
            menu = tk.Menu(self.mainMenuBar, tearoff=0)
            for cmdName, cmdFunc in menuCmd.items():
                if cmdName:
                    menu.add_command(label=cmdName, command=cmdFunc)
                else:
                    menu.add_separator()
            self.mainMenuBar.add_cascade(label=menuName, menu=menu)
            self.RootMenu[menuName] = menu
        self.__root.config(menu=self.mainMenuBar)

    def addMenu(self, menuRoot: str = '', menuLabel: str = '', menuCommand=None):
        '''增加一个菜单项
        :param menuRoot : str
            菜单的根菜单，即所属的菜单上的文字
        :param menuLabel : str
            所需要增加的项目显示的文字
        :param menuCommand : <function>
        '''
        if menuRoot in self.RootMenu.keys:
            # 如果已经有父菜单
            if menuLabel:
                # 增加菜单指令
                self.RootMenu[menuRoot].add_command(
                    label=menuLabel, command=menuCommand
                )
            else:
                # 增加分隔栏
                self.RootMenu[menuRoot].add_separator()
        else:
            # 没有父菜单则新增一个父菜单
            menu = tk.Menu(self.mainMenuBar, tearoff=False)
            if menuLabel:
                menu.add_command(label=menuLabel, command=menuCommand)
            else:
                menu.add_separator()
            self.mainMenuBar.add_cascade(label=menuRoot, menu=menu)
            self.RootMenu[menuRoot] = menu

    def initWidget(self,) -> None:
        '''设置窗口小部件，分为：
        :言·论 WordView
        :快捷按钮面板 ButtonBar
        :设置框 SettingBar
        :音轨框 TrackBar
        :各个音轨的显示框 TrackFrame
        :信息显示版 InfoBar
        '''
        self._wordviewBar = tk.Label(
            self.__root, bg='white', fg='black', text=self.wordView, font=(fontPattern[0], 30)
        )

        self.setWordView(self.wordView)

    def setWordView(self, text: str) -> None:
        self._wordviewBar['text'] = text


    # =========================================================
    # 预置函数部分
    # =========================================================

    def authorWindowStarter(
        authors: tuple = (
            ('金羿', 'Email EillesWan@outlook.com', 'QQ 2647547478'),
            ('诸葛亮与八卦阵', 'QQ 474037765'),
        )
    ):
        '''自定义作者界面'''
        from languages.lang import _
        from languages.lang import DEFAULTLANGUAGE
        from msctLib.buildIN import version

        authorWindow = tk.Tk()
        authorWindow.title(_('关于'))
        authorWindow.geometry('550x600')  # 像素
        tk.Label(authorWindow, text='', font=('', 15)).pack()
        tk.Label(authorWindow, text=_('F音创'), font=('', 35)).pack()
        tk.Label(
            authorWindow,
            text='{} {}'.format(version.version[1] + version.version[0]),
            font=('', 15),
        ).pack()
        # pack 的side可以赋值为LEFT  RTGHT  TOP  BOTTOM
        # grid 的row 是列数、column是行排，注意，这是针对空间控件本身大小来的，即是指向当前控件的第几个。
        # place的 x、y是(x,y)坐标
        tk.Label(
            authorWindow,
            image=tk.PhotoImage(file='./resources/RyounLogo.png'),
            width=200,
            height=200,
        ).pack()
        tk.Label(authorWindow, text=_('凌云pairs'), font=('', 20)).pack()
        tk.Label(authorWindow, text='', font=('', 15)).pack()
        tk.Label(authorWindow, text=_('开发者'), font=('', 15)).pack()
        for i in authors:
            for j in i:
                tk.Label(
                    authorWindow,
                    text=j,
                    font=(
                        '',
                        17 if i.index(j) == 0 else 15,
                        'bold' if i.index(j) == 0 else '',
                    ),
                ).pack()
        tk.Label(authorWindow, text='', font=('', 5)).pack()
        if DEFAULTLANGUAGE != 'zh-CN':
            tk.Label(authorWindow, text=_('译者'), font=('', 15)).pack()
            for i in _('TRANSLATERS').split(';'):
                for j in i.split(','):
                    tk.Label(
                        authorWindow,
                        text=j,
                        font=(
                            '',
                            17 if i.split(',').index(j) == 0 else 15,
                            'bold' if i.split(',').index(j) == 0 else '',
                        ),
                    ).pack()

        def exitAboutWindow():
            authorWindow.destroy()

        tk.Button(authorWindow, text=_('确定'), command=exitAboutWindow).pack()

        authorWindow.mainloop()


class ProgressBar:
    def __init__(
        self,
        root: tk.Tk = tk.Tk(),
        style: tuple = (DEFAULTBLUE, BLACK, WHITE),
        type: bool = False,
        info: str = '',
        debug: bool = False,
    ) -> None:
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


if __name__ == '__mian__':
    import os

    os.chdir('../')
    disp.authorMenu()
