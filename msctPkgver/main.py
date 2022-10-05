# -*- coding: utf-8 -*-


# 音·创 开发交流群 861684859
# Email EillesWan2006@163.com W-YI_DoctorYI@outlook.com EillesWan@outlook.com
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

import os
import mido
import brotli
import json
import uuid
import shutil
import math


def makeZip(sourceDir, outFilename, compression=8, exceptFile=None):
    """使用compression指定的算法打包目录为zip文件\n
    默认算法为DEFLATED(8),可用算法如下：\n
    STORED = 0\n
    DEFLATED = 8\n
    BZIP2 = 12\n
    LZMA = 14\n
    """
    import zipfile

    zipf = zipfile.ZipFile(outFilename, "w", compression)
    pre_len = len(os.path.dirname(sourceDir))
    for parent, dirnames, filenames in os.walk(sourceDir):
        for filename in filenames:
            if filename == exceptFile:
                continue
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            zipf.write(pathfile, arcname)
    zipf.close()


class midiConvert:
    def __init__(self):
        """简单的midi转换类，将midi文件转换为我的世界结构或者包"""
        pass

    def convert(self, midiFile: str, outputPath: str):
        """转换前需要先运行此函数来获取基本信息"""

        self.midiFile = midiFile
        """midi文件路径"""
        self.midi = mido.MidiFile(self.midiFile)
        """MidiFile对象"""
        self.outputPath = outputPath
        """输出路径"""
        # 将self.midiFile的文件名，不含路径且不含后缀存入self.midiFileName
        self.midFileName = os.path.splitext(os.path.basename(self.midiFile))[0]
        """文件名，不含路径且不含后缀"""

    def __Inst2soundIDwithX(self, instrumentID):
        """返回midi的乐器ID对应的我的世界乐器名，对于音域转换算法，如下：
            2**( ( msg.note - 60 - X ) / 12 ) 即为MC的音高，其中
            X的取值随乐器不同而变化：
            竖琴harp、电钢琴pling、班卓琴banjo、方波bit、颤音琴iron_xylophone 的时候为6
            吉他的时候为7
            贝斯bass、迪吉里杜管didgeridoo的时候为8
            长笛flute、牛铃cou_bell的时候为5
            钟琴bell、管钟chime、木琴xylophone的时候为4
            而存在一些打击乐器basedrum、hat、snare，没有音域，则没有X，那么我们返回7即可
        :param instrumentID: midi的乐器ID
        :param default: 如果instrumentID不在范围内，返回的默认我的世界乐器名称
        :return: (str我的世界乐器名, int转换算法中的X)"""
        try:
            a = {
                0: ("note.harp", 6),
                1: ("note.harp", 6),
                2: ("note.pling", 6),
                3: ("note.harp", 6),
                4: ("note.pling", 6),
                5: ("note.pling", 6),
                6: ("note.harp", 6),
                7: ("note.harp", 6),
                8: ("note.share", 7),  # 打击乐器无音域
                9: ("note.harp", 6),
                10: ("note.didgeridoo", 8),
                11: ("note.harp", 6),
                12: ("note.xylophone", 4),
                13: ("note.chime", 4),
                14: ("note.harp", 6),
                15: ("note.harp", 6),
                16: ("note.bass", 8),
                17: ("note.harp", 6),
                18: ("note.harp", 6),
                19: ("note.harp", 6),
                20: ("note.harp", 6),
                21: ("note.harp", 6),
                22: ("note.harp", 6),
                23: ("note.guitar", 7),
                24: ("note.guitar", 7),
                25: ("note.guitar", 7),
                26: ("note.guitar", 7),
                27: ("note.guitar", 7),
                28: ("note.guitar", 7),
                29: ("note.guitar", 7),
                30: ("note.guitar", 7),
                31: ("note.bass", 8),
                32: ("note.bass", 8),
                33: ("note.bass", 8),
                34: ("note.bass", 8),
                35: ("note.bass", 8),
                36: ("note.bass", 8),
                37: ("note.bass", 8),
                38: ("note.bass", 8),
                39: ("note.bass", 8),
                40: ("note.harp", 6),
                41: ("note.harp", 6),
                42: ("note.harp", 6),
                43: ("note.harp", 6),
                44: ("note.iron_xylophone", 6),
                45: ("note.guitar", 7),
                46: ("note.harp", 6),
                47: ("note.harp", 6),
                48: ("note.guitar", 7),
                49: ("note.guitar", 7),
                50: ("note.bit", 6),
                51: ("note.bit", 6),
                52: ("note.harp", 6),
                53: ("note.harp", 6),
                54: ("note.bit", 6),
                55: ("note.flute", 5),
                56: ("note.flute", 5),
                57: ("note.flute", 5),
                58: ("note.flute", 5),
                59: ("note.flute", 5),
                60: ("note.flute", 5),
                61: ("note.flute", 5),
                62: ("note.flute", 5),
                63: ("note.flute", 5),
                64: ("note.bit", 6),
                65: ("note.bit", 6),
                66: ("note.bit", 6),
                67: ("note.bit", 6),
                68: ("note.flute", 5),
                69: ("note.harp", 6),
                70: ("note.harp", 6),
                71: ("note.flute", 5),
                72: ("note.flute", 5),
                73: ("note.flute", 5),
                74: ("note.harp", 6),
                75: ("note.flute", 5),
                76: ("note.harp", 6),
                77: ("note.harp", 6),
                78: ("note.harp", 6),
                79: ("note.harp", 6),
                80: ("note.bit", 6),
                81: ("note.bit", 6),
                82: ("note.bit", 6),
                83: ("note.bit", 6),
                84: ("note.bit", 6),
                85: ("note.bit", 6),
                86: ("note.bit", 6),
                87: ("note.bit", 6),
                88: ("note.bit", 6),
                89: ("note.bit", 6),
                90: ("note.bit", 6),
                91: ("note.bit", 6),
                92: ("note.bit", 6),
                93: ("note.bit", 6),
                94: ("note.bit", 6),
                95: ("note.bit", 6),
                96: ("note.bit", 6),
                97: ("note.bit", 6),
                98: ("note.bit", 6),
                99: ("note.bit", 6),
                100: ("note.bit", 6),
                101: ("note.bit", 6),
                102: ("note.bit", 6),
                103: ("note.bit", 6),
                104: ("note.harp", 6),
                105: ("note.banjo", 6),
                106: ("note.harp", 6),
                107: ("note.harp", 6),
                108: ("note.harp", 6),
                109: ("note.harp", 6),
                110: ("note.harp", 6),
                111: ("note.guitar", 7),
                112: ("note.harp", 6),
                113: ("note.bell", 4),
                114: ("note.harp", 6),
                115: ("note.cow_bell", 5),
                116: ("note.basedrum", 7),  # 打击乐器无音域
                117: ("note.bass", 8),
                118: ("note.bit", 6),
                119: ("note.basedrum", 7),  # 打击乐器无音域
                120: ("note.guitar", 7),
                121: ("note.harp", 6),
                122: ("note.harp", 6),
                123: ("note.harp", 6),
                124: ("note.harp", 6),
                125: ("note.hat", 7),  # 打击乐器无音域
                126: ("note.basedrum", 7),  # 打击乐器无音域
                127: ("note.snare", 7),  # 打击乐器无音域
            }[instrumentID]
        except:
            a = ("note.harp", 6)
        return a

    def __score2time(self, score: int):
        return str(int(int(score / 20) / 60)) + ":" + str(int(int(score / 20) % 60))

    def __formProgressBar(
        self,
        maxscore: int,
        scoreboardname: str,
        progressbar: tuple = (
            r"▶ %%N [ %%s/%^s %%% __________ %%t|%^t ]",
            ("§e=§r", "§7=§r"),
        ),
    ) -> list:

        pgsstyle = progressbar[0]
        """用于被替换的进度条原始样式"""

        """
        | 标识符   | 指定的可变量     |
        |---------|----------------|
        | `%%N`   | 乐曲名(即传入的文件名)|
        | `%%s`   | 当前计分板值     |
        | `%^s`   | 计分板最大值     |
        | `%%t`   | 当前播放时间     |
        | `%^t`   | 曲目总时长       |
        | `%%%`   | 当前进度比率     |
        | `_`     | 用以表示进度条占位|
        """

        def __replace(
            s: str, tobeReplaced: str, replaceWith: str, times: int, other: str
        ):
            if times == 0:
                return s.replace(tobeReplaced, other)
            if times == s.count(tobeReplaced):
                return s.replace(tobeReplaced, replaceWith)
            result = ""
            t = 0
            for i in s:
                if i == tobeReplaced:
                    if t < times:
                        result += replaceWith
                        t += 1
                    else:
                        result += other
                else:
                    result += i

            return result

        idlist = {
            r"%%N": self.midFileName,
            r"%%s": r"%%s",
            r"%^s": str(maxscore),
            r"%%t": r"%%t",
            r"%^t": self.__score2time(maxscore),
            r"%%%": r"%%%",
        }

        ids = {}

        for i, j in idlist.items():
            if i != j:
                if i in pgsstyle:
                    pgsstyle = pgsstyle.replace(i, j)
            else:
                if i in pgsstyle:
                    ids[i] = True
                else:
                    ids[i] = False

        del idlist

        pgblength = pgsstyle.count("_")
        """进度条的“条”长度"""

        finalprgsbar = []

        for i in range(maxscore):
            nowstr = pgsstyle
            if ids[r"%%s"] == True:
                nowstr = nowstr.replace(r"%%s", str(i + 1))
            if ids[r"%%t"] == True:
                nowstr = nowstr.replace(r"%%t", self.__score2time(i + 1))
            if ids[r"%%%"] == True:
                nowstr = nowstr.replace(
                    r"%%%", str(int((i + 1) / maxscore * 10000) / 100) + "%"
                )

            countof_s = int((i + 1) / maxscore * pgblength)

            finalprgsbar.append(
                "title @a[scores={"
                + scoreboardname
                + "="
                + str(i + 1)
                + "}] actionbar "
                + __replace(
                    nowstr, "_", progressbar[1][0], countof_s, progressbar[1][1]
                )
            )

        return finalprgsbar

    def __formCMDblk(
        self,
        command: str,
        particularValue: int,
        impluse: int = 0,
        condition: bool = False,
        needRedstone: bool = True,
        tickDelay: int = 0,
        customName: str = "",
        executeOnFirstTick: bool = False,
        trackOutput: bool = True,
    ):
        """
        使用指定项目返回指定的指令方块放置指令项
        :param command: `str`
            指令
        :param particularValue:
            方块特殊值，即朝向
                :0	下	无条件
                :1	上	无条件
                :2	z轴负方向	无条件
                :3	z轴正方向	无条件
                :4	x轴负方向	无条件
                :5	x轴正方向	无条件
                :6	下	无条件
                :7	下	无条件

                :8	下	有条件
                :9	上	有条件
                :10	z轴负方向	有条件
                :11	z轴正方向	有条件
                :12	x轴负方向	有条件
                :13	x轴正方向	有条件
                :14	下	有条件
                :14	下	有条件
            注意！此处特殊值中的条件会被下面condition参数覆写
        :param impluse: `int 0|1|2`
            方块类型
                0脉冲 1循环 2连锁
        :param condition: `bool`
            是否有条件
        :param needRedstone: `bool`
            是否需要红石
        :param tickDelay: `int`
            执行延时
        :param customName: `str`
            悬浮字
        :param lastOutput: `str`
            上次输出字符串，注意此处需要留空
        :param executeOnFirstTick: `bool`
            执行第一个已选项(循环指令方块是否激活后立即执行，若为False，则从激活时起延迟后第一次执行)
        :param trackOutput: `bool`
            是否输出

        :return:str
        """
        block = b"\x24" + particularValue.to_bytes(2, byteorder="big", signed=False)

        for i in [
            impluse.to_bytes(4, byteorder="big", signed=False),
            bytes(command, encoding="utf-8") + b"\x00",
            bytes(customName, encoding="utf-8") + b"\x00",
            bytes("", encoding="utf-8") + b"\x00",
            tickDelay.to_bytes(4, byteorder="big", signed=True),
            executeOnFirstTick.to_bytes(1, byteorder="big"),
            trackOutput.to_bytes(1, byteorder="big"),
            condition.to_bytes(1, byteorder="big"),
            needRedstone.to_bytes(1, byteorder="big"),
        ]:
            block += i
        return block

    def _toCmdList_m1(
        self, scoreboardname: str = "mscplay", volume: float = 1.0, speed: float = 1.0
    ) -> list:
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
                        soundID, _X = self.__Inst2soundIDwithX(instrumentID)
                        singleTrack.append(
                            "execute @a[scores={"
                            + str(scoreboardname)
                            + "="
                            + str(nowscore)
                            + "}"
                            + f"] ~ ~ ~ playsound {soundID} @s ~ ~{1 / volume - 1} ~ {msg.velocity * (0.7 if msg.channel == 0 else 0.9)} {2 ** ((msg.note - 60 - _X) / 12)}"
                        )
                        commands += 1
            if len(singleTrack) != 0:
                tracks.append(singleTrack)

        return tracks, commands, maxscore

    # 值得注意的是，我这里没有修改
    def _toCmdList_m2(
        self, scoreboardname: str = "mscplay", volume: float = 1.0, speed: float = 1.0
    ) -> list:
        """
        使用金羿的转换思路，将midi转换为我的世界命令列表，使用线性方法调整音量
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
            noteOn = []

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
                    if msg.type == 'note_on' and msg.velocity != 0:
                        noteOn.append([msg, msg.note, ticks])
                    elif type_[1] is True:
                        if msg.type == 'note_on' and msg.velocity == 0:
                            for u in noteOn:
                                index = 0
                                if u[1] == msg.note:
                                    lastMessage = u[0]
                                    lastTick = u[2]
                                    break
                                index += 1
                            trackS.append(
                                NoteMessage(
                                    msg.channel,
                                    msg.note,
                                    lastMessage.velocity,
                                    lastTick,
                                    ticks - lastTick,
                                    mid,
                                )
                            )
                            # print(noteOn)
                            # print(index)
                            try:
                                noteOn.pop(index)
                            except IndexError:
                                noteOn.pop(index - 1)
                    if msg.type == "note_on" and msg.velocity != 0:
                        nowscore = round(
                            (ticks * tempo)
                            / ((self.midi.ticks_per_beat * float(speed)) * 50000)
                        )
                        maxscore = max(maxscore, nowscore)
                        soundID, _X = self.__Inst2soundIDwithX(instrumentID)
                        singleTrack.append(
                            "execute @a[scores={"
                            + str(scoreboardname)
                            + "="
                            + str(nowscore)
                            + "}"
                            + f"] ~ ~ ~ playsound {soundID} @s ~ ~{1 / volume - 1} ~ {msg.velocity * (0.7 if msg.channel == 0 else 0.9)} {2 ** ((msg.note - 60 - _X) / 12)}"
                        )
                        commands += 1
            if len(singleTrack) != 0:
                tracks.append(singleTrack)

        return tracks, commands, maxscore
    

    def _toCmdList_withDelay_m1(
        self,
        volume: float = 1.0,
        speed: float = 1.0,
        player: str = "@a",
        isMixedWithPrograssBar=False,
    ) -> list:
        """
        使用Dislink Sforza的转换思路，将midi转换为我的世界命令列表，并输出每个音符之后的延迟
        :param volume: 音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
        :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
        :param player: 玩家选择器，默认为`@a`
        :param isMixedWithPrograssBar: 进度条，（当此参数为True时使用默认进度条，当此参数为其他值为真的表达式时识别为进度条自定义参数，若为其他值为假的表达式则不生成进度条）
        :return: 全部指令列表[ ( str指令, int距离上一个指令的延迟 ),...]
        """
        tracks = {}

        if volume > 1:
            volume = 1
        if volume <= 0:
            volume = 0.001

        if isMixedWithPrograssBar == True:
            isMixedWithPrograssBar = (
                r"▶ %%N [ %%s/%^s %%% __________ %%t|%^t ]",
                ("§e=§r", "§7=§r"),
            )

        for i, track in enumerate(self.midi.tracks):

            instrumentID = 0
            ticks = 0

            for msg in track:
                ticks += msg.time
                if msg.is_meta:
                    if msg.type == "set_tempo":
                        tempo = msg.tempo
                else:
                    if msg.type == "program_change":
                        instrumentID = msg.program
                    if msg.type == "note_on" and msg.velocity != 0:
                        nowtick = round(
                            (ticks * tempo)
                            / ((self.midi.ticks_per_beat * float(speed)) * 50000)
                        )
                        soundID, _X = self.__Inst2soundIDwithX(instrumentID)
                        try:
                            tracks[nowtick].append(
                                f"execute {player} ~ ~ ~ playsound {soundID} @s ~ ~{1 / volume - 1} ~ {msg.velocity * (0.7 if msg.channel == 0 else 0.9)} {2 ** ((msg.note - 60 - _X) / 12)}"
                            )
                        except:
                            tracks[nowtick] = [
                                f"execute {player} ~ ~ ~ playsound {soundID} @s ~ ~{1 / volume - 1} ~ {msg.velocity * (0.7 if msg.channel == 0 else 0.9)} {2 ** ((msg.note - 60 - _X) / 12)}",
                            ]

        allticks = list(tracks.keys())

        if isMixedWithPrograssBar:

            pgsstyle = isMixedWithPrograssBar[0]
            """用于被替换的进度条原始样式"""

            """
            | 标识符   | 指定的可变量     |
            |---------|----------------|
            | `%%N`   | 乐曲名(即传入的文件名)|
            | `%%s`   | 当前计分板值     |
            | `%^s`   | 计分板最大值     |
            | `%%t`   | 当前播放时间     |
            | `%^t`   | 曲目总时长       |
            | `%%%`   | 当前进度比率     |
            | `_`     | 用以表示进度条占位|
            """

            def __replace(
                s: str, tobeReplaced: str, replaceWith: str, times: int, other: str
            ):
                if times == 0:
                    return s.replace(tobeReplaced, other)
                if times == s.count(tobeReplaced):
                    return s.replace(tobeReplaced, replaceWith)
                result = ""
                t = 0
                for i in s:
                    if i == tobeReplaced:
                        if t < times:
                            result += replaceWith
                            t += 1
                        else:
                            result += other
                    else:
                        result += i

                return result

            idlist = {
                r"%%N": self.midFileName,
                r"%%s": r"%%s",
                r"%^s": str(allticks[-1]),
                r"%%t": r"%%t",
                r"%^t": self.__score2time(allticks[-1]),
                r"%%%": r"%%%",
            }

            ids = {}

            for i, j in idlist.items():
                if i != j:
                    if i in pgsstyle:
                        pgsstyle = pgsstyle.replace(i, j)
                else:
                    if i in pgsstyle:
                        ids[i] = True
                    else:
                        ids[i] = False

            del idlist

            pgblength = pgsstyle.count("_")
            """进度条的“条”长度"""

        results = []

        for i in range(len(allticks)):
            if i != 0:
                for j in range(len(tracks[allticks[i]])):
                    if j != 0:
                        results.append((tracks[allticks[i]][j], 0))
                    else:
                        results.append(
                            (tracks[allticks[i]][j], allticks[i] - allticks[i - 1])
                        )
            else:
                for j in range(len(tracks[allticks[i]])):
                    results.append((tracks[allticks[i]][j], allticks[i]))

            if isMixedWithPrograssBar:

                nowstr = pgsstyle
                if ids[r"%%s"] == True:
                    nowstr = nowstr.replace(r"%%s", str(allticks[i] + 1))
                if ids[r"%%t"] == True:
                    nowstr = nowstr.replace(r"%%t", self.__score2time(allticks[i] + 1))
                if ids[r"%%%"] == True:
                    nowstr = nowstr.replace(
                        r"%%%",
                        str(int((allticks[i] + 1) / allticks[-1] * 10000) / 100) + "%",
                    )

                countof_s = int((allticks[i] + 1) / allticks[-1] * pgblength)

                titlenow = __replace(
                    nowstr,
                    "_",
                    isMixedWithPrograssBar[1][0],
                    countof_s,
                    isMixedWithPrograssBar[1][1],
                )

                results.append(
                    (
                        f"title {player} actionbar {titlenow}",
                        0,
                    )
                )

        return results

    def __fillSquareSideLength(self, total: int, maxHeight: int):
        """给定总方块数量和最大高度，返回所构成的图形外切正方形的边长
        :param total: 总方块数量
        :param maxHeight: 最大高度
        :return: 外切正方形的边长 int"""
        return math.ceil(math.sqrt(math.ceil(total / maxHeight)))

    def tomcpack(
        self,
        method: int = 1,
        isAutoReset: bool = False,
        progressbar=None,
        scoreboardname: str = "mscplay",
        volume: float = 1.0,
        speed: float = 1.0,
    ) -> bool:
        """
        使用method指定的转换算法，将midi转换为我的世界mcpack格式的包
        :param method: 转换算法
        :param isAutoReset: 是否自动重置计分板
        :param progressbar: 进度条，（当此参数为True时使用默认进度条，为其他的值为真的参数时识别为进度条自定义参数，为其他值为假的时候不生成进度条）
        :param scoreboardname: 我的世界的计分板名称
        :param volume: 音量，注意：这里的音量范围为(0,1]，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
        :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
        :return 成功与否，成功返回(True,True)，失败返回(False,str失败原因)
        """
        if method == 1:
            cmdlist, _a, maxscore = self._toCmdList_m1(scoreboardname, volume, speed)
        else:
            return (False, f"无法找到算法ID{method}对应的转换算法")
        del _a

        # 当文件f夹{self.outputPath}/temp/functions存在时清空其下所有项目，若其不存在则创建
        if os.path.exists(f"{self.outputPath}/temp/functions/"):
            shutil.rmtree(f"{self.outputPath}/temp/functions/")
        os.makedirs(f"{self.outputPath}/temp/functions/mscplay")

        # 写入manifest.json
        if not os.path.exists(f"{self.outputPath}/temp/manifest.json"):
            with open(
                f"{self.outputPath}/temp/manifest.json", "w", encoding="utf-8"
            ) as f:
                f.write(
                    '{\n  "format_version": 1,\n  "header": {\n    "description": "'
                    + self.midFileName
                    + ' Pack : behavior pack",\n    "version": [ 0, 0, 1 ],\n    "name": "'
                    + self.midFileName
                    + 'Pack",\n    "uuid": "'
                    + str(uuid.uuid4())
                    + '"\n  },\n  "modules": [\n    {\n      "description": "'
                    + f"the Player of the Music {self.midFileName}"
                    + '",\n      "type": "data",\n      "version": [ 0, 0, 1 ],\n      "uuid": "'
                    + str(uuid.uuid4())
                    + '"\n    }\n  ]\n}'
                )
        else:
            with open(
                f"{self.outputPath}/temp/manifest.json", "r", encoding="utf-8"
            ) as manifest:
                data = json.loads(manifest.read())
                data["header"][
                    "description"
                ] = f"the Player of the Music {self.midFileName}"
                data["header"]["name"] = self.midFileName
                data["header"]["uuid"] = str(uuid.uuid4())
                data["modules"][0]["description"] = "None"
                data["modules"][0]["uuid"] = str(uuid.uuid4())
                manifest.close()
            open(f"{self.outputPath}/temp/manifest.json", "w", encoding="utf-8").write(
                json.dumps(data)
            )

        # 将命令列表写入文件
        indexfile = open(
            f"{self.outputPath}/temp/functions/index.mcfunction", "w", encoding="utf-8"
        )
        for track in cmdlist:
            indexfile.write(
                "function mscplay/track" + str(cmdlist.index(track) + 1) + "\n"
            )
            with open(
                f"{self.outputPath}/temp/functions/mscplay/track{cmdlist.index(track) + 1}.mcfunction",
                "w",
                encoding="utf-8",
            ) as f:
                f.write("\n".join(track))
        indexfile.writelines(
            (
                "scoreboard players add @a[scores={"
                + scoreboardname
                + "=1..}] "
                + scoreboardname
                + " 1\n",
                (
                    "scoreboard players reset @a[scores={"
                    + scoreboardname
                    + "="
                    + str(maxscore + 20)
                    + "..}]"
                    + f" {scoreboardname}\n"
                )
                if isAutoReset
                else "",
                f"function mscplay/progressShow\n" if progressbar else "",
            )
        )

        if progressbar:
            if progressbar == True:
                with open(
                    f"{self.outputPath}/temp/functions/mscplay/progressShow.mcfunction",
                    "w",
                    encoding="utf-8",
                ) as f:
                    f.writelines(
                        "\n".join(self.__formProgressBar(maxscore, scoreboardname))
                    )
            else:
                with open(
                    f"{self.outputPath}/temp/functions/mscplay/progressShow.mcfunction",
                    "w",
                    encoding="utf-8",
                ) as f:
                    f.writelines(
                        "\n".join(
                            self.__formProgressBar(
                                maxscore, scoreboardname, progressbar
                            )
                        )
                    )

        indexfile.close()

        makeZip(
            f"{self.outputPath}/temp/", self.outputPath + f"/{self.midFileName}.mcpack"
        )

        shutil.rmtree(f"{self.outputPath}/temp/")

    def toBDXfile(
        self,
        method: int = 1,
        author: str = "Eilles",
        progressbar=False,
        maxheight: int = 64,
        scoreboardname: str = "mscplay",
        volume: float = 1.0,
        speed: float = 1.0,
        isAutoReset: bool = False,
    ):
        """
        使用method指定的转换算法，将midi转换为BDX结构文件
        :param method: 转换算法
        :param author: 作者名称
        :param progressbar: 进度条，（当此参数为True时使用默认进度条，为其他的值为真的参数时识别为进度条自定义参数，为其他值为假的时候不生成进度条）
        :param maxheight: 生成结构最大高度
        :param scoreboardname: 我的世界的计分板名称
        :param volume: 音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
        :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
        :param isAutoReset: 是否自动重置计分板
        :return 成功与否，成功返回(True,未经过压缩的源,结构占用大小)，失败返回(False,str失败原因)
        """

        if method == 1:
            cmdlist, totalcount, maxScore = self._toCmdList_m1(
                scoreboardname, volume, speed
            )
        else:
            return (False, f"无法找到算法ID {method} 对应的转换算法")

        if not os.path.exists(self.outputPath):
            os.makedirs(self.outputPath)

        with open(f"{self.outputPath}/{self.midFileName}.bdx", "w+") as f:
            f.write("BD@")

        _bytes = (
            b"BDX\x00"
            + author.encode("utf-8")
            + b" & Musicreater\x00\x01command_block\x00"
        )

        key = {
            "x": (b"\x0f", b"\x0e"),
            "y": (b"\x11", b"\x10"),
            "z": (b"\x13", b"\x12"),
        }
        """key存储了方块移动指令的数据，其中可以用key[x|y|z][0|1]来表示xyz的减或增"""
        x = "x"
        y = "y"
        z = "z"

        _sideLength = self.__fillSquareSideLength(totalcount, maxheight)

        yforward = True
        zforward = True

        nowy = 0
        nowz = 0
        nowx = 0

        commands = []

        for track in cmdlist:
            commands += track

        if isAutoReset:
            commands += (
                "scoreboard players reset @a[scores={"
                + scoreboardname
                + "="
                + str(maxScore + 20)
                + "}] "
                + scoreboardname
            )

        if progressbar:
            if progressbar == True:
                commands += self.__formProgressBar(maxScore, scoreboardname)
            else:
                commands += self.__formProgressBar(
                    maxScore, scoreboardname, progressbar
                )

        for cmd in commands:
            _bytes += self.__formCMDblk(
                cmd,
                (1 if yforward else 0)
                if (
                    ((nowy != 0) and (not yforward))
                    or ((yforward) and (nowy != maxheight))
                )
                else (3 if zforward else 2)
                if (
                    ((nowz != 0) and (not zforward))
                    or ((zforward) and (nowz != _sideLength))
                )
                else 5,
                impluse=2,
                condition=False,
                needRedstone=False,
                tickDelay=0,
                customName="",
                executeOnFirstTick=False,
                trackOutput=True,
            )

            nowy += 1 if yforward else -1

            if ((nowy > maxheight) and (yforward)) or ((nowy < 0) and (not yforward)):
                nowy -= 1 if yforward else -1

                yforward = not yforward

                nowz += 1 if zforward else -1

                if ((nowz > _sideLength) and (zforward)) or (
                    (nowz < 0) and (not zforward)
                ):
                    nowz -= 1 if zforward else -1
                    zforward = not zforward
                    _bytes += key[x][1]
                    nowx += 1
                else:

                    _bytes += key[z][int(zforward)]

            else:

                _bytes += key[y][int(yforward)]

        with open(f"{self.outputPath}/{self.midFileName}.bdx", "ab+") as f:
            f.write(brotli.compress(_bytes + b"XE"))

        return (True, _bytes, (nowx, maxheight, _sideLength))

    def toBDXfile_withDelay(
        self,
        method: int = 1,
        author: str = "Eilles",
        progressbar=False,
        maxheight: int = 64,
        volume: float = 1.0,
        speed: float = 1.0,
        player: str = "@a",
    ):
        """
        使用method指定的转换算法，将midi转换为BDX结构文件
        :param method: 转换算法
        :param author: 作者名称
        :param progressbar: 进度条，（当此参数为True时使用默认进度条，为其他的值为真的参数时识别为进度条自定义参数，为其他值为假的时候不生成进度条）
        :param maxheight: 生成结构最大高度
        :param volume: 音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
        :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
        :param player: 玩家选择器，默认为`@a`
        :return 成功与否，成功返回(True,未经过压缩的源,结构占用大小)，失败返回(False,str失败原因)
        """

        if method == 1:
            cmdlist = self._toCmdList_withDelay_m1(volume, speed, player, progressbar)
        else:
            return (False, f"无法找到算法ID {method} 对应的转换算法")

        if not os.path.exists(self.outputPath):
            os.makedirs(self.outputPath)

        with open(f"{self.outputPath}/{self.midFileName}.bdx", "w+") as f:
            f.write("BD@")

        _bytes = (
            b"BDX\x00"
            + author.encode("utf-8")
            + b" & Musicreater\x00\x01command_block\x00"
        )

        key = {
            "x": (b"\x0f", b"\x0e"),
            "y": (b"\x11", b"\x10"),
            "z": (b"\x13", b"\x12"),
        }
        """key存储了方块移动指令的数据，其中可以用key[x|y|z][0|1]来表示xyz的减或增"""
        x = "x"
        y = "y"
        z = "z"

        _sideLength = self.__fillSquareSideLength(len(cmdlist), maxheight)

        yforward = True
        zforward = True

        nowy = 0
        nowz = 0
        nowx = 0

        for cmd, delay in cmdlist:
            _bytes += self.__formCMDblk(
                cmd,
                (1 if yforward else 0)
                if (
                    ((nowy != 0) and (not yforward))
                    or ((yforward) and (nowy != maxheight))
                )
                else (3 if zforward else 2)
                if (
                    ((nowz != 0) and (not zforward))
                    or ((zforward) and (nowz != _sideLength))
                )
                else 5,
                impluse=2,
                condition=False,
                needRedstone=False,
                tickDelay=delay,
                customName="",
                executeOnFirstTick=False,
                trackOutput=True,
            )

            nowy += 1 if yforward else -1

            if ((nowy > maxheight) and (yforward)) or ((nowy < 0) and (not yforward)):
                nowy -= 1 if yforward else -1

                yforward = not yforward

                nowz += 1 if zforward else -1

                if ((nowz > _sideLength) and (zforward)) or (
                    (nowz < 0) and (not zforward)
                ):
                    nowz -= 1 if zforward else -1
                    zforward = not zforward
                    _bytes += key[x][1]
                    nowx += 1
                else:

                    _bytes += key[z][int(zforward)]

            else:

                _bytes += key[y][int(yforward)]

        with open(f"{self.outputPath}/{self.midFileName}.bdx", "ab+") as f:
            f.write(brotli.compress(_bytes + b"XE"))

        return (True, _bytes, (nowx, maxheight, _sideLength))
