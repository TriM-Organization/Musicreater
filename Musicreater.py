# -*- coding: utf-8 -*-


# W-YI 金羿
# QQ 2647547478
# 音·创 开发交流群 861684859
# Email EillesWan2006@163.com W-YI_DoctorYI@outlook.com EillesWan@outlook.com
# 版权所有 Team-Ryoun 金羿("Eilles Wan") & 诸葛亮与八卦阵("bgArray")
# 若需转载或借鉴 请附作者


"""
音·创 (Musicreater)
一款免费开源的 《我的世界：基岩版》 音乐制作软件
Musicreater (音·创)
A free opensource software which is used for creating all kinds of musics in Minecraft

   Copyright 2022 Team-Ryoun

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

#  代码写的并非十分的漂亮，还请大佬多多包涵；本软件源代码依照Apache软件协议公开

# -----------------------------分割线-----------------------------
# 诸葛亮与八卦阵帮忙修改语法 日期：---2022年1月19日
# 统计：致命（三级）错误：0个；警告（二级）错误：15个；语法（一级）错误：597个
# 目前我的Pycharm并没有显示任何错误，有错误可以向
# bgArray 诸葛亮与八卦阵
# QQ 474037765 或最好加入：音·创 开发交流群 861684859
# ------------------------- split line-----------------------------
# Zhuge Liang and Bagua array help to modify the grammar date: -- January 19, 2022
# Statistics: fatal (Level 3) errors: 0; Warning (Level 2) errors: 15; Syntax (Level 1) error: 597
# At present, my Pycham does not display any errors. If there are errors, you can report them to me
# Bgarray Zhuge Liang and Bagua array
# QQ 474037765 or better join: Musicreater development exchange group 861684859
# ------------------------- split line-----------------------------

# 下面为正文


import json
import os
import shutil
import sys
import threading
import pickle
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.simpledialog

from languages.lang import *
from msctspt.threadOpera import NewThread
from nmcsup.vers import VER

__version__ = VER[1] + VER[0]
__author__ = '金羿Eilles & 诸葛亮与八卦阵bgArray'


print('建立变量，存入内存，载入字典常量函数')

# 主体部分

# 支持多文件同时操作

# dataset[{ 'mainset':{ 'x':'y' }, 'musics': [ {  'set' :{ 'A':'B' } , 'note' : [ [ 'a' , b ], ]  }, ] }, ]

# 编辑：
# 修改主设置：   dataset[第几个项目]['mainset']['什么设置'] = '设置啥'
# 修改音乐：    dataset[第几个项目]['musics'][第几个音轨]['notes'][第几个音符][音符还是时间（0，1）] = 改成啥
# 修改音轨设置： dataset[第几个项目]['musics'][第几个音轨]['set']['什么设置'] = '设置啥'
#
# 新增音轨：  dataset[第几个项目]['musics'].append(datasetmodelpart)
#


dataset = [
    {
        'mainset': {
            'ReadMethod': 'old',
            'PackName': 'Ryoun',
            'MusicTitle': 'Noname',
            'IsRepeat': False,
            'PlayerSelect': ''
        },
        'musics': [
            {
                'set': {
                    'EntityName': 'MusicSupport',
                    'ScoreboardName': 'MusicSupport',
                    'Instrument': 'note.harp',
                    'FileName': 'Music'
                },
                'notes': [

                ]
            },
        ],
    },
]
'''一个项目中的全部数据。格式参照：
[
    {
        'mainset':{
            'PackName':'Ryoun',
            'MusicTitle':'Noname',
            'IsRepeat':False,
            'PlayerSelect':''
        },
        'musics':[
            {
                'set':{
                    'EntityName':'music_support',
                    'ScoreboardName':'music_support',
                    'Instrument':'harp',
                    'FileName':'Music'
                },
                'notes':[
                    - Note对象
                    或
                    - [MC音调, 持续时间(s)]
                ]
            },
        ],
    },
]
'''

is_new_file = True
'''这是否是一个新建的项目？'''

is_save = True
'''当前项目是否已保存？'''

ProjectName = ''
'''项目名称，即打开的msct文件名'''

clearLog = False
'''是否在程序结束时移除日志'''

NowMusic = 0
'''当前音轨'''

root = tk.Tk()
'''主窗口'''


def DMM():  # 反回字典用于编辑
    datasetmodelpart = {
        'set': {
            'EntityName': 'MusicSupport',
            'ScoreboardName': 'MusicSupport',
            'Instrument': 'note.harp',
            'FileName': 'Music'
        },
        'notes': []
    }
    return datasetmodelpart


print('完成')


def __main__():
    """音·创 本体\n
    W-YI 金羿\n
    QQ 2647547478\n
    音·创 开发交流群 861684859\n
    Email EillesWan2006@163.com W-YI_DoctorYI@outlook.com\n
    版权所有 Team-Ryoun 金羿\n
    代码根据Apache 2.0 协议开源\n
    若需转载或借鉴 请附作者\n
    """

    print('音·创 正在启动……')

    print('载入日志功能...')
    from nmcsup.log import log
    from nmcsup.log import end
    print('完成！')

    print('更新执行位置...')
    if sys.platform == 'win32':
        try:
            os.chdir(__file__[:len(__file__) - __file__[len(__file__)::-1].index('\\')])
            log('更新执行位置，当前文件位置 {}'.format(__file__))
        except FileNotFoundError:  # 程序规范修改：根据新的语法标准：except后面不能没有错误类型，所以既然是pass就随便填一个错误
            pass
    else:
        try:
            os.chdir(__file__[:len(__file__) - __file__[len(__file__)::-1].index('/')])
        except Exception:
            pass
        log('其他平台：{} 更新执行位置，当前文件位置 {}'.format(sys.platform, __file__))
    print('完成！')

    # 读取文件

    print('载入文件读取函数')

    def ReadFile(fn: str):  # -> list
        from nmcsup.nmcreader import ReadFile as fileRead
        k = fileRead(fn)
        if k is False:
            tk.messagebox.showerror(title=READABLETEXT[0], message=READABLETEXT[105].format(fn))
            return
        else:
            return k

    # 老的列表读取
    def ReadMidi(midfile: str):  # -> str
        from nmcsup.nmcreader import ReadMidi as midiRead
        k = midiRead(midfile)
        if k is False:
            tk.messagebox.showerror(title=READABLETEXT[0], message=READABLETEXT[105].format(midfile))
            return
        else:
            return k

    # 音色读取
    def LoadMidi(midfile: str):  # -> str
        from bgArrayLib.reader import midiNewReader
        k = midiNewReader(midfile)
        if k is False:
            tk.messagebox.showerror(title=READABLETEXT[0], message=READABLETEXT[105].format(midfile))
            return
        else:
            return k

    # 新的类读取
    def MidiAnalysisClass(midfile: str):
        from bgArrayLib.reader import midiClassReader
        k = midiClassReader(midfile)
        if k is False:
            tk.messagebox.showerror(title=READABLETEXT[0], message=READABLETEXT[105].format(midfile))
            return
        else:
            return k

    print('完成！')

    # 菜单命令
    print('加载菜单命令...')

    def exitapp():
        global is_save
        if is_save is not True:
            if tkinter.messagebox.askyesno(title=READABLETEXT[1], message=READABLETEXT[106]):
                SaveProject()
        log('程序正常退出')

        if os.path.isfile("1.pkl"):
            os.remove("1.pkl")

        try:
            global dataset
            del dataset
            global root
            root.destroy()
            del root
        except tkinter.TclError:
            pass

        if clearLog:
            print(READABLETEXT[2])
            # err = True
            # try:
            end()
            if os.path.exists('./log/'):
                shutil.rmtree('./log/')
            if os.path.exists('./logs/'):
                shutil.rmtree('./logs/')
            if os.path.exists('./cache/'):
                shutil.rmtree('./cache/')
            if os.path.exists('./nmcsup/log/'):
                shutil.rmtree('./nmcsup/log/')
            if os.path.exists('./nmcsup/logs/'):
                shutil.rmtree('./nmcsup/logs/')
            # err = False
            # except:
            #     print(READABLETEXT[3])
            #
            # finally:
            # if err is True:
            # print(READABLETEXT[3])

        exit()

    print('退出命令加载完成！')

    def SaveProject():
        global is_save
        if is_new_file:
            # 新的项目相等于另存为
            SaveAsProject()
            return
        else:
            if dataset[0].get('mainset').get('ReadMethod') == "old":
                # 旧项目旧存着吧
                log('存储已有文件：{}'.format(ProjectName))
                with open(ProjectName, 'w', encoding='utf-8') as f:
                    json.dump(dataset[0], f)
                tkinter.messagebox.showinfo(title=READABLETEXT[4], message=READABLETEXT[107].format(ProjectName))
                is_save = True
            elif dataset[0].get('mainset').get('ReadMethod') == "class":  # 这部分相当SaveClassProject()函数
                # if is_new_file:
                #     # 新的项目相等于另存为
                #     SaveAsClassProject()
                #     return
                # else:
                with open(ProjectName, 'wb') as f:
                    pickle.dump(dataset, f)
                    tkinter.messagebox.showinfo(title=READABLETEXT[4],
                                                message=READABLETEXT[107].format(ProjectName))
                    is_save = True
                # return
            elif dataset[0].get('mainset').get('ReadMethod') == "new":  # 这部分相当于SaveNewProject()函数
                # if is_new_file:  # 这部分相当于SaveAsNewProject()函数
                #     # 新的项目相等于另存为
                #     SaveAsNewProject()
                #     return
                # else:
                save_list = [dataset]
                try:
                    with open("1.pkl", 'rb') as r:
                        save_list.append(pickle.load(r))
                except FileNotFoundError:
                    pass
                with open(ProjectName, 'wb') as f:
                    pickle.dump(save_list, f)
                    tkinter.messagebox.showinfo(title=READABLETEXT[4],
                                                message=READABLETEXT[107].format(ProjectName))
                    is_save = True
                return

    print('保存项目命令加载完成！')

    def SaveAsProject():
        global is_save
        if dataset[0].get('mainset').get('ReadMethod') == "old":
            # 另存为项目
            fn = tkinter.filedialog.asksaveasfilename(title=READABLETEXT[5], initialdir=r'./',
                                                      filetypes=[(READABLETEXT[108][0], '.msct'),
                                                                 (READABLETEXT[109], '*')],
                                                      defaultextension='Noname.msct')
            if fn is None or fn == '':
                return
            try:
                Project_Name = fn
                with open(Project_Name, 'w', encoding='utf-8') as f:
                    json.dump(dataset[0], f)
                tkinter.messagebox.showinfo(title=READABLETEXT[4], message=READABLETEXT[107].format(Project_Name))
                is_save = True
            except TypeError:
                Project_Name = fn
                with open(Project_Name, 'wb') as f:
                    pickle.dump(dataset[0], f)
                tkinter.messagebox.showinfo(title=READABLETEXT[4], message=READABLETEXT[107].format(Project_Name))
                is_save = True
        elif dataset[0].get('mainset').get('ReadMethod') == "class":  # 等于SaveAsNewProject()函数
            fn = tkinter.filedialog.asksaveasfilename(title=READABLETEXT[5], initialdir=r'./',
                                                      filetypes=[(READABLETEXT[108][1], '.msctn'),
                                                                 (READABLETEXT[109], '*')],
                                                      defaultextension='Noname.msctn')
            if fn is None or fn == '':
                return
            Project_Name = fn
            with open(Project_Name, 'wb') as f:
                pickle.dump(dataset, f)
            tkinter.messagebox.showinfo(title=READABLETEXT[4], message=READABLETEXT[107].format(Project_Name))

            is_save = True
        elif dataset[0].get('mainset').get('ReadMethod') == "new":  # 等于SaveAsClassProject()函数
            fn = tkinter.filedialog.asksaveasfilename(title=READABLETEXT[5], initialdir=r'./',
                                                      filetypes=[(READABLETEXT[108][2], '.msctx'),
                                                                 (READABLETEXT[109], '*')],
                                                      defaultextension='Noname.msctx')
            if fn is None or fn == '':
                return
            Project_Name = fn
            save_list = [dataset]
            try:
                with open("1.pkl", 'rb') as r:
                    save_list.append(pickle.load(r))
            except FileNotFoundError:
                pass
            print(save_list)
            with open(Project_Name, 'wb') as f:
                pickle.dump(save_list, f)
            tkinter.messagebox.showinfo(title=READABLETEXT[4], message=READABLETEXT[107].format(Project_Name))
            is_save = True

    print('另存项目命令加载完成！')

    def openOldProject():
        global is_save
        if is_save is not True:
            result = tkinter.messagebox.askyesno(title=READABLETEXT[1], message=READABLETEXT[106])
            if result:
                SaveProject()
        fn = tkinter.filedialog.askopenfilename(title=READABLETEXT[6], initialdir=r'./',
                                                filetypes=[(READABLETEXT[110], '.ry.nfc'),
                                                           (READABLETEXT[111], '.ry.mfm'), (READABLETEXT[112], '*')],
                                                multiple=True)
        if fn is None or fn == '':
            return
        else:
            fn = fn[0]
        from nmcsup.nmcreader import ReadOldProject
        dataset[0] = ReadOldProject(fn)

    def openProject():
        global is_save
        global dataset
        if is_save is not True:
            result = tkinter.messagebox.askyesno(title=READABLETEXT[1], message=READABLETEXT[106])
            if result:
                SaveProject()
        fn = tkinter.filedialog.askopenfilename(title=READABLETEXT[7], initialdir=r'./',
                                                filetypes=[(READABLETEXT[108][0], '.msct'),
                                                           (READABLETEXT[108][1], '.msctn'),  # msctn: 音创新文件（用类方法解析）
                                                           (READABLETEXT[108][2], '.msctx'),  # msctx: 音创测试文件（用来支持多乐器解析）
                                                           (READABLETEXT[112], '*')],
                                                multiple=True)
        if fn is None or fn == '':
            return
        else:
            fn = fn[0]
        log("尝试打开：" + fn)
        if str(fn)[str(fn).rfind("."):] == ".msct":  # str(fn)[str(fn).rfind("."):] ->文件格式返回".xxx"
            try:
                try:
                    with open(fn, 'r', encoding='UTF-8') as C:
                        dataset[0] = json.load(C)
                    log("读取工程文件成功")
                except UnicodeDecodeError:
                    print(READABLETEXT[8].format(fn))
                    log('无法打开{}'.format(fn))
                    return
            except json.decoder.JSONDecodeError:  # 程序规范修改：根据新的语法标准：except后面不能没有错误类型，测试后改为：
                # json.decoder.JSONDecodeError
                print(READABLETEXT[8].format(fn))
                log('无法打开{}'.format(fn))
                return
        elif str(fn)[str(fn).rfind("."):] == ".msctx":
            try:
                try:
                    with open(fn, 'rb') as C:
                        # print(pickle.load(C))
                        read = pickle.load(C)  # 重要的事情说三遍！！！pickle.load只能load一次，所以多load几次就有bug，要一次读完！
                        # 重要的事情说三遍！！！pickle.load只能load一次，所以多load几次就有bug，要一次读完！
                        # 重要的事情说三遍！！！pickle.load只能load一次，所以多load几次就有bug，要一次读完！
                        # print(read)
                        dataset = read[0]
                        pkl1 = read[1]
                        log(f"读取新文件成功:\n{str(dataset[0])}")
                    with open("1.pkl", 'wb') as w:
                        pickle.dump(pkl1, w)
                except KeyError:
                    with open(fn, 'rb') as C:
                        dataset[0] = pickle.load(C)
                    log(f"读取新文件成功:\n{str(dataset[0])}")
            except pickle.UnpicklingError:  # 程序规范修改：根据新的语法标准：except后面不能没有错误类型，测试后改为：
                # pickle.UnpicklingError
                print(READABLETEXT[8].format(fn))
                log('无法打开{}'.format(fn))
                return
        elif str(fn)[str(fn).rfind("."):] == ".msctn":
            try:
                try:
                    with open(fn, 'rb') as C:
                        # print(pickle.load(C))
                        read = pickle.load(C)  # 重要的事情说三遍！！！pickle.load只能load一次，所以多load几次就有bug，要一次读完！
                        # 重要的事情说三遍！！！pickle.load只能load一次，所以多load几次就有bug，要一次读完！
                        # 重要的事情说三遍！！！pickle.load只能load一次，所以多load几次就有bug，要一次读完！
                        # print(read)
                        dataset = read
                        log("读取新文件成功")
                except KeyError:
                    with open(fn, 'rb') as C:
                        dataset[0] = pickle.load(C)
                    log("读取新文件成功")
            except pickle.UnpicklingError:  # 程序规范修改：根据新的语法标准：except后面不能没有错误类型，测试后改为：
                # pickle.UnpicklingError
                print(READABLETEXT[8].format(fn))
                log('无法打开{}'.format(fn))
                return
        else:
            return
        global is_new_file
        global ProjectName
        is_new_file = False
        ProjectName = fn
        del fn
        global NowMusic
        RefreshMain()
        RefreshMusic(NowMusic)

    print('打开项目命令加载完成！')

    def appabout():
        aabw = tk.Tk()
        aabw.title(READABLETEXT[9])
        aabw.geometry('550x600')  # 像素
        tk.Label(aabw, text='', font=('', 15)).pack()
        tk.Label(aabw, text=READABLETEXT[10], font=('', 35)).pack()
        tk.Label(aabw, text=READABLETEXT[11].format(VER[1] + VER[0]), font=('', 15)).pack()
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
            tk.Label(aabw, text=i[0], font=('', 17 if i[1] else 15, 'bold' if i[1] else '')).pack()
        tk.Label(aabw, text='', font=('', 5)).pack()
        if DEFAULTLANGUAGE != 'zh-CN':
            tk.Label(aabw, text=READABLETEXT[16], font=('', 15)).pack()
            for i in READABLETEXT['Translator']:
                tk.Label(aabw, text=i[0], font=('', 17 if i[1] else 15, 'bold' if i[1] else '')).pack()

        def exitAboutWindow():
            aabw.destroy()

        tk.Button(aabw, text=READABLETEXT[13], command=exitAboutWindow).pack()

        aabw.mainloop()

    print('关于命令加载完成！')

    def apphelp():
        def funcHelp():
            funTK = tk.Tk()
            funTK.title("函数功能查询")
            funTK.geometry('1200x1000')
            thingLabel = tk.Label(funTK, text="函数功能查询", font=('', 20))
            thingLabel.pack()
            aLabel = tk.Label(funTK, text="""文件：\n  
            打开音·创项目...: 打开三种类型的音创文件(.msct, .msctn, .msctx)\n
            打开旧项目...: 打开两种类型的音创文件(.ry.nfc, .ry.mfm)\n
            保存项目: 自动选择保存类型，并保存为音创文件(.msct, .msctn, .msctx)\n
            另存为...: 自动选择另存为类型，并保存为音创文件(.msct, .msctn, .msctx)\n
            退出  : 退出程序\n\n
            编辑：\n
            从midi导入音轨: 以旧方法(列表方法)解析midi，如果你使用这个方法解析，意味着你选择.msct文件\n
            从midi导入音轨且用新方法解析: 以新方法(类方法)解析midi，并解析乐器信息，如果你使用这个方法解析，意味着你选择.msctx文件\n
                注意！！！这个功能暂时只用于支持雪莹乐器资源包，如果你不是为了这个，最好别用！\n
            从midi导入音轨且用类方法解析: 以类方法解析midi，如果你使用这个方法解析，意味着你选择.msctn文件\n
                注意！！！这个功能暂时在开发中！！！别用！\n
            """, font=('宋体', 12))
            aLabel.pack()

        ahpw = tk.Tk()
        ahpw.title(READABLETEXT[19])
        ahpw.geometry('400x600')  # 像素
        tk.Label(ahpw, text="帮助", font=('楷体', 32)).grid(row=0, column=2)
        tk.Button(ahpw, text="函数功能查询", command=funcHelp, font=('楷体', 20)).grid(row=1, column=1)
        ahpw.mainloop()

    print('帮助命令加载完成！')

    def FromMP3():
        log('从MP3导入音乐')
        mp3file = tkinter.filedialog.askopenfilename(title=READABLETEXT[20], initialdir=r'./',
                                                     filetypes=[(READABLETEXT[113], '.mp3 .m4a'),
                                                                (READABLETEXT[112], '*')], multiple=True)
        if mp3file is None or mp3file == '':
            log('取消')
            return
        else:
            mp3file = mp3file[0]
        from nmcsup.nmcreader import ReadMidi
        from nmcsup.trans import Mp32Mid
        if not os.path.exists('./Temp/'):
            os.makedirs('./Temp/')
        Mp32Mid(mp3file, './Temp/Trans.mid')
        log('打开midi文件./Temp/Trans.mid')
        th = NewThread(ReadMidi, ('./Temp/Trans.mid',))
        th.start()
        del mp3file

        def midiSPT(th_):
            for i in th_.getResult():
                datas = DMM()
                datas['notes'] = i
                dataset[0]['musics'].append(datas)
            del th_
            global is_save
            is_save = False
            global NowMusic
            RefreshMain()
            RefreshMusic(NowMusic)

        threading.Thread(target=midiSPT, args=(th,)).start()
        del th

    print('读MP3加载完成')

    def FromListMidi():
        log('从midi导入音乐')
        midfile = tkinter.filedialog.askopenfilename(title=READABLETEXT[21], initialdir=r'./',
                                                     filetypes=[(READABLETEXT[114], '.mid .midi'),
                                                                (READABLETEXT[112], '*')], multiple=True)
        if midfile is None or midfile == '':
            log('取消')
            return
        else:
            midfile = midfile[0]
        th = NewThread(ReadMidi, (midfile,))
        th.start()
        del midfile

        def midiSPT(th_):
            try:
                try:
                    for i in th_.getResult():
                        datas = DMM()
                        datas['notes'] = i
                        dataset[0]['musics'].append(datas)
                    del th_
                    global is_save
                    is_save = False
                    global NowMusic
                    RefreshMain()
                    RefreshMusic(NowMusic)
                except OSError:
                    tkinter.messagebox.showerror(READABLETEXT[0], READABLETEXT[167])
            except AttributeError:
                try:
                    tkinter.messagebox.showerror(READABLETEXT[0], READABLETEXT[167])
                except OSError:
                    tkinter.messagebox.showerror(READABLETEXT[0], READABLETEXT[167])

        threading.Thread(target=midiSPT, args=(th,)).start()
        del th

    def FromNewMidi():
        log('从midi导入音乐并采用新读取方式')
        midfile = tkinter.filedialog.askopenfilename(title=READABLETEXT[21], initialdir=r'./',
                                                     filetypes=[(READABLETEXT[114], '.mid .midi'),
                                                                (READABLETEXT[112], '*')], multiple=True)
        if midfile is None or midfile == '':
            log('取消')
            return
        else:
            midfile = midfile[0]
        th = NewThread(LoadMidi, (midfile,))
        th.start()
        del midfile

        def midiSPT(th_):
            try:
                try:
                    for i in th_.getResult():
                        datas = DMM()
                        datas['notes'] = i
                        dataset[0]['musics'].append(datas)
                    del th_
                    global is_save
                    is_save = False
                    global NowMusic
                    RefreshMain()
                    RefreshMusic(NowMusic)
                except OSError:
                    tkinter.messagebox.showerror(READABLETEXT[0], READABLETEXT[167])
            except AttributeError:
                try:
                    tkinter.messagebox.showerror(READABLETEXT[0], READABLETEXT[167])
                except OSError:
                    tkinter.messagebox.showerror(READABLETEXT[0], READABLETEXT[167])

        threading.Thread(target=midiSPT, args=(th,)).start()
        del th
        dataset[0]['mainset']['ReadMethod'] = "new"

    def FromClassMidi():
        log('从midi导入音乐并采用类读取方式')
        midfile = tkinter.filedialog.askopenfilename(title=READABLETEXT[21], initialdir=r'./',
                                                     filetypes=[(READABLETEXT[114], '.mid .midi'),
                                                                (READABLETEXT[112], '*')], multiple=True)
        if midfile is None or midfile == '':
            log('取消')
            return
        else:
            midfile = midfile[0]
        th = NewThread(MidiAnalysisClass, (midfile,))
        th.start()
        del midfile

        def midiSPT(th_):
            for i in th_.getResult():
                datas = DMM()
                datas['notes'] = i
                dataset[0]['musics'].append(datas)
            del th_
            global is_save
            is_save = False
            global NowMusic
            RefreshMain()
            RefreshMusic(NowMusic)
        threading.Thread(target=midiSPT, args=(th,)).start()
        del th
        dataset[0]['mainset']['ReadMethod'] = "class"

    print('读midi命令加载完成！')

    def FromForm():
        log('从文本读入音轨')
        fn = tkinter.filedialog.askopenfilename(title=READABLETEXT[22], initialdir=r'./',
                                                filetypes=[(READABLETEXT[115], '.txt'), (READABLETEXT[112], '*')],
                                                multiple=True)
        if fn is None or fn == '':
            log('取消')
            return
        else:
            fn = fn[0]
        th = NewThread(ReadFile, (fn,))
        th.start()

        def midiSPT(th_):
            for i in th_.getResult():
                datas = DMM()
                datas['notes'] = i
                dataset[0]['musics'].append(datas)
            del th_
            global is_save
            is_save = False
            global NowMusic
            RefreshMain()
            RefreshMusic(NowMusic)

        threading.Thread(target=midiSPT, args=(th,)).start()

    print('读txt命令加载完成！')

    def FromText():
        log('写入音符至音轨')
        dat = tkinter.simpledialog.askstring(title=READABLETEXT[23], prompt=READABLETEXT[14], initialvalue='`1 .2 C')
        if dat is None:
            return
        datas = []
        for i in dat.split(' '):
            datas.append([str(i), 1.0])
        log(READABLETEXT[24].format(str(datas)))
        from nmcsup.trans import note2list
        datat = DMM()
        datat['notes'] = note2list(datas)
        dataset[0]['musics'].append(datat)
        del datas, datat, dat
        global is_save
        is_save = False
        global NowMusic
        RefreshMain()
        RefreshMusic(NowMusic)

    print('写入命令加载完成！')
    print('开始加载列表生成函数函数。')

    def ShowCMD():
        log('展示指令')
        global NowMusic
        from nmcsup.trans import Note2Cmd
        RefreshCMDList(
            Note2Cmd(dataset[0]['musics'][NowMusic]['notes'], dataset[0]['musics'][NowMusic]['set']['ScoreboardName'],
                     dataset[0]['musics'][NowMusic]['set']['Instrument'], dataset[0]['mainset']['PlayerSelect']))

    def MakeCMD():
        log('生成文件')
        from msctspt.funcOpera import makeFuncFiles
        file = tkinter.filedialog.askdirectory(title=READABLETEXT[25], initialdir=r'./')
        if file is None or file == '':
            log('取消')
            return
        else:
            makeFuncFiles(dataset[0], file + '/')

    def MakeCMDdir():
        log('生成函数包')
        from msctspt.funcOpera import makeFunDir
        file = tkinter.filedialog.askdirectory(title=READABLETEXT[26], initialdir=r'./')
        if file is None or file == '':
            log('取消')
            return
        else:
            makeFunDir(dataset[0], file + '/')

    def MakePackFile():
        file = tkinter.filedialog.askdirectory(title=READABLETEXT[27], initialdir=r'./')
        if file is None or file == '':
            log('取消')
            return
        import zipfile

        from msctspt.funcOpera import makeFunDir
        log('生成附加包文件')
        if not os.path.exists('./temp/'):
            os.makedirs('./temp/')
        makeFunDir(dataset[0], './temp/')

        shutil.move('./temp/{}Pack/behavior_packs/{}/functions'.format(dataset[0]['mainset']['PackName'],
                                                                       dataset[0]['mainset']['PackName']), './')

        shutil.move('./temp/{}Pack/behavior_packs/{}/manifest.json'.format(dataset[0]['mainset']['PackName'],
                                                                           dataset[0]['mainset']['PackName']), './')

        with zipfile.ZipFile('{}/{}.mcpack'.format(file, dataset[0]['mainset']['PackName']), 'w') as zipobj:
            for i in os.listdir('./functions/'):
                zipobj.write('./functions/{}'.format(i))
            zipobj.write('./manifest.json')
        shutil.move('./functions', './temp/')
        shutil.move('./manifest.json', './temp/')
        shutil.rmtree('./temp/')

    print('完成加载列表生成函数函数。')
    print('开始加载乐器类生成函数函数。')

    def MakeNewCMD():
        log('生成新文件')
        from msctspt.funcOpera import makeNewFuncFiles
        file = tkinter.filedialog.askdirectory(title=READABLETEXT[25], initialdir=r'./')
        if file is None or file == '':
            log('取消')
            return
        else:
            makeNewFuncFiles(dataset[0], file + '/')

    def MakeNewCMDdir():
        log('生成新函数包与材质包')
        from msctspt.funcOpera import makeNewFunDir
        file = tkinter.filedialog.askdirectory(title=READABLETEXT[26], initialdir=r'./')
        if file is None or file == '':
            log('取消')
            return
        else:
            makeNewFunDir(dataset[0], file + '/')

    def MakeNewFunctionPackFile():
        file = tkinter.filedialog.askdirectory(title=READABLETEXT[27], initialdir=r'./')
        if file is None or file == '':
            log('取消')
            return
        import zipfile

        from msctspt.funcOpera import makeNewFunDir
        log('生成附加包文件')
        if not os.path.exists('./temp/'):
            os.makedirs('./temp/')
        makeNewFunDir(dataset[0], './temp/')

        shutil.move('./temp/{}Pack/behavior_packs/{}/functions'.format(dataset[0]['mainset']['PackName'],
                                                                       dataset[0]['mainset']['PackName']), './')

        shutil.move('./temp/{}Pack/behavior_packs/{}/manifest.json'.format(dataset[0]['mainset']['PackName'],
                                                                           dataset[0]['mainset']['PackName']), './')

        with zipfile.ZipFile('{}/{}.mcpack'.format(file, dataset[0]['mainset']['PackName']), 'w') as zipobj:
            for i in os.listdir('./functions/'):
                zipobj.write('./functions/{}'.format(i))
            zipobj.write('./manifest.json')
        shutil.move('./functions', './temp/')
        shutil.move('./manifest.json', './temp/')
        shutil.rmtree('./temp/')

    def MakeNewFunctionPack_ResourcesPacks_File():  # 这个是直接复制资源包（散包）
        file = tkinter.filedialog.askdirectory(title=READABLETEXT[27], initialdir=r'./')
        if file is None or file == '':
            log('取消')
            return
        from bgArrayLib.sy_resourcesPacker import resources_pathSetting
        result = resources_pathSetting()
        print(result)
        if result[0] is False:
            if result[1] == 1:
                tkinter.messagebox.showerror(title=READABLETEXT[0], message=READABLETEXT[157])
            if result[1] == 2:
                tkinter.messagebox.showerror(title=READABLETEXT[0], message=READABLETEXT[158])
            return
        else:
            import zipfile

            from msctspt.funcOpera import makeNewFunDir
            log('生成附加包文件')
            if not os.path.exists('./temp/'):
                os.makedirs('./temp/')
            makeNewFunDir(dataset[0], './temp/')

            shutil.move('./temp/{}Pack/behavior_packs/{}/functions'.format(dataset[0]['mainset']['PackName'],
                                                                           dataset[0]['mainset']['PackName']), './')

            shutil.move('./temp/{}Pack/behavior_packs/{}/manifest.json'.format(dataset[0]['mainset']['PackName'],
                                                                               dataset[0]['mainset']['PackName']), './')

            with zipfile.ZipFile('{}/{}.mcpack'.format(file, dataset[0]['mainset']['PackName']), 'w') as zipobj:
                for i in os.listdir('./functions/'):
                    zipobj.write('./functions/{}'.format(i))
                zipobj.write('./manifest.json')
            shutil.move('./functions', './temp/')
            shutil.move('./manifest.json', './temp/')
            shutil.rmtree('./temp/')
            from bgArrayLib.sy_resourcesPacker import scatteredPack
            scatteredPack(file)

    print('完成加载乐器类生成函数函数。')
    print('开始加载乐器音色资源绑定函数。')

    def changeResourcesPath():
        file = tkinter.filedialog.askdirectory(title=READABLETEXT[27], initialdir=r'./')
        if file is None or file == '':
            log('取消')
            return
        from bgArrayLib.sy_resourcesPacker import resources_pathSetting
        result = resources_pathSetting(file)
        print(result)
        if result[0] is False:
            if result[1] == 1:
                tkinter.messagebox.showerror(title=READABLETEXT[0], message=READABLETEXT[157])
            if result[1] == 2:
                tkinter.messagebox.showerror(title=READABLETEXT[0], message=READABLETEXT[158])
        else:
            tkinter.messagebox.showinfo(title=READABLETEXT[1], message=READABLETEXT[159])

    print('开始加载类生成函数函数。')

    def MakeClassCMD():
        log('生成类文件')
        from msctspt.funcOpera import makeClassFuncFiles
        file = tkinter.filedialog.askdirectory(title=READABLETEXT[25], initialdir=r'./')
        if file is None or file == '':
            log('取消')
            return
        else:
            makeClassFuncFiles(dataset[0], file + '/')

    def MakeClassCMDdir():
        log('生成类函数包与材质包')
        from msctspt.funcOpera import makeClassFunDir
        file = tkinter.filedialog.askdirectory(title=READABLETEXT[26], initialdir=r'./')
        if file is None or file == '':
            log('取消')
            return
        else:
            makeClassFunDir(dataset[0], file + '/')

    def MakeClassFunctionPackFile():
        file = tkinter.filedialog.askdirectory(title=READABLETEXT[27], initialdir=r'./')
        if file is None or file == '':
            log('取消')
            return
        import zipfile

        from msctspt.funcOpera import makeClassFunDir
        log('生成附加包文件')
        if not os.path.exists('./temp/'):
            os.makedirs('./temp/')
        makeClassFunDir(dataset[0], './temp/')

        shutil.move('./temp/{}Pack/behavior_packs/{}/functions'.format(dataset[0]['mainset']['PackName'],
                                                                       dataset[0]['mainset']['PackName']), './')

        shutil.move('./temp/{}Pack/behavior_packs/{}/manifest.json'.format(dataset[0]['mainset']['PackName'],
                                                                           dataset[0]['mainset']['PackName']), './')

        with zipfile.ZipFile('{}/{}.mcpack'.format(file, dataset[0]['mainset']['PackName']), 'w') as zipobj:
            for i in os.listdir('./functions/'):
                zipobj.write('./functions/{}'.format(i))
            zipobj.write('./manifest.json')
        shutil.move('./functions', './temp/')
        shutil.move('./manifest.json', './temp/')
        shutil.rmtree('./temp/')

    print('完成加载类生成函数函数。')
    print('开始加载地图函数。')

    # 转为空方块世界
    def ToBlockWorldEpt():
        import zipfile
        global dire

        from nmcsup.trans import Cmd2World, Datas2BlkWorld, Notes2Player
        while True:
            try:
                dire = tkinter.simpledialog.askstring(title=READABLETEXT[28], prompt=READABLETEXT[116],
                                                      initialvalue='16 4 16')
                if dire is None or dire == '':
                    return
                dire = [int(dire.split(' ')[0]), int(dire.split(' ')[1]), int(dire.split(' ')[2])]
            except ValueError:  # 测试完为ValueError，故修改语法
                tkinter.messagebox.showerror(title=READABLETEXT[0], message=READABLETEXT[117])
                continue
            break
        Outdire = tkinter.filedialog.askdirectory(title=READABLETEXT[29], initialdir=r'./')
        if Outdire is None or Outdire == '':
            log('取消')
            return
        else:
            Outdire = '{}/{}/'.format(Outdire[0], dataset[0]['mainset']['PackName'])
        with zipfile.ZipFile('./nmcsup/EptWorld.zip') as zipobj:  # , 'r' （参数等于默认时不写）
            zipobj.extractall(Outdire)
        NoteData = []
        for i in dataset[0]['musics']:
            NoteData.append(i['notes'])
        Datas2BlkWorld(NoteData, Outdire, dire)
        del NoteData
        for i in range(len(dataset[0]['musics'])):
            Cmd2World(Notes2Player(dataset[0]['musics'][i]['notes'], [dire[0], dire[1], dire[2] + i],
                                   {'Ent': dataset[0]['musics'][i]['set']['EntityName'],
                                    'Pls': dataset[0]['mainset']['PlayerSelect'],
                                    'Ins': dataset[0]['musics'][i]['set']['Instrument']}), Outdire,
                      [dire[0] - 5 - i, dire[1], dire[2]])
        del dire, Outdire

    # 转为已存在的方块世界
    def ToBlockWorld():
        from nmcsup.trans import Cmd2World, Datas2BlkWorld, Notes2Player
        global dire
        while True:
            try:
                dire = tkinter.simpledialog.askstring(title=READABLETEXT[28], prompt=READABLETEXT[116],
                                                      initialvalue='16 4 16')
                if dire is None or dire == '':
                    return
                dire = [int(dire.split(' ')[0]), int(dire.split(' ')[1]), int(dire.split(' ')[2])]
            except ValueError:  # 测试完为ValueError，故修改语法
                tkinter.messagebox.showerror(title=READABLETEXT[0], message=READABLETEXT[117])
                continue
            break
        Outdire = tkinter.filedialog.askdirectory(title=READABLETEXT[29], initialdir=r'./')
        if Outdire is None or Outdire == '':
            log('取消')
            return
        else:
            Outdire += '/'
        NoteData = []
        for i in dataset[0]['musics']:
            NoteData.append(i['notes'])
        Datas2BlkWorld(NoteData, Outdire, dire)
        del NoteData
        for i in range(len(dataset[0]['musics'])):
            Cmd2World(Notes2Player(dataset[0]['musics'][i]['notes'], [dire[0], dire[1], dire[2] + i],
                                   {'Ent': dataset[0]['musics'][i]['set']['EntityName'],
                                    'Pls': dataset[0]['mainset']['PlayerSelect'],
                                    'Ins': dataset[0]['musics'][i]['set']['Instrument']}), Outdire,
                      [dire[0] - 5 - i, dire[1], dire[2]])
        del dire, Outdire

    # 生成函数播放器
    def MakeFuncPlayer():
        global dire
        while True:
            try:
                dire = tkinter.simpledialog.askstring(title=READABLETEXT[28], prompt=READABLETEXT[116],
                                                      initialvalue='16 4 16')
                if dire is None or dire == '':
                    return
                dire = [int(dire.split(' ')[0]), int(dire.split(' ')[1]), int(dire.split(' ')[2])]
            except ValueError:  # 测试完为ValueError，故修改语法
                tkinter.messagebox.showerror(title=READABLETEXT[0], message=READABLETEXT[117])
                continue
            break
        Outdire = tkinter.filedialog.askdirectory(title=READABLETEXT[30], initialdir=r'./')
        if Outdire is None or Outdire == '':
            return
        else:
            Outdire = '{}/{}/'.format(Outdire, dataset[0]['mainset']['PackName'])
        from nmcsup.trans import Notes2Player
        for i in range(len(dataset[0]['musics'])):
            open(Outdire + dataset[0]['musics'][i]['set']['FileName'] + '_' + str(i) + '.mcfunction', 'w',
                 encoding='utf-8').writelines(
                Notes2Player(dataset[0]['musics'][i]['notes'], [dire[0], dire[1], dire[2] + i],
                             {'Ent': dataset[0]['musics'][i]['set']['EntityName'],
                              'Pls': dataset[0]['mainset']['PlayerSelect'],
                              'Ins': dataset[0]['musics'][i]['set']['Instrument']}))

    # 转为空指令世界
    def ToCmdWorldEpt():
        import zipfile
        global dire

        from nmcsup.trans import Cmd2World, Note2Cmd
        while True:
            try:
                dire = tkinter.simpledialog.askstring(title=READABLETEXT[28], prompt=READABLETEXT[116],
                                                      initialvalue='16 4 16')
                if dire is None or dire == '':
                    return
                dire = [int(dire.split(' ')[0]), int(dire.split(' ')[1]), int(dire.split(' ')[2])]
            except ValueError:  # 测试完为ValueError，故修改语法
                tkinter.messagebox.showerror(title=READABLETEXT[0], message=READABLETEXT[117])
                continue
            break
        Outdire = tkinter.filedialog.askdirectory(title=READABLETEXT[29], initialdir=r'./')
        if Outdire is None or Outdire == '':
            return
        else:
            Outdire += '/' + dataset[0]['mainset']['PackName'] + '/'
        with zipfile.ZipFile('./nmcsup/EptWorld.zip') as zipobj:  # , 'r' （默认参数不用设置）
            zipobj.extractall(Outdire)
        for i in range(len(dataset[0]['musics'])):
            Cmd2World(Note2Cmd(dataset[0]['musics'][i]['notes'], dataset[0]['musics'][i]['set']['ScoreboardName'],
                               dataset[0]['musics'][i]['set']['Instrument'], dataset[0]['mainset']['PlayerSelect'],
                               True), Outdire, [dire[0], dire[1], dire[2] + i])
        del dire, Outdire

    # 转为已存在的指令世界
    def ToCmdWorld():
        global dire
        from nmcsup.trans import Cmd2World, Note2Cmd
        while True:
            try:
                dire = tkinter.simpledialog.askstring(title=READABLETEXT[28], prompt=READABLETEXT[116],
                                                      initialvalue='16 4 16')
                if dire is None or dire == '':
                    return
                dire = [int(dire.split(' ')[0]), int(dire.split(' ')[1]), int(dire.split(' ')[2])]
            except ValueError:  # 测试完为ValueError，故修改语法
                tkinter.messagebox.showerror(title=READABLETEXT[0], message=READABLETEXT[117])
                continue
            break
        Outdire = tkinter.filedialog.askdirectory(title=READABLETEXT[29], initialdir=r'./')
        if Outdire is None or Outdire == '':
            return
        else:
            Outdire += '/'
        for i in range(len(dataset[0]['musics'])):
            Cmd2World(Note2Cmd(dataset[0]['musics'][i]['notes'], dataset[0]['musics'][i]['set']['ScoreboardName'],
                               dataset[0]['musics'][i]['set']['Instrument'], dataset[0]['mainset']['PlayerSelect'],
                               True), Outdire, [dire[0], dire[1], dire[2] + i])
        del dire, Outdire

    # 函数输入指令块
    def func2World():
        from nmcsup.trans import Cmd2World
        global dire
        while True:
            try:
                dire = tkinter.simpledialog.askstring(title=READABLETEXT[28], prompt=READABLETEXT[116],
                                                      initialvalue='16 4 16')
                if dire is None or dire == '':
                    return
                dire = [int(dire.split(' ')[0]), int(dire.split(' ')[1]), int(dire.split(' ')[2])]
            except ValueError:  # 测试完为ValueError，故修改语法
                tkinter.messagebox.showerror(title=READABLETEXT[0], message=READABLETEXT[117])
                continue
            break
        Outdire = tkinter.filedialog.askdirectory(title=READABLETEXT[29], initialdir=r'./')
        if Outdire is None or Outdire == '':
            return
        else:
            Outdire += '/'
        Cmd2World(open(tkinter.filedialog.askopenfilename(title=READABLETEXT[31], initialdir=r'./',
                                                          filetypes=[(READABLETEXT[118], '.mcfunction'),
                                                                     (READABLETEXT[112], '*')], multiple=True)[0], 'r',
                       encoding='utf-8').readlines(), Outdire, dire)

    # 大函数分割并载入执行链
    def bigFunc2World():
        log('分割大函数')
        global dire
        import uuid

        from msctspt.funcOpera import funSplit
        from msctspt.transfer import hans2pinyin
        from nmcsup.trans import Cmd2World
        while True:
            try:
                dire = tkinter.simpledialog.askstring(title=READABLETEXT[28], prompt=READABLETEXT[119],
                                                      initialvalue='16 4 16')
                if dire is None or dire == '':
                    return
                dire = [int(dire.split(' ')[0]), int(dire.split(' ')[1]), int(dire.split(' ')[2])]
            except ValueError:  # 测试完为ValueError，故修改语法
                tkinter.messagebox.showerror(title=READABLETEXT[0], message=READABLETEXT[117])
                continue
            break
        Outdire = tkinter.filedialog.askdirectory(title=READABLETEXT[29], initialdir=r'./')
        if Outdire is None or Outdire == '':
            log('取消')
            return
        else:
            Outdire += '/'
        log('获得地图地址：' + Outdire)
        fileName = tkinter.filedialog.askopenfilename(title=READABLETEXT[31], initialdir=r'./',
                                                      filetypes=[(READABLETEXT[118], '.mcfunction'),
                                                                 (READABLETEXT[112], '*')], multiple=True)
        if fileName is None or fileName == '':
            log('取消')
            return
        else:
            fileName = fileName[0]
        log('获得文件名：' + fileName)
        bigFile = open(fileName, 'r', encoding='utf-8')
        parts = funSplit(bigFile)
        if parts == -1:
            tkinter.messagebox.showerror(title=READABLETEXT[0], message=READABLETEXT[121])
            return
        log('创建函数文件夹')
        packName = fileName[len(fileName) - fileName[::-1].index('/'):fileName.index('.')]
        packDire = hans2pinyin(packName)
        try:
            os.makedirs(Outdire + 'behavior_packs/' + packDire + '/functions/')
        except FileExistsError:
            log('已存在文件夹')
        log('创建manifest.json以及world_behavior_packs.json')
        behaviorUuid = uuid.uuid4()
        if os.path.exists(Outdire + 'world_behavior_packs.json'):
            with open(Outdire + 'world_behavior_packs.json', 'r') as f:
                have = json.load(f)
            have.append({'pack_id': str(behaviorUuid), 'version': [0, 0, 1]})
            with open(Outdire + 'world_behavior_packs.json', 'w', encoding='utf-8') as f:
                json.dump(have, f)
            del have
        else:
            with open(Outdire + 'world_behavior_packs.json', 'w', encoding='utf-8') as f:
                f.write('[\n  {\'pack_id\': \'' + str(behaviorUuid) + '\',\n  \'version\': [ 0, 0, 1 ]}\n]')
        with open(Outdire + 'behavior_packs/' + packDire + '/manifest.json', 'w') as f:
            f.write(
                '{\n  \'format_version\': 1,\n  \'header\': {\n    \'description\': \'' + packName +
                ' Pack : behavior pack\',\n    \'version\': [ 0, 0, 1 ],\n    \'name\': \'' + packName +
                'Pack\',\n    \'uuid\': \'' + str(
                    behaviorUuid) + '\'\n  },\n  \'modules\': [\n    {\n      \'description\': \'' + packName +
                ' Pack : behavior pack\',\n      \'type\': '
                '\'data\',\n      \'version\': [ 0, 0, 1 ],\n      \'uuid\': \'' + str(
                    uuid.uuid4()) + '\'\n    }\n  ]\n}')  # 要求文段不能过长
        cmdlist = []
        for i in parts:
            open(Outdire + 'behavior_packs/' + packDire + '/functions/' + packDire + str(
                parts.index(i) + 1) + '.mcfunction', 'w', encoding='utf-8').writelines(i)
            cmdlist.append('function ' + packDire + str(parts.index(i) + 1))
        Cmd2World(cmdlist, Outdire, dire)
        del cmdlist, behaviorUuid, Outdire, fileName, bigFile, parts, dire, packName, packDire

    def toScbBDXfile():
        log('单音轨转BDX')
        from msctspt.transfer import note2bdx
        global dire
        while True:
            try:
                dire = tkinter.simpledialog.askstring(title=READABLETEXT[28], prompt=READABLETEXT[122],
                                                      initialvalue='0 0 0')
                if dire is None or dire == '':
                    return
                dire = [int(dire.split(' ')[0]), int(dire.split(' ')[1]), int(dire.split(' ')[2])]
            except ValueError:  # 测试完为ValueError，故修改语法
                tkinter.messagebox.showerror(title=READABLETEXT[0], message=READABLETEXT[117])
                continue
            break

        fileName = tkinter.filedialog.asksaveasfilename(title=READABLETEXT[32], initialdir=r'./',
                                                        filetypes=[(READABLETEXT[123], '.bdx'),
                                                                   (READABLETEXT[112], '*')],
                                                        defaultextension=dataset[0]['mainset']['PackName'] + '.bdx',
                                                        initialfile=dataset[0]['mainset']['PackName'] + '.bdx')
        if fileName is None or fileName == '':
            log('取消')
            return

        log('获得文件名：' + fileName)

        res = note2bdx(fileName, dire, dataset[0]['musics'][NowMusic]['notes'],
                       dataset[0]['musics'][NowMusic]['set']['ScoreboardName'],
                       dataset[0]['musics'][NowMusic]['set']['Instrument'], dataset[0]['mainset']['PlayerSelect'])
        log('转换结束！\n' + str(res))
        tkinter.messagebox.showinfo(READABLETEXT[33], READABLETEXT[124].format(str(res)))

    def toBDXfile():
        log('整首歌转BDX')
        from msctspt.transfer import music2BDX
        global dire
        while True:
            try:
                dire = tkinter.simpledialog.askstring(title=READABLETEXT[28], prompt=READABLETEXT[122],
                                                      initialvalue='0 0 0')
                if dire is None or dire == '':
                    return
                dire = [int(dire.split(' ')[0]), int(dire.split(' ')[1]), int(dire.split(' ')[2])]
            except ValueError:  # 测试完为ValueError，故修改语法
                tkinter.messagebox.showerror(title=READABLETEXT[0], message=READABLETEXT[117])
                continue
            break

        fileName = tkinter.filedialog.asksaveasfilename(title=READABLETEXT[32], initialdir=r'./',
                                                        filetypes=[(READABLETEXT[123], '.bdx'),
                                                                   (READABLETEXT[112], '*')],
                                                        defaultextension=dataset[0]['mainset']['PackName'] + '.bdx',
                                                        initialfile=dataset[0]['mainset']['PackName'] + '.bdx')

        maxHeight = 200
        print(maxHeight)  # 使用变量

        while True:
            maxHeight = tkinter.simpledialog.askinteger(title=READABLETEXT[28],
                                                        prompt=READABLETEXT[93],
                                                        initialvalue='200')
            if maxHeight >= 5:
                break
            elif maxHeight is None:
                log('取消')
                return
            else:
                tkinter.messagebox.showerror(title=READABLETEXT[0], message=READABLETEXT[94])
                continue

        if fileName is None or fileName == '':
            log('取消')
            return

        log('获得文件名：' + fileName)

        res = music2BDX(fileName, dire, dataset[0], )
        log('转换结束！\n' + str(res))
        tkinter.messagebox.showinfo(READABLETEXT[33], READABLETEXT[124].format(str(res)))

    def wsPlay():
        from msctspt.transfer import note2webs
        spd = tkinter.simpledialog.askfloat(READABLETEXT[34], prompt=READABLETEXT[125], initialvalue='5.0')
        tkinter.messagebox.showinfo(title=READABLETEXT[35], message=READABLETEXT[126])
        note2webs(dataset[0]['musics'][NowMusic]['notes'], dataset[0]['musics'][NowMusic]['set']['Instrument'], spd,
                  dataset[0]['mainset']['PlayerSelect'])

    def toRSworldEPT():
        import zipfile
        global dire
        dire = ""

        from msctspt.transfer import note2RSworld
        while True:
            try:
                dire = tkinter.simpledialog.askstring(title=READABLETEXT[28], prompt=READABLETEXT[116],
                                                      initialvalue='16 4 16')
                if dire is None or dire == '':
                    return
                dire = [int(dire.split(' ')[0]), int(dire.split(' ')[1]), int(dire.split(' ')[2])]
            except ValueError:  # 测试完为ValueError，故修改语法
                tkinter.messagebox.showerror(title=READABLETEXT[0], message=READABLETEXT[117])
                continue
            break
        Outdire = tkinter.filedialog.askdirectory(title=READABLETEXT[29], initialdir=r'./')
        if Outdire is None or Outdire == '':
            return
        else:
            Outdire += '/' + dataset[0]['mainset']['PackName'] + '/'
        with zipfile.ZipFile('./nmcsup/EptWorld.zip') as zipobj:  # , 'r'（默认参数不用写）
            zipobj.extractall(Outdire)
        for i in range(len(dataset[0]['musics'])):
            note2RSworld(Outdire, dire, dataset[0]['musics'][i]['notes'], dataset[0]['musics'][i]['set']['Instrument'])

        del dire, Outdire

    def toRSworld():
        from msctspt.transfer import note2RSworld
        global dire
        dire = ""
        while True:
            try:
                dire = tkinter.simpledialog.askstring(title=READABLETEXT[28], prompt=READABLETEXT[116],
                                                      initialvalue='16 4 16')
                if dire is None or dire == '':
                    return
                dire = [int(dire.split(' ')[0]), int(dire.split(' ')[1]), int(dire.split(' ')[2])]
            except ValueError:  # 测试完为ValueError，故修改语法
                tkinter.messagebox.showerror(title=READABLETEXT[0], message=READABLETEXT[117])
                continue
            break
        Outdire = tkinter.filedialog.askdirectory(title=READABLETEXT[29], initialdir=r'./')
        if Outdire is None or Outdire == '':
            return
        else:
            Outdire += '/'
        for i in range(len(dataset[0]['musics'])):
            note2RSworld(Outdire, dire, dataset[0]['musics'][i]['notes'], dataset[0]['musics'][i]['set']['Instrument'])
        del dire, Outdire

    def world2RyStruct():
        global begp
        global endp
        outdir = tkinter.filedialog.askdirectory(title=READABLETEXT[36], initialdir=r'./')
        if outdir is None or outdir == '':
            return
        else:
            outdir += '/'
        while True:
            try:
                begp = tkinter.simpledialog.askstring(title=READABLETEXT[28], prompt=READABLETEXT[127],
                                                      initialvalue='16 4 16')
                if begp is None or begp == '':
                    return
                begp = [int(begp.split(' ')[0]), int(begp.split(' ')[1]), int(begp.split(' ')[2])]
            except ValueError:  # 测试完为ValueError，故修改语法
                tkinter.messagebox.showerror(title=READABLETEXT[0], message=READABLETEXT[117])
                continue
            break
        while True:
            try:
                endp = tkinter.simpledialog.askstring(title=READABLETEXT[28], prompt=READABLETEXT[128],
                                                      initialvalue='16 4 16')
                if endp is None or endp == '':
                    return
                endp = [int(endp.split(' ')[0]), int(endp.split(' ')[1]), int(endp.split(' ')[2])]
            except ValueError:  # 测试完为ValueError，故修改语法
                tkinter.messagebox.showerror(title=READABLETEXT[0], message=READABLETEXT[117])
                continue
            break
        isAir = tkinter.messagebox.askyesno(READABLETEXT[37], READABLETEXT[129])
        fileName = tkinter.filedialog.asksaveasfilename(title=READABLETEXT[38], initialdir=r'./',
                                                        filetypes=[(READABLETEXT[130], '.RyStruct'),
                                                                   (READABLETEXT[112], '*')],
                                                        defaultextension='*.RyStruct', initialfile='*.RyStruct')
        if fileName is None or fileName == '':
            log('取消')
            return
        from msctspt.transfer import ryStruct
        rys = ryStruct(outdir)
        rys.world2Rys(begp, endp, isAir)
        # error1 = True
        try:
            with open(fileName, 'w', encoding='utf-8') as f:
                json.dump(rys.RyStruct, f, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False)
            tkinter.messagebox.showinfo(READABLETEXT[33], READABLETEXT[131].format(fileName))
            # error1 = False
        except:
            tkinter.messagebox.showerror(READABLETEXT[39], READABLETEXT[132].format(fileName, str(rys.RyStruct)))
            rys.closeLevel()
        # finally:
        # if error1 is True:
        # tkinter.messagebox.showerror(READABLETEXT[39], READABLETEXT[132].format(fileName, str(rys.RyStruct)))
        # rys.closeLevel()

    def world2BDX():
        tkinter.messagebox.showerror(READABLETEXT[0], READABLETEXT[133])

    # 使用邮件反馈bug
    def sendBugReport():
        from msctspt.bugReporter import report
        name = tkinter.simpledialog.askstring(title=READABLETEXT[40], prompt=READABLETEXT[134])
        contact = tkinter.simpledialog.askstring(title=READABLETEXT[40], prompt=READABLETEXT[135])
        describetion = tkinter.simpledialog.askstring(title=READABLETEXT[40], prompt=READABLETEXT[136])
        report(name, contact, describetion).emailReport()
        del name, contact, describetion

    def ClearLog():
        global clearLog
        clearLog = not clearLog
        if clearLog:
            tkinter.messagebox.showinfo(READABLETEXT[33], READABLETEXT[137])
        else:
            tkinter.messagebox.showinfo(READABLETEXT[33], READABLETEXT[138])

    print('生成部分及其余命令加载完成！')

    print('完成！')

    # 窗口部分
    print('增加窗口元素...')
    global root
    global __version__

    root.title(READABLETEXT[41].format(__version__))
    root.geometry('900x900')  # 像素
    try:
        root.iconbitmap(bitmap='./resources/musicreater.ico', default='./resources/musicreater.ico')
    except:
        pass

    print('完成！')

    print('加载点击与页面更新命令...')

    # 音轨菜单被点击

    def MusicList_selected(event):
        global NowMusic
        NowMusic = ListMusicList.get(ListMusicList.curselection())
        log('刷新音轨' + str(NowMusic))
        RefreshMusic(NowMusic)
        print(event)  # 保证变量使用（虽然我不清楚金羿这为啥不调用要写个event）

    # 音符菜单被点击
    def NoteList_selected(event):
        print(event)  # 保证变量使用（虽然我不清楚金羿这为啥不调用要写个event）
        pass  # 编辑音符操作

    def CMDList_selected(event):
        print(event)  # 保证变量使用（虽然我不清楚金羿这为啥不调用要写个event）
        pass  # 命令编辑操作

    CMDList_selected("")  # 保证函数使用
    # ！！！！！上面这行在写完这个函数之后记得删！！！！

    print('菜单点击命令加载完成！')

    # 刷新音轨部分
    def RefreshMusic(Music=0):
        LabelEntityName['text'] = READABLETEXT[42].format(dataset[0]['musics'][Music]['set']['EntityName'])
        LabelScoreboardName['text'] = READABLETEXT[43].format(dataset[0]['musics'][Music]['set']['ScoreboardName'])
        LabelInstrument['text'] = READABLETEXT[44].format(dataset[0]['musics'][Music]['set']['Instrument'])
        LabelFileName['text'] = READABLETEXT[45].format(dataset[0]['musics'][Music]['set']['FileName'])
        NoteList_var.set(())  # 为列表框设置新值
        for i in dataset[0]['musics'][Music]['notes']:
            ListNoteList.insert(tk.END, str(i))

    # 刷新主要部分
    def RefreshMain():
        LabelPackName['text'] = READABLETEXT[46].format(str(dataset[0]['mainset']['PackName']))
        # print(LabelPackName)
        LabelMusicTitle['text'] = READABLETEXT[47].format(str(dataset[0]['mainset']['MusicTitle']))
        LabelIsRepeat['text'] = READABLETEXT[48].format(str(dataset[0]['mainset']['IsRepeat']))
        LabelPlayerSelect['text'] = READABLETEXT[49].format(str(dataset[0]['mainset']['PlayerSelect']))
        MusicList_var.set(())  # 为列表框设置新值
        for i in range(len(dataset[0]['musics'])):
            ListMusicList.insert(tk.END, i)
        global NowMusic
        NowMusic = 0

    def RefreshCMDList(CMDList):
        ListCMDList.delete(tk.END)
        for i in CMDList:
            ListCMDList.insert(tk.END, str(i))

    print('页面刷新函数加载完成！')

    def changePackName(event):
        a = tkinter.simpledialog.askstring(title=READABLETEXT[50], prompt=READABLETEXT[139], initialvalue='Ryoun')
        if a is None:
            return
        dataset[0]['mainset']['PackName'] = a
        del a
        RefreshMain()
        print(event)  # 保证变量使用（虽然我不清楚金羿这为啥不调用要写个event）

    def changeMusicTitle(event):
        a = tkinter.simpledialog.askstring(title=READABLETEXT[50], prompt=READABLETEXT[140], initialvalue='Noname')
        if a is None:
            return
        dataset[0]['mainset']['MusicTitle'] = a
        RefreshMain()
        print(event)  # 保证变量使用（虽然我不清楚金羿这为啥不调用要写个event）

    def changeIsRepeat(event):
        dataset[0]['mainset']['IsRepeat'] = not dataset[0]['mainset']['IsRepeat']
        RefreshMain()
        print(event)  # 保证变量使用（虽然我不清楚金羿这为啥不调用要写个event）

    def changePlayerSelect(event):
        dataset[0]['mainset']['PlayerSelect'] = tkinter.simpledialog.askstring(title=READABLETEXT[50],
                                                                               prompt=READABLETEXT[141],
                                                                               initialvalue='')
        if dataset[0]['mainset']['PlayerSelect'] is None:
            dataset[0]['mainset']['PlayerSelect'] = ''
        RefreshMain()
        print(event)  # 保证变量使用（虽然我不清楚金羿这为啥不调用要写个event）

    def changeEntityName(event):
        global NowMusic
        a = tkinter.simpledialog.askstring(title=READABLETEXT[51], prompt=READABLETEXT[142],
                                           initialvalue='musicSupport')
        if a is None:
            return
        dataset[0]['musics'][NowMusic]['set']['EntityName'] = a
        RefreshMusic(NowMusic)
        print(event)  # 保证变量使用（虽然我不清楚金羿这为啥不调用要写个event）

    def changeScoreboardName(event):
        global NowMusic
        a = tkinter.simpledialog.askstring(title=READABLETEXT[51], prompt=READABLETEXT[143],
                                           initialvalue='musicSupport')
        if a is None:
            return
        dataset[0]['musics'][NowMusic]['set']['ScoreboardName'] = a
        RefreshMusic(NowMusic)
        print(event)  # 保证变量使用（虽然我不清楚金羿这为啥不调用要写个event）

    def changeInstrument(event):
        from nmcsup.const import Instuments as inst
        global NowMusic
        while True:  # 改正：(True)
            instemp = tkinter.simpledialog.askstring(title=READABLETEXT[51], prompt=READABLETEXT[144],
                                                     initialvalue='note.harp')
            if instemp not in inst.keys():  # 改正：not instemp in inst.keys() ，not in 为固定写法
                if tkinter.messagebox.askyesno(title=READABLETEXT[1], message=READABLETEXT[145]):
                    dataset[0]['musics'][NowMusic]['set']['Instrument'] = instemp
                    del instemp
                    break
                else:
                    smsg = READABLETEXT[52]
                    for i, j in inst.items():
                        smsg += i + ' : ' + j + '\n'
                    tkinter.messagebox.showinfo(title=READABLETEXT[1], message=smsg)
                    del smsg
            else:
                dataset[0]['musics'][NowMusic]['set']['Instrument'] = instemp
                del instemp
                break
        RefreshMusic(NowMusic)
        print(event)  # 保证变量使用（虽然我不清楚金羿这为啥不调用要写个event）

    def changeFileName(event):
        global NowMusic
        a = tkinter.simpledialog.askstring(title=READABLETEXT[51], prompt=READABLETEXT[146], initialvalue='Music')
        if a is None:
            return
        dataset[0]['musics'][NowMusic]['set']['FileName'] = a
        RefreshMusic(NowMusic)
        print(event)  # 保证变量使用（虽然我不清楚金羿这为啥不调用要写个event）

    print('标签点击命令加载完成！')

    def ResetSetting():
        global dataset
        dataset[0]['mainset'] = {'PackName': 'Ryoun', 'MusicTitle': 'Noname', 'IsRepeat': False, 'PlayerSelect': ''}
        RefreshMain()

    def DelNowMusic():
        global NowMusic
        del dataset[0]['musics'][NowMusic]
        NowMusic -= 1
        RefreshMain()
        RefreshMusic(NowMusic)

    from nmcsup.vers import resetver

    print('按钮点击命令加载完成！')
    print('完成！')
    print('加载菜单与页面...')

    # 创建一个菜单
    main_menu_bar = tk.Menu(root)

    # 创建文件菜单
    filemenu = tk.Menu(main_menu_bar, tearoff=0)

    filemenu.add_command(label=READABLETEXT[53], command=openProject)
    filemenu.add_command(label=READABLETEXT[54], command=openOldProject)
    filemenu.add_command(label=READABLETEXT[55], command=SaveProject)
    filemenu.add_command(label=READABLETEXT[56], command=SaveAsProject)

    filemenu.add_separator()  # 分隔符

    filemenu.add_command(label=READABLETEXT[57], command=exitapp)

    # 将子菜单加入到菜单条中
    main_menu_bar.add_cascade(label=READABLETEXT[58], menu=filemenu)

    # 创建编辑菜单
    editmenu = tk.Menu(main_menu_bar, tearoff=0)
    editmenu.add_command(label=READABLETEXT[59], command=FromMP3)
    editmenu.add_command(label=READABLETEXT[60], command=FromListMidi)
    editmenu.add_command(label=READABLETEXT[61], command=FromForm)
    editmenu.add_command(label=READABLETEXT[62], command=FromText)
    editmenu.add_separator()
    editmenu.add_command(label=READABLETEXT[160], command=FromClassMidi)
    editmenu.add_command(label=READABLETEXT[148], command=FromNewMidi)
    # 将子菜单加入到菜单条中
    main_menu_bar.add_cascade(label=READABLETEXT[63], menu=editmenu)

    # 创建函数菜单
    funcmenu = tk.Menu(main_menu_bar, tearoff=0)
    funcmenu.add_command(label=READABLETEXT[64], command=MakeCMD)
    funcmenu.add_command(label=READABLETEXT[65], command=MakeCMDdir)
    funcmenu.add_command(label=READABLETEXT[66], command=MakePackFile)
    funcmenu.add_separator()
    funcmenu.add_command(label=READABLETEXT[147], command=MakeNewCMD)
    funcmenu.add_command(label=READABLETEXT[153], command=MakeNewCMDdir)
    funcmenu.add_command(label=READABLETEXT[154], command=MakeNewFunctionPackFile)
    funcmenu.add_command(label=READABLETEXT[155], command=MakeNewFunctionPack_ResourcesPacks_File)
    funcmenu.add_separator()
    funcmenu.add_command(label=READABLETEXT[164], command=MakeClassCMD)
    funcmenu.add_command(label=READABLETEXT[165], command=MakeClassCMDdir)
    funcmenu.add_command(label=READABLETEXT[166], command=MakeClassFunctionPackFile)

    # 将子菜单加入到菜单条中
    main_menu_bar.add_cascade(label=READABLETEXT[67], menu=funcmenu)

    # 创建世界菜单
    worldmenu = tk.Menu(main_menu_bar, tearoff=0)
    worldmenu.add_command(label=READABLETEXT[68], command=ToBlockWorldEpt)
    worldmenu.add_command(label=READABLETEXT[69], command=ToBlockWorld)
    worldmenu.add_separator()
    worldmenu.add_command(label=READABLETEXT[70], command=ToCmdWorldEpt)
    worldmenu.add_command(label=READABLETEXT[71], command=ToCmdWorld)
    worldmenu.add_separator()
    worldmenu.add_command(label=READABLETEXT[72], command=toRSworldEPT)
    worldmenu.add_command(label=READABLETEXT[73], command=toRSworld)
    # 将子菜单加入到菜单条中
    main_menu_bar.add_cascade(label=READABLETEXT[74], menu=worldmenu)

    # 创建结构功能菜单
    structureMenu = tk.Menu(main_menu_bar, tearoff=0)
    structureMenu.add_command(label=READABLETEXT[92], command=toBDXfile)
    structureMenu.add_command(label=READABLETEXT[76], command=toScbBDXfile)
    structureMenu.add_command(label=READABLETEXT[77], command=world2BDX)
    structureMenu.add_separator()
    structureMenu.add_command(label=READABLETEXT[78], command=world2RyStruct)

    main_menu_bar.add_cascade(label=READABLETEXT[95], menu=structureMenu)

    # 创建辅助功能菜单
    otherMenu = tk.Menu(main_menu_bar, tearoff=0)
    otherMenu.add_command(label=READABLETEXT[75], command=MakeFuncPlayer)
    otherMenu.add_separator()
    otherMenu.add_command(label=READABLETEXT[79], command=func2World)
    otherMenu.add_command(label=READABLETEXT[80], command=bigFunc2World)

    main_menu_bar.add_cascade(label=READABLETEXT[81], menu=otherMenu)

    # 创建实验功能菜单
    trymenu = tk.Menu(main_menu_bar, tearoff=0)
    trymenu.add_command(label=READABLETEXT[82], command=ShowCMD)
    trymenu.add_command(label=READABLETEXT[83], command=wsPlay)
    # 将子菜单加入到菜单条中
    main_menu_bar.add_cascade(label=READABLETEXT[84], menu=trymenu)

    # 创建帮助菜单
    helpmenu = tk.Menu(main_menu_bar, tearoff=0)
    helpmenu.add_command(label=READABLETEXT[85], command=ClearLog)
    helpmenu.add_command(label=READABLETEXT[86], command=resetver)
    helpmenu.add_command(label=READABLETEXT[152], command=end)
    helpmenu.add_command(label=READABLETEXT[156], command=changeResourcesPath)

    helpmenu.add_separator()  # 分隔符

    helpmenu.add_command(label=READABLETEXT[87], command=apphelp)
    helpmenu.add_command(label=READABLETEXT[88], command=appabout)
    helpmenu.add_command(label=READABLETEXT[89], command=sendBugReport)
    # 将子菜单加入到菜单条中
    main_menu_bar.add_cascade(label=READABLETEXT[90], menu=helpmenu)

    # 窗口内容

    # 上半部分框
    UpFrame = tk.Frame(root)

    # 左边的框（音乐总设置）
    UpLeftFrame = tk.Frame(UpFrame, bg='white')
    # 大标题
    tk.Label(UpLeftFrame, text=READABLETEXT[91], font=('', 20)).pack()
    # 按钮式文本
    LabelPackName = tk.Label(UpLeftFrame, bg='white',
                             text=READABLETEXT[46].format(str(dataset[0]['mainset']['PackName'])), font=('', 15))
    LabelMusicTitle = tk.Label(UpLeftFrame, bg='white',
                               text=READABLETEXT[47].format(str(dataset[0]['mainset']['MusicTitle'])), font=('', 15))
    LabelIsRepeat = tk.Label(UpLeftFrame, bg='white',
                             text=READABLETEXT[48].format(str(dataset[0]['mainset']['IsRepeat'])), font=('', 15))
    LabelPlayerSelect = tk.Label(UpLeftFrame, bg='white',
                                 text=READABLETEXT[49].format(str(dataset[0]['mainset']['PlayerSelect'])),
                                 font=('', 15))
    # 绑定按钮
    LabelPackName.bind('<Button-1>', changePackName)
    LabelMusicTitle.bind('<Button-1>', changeMusicTitle)
    LabelIsRepeat.bind('<Button-1>', changeIsRepeat)
    LabelPlayerSelect.bind('<Button-1>', changePlayerSelect)
    # 装入容器
    LabelPackName.pack()
    LabelMusicTitle.pack()
    LabelIsRepeat.pack()
    LabelPlayerSelect.pack()
    # 按钮：重置项目设置
    tk.Button(UpLeftFrame, text=READABLETEXT[96], command=ResetSetting).pack()
    # 装入窗口
    UpLeftFrame.pack(side='left')
    
    # 中间的框容器
    UpMidleFrame = tk.Frame(UpFrame, bg='blue')
    # 列表
    MusicList_var = tk.StringVar()
    ListMusicList = tk.Listbox(UpMidleFrame, listvariable=MusicList_var)
    ListMusicList.bind('<ButtonRelease-1>', MusicList_selected)  # 设置选中响应函数
    ListMusicList.pack(side='left')
    # 滑块
    tk.Scrollbar(UpMidleFrame, command=ListMusicList.yview).pack(side='left', fill='y')
    # 装入窗口
    UpMidleFrame.pack(side='left')

    # 右边的框容器
    UpRightFrame = tk.Frame(UpFrame, bg='white')
    # 大标题
    tk.Label(UpRightFrame, text=READABLETEXT[97], font=('', 20)).pack()
    # 按钮式文本
    LabelEntityName = tk.Label(UpRightFrame, bg='white',
                               text=READABLETEXT[42].format(dataset[0]['musics'][NowMusic]['set']['EntityName']),
                               font=('', 15))
    LabelScoreboardName = tk.Label(UpRightFrame, bg='white', text=READABLETEXT[43].format(
        dataset[0]['musics'][NowMusic]['set']['ScoreboardName']), font=('', 15))
    LabelInstrument = tk.Label(UpRightFrame, bg='white',
                               text=READABLETEXT[44].format(dataset[0]['musics'][NowMusic]['set']['Instrument']),
                               font=('', 15))
    LabelFileName = tk.Label(UpRightFrame, bg='white',
                             text=READABLETEXT[45].format(dataset[0]['musics'][NowMusic]['set']['FileName']),
                             font=('', 15))
    # 绑定按钮
    LabelEntityName.bind('<Button-1>', changeEntityName)
    LabelScoreboardName.bind('<Button-1>', changeScoreboardName)
    LabelInstrument.bind('<Button-1>', changeInstrument)
    LabelFileName.bind('<Button-1>', changeFileName)
    # 装入框容器
    LabelEntityName.pack()
    LabelScoreboardName.pack()
    LabelInstrument.pack()
    LabelFileName.pack()
    # 按钮：删除选中音轨
    tk.Button(UpRightFrame, text=READABLETEXT[102], command=DelNowMusic).pack()
    # 装入窗口
    UpRightFrame.pack(side='left')

    # 上半部分框容器装入窗口
    UpFrame.pack()

    # 下半部分框容器
    DownFrame = tk.Frame(root, bg='blue')

    # 经典名言语录
    import random
    texts = open('./resources/myWords.txt', 'r', encoding='utf-8').readlines()
    tk.Label(DownFrame, text=texts[random.randint(0, len(texts) - 1)].replace('\n', '').replace('\\n', '\n'),
             fg='white', bg='black', font=('DengXian Light', 20)).pack(fill='x')
    del texts

    # 音符列表菜单
    NoteList_var = tk.StringVar()
    ListNoteList = tk.Listbox(DownFrame, listvariable=NoteList_var, width=40, height=30)
    ListNoteList.bind('<ButtonRelease-1>', NoteList_selected)  # 设置选中响应函数
    ListNoteList.pack(side='left')
    # 音符列表滑块
    tk.Scrollbar(DownFrame, command=ListNoteList.yview).pack(side='left', fill='y')

    # 指令列表菜单
    ListCMDList = tk.Text(DownFrame, height=37, width=40)
    ListCMDList.pack(side='left')
    # 指令列表滑块
    tk.Scrollbar(DownFrame, command=ListCMDList.yview).pack(fill='y', side='left')

    # 下半部分容器载入窗口
    DownFrame.pack()

    RefreshMain()

    # 将菜单添加到主窗口中
    root.config(menu=main_menu_bar)

    print('完成！')

    log('启动root.mainloop（窗口）')

    if len(sys.argv) != 1:
        log('初始化打开音·创项目' + sys.argv[1])
        global is_save
        is_save = True
        error = True
        try:
            with open(sys.argv[1], 'r', encoding='UTF-8') as c:
                dataset[0] = json.load(c)
                error = False
        except OSError:
            print(READABLETEXT[8].format(sys.argv[1]))
            log('无法打开' + sys.argv[1])
            return
        finally:
            if error is True:
                print(READABLETEXT[8].format(sys.argv[1]))
                log('无法打开' + sys.argv[1])
                return
        global is_new_file
        global ProjectName
        is_new_file = False
        ProjectName = sys.argv[1]
        RefreshMain()
        RefreshMusic(NowMusic)

    # 进入窗口消息循环
    root.mainloop()
    log('退出')
    del filemenu, editmenu, helpmenu, otherMenu

    exitapp()


if __name__ == '__main__':
    __main__()

##################

    # def openNewProject():
    #     global is_save
    #     if is_save is not True:
    #         result = tkinter.messagebox.askyesno(title=READABLETEXT[1], message=READABLETEXT[106])
    #         if result:
    #             SaveProject()
    #     fn = tkinter.filedialog.askopenfilename(title=READABLETEXT[7], initialdir=r'./',
    #                                             filetypes=[(READABLETEXT[108], '.msct'), (READABLETEXT[112], '*')],
    #                                             multiple=True)
    #     if fn is None or fn == '':
    #         return
    #     else:
    #         # print(fn)
    #         fn = fn[0]
    #         # print(fn)
    #     log("尝试打开：" + fn)
    #     try:
    #         try:
    #             with open(fn, 'rb') as C:
    #                 global dataset
    #                 # print(pickle.load(C))
    #                 read = pickle.load(C)  # 重要的事情说三遍！！！pickle.load只能load一次，所以多load几次就有bug，要一次读完！
    #                 # 重要的事情说三遍！！！pickle.load只能load一次，所以多load几次就有bug，要一次读完！
    #                 # 重要的事情说三遍！！！pickle.load只能load一次，所以多load几次就有bug，要一次读完！
    #                 # print(read)
    #                 dataset = read[0]
    #                 pkl1 = read[1]
    #                 log("读取新文件成功")
    #             with open("1.pkl", 'wb') as w:
    #                 pickle.dump(pkl1, w)
    #         except KeyError:
    #             with open(fn, 'rb') as C:
    #                 dataset[0] = pickle.load(C)
    #             log("读取新文件成功")
    #     except pickle.UnpicklingError:  # 程序规范修改：根据新的语法标准：except后面不能没有错误类型，测试后改为：
    #         # pickle.UnpicklingError
    #         print(READABLETEXT[8].format(fn))
    #         log('无法打开{}'.format(fn))
    #         return
    #     global is_new_file
    #     global ProjectName
    #     is_new_file = False
    #     ProjectName = fn
    #     del fn
    #     global NowMusic
    #     RefreshMain()
    #     RefreshMusic(NowMusic)

    # def openClassProject():
    #     global is_save
    #     if is_save is not True:
    #         result = tkinter.messagebox.askyesno(title=READABLETEXT[1], message=READABLETEXT[106])
    #         if result:
    #             SaveProject()
    #     fn = tkinter.filedialog.askopenfilename(title=READABLETEXT[7], initialdir=r'./',
    #                                             filetypes=[(READABLETEXT[108], '.msct'), (READABLETEXT[112], '*')],
    #                                             multiple=True)
    #     if fn is None or fn == '':
    #         return
    #     else:
    #         # print(fn)
    #         fn = fn[0]
    #         # print(fn)
    #     log("尝试打开：" + fn)
    #     try:
    #         try:
    #             with open(fn, 'rb') as C:
    #                 global dataset
    #                 # print(pickle.load(C))
    #                 read = pickle.load(C)  # 重要的事情说三遍！！！pickle.load只能load一次，所以多load几次就有bug，要一次读完！
    #                 # 重要的事情说三遍！！！pickle.load只能load一次，所以多load几次就有bug，要一次读完！
    #                 # 重要的事情说三遍！！！pickle.load只能load一次，所以多load几次就有bug，要一次读完！
    #                 # print(read)
    #                 dataset = read
    #                 log("读取新文件成功")
    #         except KeyError:
    #             with open(fn, 'rb') as C:
    #                 dataset[0] = pickle.load(C)
    #             log("读取新文件成功")
    #     except pickle.UnpicklingError:  # 程序规范修改：根据新的语法标准：except后面不能没有错误类型，测试后改为：
    #         # pickle.UnpicklingError
    #         print(READABLETEXT[8].format(fn))
    #         log('无法打开{}'.format(fn))
    #         return
    #     global is_new_file
    #     global ProjectName
    #     is_new_file = False
    #     ProjectName = fn
    #     del fn
    #     global NowMusic
    #     RefreshMain()
    #     RefreshMusic(NowMusic)


# ------------------
    # filemenu.add_separator()
    #
    # filemenu.add_command(label=READABLETEXT[149], command=openNewProject)
    # filemenu.add_command(label=READABLETEXT[150], command=SaveNewProject)
    # filemenu.add_command(label=READABLETEXT[151], command=SaveAsNewProject)

    # filemenu.add_separator()
    #
    # filemenu.add_command(label=READABLETEXT[161], command=openClassProject)
    # filemenu.add_command(label=READABLETEXT[162], command=SaveClassProject)
    # filemenu.add_command(label=READABLETEXT[163], command=SaveAsClassProject)
