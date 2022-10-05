import mido


def delete_extra_zero(n: float) -> int or float:
    """
    删除多余的0
    ————————————————
    版权声明：本文为CSDN博主「XerCis」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
    原文链接：https://blog.csdn.net/lly1122334/article/details/108770141
    删除小数点后多余的0
    :param n: input
    :return:  output
    """
    n = '{:g}'.format(n)
    n = float(n) if '.' in n else int(n)  # 含小数点转float否则int
    return n


def bpm_by_MetaMessage_Set_tempo(tmp: int) -> int or float:
    """
    midi文件tempo事件bpm算法。
    A function that's used to compute the bpm of a midiFile,
    which algorithm is made up of midiFile's tempo meta message.
    :param tmp:输入mid的metaMessage中速度tempo值
    input the tempo value which is in the tempo meta message.
    :return:bpm

    This algorithm is made by ©bgArray.
    算法版权归©诸葛亮与八卦阵所有。
    """
    second = tmp / 1000000
    bpm = delete_extra_zero(60 / second)
    # debug.dp(bpm)
    return bpm


class NoteMessage:
    def __init__(self, channel, pitch, velocity, startT, lastT, midi, now_bpm, change_bpm=None):
        self.channel = channel
        self.note = pitch
        self.velocity = velocity
        self.startTime = startT
        self.lastTime = lastT
        self.tempo = now_bpm  # 这里要程序实现获取bpm可以参考我的程序

        def mt2gt(mt, tpb_a, bpm_a):
            return mt / tpb_a / bpm_a * 60
        self.startTrueTime = mt2gt(self.startTime, midi.ticks_per_beat, self.tempo)  # / 20
        # delete_extra_zero(round_up())
        if change_bpm is not None:
            self.lastTrueTime = mt2gt(self.lastTime, midi.ticks_per_beat, change_bpm)  # / 20
        else:
            self.lastTrueTime = mt2gt(self.lastTime, midi.ticks_per_beat, self.tempo)  # / 20
        # delete_extra_zero(round_up())
        print((self.startTime * self.tempo) / (midi.ticks_per_beat * 50000))

    def __str__(self):
        return "noteMessage channel=" + str(self.channel) + " note=" + str(self.note) + " velocity=" + \
               str(self.velocity) + " startTime=" + str(self.startTime) + " lastTime=" + str(self.lastTime) + \
               " startTrueTime=" + str(self.startTrueTime) + " lastTrueTime=" + str(self.lastTrueTime)


def load(mid: mido.MidiFile):

    type_ = [False, False, False]  # note_off / note_on+0 / mixed

    is_tempo = False

    # 预检
    for i, track in enumerate(mid.tracks):
        for msg in track:
            # print(msg)
            if msg.is_meta is not True:
                if msg.type == 'note_on' and msg.velocity == 0:
                    type_[1] = True
                elif msg.type == "note_off":
                    type_[0] = True
            if msg.is_meta is True and msg.type == "set_tempo":
                is_tempo = True

    if is_tempo is not True:
        raise Exception("这个mid没有可供计算时间的tempo事件")

    if type_[0] is True and type_[1] is True:
        type_[2] = True
        type_[1] = False
        type_[0] = False
    print(type_)

    bpm = 0
    recent_change_bpm = 0
    is_change_bpm = False
    # 实检
    for i, track in enumerate(mid.tracks):
        noteOn = []
        trackS = []
        ticks = 0
        for msg in track:
            print(msg)
            ticks += msg.time
            print(ticks)
            if msg.is_meta is True and msg.type == "set_tempo":
                recent_change_bpm = bpm
                bpm = bpm_by_MetaMessage_Set_tempo(msg.tempo)
                is_change_bpm = True
            # print((ticks * 92) / (mid.ticks_per_beat * 50000))
            # MC_tick = delete_extra_zero(round_up(
            #     (ticks * 92) / (mid.ticks_per_beat * 50000)
            # ))
            # print(MC_tick)
            # print(ticks / mid.ticks_per_beat / 92 * 60)
            if msg.type == 'note_on' and msg.velocity != 0:
                noteOn.append([msg, msg.note, ticks])
            if type_[1] is True:
                if msg.type == 'note_on' and msg.velocity == 0:
                    for u in noteOn:
                        index = 0
                        if u[1] == msg.note:
                            lastMessage = u[0]
                            lastTick = u[2]
                            break
                        index += 1
                    print(lastTick)
                    if is_change_bpm and recent_change_bpm != 0:
                        trackS.append(NoteMessage(msg.channel, msg.note, lastMessage.velocity, lastTick, ticks - lastTick,
                                                  mid, recent_change_bpm, bpm))
                        is_change_bpm = False
                    else:
                        trackS.append(
                            NoteMessage(msg.channel, msg.note, lastMessage.velocity, lastTick, ticks - lastTick,
                                        mid, bpm))
                    # print(noteOn)
                    # print(index)
                    try:
                        noteOn.pop(index)
                    except IndexError:
                        noteOn.pop(index - 1)
        print(trackS)
        for j in trackS:
            print(j)


if __name__ == '__main__':
    load(mido.MidiFile("test.mid"))
