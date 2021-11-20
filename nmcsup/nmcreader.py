
"""音创系列的文件读取功能"""




from nmcsup.log import log
from nmcsup.const import notes



#从格式文本文件读入一个音轨并存入一个列表
def ReadFile(fn : str) -> list:
    from nmcsup.trans import note2list
    log('打开'+fn+"并读取音符")
    try:
        nat = open(fn, 'r', encoding='UTF-8').read().split(" ")
        del fn
    except:
        log("找不到读取目标文件")
        return False
    Notes = []
    log(str(nat)+"已读取")
    for i in range(int(len(nat)/2)):
        Notes.append([nat[i*2], float(nat[i*2+1])])
    Notes = note2list(Notes)
    log('音符数据更新'+str(Notes))
    return [Notes,]


#从midi读入多个音轨，返回多个音轨列表
def ReadMidi(midfile : str ) -> list:
    import mido
    from msctspt.threadOpera import NewThread
    Notes = []
    try:
        mid = mido.MidiFile(midfile)
    except:
        log("找不到文件或无法读取文件"+midfile)
        return False
    # 解析
    ks = list(notes.values())
    def loadMidi(track):
        datas = []
        for i in track:
            if i.is_meta:
                log('元信息'+str(i))
                pass  # 不处理元信息
            elif 'note_on' in str(i):
                msg = str(i).replace("note=", '').replace("time=", '').split(" ")
                log('音符on消息，处理后：'+str(msg))
                if msg[4] == '0':
                    datas.append([ks[int(msg[2])-20][0], 1.0])
                    log('延续时间0tick--：添加音符'+str([ks[int(msg[2])-20][0], 1.0]))
                else:
                    datas.append([ks[int(msg[2])-20][0], float(msg[4])/480])
                    log('延续时间'+msg[4]+'tick--：添加音符' +str([ks[int(msg[2])-20][0], float(msg[4])/480]))
                del msg
        log('音符增加'+str(datas))
        return datas
    for j, track in enumerate(mid.tracks):
        th = NewThread(loadMidi,(track,))
        th.start()
        Notes.append(th.getResult())
    del ks
    return Notes




def ReadOldProject(fn:str) -> list:
    import json
    from nmcsup.trans import note2list
    log("读取文件："+fn)
    try:
        with open(fn, 'r', encoding='UTF-8') as c:
            dataset = json.load(c)
    except:
        print('找不到文件：'+fn+"，请查看您是否输入正确")
        log("丢失"+fn)
        return False
    for i in range(len(dataset['musics'])):
        dataset['musics'][i]['notes'] = note2list(dataset['musics'][i]['notes'])
    #返回 音轨列表 选择器
    return dataset


