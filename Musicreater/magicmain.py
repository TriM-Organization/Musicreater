# -*- coding: utf-8 -*-
"""
功能测试 若非已知 请勿更改
此文件仅供功能测试，并非实际调用的文件
请注意，此处的文件均为测试使用
不要更改 不要更改 不要更改
请注意这里的一切均需要其原作者更改
这里用于放置一些新奇的点子
用于测试
不要更改 不要更改 不要更改！
"""

# 音·创 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 版权所有 金羿("Eilles Wan") & 诸葛亮与八卦阵("bgArray") & 鸣凤鸽子("MingFengPigeon")
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md


"""
音·创 (Musicreater)
是一款免费开源的针对《我的世界》的midi音乐转换库
Musicreater (音·创)
A free open source library used for convert midi file into formats that is suitable for **Minecraft**.

版权所有 © 2023 音·创 开发者
Copyright © 2023 all the developers of Musicreater

开源相关声明请见 ../License.md
Terms & Conditions: ../License.md
"""



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




# ============================
from typing import Literal
from ..constants import x,y,z

# 不要用 没写完
def delay_to_note_blocks(
    baseblock: str = "stone", 
    position_forward: Literal['x','y','z'] = z,
):
    """传入音符，生成以音符盒存储的红石音乐
    :param:
        baseblock: 中继器的下垫方块
        position_forward: 结构延长方向
    :return 是否生成成功
    """

    from TrimMCStruct import Structure, Block

    struct = Structure(
        (_sideLength, max_height, _sideLength),  # 声明结构大小
    )

    log = print

    startpos = [0,0,0]


    # 1拍 x 2.5 rt
    for i in notes:
        error = True
        try:
            struct.set_block(
                [startpos[0], startpos[1] + 1, startpos[2]],
                form_note_block_in_NBT_struct(height2note[i[0]], instrument),
            )
            struct.set_block(startpos, Block("universal_minecraft", instuments[i[0]][1]),)
            error = False
        except ValueError:
            log("无法放置音符：" + str(i) + "于" + str(startpos))
            struct.set_block(Block("universal_minecraft", baseblock), startpos)
            struct.set_block(
                Block("universal_minecraft", baseblock),
                [startpos[0], startpos[1] + 1, startpos[2]],
            )
        finally:
            if error is True:
                log("无法放置音符：" + str(i) + "于" + str(startpos))
                struct.set_block(Block("universal_minecraft", baseblock), startpos)
                struct.set_block(
                    Block("universal_minecraft", baseblock),
                    [startpos[0], startpos[1] + 1, startpos[2]],
                )
        delay = int(i[1] * speed + 0.5)
        if delay <= 4:
            startpos[0] += 1
            struct.set_block(
                form_repeater_in_NBT_struct(delay, "west"),
                [startpos[0], startpos[1] + 1, startpos[2]],
            )
            struct.set_block(Block("universal_minecraft", baseblock), startpos)
        else:
            for j in range(int(delay / 4)):
                startpos[0] += 1
                struct.set_block(
                    form_repeater_in_NBT_struct(4, "west"),
                    [startpos[0], startpos[1] + 1, startpos[2]],
                )
                struct.set_block(Block("universal_minecraft", baseblock), startpos)
            if delay % 4 != 0:
                startpos[0] += 1
                struct.set_block(
                    form_repeater_in_NBT_struct(delay % 4, "west"),
                    [startpos[0], startpos[1] + 1, startpos[2]],
                )
                struct.set_block(Block("universal_minecraft", baseblock), startpos)
        startpos[0] += posadder[0]
        startpos[1] += posadder[1]
        startpos[2] += posadder[2]