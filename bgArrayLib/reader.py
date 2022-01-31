# -*- coding: utf-8 -*-


from nmcsup.log import log
import pickle


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


def midiNewReader(midfile: str):
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
