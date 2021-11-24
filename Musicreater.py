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
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.simpledialog

from msctspt.threadOpera import NewThread
from nmcsup.vers import VER





__version__ = VER[1]+VER[0]
__author__ = 'W-YI （金羿）'





import sys


# if sys.platform != 'win32':
#     print("您当前的运行环境不符合要求。")
#     print(__author__+" 音·创 当前版本"+__version__)
#     print("按下回车退出程序")
#     input()
#     exit()





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


is_new_file = True
is_save = True
ProjectName = ''
clearLog = False;
NowMusic = 0
root = tk.Tk()


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











def __main__():
    '''音·创 本体\n
    W-YI 金羿\n
    QQ 2647547478\n
    音·创 开发交流群 861684859\n
    Email EillesWan2006@163.com W-YI_DoctorYI@outlook.com\n
    版权所有 Team-Ryoun 金羿\n
    若需转载或借鉴 请附作者\n
    '''

    print("音·创 正在启动……")



    print('载入日志功能...')
    from nmcsup.log import log
    print('完成！')



    print("更新执行位置...")
    if sys.platform == 'win32':
        os.chdir(__file__[:len(__file__)-__file__[len(__file__)::-1].index('\\')])
        log("更新执行位置，当前文件位置"+__file__)
    else:
        try:
            os.chdir(__file__[:len(__file__)-__file__[len(__file__)::-1].index('/')])
        except:
            pass
        log("其他平台："+sys.platform+"更新执行位置，当前文件位置"+__file__)
    print('完成！')




    # 读取文件


    print("载入文件读取函数")

    def ReadFile(fn:str) -> list:
        from nmcsup.nmcreader import ReadFile as fileRead
        k = fileRead(fn)
        if k == False :
            tk.messagebox.showerror(title='错误', message="找不到文件😢："+fn)
            return
        else:
            return k


    def ReadMidi(midfile:str) -> str:
        from nmcsup.nmcreader import ReadMidi as midiRead
        k = midiRead(midfile)
        if k == False :
            tk.messagebox.showerror(title='错误', message="找不到文件或无法读取文件😢："+midfile)
            return
        else:
            return k


    print('完成！')




    # 菜单命令
    print('加载菜单命令...');

    def exitapp():
        global is_save
        if is_save != True:
            if tkinter.messagebox.askyesno(title='提示', message='您当前的项目已修改但未存储，是否先保存当前项目？'):
                SaveProject()
        log("程序正常退出")




        try:
            global dataset
            del dataset
            global root
            root.destroy()
            del root
        except:
            pass;



        if clearLog :
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
        

    print('退出命令加载完成！')



    def SaveProject():
        if is_new_file:
            # 新的项目相等于另存为
            SaveAsProject()
            return
        else:
            # 旧项目旧存着吧
            log("存储已有文件："+ProjectName)
            with open(ProjectName, 'w', encoding='utf-8') as f:
                json.dump(dataset[0], f)
            tkinter.messagebox.showinfo(title='已存储', message='项目已经存储至：'+ProjectName)
        global is_save
        is_save = True


    print('保存项目命令加载完成！')


    def SaveAsProject():
        # 另存为项目
        log("另存项目")
        fn = tkinter.filedialog.asksaveasfilename(title='新建 音·创 项目', initialdir=r'./', filetypes=[('音·创工程文件', '.msct'), ('任意类型', '*')], defaultextension='Noname.msct')
        if fn == None or fn =='':
            log("取消")
            return
        ProjectName = fn
        log("新建文件："+ProjectName)
        with open(ProjectName, 'w', encoding='utf-8') as f:
            json.dump(dataset[0], f)
        tkinter.messagebox.showinfo(title='已存储', message='项目已经存储至：'+ProjectName)
        global is_save
        is_save = True


    print('另存项目命令加载完成！')


    def openOldProject():
        log("打开旧版本项目")
        global is_save
        if is_save != True:
            result = tkinter.messagebox.askyesno(title='提示', message='您当前的项目已修改但未存储，是否先保存当前项目？')
            log('询问是否存储:'+str(result))
            if result:
                SaveProject()
        fn = tkinter.filedialog.askopenfilename(title='请选择旧类型的项目', initialdir=r'./', filetypes=[('函数音创工程文件', '.ry.nfc'), ('MMFM0.0.6版本工程文件', '.ry.mfm'), ('全部类型', '*')], multiple=True)
        if fn == None or fn == '':
            log("取消")
            return
        else:
            fn = fn[0]
        log("读取文件："+fn)
        from nmcsup.nmcreader import ReadOldProject
        dataset[0] = ReadOldProject(fn)



    def openProject():
        log("打开音·创项目")
        global is_save
        if is_save != True:
            result = tkinter.messagebox.askyesno(title='提示', message='您当前的项目已修改但未存储，是否先保存当前项目？')
            log('询问是否存储:'+str(result))
            if result:
                SaveProject()
        fn = tkinter.filedialog.askopenfilename(title='请选择 音·创 项目', initialdir=r'./', filetypes=[('音·创工程文件', '.msct'),('全部类型', '*')], multiple=True)
        if fn == None or fn == '':
            log("取消")
            return
        else:
            fn = fn[0]
        log("读取文件："+fn)
        try:
            with open(fn, 'r', encoding='UTF-8') as c:
                dataset[0] = json.load(c)
        except:
            print('无法打开文件：'+fn+"，请查看您是否输入正确")
            log("无法打开"+fn)
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
        aabw.title(u'音·创 - 关于')
        aabw.geometry('400x600')  # 像素
        tk.Label(aabw, text='', font=('', 15)).pack()
        tk.Label(aabw, text='我的世界音·创', font=('', 35)).pack()
        tk.Label(aabw, text='当前版本：'+VER[1]+VER[0], font=('', 15)).pack()
        # pack 的side可以赋值为LEFT  RTGHT  TOP  BOTTOM
        # grid 的row 是列数、column是行排，注意，这是针对空间控件本身大小来的，即是指向当前控件的第几个。
        # place的 x、y是(x,y)坐标
        #pic = tk.PhotoImage(file="./bin/pics/Ryoun_S.png")
        #tk.Label(aabw, image=pic, width=200, height=200).pack()
        #del pic
        tk.Label(aabw, text='', font=('', 5)).pack()
        tk.Label(aabw, text='凌云我的世界开发团队', font=('', 20)).pack()
        tk.Label(aabw, text='×', font=('', 20)).pack()
        tk.Label(aabw, text='凌云软件开发团队', font=('', 20)).pack()
        tk.Label(aabw, text='', font=('', 15)).pack()
        tk.Label(aabw, text='唯一开发者：金羿（W-YI）', font=('', 15)).pack()
        tk.Label(aabw, text='Email: EillesWan@outlook.com', font=('', 15)).pack()
        tk.Label(aabw, text='QQ: 2647547478', font=('', 15)).pack()
        tk.Label(aabw, text='讨论群: 861684859', font=('', 15)).pack()
        
        aabw.mainloop()


    print('关于命令加载完成！')


    def apphelp():
        ahpw = tk.Tk()
        ahpw.title(u'音·创 - 帮助')
        ahpw.geometry('400x600')  # 像素

        ahpw.mainloop()

    print('帮助命令加载完成！')



    def FromMP3():
        log("从MP3导入音乐");
        mp3file = tkinter.filedialog.askopenfilename(title='请选择钢琴声音的 MP3 文件', initialdir=r'./', filetypes=[('钢琴声音的MP3', '.mp3'), ('全部类型', '*')], multiple=True)
        if mp3file == None or mp3file == '':
            log("取消")
            return
        else:
            mp3file = mp3file[0]
        log("转换mp3文件"+mp3file)
        from nmcsup.nmcreader import ReadMidi
        from nmcsup.trans import Mp32Mid
        if not os.path.exists('./Temp/'):
            os.makedirs('./Temp/')
        Mp32Mid(mp3file,'./Temp/Trans.mid')
        log("打开midi文件./Temp/Trans.mid")
        th = NewThread(ReadMidi, ('./Temp/Trans.mid',))
        th.start()
        del mp3file
        def midiSPT(th):
            for i in th.getResult():
                datas = DMM()
                datas['notes'] = i
                dataset[0]['musics'].append(datas)
            del th
            global is_save
            is_save = False
            global NowMusic
            RefreshMain()
            RefreshMusic(NowMusic)
        threading.Thread(target=midiSPT, args=(th,)).start()
        del th

    print("读MP3加载完成")


    def FromMidi():
        log("从midi导入音乐")
        midfile = tkinter.filedialog.askopenfilename(title='请选择 MIDI 文件', initialdir=r'./', filetypes=[('Midi文件', '.mid .midi'), ('全部类型', '*')], multiple=True)
        if midfile == None or midfile == '':
            log("取消")
            return
        else:
            midfile = midfile[0]
        log("开新线程打开midi文件"+midfile)
        th = NewThread(ReadMidi, (midfile,))
        th.start()
        del midfile
        def midiSPT(th):
            for i in th.getResult():
                datas = DMM()
                datas['notes'] = i
                dataset[0]['musics'].append(datas)
            del th
            global is_save
            is_save = False
            global NowMusic
            RefreshMain()
            RefreshMusic(NowMusic)
        threading.Thread(target=midiSPT, args=(th,)).start()
        del th


    print('读midi命令加载完成！')


    def FromForm():
        log("从文本读入音轨")
        fn = tkinter.filedialog.askopenfilename(title='请选择 音符文本 文件', initialdir=r'./', filetypes=[('文本文件', '.txt'), ('全部类型', '*')], multiple=True)
        if fn == None or fn =='':
            log("取消")
            return
        else:
            fn = fn[0]
        log("打开音符文件"+fn)
        th = NewThread(ReadFile, (fn,))
        th.start()
        def midiSPT(th):
            for i in th.getResult():
                datas = DMM()
                datas['notes'] = i
                dataset[0]['musics'].append(datas)
            del th
            global is_save
            is_save = False
            global NowMusic
            RefreshMain()
            RefreshMusic(NowMusic)
        threading.Thread(target=midiSPT, args=(th,)).start()


    print('读txt命令加载完成！')


    def FromText():
        log("写入音符至音轨")
        dat = tkinter.simpledialog.askstring(title='获取信息', prompt='请输入音符：', initialvalue='`1 .2 C')
        if dat == None:
            return
        datas = []
        for i in dat.split(" "):
            datas.append([str(i), 1.0])
        log('音符数据写入'+str(datas))
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



    def ShowCMD():
        log("展示指令")
        global NowMusic
        from nmcsup.trans import Note2Cmd
        RefreshCMDList(Note2Cmd(dataset[0]['musics'][NowMusic]['notes'],dataset[0]['musics'][NowMusic]['set']['ScoreboardName'],dataset[0]['musics'][NowMusic]['set']['Instrument'],dataset[0]['mainset']['PlayerSelect']))


    def MakeCMD():
        log("生成文件")
        from msctspt.funcOpera import makeFuncFiles
        file = tkinter.filedialog.askdirectory(title='请选择文件生成的位置', initialdir=r'./')
        if file == None or file =='':
            log("取消")
            return;
        else:
            makeFuncFiles(dataset[0], file+'/')


    def MakeCMDdir():
        log("生成函数包")
        from msctspt.funcOpera import makeFunDir
        file = tkinter.filedialog.askdirectory(title='请选择文件夹生成的位置', initialdir=r'./')
        if file == None or file =='':
            log("取消")
            return;
        else:
            makeFunDir(dataset[0], file+'/')


    def MakePackFile():
        file = tkinter.filedialog.askdirectory(title='请选择.mcpack文件生成的位置', initialdir=r'./')
        if file == None or file =='':
            log("取消")
            return;
        import zipfile

        from msctspt.funcOpera import makeFunDir
        log("生成附加包文件")
        if not os.path.exists('./temp/'):
            os.makedirs('./temp/')
        makeFunDir(dataset[0], './temp/')
        shutil.move('./temp/'+dataset[0]['mainset']['PackName'] +"Pack/behavior_packs/"+dataset[0]['mainset']['PackName']+"/functions",'./')
        shutil.move('./temp/'+dataset[0]['mainset']['PackName'] +"Pack/behavior_packs/"+dataset[0]['mainset']['PackName']+"/manifest.json",'./')
        with zipfile.ZipFile(file+'/'+dataset[0]['mainset']['PackName']+'.mcpack', "w") as zipobj:
            for i in os.listdir('./functions/'):
                zipobj.write('./functions/'+i)
            zipobj.write('./manifest.json')
        shutil.move('./functions','./temp/')
        shutil.move('./manifest.json','./temp/')
        shutil.rmtree("./temp/")






    #转为空方块世界
    def ToBlockWorldEpt():
        import zipfile

        from nmcsup.trans import Cmd2World, Datas2BlkWorld, Notes2Player
        while True:
            try:
                dire = tkinter.simpledialog.askstring(title = '坐标信息输入',prompt='请输入坐标：',initialvalue = '16 4 16')
                if dire == None or dire == '':
                    return;
                dire = [int(dire.split(' ')[0]), int(dire.split(' ')[1]), int(dire.split(' ')[2])]
            except:
                tkinter.messagebox.showerror(title="错误❌", message="您输入的格式有误，请重新输入！");
                continue
            break
        Outdire = tkinter.filedialog.askdirectory(title='请选择世界文件夹生成的位置', initialdir=r'./');
        if Outdire == None or Outdire == '':
            log("取消")
            return;
        else:
            Outdire = Outdire[0]+'/'+dataset[0]['mainset']['PackName']+'/';
        with zipfile.ZipFile("./nmcsup/EptWorld.zip", "r") as zipobj:
            zipobj.extractall(Outdire)
        NoteData = []
        for i in dataset[0]['musics']:
            NoteData.append(i['notes'])
        Datas2BlkWorld(NoteData,Outdire,dire)
        del NoteData
        for i in range(len(dataset[0]['musics'])):
            Cmd2World(Notes2Player(dataset[0]['musics'][i]['notes'],[dire[0],dire[1],dire[2]+i],{'Ent':dataset[0]['musics'][i]['set']['EntityName'],'Pls':dataset[0]['mainset']['PlayerSelect'],'Ins':dataset[0]['musics'][i]['set']['Instrument']}),Outdire,[dire[0]-5-i,dire[1],dire[2]])
        del dire, Outdire
        



    #转为已存在的方块世界
    def ToBlockWorld():
        from nmcsup.trans import Cmd2World, Datas2BlkWorld, Notes2Player
        while True:
            try:
                dire = tkinter.simpledialog.askstring(title = '坐标信息输入',prompt='请输入坐标：',initialvalue = '16 4 16')
                if dire == None or dire == '':
                    return;
                dire = [int(dire.split(' ')[0]), int(dire.split(' ')[1]), int(dire.split(' ')[2])]
            except:
                tkinter.messagebox.showerror(title="错误❌", message="您输入的格式有误，请重新输入！");
                continue
            break
        Outdire = tkinter.filedialog.askdirectory(title='请选择世界文件夹生成的位置', initialdir=r'./');
        if Outdire == None or Outdire == '':
            log("取消")
            return;
        else:
            Outdire+='/';
        NoteData = []
        for i in dataset[0]['musics']:
            NoteData.append(i['notes'])
        Datas2BlkWorld(NoteData,Outdire,dire)
        del NoteData
        for i in range(len(dataset[0]['musics'])):
            Cmd2World(Notes2Player(dataset[0]['musics'][i]['notes'],[dire[0],dire[1],dire[2]+i],{'Ent':dataset[0]['musics'][i]['set']['EntityName'],'Pls':dataset[0]['mainset']['PlayerSelect'],'Ins':dataset[0]['musics'][i]['set']['Instrument']}),Outdire,[dire[0]-5-i,dire[1],dire[2]])
        del dire, Outdire
        



    #生成函数播放器
    def MakeFuncPlayer():
        while True:
            try:
                dire = tkinter.simpledialog.askstring(title = '坐标信息输入',prompt='请输入坐标：',initialvalue = '16 4 16')
                if dire == None or dire == '':
                    return;
                dire = [int(dire.split(' ')[0]), int(dire.split(' ')[1]), int(dire.split(' ')[2])]
            except:
                tkinter.messagebox.showerror(title="错误❌", message="您输入的格式有误，请重新输入！");
                continue
            break
        Outdire = tkinter.filedialog.askdirectory(title='请选择函数包生成的位置', initialdir=r'./');
        if Outdire == None or Outdire == '':
            return;
        else:
            Outdire+='/'+dataset[0]['mainset']['PackName']+'/';
        from nmcsup.trans import Notes2Player
        for i in range(len(dataset[0]['musics'])):
            open(Outdire+dataset[0]['musics'][i]['set']['FileName']+'_'+str(i)+'.mcfunction','w',encoding='utf-8').writelines(Notes2Player(dataset[0]['musics'][i]['notes'],[dire[0],dire[1],dire[2]+i],{'Ent':dataset[0]['musics'][i]['set']['EntityName'],'Pls':dataset[0]['mainset']['PlayerSelect'],'Ins':dataset[0]['musics'][i]['set']['Instrument']}))
        




    #转为空指令世界
    def ToCmdWorldEpt():
        import zipfile

        from nmcsup.trans import Cmd2World, Note2Cmd
        while True:
            try:
                dire = tkinter.simpledialog.askstring(title = '坐标信息输入',prompt='请输入坐标：',initialvalue = '16 4 16');
                if dire == None or dire == '':
                    return;
                dire = [int(dire.split(' ')[0]), int(dire.split(' ')[1]), int(dire.split(' ')[2])];
            except:
                tkinter.messagebox.showerror(title="错误❌", message="您输入的格式有误，请重新输入！");
                continue;
            break;
        Outdire = tkinter.filedialog.askdirectory(title='请选择世界文件夹生成的位置', initialdir=r'./');
        if Outdire == None or Outdire == '':
            return;
        else:
            Outdire+='/'+dataset[0]['mainset']['PackName']+'/';
        with zipfile.ZipFile("./nmcsup/EptWorld.zip", "r") as zipobj:
            zipobj.extractall(Outdire);
        for i in range(len(dataset[0]['musics'])):
            Cmd2World(Note2Cmd(dataset[0]['musics'][i]['notes'],dataset[0]['musics'][i]['set']['ScoreboardName'],dataset[0]['musics'][i]['set']['Instrument'],dataset[0]['mainset']['PlayerSelect'],True),Outdire,[dire[0],dire[1],dire[2]+i])
        del dire,Outdire;
        


    #转为已存在的指令世界
    def ToCmdWorld():
        from nmcsup.trans import Cmd2World, Note2Cmd
        while True:
            try:
                dire = tkinter.simpledialog.askstring(title = '坐标信息输入',prompt='请输入坐标：',initialvalue = '16 4 16')
                if dire == None or dire == '':
                    return;
                dire = [int(dire.split(' ')[0]), int(dire.split(' ')[1]), int(dire.split(' ')[2])]
            except:
                tkinter.messagebox.showerror(title="错误❌", message="您输入的格式有误，请重新输入！");
                continue
            break
        Outdire = tkinter.filedialog.askdirectory(title='请选择世界文件夹生成的位置', initialdir=r'./');
        if Outdire == None or Outdire == '':
            return;
        else:
            Outdire+='/';
        for i in range(len(dataset[0]['musics'])):
            Cmd2World(Note2Cmd(dataset[0]['musics'][i]['notes'],dataset[0]['musics'][i]['set']['ScoreboardName'],dataset[0]['musics'][i]['set']['Instrument'],dataset[0]['mainset']['PlayerSelect'],True),Outdire,[dire[0],dire[1],dire[2]+i])
        del dire,Outdire;
        




    #函数输入指令块
    def func2World():
        from nmcsup.trans import Cmd2World
        while True:
            try:
                dire = tkinter.simpledialog.askstring(title = '坐标信息输入',prompt='请输入坐标：',initialvalue = '16 4 16')
                if dire == None or dire == '':
                    return;
                dire = [int(dire.split(' ')[0]), int(dire.split(' ')[1]), int(dire.split(' ')[2])]
            except:
                tkinter.messagebox.showerror(title="错误❌", message="您输入的格式有误，请重新输入！");
                continue
            break
        Outdire = tkinter.filedialog.askdirectory(title='请选择世界文件夹生成的位置', initialdir=r'./');
        if Outdire == None or Outdire == '':
            return;
        else:
            Outdire+='/';
        Cmd2World(open(tkinter.filedialog.askopenfilename(title='请选择 .mcfunction 文件', initialdir=r'./', filetypes=[('我的世界指令函数文件', '.mcfunction'), ('全部类型', '*')], multiple=True)[0],'r',encoding='utf-8').readlines(),Outdire,dire)




    #大函数分割并载入执行链
    def bigFunc2World():
        log("分割大函数")
        import uuid

        from msctspt.funcOpera import funSplit
        from msctspt.transfer import hans2pinyin
        from nmcsup.trans import Cmd2World
        while True:
            try:
                dire = tkinter.simpledialog.askstring(title = '坐标信息输入',prompt='请输入执行链生成坐标：',initialvalue = '16 4 16');
                if dire == None or dire == '':
                    return;
                dire = [int(dire.split(' ')[0]), int(dire.split(' ')[1]), int(dire.split(' ')[2])];
            except:
                tkinter.messagebox.showerror(title="错误❌", message="您输入的格式有误，请重新输入。");
                continue
            break
        Outdire = tkinter.filedialog.askdirectory(title='请选择世界文件夹生成的位置', initialdir=r'./');
        if Outdire == None or Outdire == '':
            log("取消")
            return;
        else:
            Outdire+='/';
        log("获得地图地址："+Outdire)
        fileName = tkinter.filedialog.askopenfilename(title='请选择 .mcfunction 文件', initialdir=r'./', filetypes=[('我的世界指令函数文件', '.mcfunction'), ('全部类型', '*')], multiple=True)
        if fileName == None or fileName == '':
            log("取消")
            return;
        else:
            fileName = fileName[0]
        log("获得文件名："+fileName)
        bigFile = open(fileName,'r',encoding='utf-8')
        parts = funSplit(bigFile)
        if parts == -1:
            tkinter.messagebox.showerror(title="错误❌", message="您的函数文件不大于10k条指令，无需进行分割操作。");
            return;
        log("创建函数文件夹")
        packName = fileName[len(fileName)-fileName[::-1].index('/'):fileName.index('.')]
        packDire = hans2pinyin(packName)
        try:
            os.makedirs(Outdire+"behavior_packs/"+packDire+"/functions/");
        except:
            log("已存在文件夹")
        log("创建manifest.json以及world_behavior_packs.json")
        behaviorUuid = uuid.uuid4()
        if os.path.exists(Outdire+"world_behavior_packs.json"):
            with open(Outdire+"world_behavior_packs.json", "r") as f:
                have = json.load(f)
            have.append({"pack_id": str(behaviorUuid), "version": [ 0, 0, 1 ]})
            with open(Outdire+"world_behavior_packs.json", "w",encoding="utf-8") as f:
                json.dump(have,f)
            del have
        else:
            with open(Outdire+"world_behavior_packs.json", "w",encoding="utf-8") as f:
                f.write("[\n  {\"pack_id\": \"" + str(behaviorUuid) +"\",\n  \"version\": [ 0, 0, 1 ]}\n]")
        with open(Outdire+"behavior_packs/"+packDire+"/manifest.json", "w") as f:
            f.write("{\n  \"format_version\": 1,\n  \"header\": {\n    \"description\": \""+packName+" Pack : behavior pack\",\n    \"version\": [ 0, 0, 1 ],\n    \"name\": \""+packName+"Pack\",\n    \"uuid\": \"" + str(behaviorUuid) + "\"\n  },\n  \"modules\": [\n    {\n      \"description\": \""+packName+" Pack : behavior pack\",\n      \"type\": \"data\",\n      \"version\": [ 0, 0, 1 ],\n      \"uuid\": \"" + str(uuid.uuid4()) + "\"\n    }\n  ]\n}")
        cmdlist = []
        for i in parts :
            open(Outdire+"behavior_packs/"+packDire+"/functions/"+packDire+str(parts.index(i)+1)+".mcfunction",'w',encoding='utf-8').writelines(i);
            cmdlist.append("function "+packDire+str(parts.index(i)+1))
        Cmd2World(cmdlist,Outdire,dire)
        del cmdlist,behaviorUuid,Outdire,fileName,bigFile,parts,dire,packName,packDire




    def toScbBDXfile():
        from msctspt.transfer import note2bdx
        while True:
            try:
                dire = tkinter.simpledialog.askstring(title = '坐标信息输入',prompt='请输入执行链生成相对坐标：',initialvalue = '0 0 0');
                if dire == None or dire == '':
                    return;
                dire = [int(dire.split(' ')[0]), int(dire.split(' ')[1]), int(dire.split(' ')[2])];
            except:
                tkinter.messagebox.showerror(title="错误❌", message="您输入的格式有误，请重新输入。");
                continue
            break
        
        fileName = tkinter.filedialog.asksaveasfilename(title='请选择需要生成的.bdx文件', initialdir=r'./', filetypes=[('FastBuilder结构文件', '.bdx'), ('全部类型', '*')], defaultextension=dataset[0]['mainset']['PackName']+'.bdx',initialfile=dataset[0]['mainset']['PackName']+'.bdx')
        if fileName == None or fileName == '':
            log("取消")
            return;
        
        log("获得文件名："+fileName)

        res = note2bdx(fileName,dire,dataset[0]['musics'][NowMusic]['notes'],dataset[0]['musics'][NowMusic]['set']['ScoreboardName'],dataset[0]['musics'][NowMusic]['set']['Instrument'],dataset[0]['mainset']['PlayerSelect'])
        log('转换结束！\n'+str(res))
        tkinter.messagebox.showinfo("生成结果",'转换结束！\n'+str(res))




    def wsPlay():
        from msctspt.transfer import note2webs
        spd = tkinter.simpledialog.askfloat("输入播放速度",prompt='一秒，音乐走几拍？',initialvalue = '5.0')
        tkinter.messagebox.showinfo(title="创建中", message="请在游戏中使用connect指令连接localhost:8080，即可播放");
        note2webs(dataset[0]['musics'][NowMusic]['notes'],dataset[0]['musics'][NowMusic]['set']['Instrument'],spd,dataset[0]['mainset']['PlayerSelect'])





    def toRSworldEPT():
        import zipfile

        from msctspt.transfer import note2RSworld
        while True:
            try:
                dire = tkinter.simpledialog.askstring(title = '坐标信息输入',prompt='请输入坐标：',initialvalue = '16 4 16');
                if dire == None or dire == '':
                    return;
                dire = [int(dire.split(' ')[0]), int(dire.split(' ')[1]), int(dire.split(' ')[2])];
            except:
                tkinter.messagebox.showerror(title="错误❌", message="您输入的格式有误，请重新输入！");
                continue;
            break;
        Outdire = tkinter.filedialog.askdirectory(title='请选择世界文件夹生成的位置', initialdir=r'./');
        if Outdire == None or Outdire == '':
            return;
        else:
            Outdire+='/'+dataset[0]['mainset']['PackName']+'/';
        with zipfile.ZipFile("./nmcsup/EptWorld.zip", "r") as zipobj:
            zipobj.extractall(Outdire);
        for i in range(len(dataset[0]['musics'])):
            note2RSworld(Outdire,dire,dataset[0]['musics'][i]['notes'],dataset[0]['musics'][i]['set']['Instrument'])
            
        del dire,Outdire;



    def toRSworld():
        from msctspt.transfer import note2RSworld
        while True:
            try:
                dire = tkinter.simpledialog.askstring(title = '坐标信息输入',prompt='请输入坐标：',initialvalue = '16 4 16')
                if dire == None or dire == '':
                    return;
                dire = [int(dire.split(' ')[0]), int(dire.split(' ')[1]), int(dire.split(' ')[2])]
            except:
                tkinter.messagebox.showerror(title="错误❌", message="您输入的格式有误，请重新输入！");
                continue
            break
        Outdire = tkinter.filedialog.askdirectory(title='请选择世界文件夹生成的位置', initialdir=r'./');
        if Outdire == None or Outdire == '':
            return;
        else:
            Outdire+='/';
        for i in range(len(dataset[0]['musics'])):
            note2RSworld(Outdire,dire,dataset[0]['musics'][i]['notes'],dataset[0]['musics'][i]['set']['Instrument'])
        del dire,Outdire;




    def world2RyStruct():
        outdir = tkinter.filedialog.askdirectory(title='请选择世界文件夹所在的位置', initialdir=r'./');
        if outdir == None or outdir == '':
            return;
        else:
            outdir+='/';
        while True:
            try:
                begp = tkinter.simpledialog.askstring(title = '坐标信息输入',prompt='请输入区域选择的开始坐标：',initialvalue = '16 4 16')
                if begp == None or begp == '':
                    return;
                begp = [int(begp.split(' ')[0]), int(begp.split(' ')[1]), int(begp.split(' ')[2])]
            except:
                tkinter.messagebox.showerror(title="错误❌", message="您输入的格式有误，请重新输入！");
                continue
            break
        while True:
            try:
                endp = tkinter.simpledialog.askstring(title = '坐标信息输入',prompt='请输入区域选择的结束坐标：',initialvalue = '16 4 16')
                if endp == None or endp == '':
                    return;
                endp = [int(endp.split(' ')[0]), int(endp.split(' ')[1]), int(endp.split(' ')[2])]
            except:
                tkinter.messagebox.showerror(title="错误❌", message="您输入的格式有误，请重新输入！");
                continue
            break
        isAir = tkinter.messagebox.askyesno("请确认","所选区块导出时是否需要保留空气方块？")
        fileName = tkinter.filedialog.asksaveasfilename(title='生成.RyStruct文件', initialdir=r'./', filetypes=[('音·创结构文件', '.RyStruct'), ('全部类型', '*')], defaultextension='*.RyStruct',initialfile='*.RyStruct')
        if fileName == None or fileName == '':
            log("取消")
            return;
        from msctspt.transfer import ryStruct
        rys = ryStruct(outdir)
        rys.world2Rys(begp,endp,isAir)
        try:
            with open(fileName,'w',encoding='utf-8') as f:
                json.dump(rys.RyStruct,f,sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False)
            tkinter.messagebox.showinfo("成功✔",'文件已生成\n'+fileName)
        except:
            tkinter.messagebox.showerror("失败❌",'文件无法生成\n'+fileName+'\n'+str(rys.RyStruct))
            rys.closeLevel()
            


    def world2BDX():
        tkinter.messagebox.showerror("错误",'本功能尚未开发。')














    #使用邮件反馈bug
    def sendBugReport():
        from msctspt.bugReporter import report
        name = tkinter.simpledialog.askstring(title = '邮件反馈信息输入',prompt='您的称呼')
        contact = tkinter.simpledialog.askstring(title = '邮件反馈信息输入',prompt='您的联系方式')
        describetion = tkinter.simpledialog.askstring(title = '邮件反馈信息输入',prompt='您对问题的描述')
        report(name,contact,describetion).emailReport()
        del name,contact,describetion











    def ClearLog():
        global clearLog;
        clearLog = not clearLog;
        if clearLog:
            tkinter.messagebox.showinfo("完成！✔",'在程序结束后将清除日志及临时文件信息。');
        else:
            tkinter.messagebox.showinfo("完成！✔",'在程序结束后将不会清除日志及临时文件信息。');




    print('生成部分及其余命令加载完成！');


    print('完成！');

    # 窗口部分
    print('增加窗口元素...');
    global root

    root.title(u'音·创 - 金羿 - '+VER[1]+VER[0]);
    root.geometry('800x800');  # 像素

    print('完成！')


    print('加载点击与页面更新命令...')

    # 音轨菜单被点击


    def MusicList_selected(event):
        global NowMusic
        NowMusic = ListMusicList.get(ListMusicList.curselection())
        log('刷新音轨'+str(NowMusic))
        RefreshMusic(NowMusic)


    # 音符菜单被点击
    def NoteList_selected(event):
        pass  # 编辑音符操作


    def CMDList_selected(event):
        pass  # 命令编辑操作


    print('菜单点击命令加载完成！')


    # 刷新音轨部分
    def RefreshMusic(Music=0):
        LabelEntityName['text'] = '执行实体名： ' + dataset[0]['musics'][Music]['set']['EntityName']
        LabelScoreboardName['text'] = '使用计分板： ' + dataset[0]['musics'][Music]['set']['ScoreboardName']
        LabelInstrument['text'] = '所用的乐器： ' + dataset[0]['musics'][Music]['set']['Instrument']
        LabelFileName['text'] = '当前音轨名： ' + dataset[0]['musics'][Music]['set']['FileName']
        NoteList_var.set(())  # 为列表框设置新值
        for i in dataset[0]['musics'][Music]['notes']:
            ListNoteList.insert(tk.END, str(i))


    # 刷新主要部分
    def RefreshMain():
        LabelPackName['text'] = '包名： '+str(dataset[0]['mainset']['PackName'])
        LabelMusicTitle['text'] = '音乐标题： '+str(dataset[0]['mainset']['MusicTitle'])
        LabelIsRepeat['text'] = '是否重复： '+str(dataset[0]['mainset']['IsRepeat'])
        LabelPlayerSelect['text'] = '玩家选择器:'+str(dataset[0]['mainset']['PlayerSelect'])
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
        a = tkinter.simpledialog.askstring(title='修改主设置', prompt='修改包名', initialvalue='Ryoun')
        if a == None:
            return
        dataset[0]['mainset']['PackName'] = a
        del a 
        RefreshMain()


    def changeMusicTitle(event):
        a = tkinter.simpledialog.askstring(title='修改主设置', prompt='修改音乐标题', initialvalue='Noname')
        if a == None:
            return
        dataset[0]['mainset']['MusicTitle'] = a 
        RefreshMain()


    def changeIsRepeat(event):
        dataset[0]['mainset']['IsRepeat'] = not dataset[0]['mainset']['IsRepeat']
        RefreshMain()


    def changePlayerSelect(event):
        dataset[0]['mainset']['PlayerSelect'] = tkinter.simpledialog.askstring(title='修改主设置', prompt='修改玩家选择器\n注意！要加上中括号[]', initialvalue='')
        if dataset[0]['mainset']['PlayerSelect'] == None:
            dataset[0]['mainset']['PlayerSelect'] = ''
        RefreshMain()


    def changeEntityName(event):
        global NowMusic
        a = tkinter.simpledialog.askstring(title='修改节设置', prompt='修改本音轨的执行实体名：', initialvalue='musicSupport')
        if a == None:
            return
        dataset[0]['musics'][NowMusic]['set']['EntityName'] = a 
        RefreshMusic(NowMusic)


    def changeScoreboardName(event):
        global NowMusic
        a = tkinter.simpledialog.askstring(title='修改节设置', prompt='修改本音轨所用的积分板：', initialvalue='musicSupport')
        if a == None:
            return
        dataset[0]['musics'][NowMusic]['set']['ScoreboardName'] = a 
        RefreshMusic(NowMusic)


    def changeInstrument(event):
        from nmcsup.const import Instuments as inst
        global NowMusic
        while(True):
            instemp = tkinter.simpledialog.askstring(title='修改节设置', prompt='修改本音轨所用乐器：', initialvalue='note.harp')
            if not instemp in inst.keys():
                if tkinter.messagebox.askyesno(title='注意', message='您输入的乐器并非游戏内置乐器，是否继续用您输入的字符作为乐器？'):
                    dataset[0]['musics'][NowMusic]['set']['Instrument'] = instemp
                    del instemp
                    break
                else:
                    smsg = '游戏内置乐器如下：请输入英文\n'
                    for i, j in inst.items():
                        smsg += i+' : '+j+'\n'
                    tkinter.messagebox.showinfo(title='提示', message=smsg)
                    del smsg
            else:
                dataset[0]['musics'][NowMusic]['set']['Instrument'] = instemp
                del instemp
                break
        RefreshMusic(NowMusic)


    def changeFileName(event):
        global NowMusic
        a = tkinter.simpledialog.askstring(title='修改节设置', prompt='修改本音轨生成的文件名：', initialvalue='Music')
        if a == None:
            return
        dataset[0]['musics'][NowMusic]['set']['FileName'] = a
        RefreshMusic(NowMusic)


    print('标签点击命令加载完成！')


    def ResetSetting():
        global dataset
        dataset[0]['mainset'] = {'PackName': "Ryoun",'MusicTitle': 'Noname','IsRepeat': False,'PlayerSelect': ''}
        RefreshMain()


    def DelNowMusic():
        global NowMusic
        del dataset[0]['musics'][NowMusic]
        NowMusic -= 1
        RefreshMain()
        RefreshMusic(NowMusic)


    print('按钮点击命令加载完成！')

    print('完成！')


    print('加载菜单与页面...')

    # 创建一个菜单
    main_menu_bar = tk.Menu(root)


    # 创建文件菜单
    filemenu = tk.Menu(main_menu_bar, tearoff=0)

    filemenu.add_command(label=u"打开音·创项目...", command=openProject)
    filemenu.add_command(label=u"打开旧项目...", command=openOldProject)
    filemenu.add_command(label=u"保存项目", command=SaveProject)
    filemenu.add_command(label=u"另存为...", command=SaveAsProject)

    filemenu.add_separator()  # 分隔符

    filemenu.add_command(label=u"退出", command=exitapp)

    # 将子菜单加入到菜单条中
    main_menu_bar.add_cascade(label=u"文件", menu=filemenu)


    # 创建编辑菜单
    editmenu = tk.Menu(main_menu_bar, tearoff=0)
    editmenu.add_command(label=u"从钢琴MP3导入音轨", command=FromMP3)
    editmenu.add_command(label=u"从midi导入音轨", command=FromMidi)
    editmenu.add_command(label=u"从文本文件导入音轨", command=FromForm)
    editmenu.add_command(label=u"输入音符至音轨", command=FromText)
    # 将子菜单加入到菜单条中
    main_menu_bar.add_cascade(label=u"编辑", menu=editmenu)



    #创建函数菜单
    funcmenu = tk.Menu(main_menu_bar, tearoff=0)
    funcmenu.add_command(label=u"生成文件至...", command=MakeCMD)
    funcmenu.add_command(label=u"生成函数包至...", command=MakeCMDdir)
    funcmenu.add_command(label=u"生成附加包文件至...", command=MakePackFile)
    # 将子菜单加入到菜单条中
    main_menu_bar.add_cascade(label=u"函数(包)", menu=funcmenu)




    #创建世界菜单
    worldmenu = tk.Menu(main_menu_bar, tearoff=0);
    worldmenu.add_command(label=u"将音乐以方块存储生成地图", command=ToBlockWorldEpt);
    worldmenu.add_command(label=u"将音乐以方块存储载入地图…", command=ToBlockWorld);
    worldmenu.add_separator()
    worldmenu.add_command(label=u"将音乐以指令存储生成地图", command=ToCmdWorldEpt);
    worldmenu.add_command(label=u"将音乐以指令存储载入地图…", command=ToCmdWorld);
    worldmenu.add_separator()
    worldmenu.add_command(label=u"将音乐以音符盒存储生成地图", command=toRSworldEPT);
    worldmenu.add_command(label=u"将音乐以音符盒存储载入地图…", command=toRSworld);
    # 将子菜单加入到菜单条中
    main_menu_bar.add_cascade(label=u"世界", menu=worldmenu);


    # 创建其他功能菜单
    otherMenu = tk.Menu(main_menu_bar, tearoff=0)
    otherMenu.add_command(label=u"生成符合当前音乐的函数播放器…", command=MakeFuncPlayer)
    otherMenu.add_separator();
    otherMenu.add_command(label=u"将选中音轨以指令存储生成.bdx文件…", command=toScbBDXfile)
    otherMenu.add_command(label=u"由地图导出至.bdx文件…", command=world2BDX)
    otherMenu.add_command(label=u"由地图导出至.RyStruct文件…", command=world2RyStruct)
    otherMenu.add_separator();
    otherMenu.add_command(label=u"将函数载入世界…", command=func2World);
    otherMenu.add_command(label=u"将大函数分割并建立执行链…", command=bigFunc2World);

    main_menu_bar.add_cascade(label=u"辅助功能", menu=otherMenu);


    # 创建实验功能菜单
    trymenu = tk.Menu(main_menu_bar, tearoff=0)
    trymenu.add_command(label=u"展示生成结果", command=ShowCMD)
    trymenu.add_command(label=u"建立位于localhost:8080上的websocket服务器播放选中音轨", command=wsPlay)
    # 将子菜单加入到菜单条中
    main_menu_bar.add_cascade(label=u"实验功能", menu=trymenu)





    from nmcsup.vers import resetver

    # 创建帮助菜单
    helpmenu = tk.Menu(main_menu_bar, tearoff=0)
    helpmenu.add_command(label=u"清除临时文件", command=ClearLog)
    helpmenu.add_command(label=u"清除存在文件", command=resetver)

    helpmenu.add_separator()  # 分隔符

    helpmenu.add_command(label=u"帮助", command=apphelp)
    helpmenu.add_command(label=u"关于", command=appabout)
    helpmenu.add_command(label=u"发送错误日志反馈",command=sendBugReport)
    # 将子菜单加入到菜单条中
    main_menu_bar.add_cascade(label=u"帮助与疑问", menu=helpmenu)


    # 窗口内容

    UpFrame = tk.Frame(root)


    UpLeftFrame = tk.Frame(UpFrame, bg='white')

    # 文本
    tk.Label(UpLeftFrame, text='音乐总设置(项目设置)', font=('', 20)).pack()

    LabelPackName = tk.Label(UpLeftFrame, bg='white', text='地图/函数包名： ', font=('', 15))
    LabelMusicTitle = tk.Label(UpLeftFrame, bg='white',text='音乐标题： ', font=('', 15))
    LabelIsRepeat = tk.Label(UpLeftFrame, bg='white', text='是否重复： ', font=('', 15))
    LabelPlayerSelect = tk.Label(UpLeftFrame, bg='white', text='玩家选择器:', font=('', 15))

    LabelPackName.bind("<Button-1>", changePackName)
    LabelMusicTitle.bind("<Button-1>", changeMusicTitle)
    LabelIsRepeat.bind("<Button-1>", changeIsRepeat)
    LabelPlayerSelect.bind("<Button-1>", changePlayerSelect)

    LabelPackName.pack()
    LabelMusicTitle.pack()
    LabelIsRepeat.pack()
    LabelPlayerSelect.pack()

    # 按钮：重置项目设置
    tk.Button(UpLeftFrame, text='重置项目设置', command=ResetSetting).pack()


    UpLeftFrame.pack(side=tk.LEFT)


    UpMidleFrame = tk.Frame(UpFrame, bg='blue')

    MusicList_var = tk.StringVar()
    ListMusicList = tk.Listbox(UpMidleFrame, listvariable=MusicList_var)

    ListMusicList.bind('<ButtonRelease-1>', MusicList_selected)  # 设置选中响应函数

    ListMusicList.pack()


    UpMidleFrame.pack(side=tk.LEFT)


    UpRightFrame = tk.Frame(UpFrame, bg='white')


    tk.Label(UpRightFrame, text='当前音轨设置(段落设置)', font=('', 20)).pack()

    LabelEntityName = tk.Label(UpRightFrame, bg='white',text='执行实体名： ', font=('', 15))
    LabelScoreboardName = tk.Label(UpRightFrame, bg='white', text='使用计分板： ', font=('', 15))
    LabelInstrument = tk.Label(UpRightFrame, bg='white',text='所用的乐器： ', font=('', 15))
    LabelFileName = tk.Label(UpRightFrame, bg='white',text='当前音轨名： ', font=('', 15))


    LabelEntityName.bind("<Button-1>", changeEntityName)
    LabelScoreboardName.bind("<Button-1>", changeScoreboardName)
    LabelInstrument.bind("<Button-1>", changeInstrument)
    LabelFileName.bind("<Button-1>", changeFileName)


    LabelEntityName.pack()
    LabelScoreboardName.pack()
    LabelInstrument.pack()
    LabelFileName.pack()

    # 按钮：删除选中音轨
    tk.Button(UpRightFrame, text='删除选中音轨', command=DelNowMusic).pack()


    UpRightFrame.pack(side=tk.LEFT)


    UpFrame.pack()


    DownFrame = tk.Frame(root, bg='blue')


    # 音符列表菜单
    NoteList_var = tk.StringVar()
    ListNoteList = tk.Listbox(DownFrame, listvariable=NoteList_var, width=40, height=30)

    ListNoteList.bind('<ButtonRelease-1>', NoteList_selected)  # 设置选中响应函数

    ListNoteList.pack(side=tk.LEFT)


    # 指令列表菜单
    ListCMDList = tk.Text(DownFrame)

    ListCMDList.pack(side=tk.RIGHT)

    DownFrame.pack()


    RefreshMain()


    # 将菜单添加到主窗口中
    root.config(menu=main_menu_bar)

    print('完成！')


    log("启动root.mainloop（窗口）")


    if len(sys.argv) != 1:
        log("初始化打开音·创项目"+sys.argv[1])
        global is_save
        is_save = True
        try:
            with open(sys.argv[1], 'r', encoding='UTF-8') as c:
                dataset[0] = json.load(c)
        except:
            print('无法打开文件：'+sys.argv[1]+"，请查看您是否输入正确")
            log("无法打开"+sys.argv[1])
            return
        global is_new_file
        global ProjectName
        is_new_file = False
        ProjectName = sys.argv[1]
        global NowMusic
        RefreshMain()
        RefreshMusic(NowMusic)


    # 进入窗口消息循环
    root.mainloop()
    log("退出")
    del filemenu, editmenu, helpmenu, otherMenu

    exitapp()


if __name__ == '__main__':
    __main__();


