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

global __root
global title
global menuWidgets
global wordView
global buttons
global settingBox
global notemap
global infoBar
global debug


__root = None
'''窗口根'''
# 音·创 的基本Tk窗口显示函数


def initWindow(
    Debug: bool = False,
    title_: str = '音·创',
    geometry: str = '0x0',
    iconbitmap: tuple = ('./resources/musicreater.ico', './resources/musicreater.ico'),
    menuWidget: dict = {},
    wordview: str = '音·创 Musicreater',
    button: list = [],
    settingbox: list = [],
    notemap_: list = [],
    infobar: str = '就绪',
) -> None:
    '''使用参数建立基本的 音·创 窗口
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
    :param infobar str 显示信息用
    '''

    if Debug:
        log('载入参数')

    # 载入参量 注意！图标将不被载入参数

    global title
    global menuWidgets
    global wordView
    global buttons
    global settingBox
    global notemap
    global infoBar
    global debug



    title = title_
    '''窗口标题'''

    menuWidgets = menuWidget
    '''菜单设定项'''

    wordView = wordview
    '''言·论 所显示的文字'''

    buttons = button
    '''快捷功能按钮'''

    settingBox = settingbox
    '''设置框'''

    notemap = notemap_
    '''音符列表'''

    infoBar = infobar
    '''信息显示版所显示的文字'''

    debug = Debug
    '''是否打开调试模式'''

    setTitle()

    setGeometry(geometry)
    setIcon(*iconbitmap)

    setMenu()

    initWidget()

def winstart() -> None:
    # 启动主消息循环
    __root.mainloop()

# =========================================================
# 设定函数部分
# =========================================================

def setTitle( title_: str = '') -> None:
    '''设置窗口标题
    :param title: str 窗口标题'''
    global title
    if title:
        title = title_
    __root.title(title)
    if debug:
        log(f"设置窗口标题 {title}")

def setGeometry( geometry: str = '0x0') -> None:
    '''设置窗口大小
    :param geometry: str 窗口大小'''
    __root.geometry(geometry)
    if debug:
        log(f"设置窗口大小{geometry}")

def setIcon( bitmap: str = './musicreater.ico', default: str = '') -> bool:
    '''设置窗口图标
    :param bitmap: str 图标路径
    :param default: str 设置对于全局的默认图标路径
    注意，default参数仅在Windows下有效，其意为将所有没有图标的窗口设置默认图标。如果在非Windows环境使用default参数，将会引发一个错误
    :retuen bool 是否成功设置图标'''

    try:
        if default:
            __root.iconbitmap(bitmap, default)
            log(f'设置图标为{bitmap}，默认为{default}')
        else:
            __root.iconbitmap(bitmap)
            log(f'设置图标为{bitmap}')
        return True
    except Exception as e:
        log(str(e), 'ERROR')
        if debug:
            raise e
        return False

def setMenu() -> None:
    '''设置根菜单'''
    
    global _RootMenu
    global _mainMenuBar

    if not menuWidgets:
        # 如果传入空参数则返回当前菜单
        try:
            return _RootMenu
        except Exception as E:
            if debug:
                raise E
            log('无法读取菜单信息', 'WARRING')
    # 如果不是空参数则新建菜单
    log('新建一个菜单')

    _RootMenu = {}
    _mainMenuBar = tk.Menu(__root)
    for menuName, menuCmd in menuWidgets.items():
        # 取得一个菜单名和一堆菜单函数及其显示名称
        menu = tk.Menu(_mainMenuBar, tearoff=0)
        for cmdName, cmdFunc in menuCmd.items():
            if cmdName:
                menu.add_command(label=cmdName, command=cmdFunc)
                log('菜单项 -- ' + cmdName)
            else:
                menu.add_separator()
                log('分隔符 -- 分隔符')
        _mainMenuBar.add_cascade(label=menuName, menu=menu)
        _RootMenu[menuName] = menu
        log('计入一个菜单 -- ' + menuName)
    __root.config(menu=_mainMenuBar)
    log('菜单设置完毕')

def addMenu( menuRoot: str = '', menuLabel: str = '', menuCommand=None):
    '''增加一个菜单项
    :param menuRoot : str
        菜单的根菜单，即所属的菜单上的文字
    :param menuLabel : str
        所需要增加的项目显示的文字
    :param menuCommand : <function>
    '''
    
    global _RootMenu
    global _mainMenuBar

    if menuRoot in _RootMenu.keys:
        # 如果已经有父菜单
        if menuLabel:
            # 增加菜单指令
            _RootMenu[menuRoot].add_command(
                label=menuLabel, command=menuCommand
            )
        else:
            # 增加分隔栏
            _RootMenu[menuRoot].add_separator()
    else:
        # 没有父菜单则新增一个父菜单
        menu = tk.Menu(_mainMenuBar, tearoff=False)
        if menuLabel:
            menu.add_command(label=menuLabel, command=menuCommand)
        else:
            menu.add_separator()
        _mainMenuBar.add_cascade(label=menuRoot, menu=menu)
        _RootMenu[menuRoot] = menu

def initWidget(
    
) -> None:
    '''设置窗口小部件，分为：
    :言·论 WordView
    :快捷按钮面板 ButtonBar
    :设置框 SettingBar
    :音轨框 TrackBar
    :各个音轨的显示框 TrackFrame
    :信息显示版 InfoBar
    '''

    global _wordviewBar
    global _infoBar
    global _buttonBar

    _wordviewBar = tk.Label(
        __root,
        bg='black',
        fg='white',
        text=wordView,
        font=(fontPattern[0], 30),
    )
    # 定义 言·论 版面
    log('言·论版面设置完成')

    _infoBar = tk.Label(
        __root,
        bg='white',
        fg='black',
        text=infoBar,
        font=(fontPattern[0], 10),
    )
    # 定义 信息显示版
    log('信息显示版设置完成')

    _buttonBar = tk.Frame(
        __root,
        bd=2,
    )
    # 定义 快捷按钮面板. 注意！这里是以一个Frame为容器，而不是一个Button列表，后面的版面也以Frame容器居多

    setButtonBar(buttons)

    _wordviewBar.pack(side='top', fill='x')
    _buttonBar.pack(side='top', fill='x')

    _infoBar.pack(side='bottom', fill='x')

def setButtonBar(
    
    buttonList: list = [],
    defaultMissingTexturePath: str = './resources/uimage/missing_texture.png',
    separatorButtonTexturePath: str = './resources/uimage/separator_line.png',
) -> None:
    '''设置快捷按钮面板
    :param buttonList : list
        快捷按钮列表，每个元素为一个字典，字典的键为按钮名称，值为一个元组，元组中第一项为按钮的图标，第二项为按钮的回调函数
    '''

    # 图标应该如下
    # 新建 打开 保存 |

    global _buttonBarList

    _buttonBarList = []
    '''按钮对象列表，注意软件调用的时候千万别动！'''

    separatorimg = tk.PhotoImage(file=separatorButtonTexturePath)

    for buttons in buttonList:
        # 循环每个按钮组
        for name, args in buttons.items():
            # 循环每个按钮
            try:
                img = tk.PhotoImage(file=args[0])
            except:
                log('载入图片失败，使用默认图片','WARNING')
                if debug:
                    raise FileNotFoundError(f'图片{args[0]}不存在')
                img = tk.PhotoImage(file=defaultMissingTexturePath)
            button = tk.Button(
                _buttonBar,
                text=name,
                command=args[1],
                image=img,
                bd=2,
                compound='center',
                font=(fontPattern[0], 10),
            )
            button.pack(side='left', padx=5, pady=5)
            _buttonBarList.append(button)
            # 添加按钮
        tk.Label(_buttonBar, image=separatorimg).pack(
            side='left', padx=5, pady=5
        )

def setWordView( text: str) -> None:
    '''重新设置言·论版的文字'''
    _wordviewBar['text'] = text

def setInfoBar( text: str) -> None:
    '''重新设置信息显示版的文字'''
    _infoBar['text'] = text

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
        text='{} {}'.format(version.version[1] , version.version[0]),
        font=('', 15),
    ).pack()
    # pack 的side可以赋值为LEFT  RTGHT  TOP  BOTTOM
    # grid 的row 是列数、column是行排，注意，这是针对空间控件本身大小来的，即是指向当前控件的第几个。
    # place的 x、y是(x,y)坐标
    rylogo = tk.PhotoImage(file='./resources/RyounLogo.png')
    tk.Label(
        authorWindow,
        image=rylogo,
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
        root = root


# TODO
# 单选框与复选框


if __name__ == '__mian__':
    import os

    os.chdir('../')
    authorWindowStarter()