"""音创系列的文件读取功能"""

# 诸葛亮与八卦阵帮忙修改语法 日期：---2022年1月19日
# 统计：致命（三级）错误：0个；警告（二级）错误：3个；语法（一级）错误：22个


from nmcsup.log import log
from nmcsup.const import notes
import pickle


# 从格式文本文件读入一个音轨并存入一个列表
def ReadFile(fn: str):  # -> list
    from nmcsup.trans import note2list
    log('打开' + fn + "并读取音符")
    try:
        nat = open(fn, 'r', encoding='UTF-8').read().split(" ")
        del fn
    except FileNotFoundError:
        log("找不到读取目标文件")
        return False
    Notes = []
    log(str(nat) + "已读取")
    for i in range(int(len(nat) / 2)):
        Notes.append([nat[i * 2], float(nat[i * 2 + 1])])
    Notes = note2list(Notes)
    log('音符数据更新' + str(Notes))
    return [Notes, ]


# 从midi读入多个音轨，返回多个音轨列表
def ReadMidi(midfile: str):  # -> list
    import mido
    from msctspt.threadOpera import NewThread
    Notes = []
    try:
        mid = mido.MidiFile(midfile)
    except FileNotFoundError:
        log("找不到文件或无法读取文件" + midfile)
        return False
    # 解析
    ks = list(notes.values())

    def loadMidi(track1):
        datas = []
        for i in track1:
            if i.is_meta:
                log('元信息' + str(i))
                pass  # 不处理元信息
            elif 'note_on' in str(i):
                msg = str(i).replace("note=", '').replace("time=", '').split(" ")
                log('音符on消息，处理后：' + str(msg))
                if msg[4] == '0':
                    datas.append([ks[int(msg[2]) - 20][0], 1.0])
                    log('延续时间0tick--：添加音符' + str([ks[int(msg[2]) - 20][0], 1.0]))
                else:
                    datas.append([ks[int(msg[2]) - 20][0], float(msg[4]) / 480])
                    log('延续时间' + msg[4] + 'tick--：添加音符' + str([ks[int(msg[2]) - 20][0], float(msg[4]) / 480]))
                del msg
        log('音符增加' + str(datas))
        return datas

    for j, track in enumerate(mid.tracks):
        th = NewThread(loadMidi, (track,))
        th.start()
        Notes.append(th.getResult())
    del ks
    return Notes


class Note:
    def __init__(self, channel, pitch, velocity, time, time_position, instrument):
        self.channel = channel
        self.pitch = pitch
        self.velocity = velocity
        self.delay = time
        self.time_position = time_position
        self.instrument = instrument
        self.CD = "d"

    def get_CD(self, start, end):
        if end - start > 1.00:
            self.CD = "c"
        else:
            self.CD = "d"


def midi_conversion(midfile: str):
    import mido
    # from msctspt.threadOpera import NewThread
    from bgArrayLib.bpm import get

    def Time(mt, tpb_a, bpm_a):
        return round(mt / tpb_a / bpm_a * 60 * 20)

    Notes = []
    tracks = []
    note_list = []
    close = []
    on = []
    off = []
    instruments = []
    isPercussion = False
    try:
        mid = mido.MidiFile(midfile)
    except FileNotFoundError:
        log("找不到文件或无法读取文件" + midfile)
        return False
    tpb = mid.ticks_per_beat
    bpm = get(midfile)
    # 解析
    # def loadMidi(track1):
    for track in mid.tracks:
        overallTime = 0.0
        instrument = 0
        for i in track:
            overallTime += i.time
            try:
                if i.channel != 9:
                    # try:
                    #     log("event_type(事件): " + str(i.type) + " channel(音轨): " + str(i.channel) +
                    #     " note/pitch(音高): " +
                    #         str(i[2]) +
                    #         " velocity(力度): " + str(i.velocity) + " time(间隔时间): " + str(i.time) +
                    #         " overallTime/globalTime/timePosition: " + str(overallTime) + " \n")
                    # except AttributeError:
                    #     log("event_type(事件): " + str(i.type) + " thing(内容)：" + str(i) + " \n")
                    if 'program_change' in str(i):
                        instrument = i.program
                        if instrument > 119:  # 音色不够
                            pass
                        else:
                            instruments.append(i.program)
                    if 'note_on' in str(i) and i.velocity > 0:
                        print(i)
                        # print(i.note)
                        # print([Note(i.channel, i.note, i.velocity, i.time, Time(overallTime, tpb, bpm), instrument)])
                        tracks.append(
                            [Note(i.channel, i.note, i.velocity, i.time, Time(overallTime, tpb, bpm), instrument)])
                        note_list.append(
                            [i.channel, i.note, i.velocity, i.time, Time(overallTime, tpb, bpm), instrument])
                        on.append([i.note, Time(overallTime, tpb, bpm)])
                        # return [Note(i.channel, i, i.velocity, i.time, Time(overallTime, tpb, bpm))]
                    if 'note_off' in str(i) or 'note_on' in str(i) and i.velocity == 0:
                        # print(i)
                        # print([Note(i.channel, i.note, i.velocity, i.time, Time(overallTime, tpb, bpm))])
                        close.append(
                            [Note(i.channel, i.note, i.velocity, i.time, Time(overallTime, tpb, bpm), instrument)])
                        off.append([i.note, Time(overallTime, tpb, bpm)])
                        # return [Note(i.channel, i, i.velocity, i.time, Time(overallTime, tpb, bpm))]
            except AttributeError:
                pass
            if 'note_on' in str(i) and i.channel == 9:
                if 'note_on' in str(i) and i.velocity > 0:
                    print(i)
                    # print(i.note)
                    # print([Note(i.channel, i.note, i.velocity, i.time, Time(overallTime, tpb, bpm), -1)])
                    tracks.append([Note(i.channel, i.note, i.velocity, i.time, Time(overallTime, tpb, bpm), -1)])
                    note_list.append([i.channel, i.note, i.velocity, i.time, Time(overallTime, tpb, bpm), -1])
                    on.append([i.note, Time(overallTime, tpb, bpm)])
                    isPercussion = True
                    # return [Note(i.channel, i, i.velocity, i.time, Time(overallTime, tpb, bpm))]
        Notes.append(tracks)
    if instruments is []:
        instruments.append(0)
    instruments = list(set(instruments))
    with open("1.pkl", 'wb') as b:
        pickle.dump([instruments, isPercussion], b)

    # for j, track in enumerate(mid.tracks):
    #     th = NewThread(loadMidi, (track,))
    #     th.start()
    #     Notes.append(th.getResult())

    # print(Notes)
    print(Notes.__len__())
    # print(note_list)
    print(instruments)
    return Notes
    # return [Notes, note_list]


def midiClassReader(midfile: str):
    import mido
    from bgArrayLib.bpm import get

    def Time(mt, tpb_a, bpm_a):
        return round(mt / tpb_a / bpm_a * 60 * 20)
    Notes = []
    tracks = []
    try:
        mid = mido.MidiFile(midfile)
    except FileNotFoundError:
        log("找不到文件或无法读取文件" + midfile)
        return False
    tpb = mid.ticks_per_beat
    bpm = get(midfile)
    for track in mid.tracks:
        overallTime = 0.0
        instrument = 0
        for i in track:
            overallTime += i.time
            if 'note_on' in str(i) and i.velocity > 0:
                print(i)
                tracks.append(
                    [Note(i.channel, i.note, i.velocity, i.time, Time(overallTime, tpb, bpm), instrument)])
        Notes.append(tracks)
    print(Notes.__len__())
    return Notes


def ReadOldProject(fn: str):  # -> list
    import json
    from nmcsup.trans import note2list
    log("读取文件：" + fn)
    try:
        with open(fn, 'r', encoding='UTF-8') as c:
            dataset = json.load(c)
    except FileNotFoundError:
        print('找不到文件：' + fn + "，请查看您是否输入正确")
        log("丢失" + fn)
        return False
    for i in range(len(dataset['musics'])):
        dataset['musics'][i]['notes'] = note2list(dataset['musics'][i]['notes'])
    # 返回 音轨列表 选择器
    return dataset


if __name__ == '__main__':
    # a = midi_conversion("L:\\0WorldMusicCreater-MFMS new edition\\框架\\v0.3.2\\Musicreater\\测试用\\同道殊途标准.mid")
    # midi_conversion("L:\\0WorldMusicCreater-MFMS new edition\\框架\\v0.3.2\\Musicreater\\测试用\\"
    #                 "Illusionary_Daytime_--------幻昼.mid")
    # a = midi_conversion(r"C:\Users\lc\Documents\MuseScore3\乐谱\架子鼓.mid")
    a = midi_conversion(r"C:\Users\lc\Documents\MuseScore3\乐谱\stay2.mid")
    # print(a)
