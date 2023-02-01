# -*- coding: utf-8 -*-


# 音·创 开发交流群 861684859
# 版权所有 金羿("Eilles Wan") & 诸葛亮与八卦阵("bgArray") & 鸣凤鸽子("MingFengPigeon")
# 若需使用或借鉴 请依照 Apache 2.0 许可证进行许可


"""
音·创 库版 (Musicreater Package Version)
是一款免费开源的针对《我的世界：基岩版》的midi音乐转换库
注意！除了此源文件以外，任何属于此仓库以及此项目的文件均依照Apache许可证进行许可
Musicreater pkgver (Package Version 音·创 库版)
A free open source library used for convert midi file into formats that is suitable for **Minecraft: Bedrock Edition**.
Note! Except for this source file, all the files in this repository and this project are licensed under Apache License 2.0

   Copyright 2022 all the developers of Musicreater

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


def _toCmdList_m1(
        self,
        scoreboardname: str = "mscplay",
        volume: float = 1.0,
        speed: float = 1.0) -> list:
    """
    使用Dislink Sforza的转换思路，将midi转换为我的世界命令列表
    :param scoreboardname: 我的世界的计分板名称
    :param volume: 音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
    :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
    :return: tuple(命令列表, 命令个数, 计分板最大值)
    """
    tracks = []
    if volume > 1:
        volume = 1
    if volume <= 0:
        volume = 0.001

    commands = 0
    maxscore = 0

    for i, track in enumerate(self.midi.tracks):

        ticks = 0
        instrumentID = 0
        singleTrack = []

        for msg in track:
            ticks += msg.time
            # print(msg)
            if msg.is_meta:
                if msg.type == "set_tempo":
                    tempo = msg.tempo
            else:
                if msg.type == "program_change":
                    # print("TT")
                    instrumentID = msg.program
                if msg.type == "note_on" and msg.velocity != 0:
                    nowscore = round(
                        (ticks * tempo)
                        / ((self.midi.ticks_per_beat * float(speed)) * 50000)
                    )
                    maxscore = max(maxscore, nowscore)
                    soundID, _X = self.__Inst2soundID_withX(instrumentID)
                    singleTrack.append(
                        "execute @a[scores={" +
                        str(scoreboardname) +
                        "=" +
                        str(nowscore) +
                        "}" +
                        f"] ~ ~ ~ playsound {soundID} @s ~ ~{1 / volume - 1} ~ {msg.velocity * (0.7 if msg.channel == 0 else 0.9)} {2 ** ((msg.note - 60 - _X) / 12)}")
                    commands += 1
        if len(singleTrack) != 0:
            tracks.append(singleTrack)

    return [tracks, commands, maxscore]









# ============================




import mido





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
                bpm =  60000000 / msg.tempo
                is_change_bpm = True

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






