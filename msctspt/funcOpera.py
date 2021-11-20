# -*- coding: utf-8 -*-
"""音·创 的函数操作和一些其他功能"""


from nmcsup.log import log



def delPart(Data,starter,ender,includeStart :bool= True,includend :bool= True):
    '''删除序列从starter物件到ender物件之间的部分\n
    includeStart与inclodend分别控制此函数是否包括starter和ender物件所在部分，默认为真\n
    starter与ender若为None则默认从首或尾开始'''
    try:
        if starter == None:
            includeStart = True;
            starter = Data[0];
        if ender == None:
            includend = True;
            ender = Data[len(Data)-1];
        if includend:
            if includeStart:
                return Data[Data.index(starter):len(Data)-Data[len(Data)::-1].index(ender)];
            else:
                return Data[Data.index(starter)+1:len(Data)-Data[len(Data)::-1].index(ender)];
        else:
            if includeStart:
                return Data[Data.index(starter):len(Data)-Data[len(Data)::-1].index(ender)-1];
            else:
                return Data[Data.index(starter)+1:len(Data)-Data[len(Data)::-1].index(ender)-1];
    except:
        return 0


def keepart(Data,starter,ender,includeStart :bool= True,includend :bool= True):
    '''保留序列从starter物件到ender物件之间的部分\n
    includeStart与inclodend分别控制此函数是否包括starter和ender物件所在部分，默认为真\n
    starter与ender若为None则默认从首或尾开始'''
    try:
        if starter == None:
            includeStart = True;
            starter = Data[0];
        if ender == None:
            includend = True;
            ender = Data[len(Data)-1];
        if includend:
            if includeStart:
                return Data[Data.index(starter):Data.index(ender)+1];
            else:
                return Data[Data.index(starter)+1:Data.index(ender)+1];
        else:
            if includeStart:
                return Data[Data.index(starter):Data.index(ender)];
            else:
                return Data[Data.index(starter)+1:Data.index(ender)];
    except:
        return 0









def lenFunction(fun) -> int:
    '''取得函数指令部分长度，即忽略#开头的注释'''
    try:
        l = 0;
        for i in fun:
            if i.replace(" ",'')[0] == '#':
                l += 1;
        return len(fun)-l;
    except:
        return -1;



def funSplit(bigFile,maxCmdLen : int = 10000 ):
    '''分割bigFile大的函数文件，bigFile需要读入文件流\n
    返回的部分，每行指令皆带有行尾换行符\\n\n
    返回-1为大小低于maxCmdLen最长函数指令长度'''
    bigFile = bigFile.readlines()
    if lenFunction(bigFile) < maxCmdLen:
        return -1;
    part = [];
    parts = [];
    l = 0;
    for i in bigFile:
        if i.replace(" ",'')[0] == '#':
            part.append(i+'\n');
        else:
            part.append(i+'\n');
            l += 1;
        if l >= 10000:
            parts.append(part)
            part = [];
            l = 0;
    return parts;









def makeFuncFiles(musicset, path='./'):
    '''在指定目录下生成函数文件'''
    from nmcsup.trans import Note2Cmd
    commands = []
    starts = []
    log("=========================正在在此处生成文件:"+path)
    maxlen = -1
    for i in range(len(musicset['musics'])):
        log('写入第'+str(i)+'个数据')
        commands.append("scoreboard players add @e[name=\""+musicset['musics'][i]['set']['EntityName']+"\"] "+musicset['musics'][i]['set']['ScoreboardName']+" 1\n")
        commands.append("execute @e[name=\""+musicset['musics'][i]['set']['EntityName'] +"\",scores={"+musicset['musics'][i]['set']['ScoreboardName']+"=1..10}] ~~~ title @a"+musicset['mainset']['PlayerSelect']+" title "+musicset['mainset']['MusicTitle']+"\n")
        commands.append("execute @e[name=\""+musicset['musics'][i]['set']['EntityName'] +"\",scores={"+musicset['musics'][i]['set']['ScoreboardName']+"=1..10}] ~~~ title @a"+musicset['mainset']['PlayerSelect']+" subtitle 本函数乐曲由§b§l凌云§r§3函数音乐创建§r生成\n")
        if len(musicset['musics'][i]['notes']) > maxlen:
            maxlen = len(musicset['musics'][i]['notes'])
        starts.append("scoreboard objectives add " +musicset['musics'][i]['set']['ScoreboardName']+" dummy\n")
        starts.append("summon armor_stand " +musicset['musics'][i]['set']['EntityName']+'\n')
        with open(path+musicset['mainset']['MusicTitle']+'_Part'+str(i)+'.mcfunction', 'w', encoding='UTF-8') as f:
            f.writelines(Note2Cmd(musicset['musics'][i]['notes'],musicset['musics'][i]['set']['ScoreboardName'],musicset['musics'][i]['set']['Instrument'],musicset['mainset']['PlayerSelect'],True))
    if musicset['mainset']['IsRepeat']:
        log("增加重复语句")
        for i in range(len(musicset['musics'])):
            commands.append("execute @e[name=\""+musicset['musics'][i]['set']['EntityName']+"\",scores={"+musicset['musics'][i]['set']['ScoreboardName']+"="+str((maxlen+2)*10)+"}] ~~~ scoreboard players set @e[name=\""+musicset['musics'][i]['set']['EntityName']+"\"] "+musicset['musics'][i]['set']['ScoreboardName']+" -1\n")
    log("增加版权语句")
    commands.append("\n\n# 凌云我的世界开发团队 x 凌云软件开发团队  : W-YI（金羿）\n")
    starts.append("\n\n# 凌云我的世界开发团队 x 凌云软件开发团队  : W-YI（金羿）\n")
    log("写入支持文件")
    with open(path+musicset['mainset']['MusicTitle']+'_Support.mcfunction', 'w', encoding='UTF-8') as f:
        f.writelines(commands)
    log("写入开始文件")
    with open(path+'Start_'+musicset['mainset']['MusicTitle']+'.mcfunction', 'w', encoding='UTF-8') as f:
        f.writelines(starts)
    del commands, starts, maxlen
    log("完成============================")







def makeFunDir(musicset, path='./'):
    '''在指定目录下生成函数包文件夹'''
    import os
    import uuid
    log("=============================生成函数包文件夹")
    # note,packname="Ryoun",FileName="Music",EntityName_='music_support',ScoreboardName_='music_support',MusicTitle_='Noname',PlayerSelect_='',Repeat_=False,Instrument_='harp'
    try:
        os.makedirs(path+musicset['mainset']['PackName'] +"Pack/behavior_packs/"+musicset['mainset']['PackName']+"/functions")
        log("已创建目录"+path+musicset['mainset']['PackName'] +"Pack/behavior_packs/"+musicset['mainset']['PackName']+"/functions")
    except:
        log("目录已有无需创建")
        pass
    # 判断文件皆存在
    if not(os.path.exists(path+musicset['mainset']['PackName']+"Pack/world_behavior_packs.json") and os.path.exists(path+musicset['mainset']['PackName']+"Pack/behavior_packs/"+musicset['mainset']['PackName']+"/manifest.json")):
        log("创建manifest.json以及world_behavior_packs.json")
        behaviorUuid = uuid.uuid4()
        with open(path+musicset['mainset']['PackName']+"Pack/world_behavior_packs.json", "w") as f:
            f.write("[\n  {\"pack_id\": \"" + str(behaviorUuid) +"\",\n  \"version\": [ 0, 0, 1 ]}\n]")
        with open(path+musicset['mainset']['PackName']+"Pack/behavior_packs/"+musicset['mainset']['PackName']+"/manifest.json", "w") as f:
            f.write("{\n  \"format_version\": 1,\n  \"header\": {\n    \"description\": \""+musicset['mainset']['PackName']+" Pack : behavior pack\",\n    \"version\": [ 0, 0, 1 ],\n    \"name\": \""+musicset['mainset']['PackName']+"Pack\",\n    \"uuid\": \"" + str(behaviorUuid) + "\"\n  },\n  \"modules\": [\n    {\n      \"description\": \""+musicset['mainset']['PackName']+" Pack : behavior pack\",\n      \"type\": \"data\",\n      \"version\": [ 0, 0, 1 ],\n      \"uuid\": \"" + str(uuid.uuid4()) + "\"\n    }\n  ]\n}")
    makeFuncFiles(musicset, path+musicset['mainset']['PackName'] +"Pack/behavior_packs/"+musicset['mainset']['PackName']+"/functions/")
    log("完成============================")












'''
这里是往事，用于记载一些用不到的功能

#存在于 Musicreater.py 播放(试听)音乐
def PlayNote(Notes, t=480):  # Notes是音符列表，t是一拍占有的毫秒数
    tkinter.messagebox.showinfo(title='提示！', message="播放发音不一定标准\n说不定还会坏音响/(ㄒoㄒ)/~~qwq\n请注意。")
    import winsound
    import time
    from nmcsup.trans import mcnote2freq
    Notes = mcnote2freq(Notes)
    for frequency, duration in Notes:
        log("播放："+str([int(frequency), int(duration*t)]))
        if int(frequency) != 0:
            winsound.Beep(int(frequency), int(duration*t))
        elif int(frequency) == 0:
            time.sleep(duration*t/1000)

#同上，执行播放命令
def PlayOne():
    log("试听")
    tkinter.messagebox.showwarning(title="警告⚠", message="试听音质可能引起您的不适，更可能引起您的扬声器的不适，请酌情播放。")
    global NowMusic
    PlayNote(dataset[0]['musics'][NowMusic]['notes'])



#同上，是早期 MinecraftMusicFunctionMaker.py (函数音创)的代码转移至音·创时的注解
n2c(dataset[0]['musics'][i]['notes'],EntityName=dataset[0]['musics'][i]['set']['EntityName'],ScoreboardName=dataset[0]['musics'][i]['set']['ScoreboardName'],PlayerSelect=dataset[0]['mainset']['PlayerSelect'],Instrument=dataset[0]['musics'][i]['set']["Instrument"])


'''

