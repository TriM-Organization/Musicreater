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
        '''

        self.root = root
        self.title = title
        self.geometry = geometry
        self.menuWidget = menuWidget
        self.wordView = wordView
        self.buttons = buttons
        self.settingBox = settingBox
        self.notemap = notemap

        self.setTitle(title, debug)
        self.setGeometry(geometry, debug)
        self.setIcon(*iconbitmap, debug=debug)

        self.setMenu(menuWidget)

        self.initWidget(wordView, buttons, settingBox, notemap)

    def setTitle(self, title: str = '', debug: bool = False) -> None:
        '''设置窗口标题'''
        self.root.title = title
        if debug:
            log(f"设置窗口标题{title}")

    def setGeometry(self, geometry: str = '0x0', debug: bool = False) -> None:
        '''设置窗口大小'''
        self.root.geometry(geometry)
        if debug:
            log(f"设置窗口大小{geometry}")

    def setIcon(
        self, bitmap: str = './musicreater.ico', default: str = '', debug: bool = False
    ) -> None:
        '''设置窗口图标
        注意，default参数仅在Windows下有效，其意为将所有没有图标的窗口设置默认图标
        如果在非Windows环境使用default参数，一个Error将被升起'''
        if not debug:
            try:
                if default:
                    self.root.iconbitmap(bitmap, default)
                    log(f'设置图标为{bitmap}，默认为{default}')
                else:
                    self.root.iconbitmap(bitmap)
                    log(f'设置图标为{bitmap}')
                return True
            except Exception as e:
                log(str(e), 'ERROR')
                return False
        else:
            self.root.iconbitmap(bitmap, default)
            return

    def setMenu(self, menuWidgets: dict = {}, debug: bool = False) -> None:
        '''设置根菜单'''
        if not menuWidgets:
            # 如果传入空参数则返回当前菜单
            try:
                return self.RootMenu
            except Exception as E:
                if debug:
                    raise E
                else:
                    log('无法读取菜单信息', 'WARRING')
        # 如果不是空参数则新建菜单
        self.RootMenu = {}
        self.mainMenuBar = tk.Menu(self.root)
        for menuName, menuCmd in menuWidgets.items():
            # 取得一个菜单名和一堆菜单函数及其显示名称
            menu = tk.Menu(self.mainMenuBar, tearoff=0)
            for cmdName, cmdFunc in menuCmd.items():
                if cmdName:
                    menu.add_command(label=cmdName, command=cmdFunc)
                else:
                    menu.add_separator()
            self.mainMenuBar.add_cascade(label=menuName, menu=menu)
            self.RootMenu[menuName] = menu
        self.root.config(menu=self.mainMenuBar)

    def addMenu(self, menuRoot: str = '', menuLabel: str = '', menuCommand = None):
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

    def initWidget(
        self,
        wordView: str = '音·创 Musicreater',
        buttons: list = [],
        settingBox: list = [],
        notemap: list = [],
    ) -> None:
        '''设置窗口小部件，分为：
        :言·论 WordView
        :快捷按钮面板 ButtonBar
        :设置框 SettingBar
        :音轨框 TrackBar
        :各个音轨的显示框 TrackFrame
        :信息显示版 InfoBar
        '''
        self._wordviewBar = tk.Label(self.root, bg='white', fg='black', text=wordView)

        self.setWordView(wordView)

    def setWordView(self, text: str) -> None:
        self._wordviewBar['text'] = text


def authorMenu(
    authors: tuple = (('金羿', 'EillesWan@outlook.com'), ('诸葛亮与八卦阵', '474037765'))
):
    '''自定义作者界面'''
    from languages.lang import _
    from msctLib.buildIN import version

    aabw = tk.Tk()
    aabw.title(_('关于'))
    aabw.geometry('550x600')  # 像素
    tk.Label(aabw, text='', font=('', 15)).pack()
    tk.Label(aabw, text=_('F音创'), font=('', 35)).pack()
    tk.Label(
        aabw,
        text='{} {}'.format(version.version[1] + version.version[0]),
        font=('', 15),
    ).pack()
    # pack 的side可以赋值为LEFT  RTGHT  TOP  BOTTOM
    # grid 的row 是列数、column是行排，注意，这是针对空间控件本身大小来的，即是指向当前控件的第几个。
    # place的 x、y是(x,y)坐标
    # pic = tk.PhotoImage(file='./bin/pics/Ryoun_S.png')
    # tk.Label(aabw, image=pic, width=200, height=200).pack()
    # del pic
    tk.Label(aabw, text='', font=('', 5)).pack()
    tk.Label(aabw, text=READABLETEXT[12], font=('', 20)).pack()
    tk.Label(aabw, text='', font=('', 15)).pack()
    for i in READABLETEXT[15]:
        tk.Label(
            aabw, text=i[0], font=('', 17 if i[1] else 15, 'bold' if i[1] else '')
        ).pack()
    tk.Label(aabw, text='', font=('', 5)).pack()
    if DEFAULTLANGUAGE != 'zh-CN':
        tk.Label(aabw, text=READABLETEXT[16], font=('', 15)).pack()
        for i in READABLETEXT['Translator']:
            tk.Label(
                aabw, text=i[0], font=('', 17 if i[1] else 15, 'bold' if i[1] else '')
            ).pack()

    def exitAboutWindow():
        aabw.destroy()

    tk.Button(aabw, text=READABLETEXT[13], command=exitAboutWindow).pack()

    aabw.mainloop()


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
