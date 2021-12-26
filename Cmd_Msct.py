# -*- coding: utf-8 -*-


# W-YI 金羿
# QQ 2647547478
# 音·创 开发交流群 861684859
# Email EillesWan2006@163.com W-YI_DoctorYI@outlook.com
# 版权所有 Team-Ryoun 金羿
# 若需转载或借鉴 请附作者


#  代码写的并非十分的漂亮，还请大佬多多包涵；本软件源代码依照Apache软件协议公开


import json
import os
import shutil
import threading
import sys

from msctspt.threadOpera import NewThread
from msctspt.bugReporter import version
from nmcsup.log import log

__version__ = version.version[1]+version.version[0]
__author__ = 'W-YI （金羿）'


log("系统工作————————加载变量及函数")


print("更新执行位置...")

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
print('完成！')


def __main__():

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
    '''
    dataset=[
                {
                    'mainset':{
                        'PackName':"Ryoun",
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
                                'FileName':"Music"
                            },
                            'notes':[
                                [0.0,1.0],
                            ]
                        },
                    ],
                },
            ]
    '''

    global dataset

    dataset = [
        {
            'mainset': {
                'PackName': "Ryoun",
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
                        'FileName': "Music"
                    },
                    'notes': [
                        [0.0, 1.0],
                    ]
                },
            ],
        },
    ]

    global is_new_file
    global is_save
    global ProjectName
    global NowMusic

    is_new_file = True
    is_save = True
    ProjectName = ''
    NowMusic = 0

    def DMM():  # 反回字典用于编辑
        datasetmodelpart = {
            'set': {
                'EntityName': 'MusicSupport',
                'ScoreboardName': 'MusicSupport',
                'Instrument': 'note.harp',
                'FileName': "Music"
            },
            'notes': []
        }
        return datasetmodelpart

    print("完成")

    # 菜单命令
    print('加载菜单命令...')

    def exitapp(cmd):

        log("程序正常退出", False)
        global is_save
        if is_save == False:
            if '/s' in cmd:
                saveProject()
            else:
                print("您尚未保存，请使用 /s 开关保存并退出")
                return

        try:
            global dataset
            del dataset
        except:
            pass

        if '/c' in cmd:
            print("清除log（此句不载入日志）")
            try:
                if os.path.exists("./log/"):
                    shutil.rmtree("./log/")
                if os.path.exists("./logs/"):
                    shutil.rmtree("./logs/")
                if os.path.exists("./cache/"):
                    shutil.rmtree("./cache/")
            except:
                print("无法清除日志及临时文件")

        exit()

    print('退出函数加载完成！')

    print("载入文件读取函数")

    def ReadFile(fn: str) -> list:
        from nmcsup.nmcreader import ReadFile as fileRead
        k = fileRead(fn)
        if k == False:
            log("找不到"+fn)
            return
        else:
            return k

    def ReadMidi(midfile: str) -> str:
        from nmcsup.nmcreader import ReadMidi as midiRead
        k = midiRead(midfile)
        if k == False:
            log("找不到"+midfile)
            return
        else:
            return k

    print('完成！')

    print("载入命令函数")

    def saveProject(cmd: list):
        global is_new_file
        if '/a' in cmd:
            log("另存项目")
            ProjectName = cmd[cmd.index('/a')+1]
        else:
            if is_new_file:
                print("初次存储请使用 /a 开关规定存储文件名")
                log("文件为未保存")
                return

        log("存储文件："+ProjectName)
        with open(ProjectName, 'w', encoding='utf-8') as f:
            json.dump(dataset[0], f)
        global is_save
        is_save = True

    print('保存项目函数加载完成！')

    def loadMusic(cmd: list):
        if '/mid' in cmd:
            th = NewThread(ReadMidi, (cmd[cmd.index('/mid')+1],))
            th.start()

            def midiSPT(th):
                for i in th.getResult():
                    datas = DMM()
                    datas['notes'] = i
                    dataset[0]['musics'].append(datas)
                del th
                global is_save
                is_save = False
            threading.Thread(target=midiSPT, args=(th,)).start()
            del th
        elif '/txt' in cmd:
            th = NewThread(ReadFile, (cmd[cmd.index('/txt')+1],))
            th.start()

            def midiSPT(th):
                for i in th.getResult():
                    datas = DMM()
                    datas['notes'] = i
                    dataset[0]['musics'].append(datas)
                del th
                global is_save
                is_save = False
            threading.Thread(target=midiSPT, args=(th,)).start()
        elif '/input' in cmd:
            datas = []
            for i in cmd[cmd.index('/input')+1:]:
                datas.append([str(i), 1.0])
            from nmcsup.trans import note2list
            datat = DMM()
            datat['notes'] = note2list(datas)
            dataset[0]['musics'].append(datat)
            del datas, datat
            global is_save
            is_save = False

    print('音轨载入函数加载完成！')

    def funBuild(cmd: list):
        if '/file' in cmd:
            from msctspt.funcOpera import makeFuncFiles
            makepath = cmd[cmd.index('/file')+1]
            if makepath[-1] != '/':
                makepath += '/'
            makeFuncFiles(dataset[0], makepath)
        elif '/directory' in cmd:
            from msctspt.funcOpera import makeFunDir
            makepath = cmd[cmd.index('/directory')+1]
            if makepath[-1] != '/':
                makepath += '/'
            makeFunDir(dataset[0], makepath)
        elif '/mcpack' in cmd:
            import zipfile
            from msctspt.funcOpera import makeFunDir
            makepath = cmd[cmd.index('/mcpack')+1]
            if makepath[-1] != '/':
                makepath += '/'

            if not os.path.exists('./temp/'):
                os.makedirs('./temp/')
            makeFunDir(dataset[0], './temp/')
            shutil.move('./temp/'+dataset[0]['mainset']['PackName'] +
                        "Pack/behavior_packs/"+dataset[0]['mainset']['PackName']+"/functions", './')
            shutil.move('./temp/'+dataset[0]['mainset']['PackName'] + "Pack/behavior_packs/" +
                        dataset[0]['mainset']['PackName']+"/manifest.json", './')
            with zipfile.ZipFile(makepath+dataset[0]['mainset']['PackName']+'.mcpack', "w") as zipobj:
                for i in os.listdir('./functions/'):
                    zipobj.write('./functions/'+i)
                zipobj.write('./manifest.json')
            shutil.move('./functions', './temp/')
            shutil.move('./manifest.json', './temp/')
            shutil.rmtree("./temp/")

    print("函数建立函数加载完成")

    if sys.platform == 'win32':
        os.system("cls")
    else:
        os.system("clear")

    if sys.platform in ('win32', 'linux'):
        print("您当前的运行环境为标准桌面，您可以打开 Musicreater.py 运行窗口模式的 音·创")
        print("您也可以输入 win 指令在不退出命令行模式的同时打开窗口模式\n")

    print(__author__+" 音·创 —— 当前核心版本 "+__version__+'\n')

    nowWorkPath = os.path.split(os.path.realpath(__file__))[0]

    while True:

        strcmd = input("MSCT "+nowWorkPath+">")
        cmd = strcmd.lower().split(' ')

        if cmd[0] == 'exit':
            exitapp(cmd[1:])
        elif cmd[0] == 'save':
            saveProject(cmd[1:])
        elif cmd[0] == 'load':
            loadMusic(cmd[1:])
        elif cmd[0] == 'win':
            def run(cmd):
                os.system(cmd)
            if sys.platform == 'win32':
                NewThread(run, ("python "+os.path.split(os.path.realpath(__file__))
                          [0]+"/Musicreater.py",)).start()
            else:
                NewThread(run, ("python3 "+os.path.split(os.path.realpath(__file__))
                          [0]+"/Musicreater.py",)).start()
        elif cmd[0] == 'chdir':
            nowWorkPath = os.path.realpath(cmd[1])
            os.chdir(nowWorkPath)
        elif cmd[0] == 'build':
            funBuild(cmd[1:])
        else:
            os.system(strcmd)


if __name__ == '__main__':
    __main__()
