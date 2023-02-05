# -*- coding: utf-8 -*-


# 音·创 开发交流群 861684859
# Email EillesWan2006@163.com W-YI_DoctorYI@outlook.com EillesWan@outlook.com
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

import mido
import brotli
import json
import uuid
import shutil

from .utils import *
from .exceptions import *
from .instConstants import *

from typing import TypeVar, Union

T = TypeVar("T")  # Declare type variable
VM = TypeVar("VM", mido.MidiFile, None)  # void mido


class SingleNote:
    def __init__(
        self, instrument: int, pitch: int, velocity: int, startTime: int, lastTime: int
    ):
        """用于存储单个音符的类
        :param instrument 乐器编号
        :param pitch 音符编号
        :param velocity 力度/响度
        :param startTime 开始之时(ms)
            注：此处的时间是用从乐曲开始到当前的毫秒数
        :param lastTime 音符延续时间(ms)"""
        self.instrument: int = instrument
        """乐器编号"""
        self.note: int = pitch
        """音符编号"""
        self.velocity: int = velocity
        """力度/响度"""
        self.startTime: int = startTime
        """开始之时 ms"""
        self.lastTime: int = lastTime
        """音符持续时间 ms"""

    @property
    def inst(self):
        """乐器编号"""
        return self.instrument

    @inst.setter
    def inst(self, inst_):
        self.instrument = inst_

    @property
    def pitch(self):
        """音符编号"""
        return self.note

    def __str__(self):
        return (
            f"Note(inst = {self.inst}, pitch = {self.note}, velocity = {self.velocity}, "
            f"startTime = {self.startTime}, lastTime = {self.lastTime}, )"
        )

    def __tuple__(self):
        return self.inst, self.note, self.velocity, self.startTime, self.lastTime

    def __dict__(self):
        return {
            "inst": self.inst,
            "pitch": self.note,
            "velocity": self.velocity,
            "startTime": self.startTime,
            "lastTime": self.lastTime,
        }


class MethodList(list):
    def __init__(self, in_=()):
        super().__init__()
        self._T = [_x for _x in in_]

    def __getitem__(self, item) -> T:
        return self._T[item]
    
    def __len__(self) -> int:
        return self._T.__len__()


"""
学习笔记：
tempo:  microseconds per quarter note 毫秒每四分音符，换句话说就是一拍占多少毫秒
tick:  midi帧
ticks_per_beat:  帧每拍，即一拍多少帧

那么：

tick / ticks_per_beat => amount_of_beats 拍数(四分音符数)

tempo * amount_of_beats => 毫秒数

所以：

tempo * tick / ticks_per_beat => 毫秒数

###########

seconds per tick:
(tempo / 1000000.0) / ticks_per_beat

seconds:
tick * tempo / 1000000.0 / ticks_per_beat

microseconds:
tick * tempo / 1000.0 / ticks_per_beat

gameticks:
tick * tempo / 1000000.0 / ticks_per_beat * 一秒多少游戏刻


"""


class midiConvert:
    def __init__(self, debug: bool = False):
        """简单的midi转换类，将midi文件转换为我的世界结构或者包"""
        self.debugMode: bool = debug

        self.midiFile: str = ""
        self.midi: VM = None
        self.outputPath: str = ""
        self.midFileName: str = ""
        self.exeHead = ""
        self.methods = MethodList(
            [self._toCmdList_m1, self._toCmdList_m2, self._toCmdList_m3, self._toCmdList_m4]
        )

        self.methods_byDelay = MethodList(
            [
                self._toCmdList_withDelay_m1,
                self._toCmdList_withDelay_m2,
            ]
        )

    def convert(self, midiFile: str, outputPath: str, oldExeFormat: bool = True):
        """转换前需要先运行此函数来获取基本信息"""

        self.midiFile = midiFile
        """midi文件路径"""

        try:
            self.midi = mido.MidiFile(self.midiFile)
            """MidiFile对象"""
        except Exception as E:
            raise MidiDestroyedError(f"文件{self.midiFile}损坏：{E}")

        self.outputPath = os.path.abspath(outputPath)
        """输出路径"""
        # 将self.midiFile的文件名，不含路径且不含后缀存入self.midiFileName
        self.midFileName = os.path.splitext(os.path.basename(self.midiFile))[0]
        """文件名，不含路径且不含后缀"""

        self.exeHead = (
            "execute {} ~ ~ ~ "
            if oldExeFormat
            else "execute as {} at @s positioned ~ ~ ~ run "
        )
        """execute指令的应用，两个版本提前决定。"""

    @staticmethod
    def __Inst2soundID_withX(instrumentID):
        """返回midi的乐器ID对应的我的世界乐器名，对于音域转换算法，如下：
            2**( ( msg.note - 60 - X ) / 12 ) 即为MC的音高，其中
            X的取值随乐器不同而变化：
            竖琴harp、电钢琴pling、班卓琴banjo、方波bit、颤音琴iron_xylophone 的时候为6
            吉他的时候为7
            贝斯bass、迪吉里杜管didgeridoo的时候为8
            长笛flute、牛铃cou_bell的时候为5
            钟琴bell、管钟chime、木琴xylophone的时候为4
            而存在一些打击乐器bd(basedrum)、hat、snare，没有音域，则没有X，那么我们返回7即可
        :param instrumentID: midi的乐器ID
        default: 如果instrumentID不在范围内，返回的默认我的世界乐器名称
        :return: (str我的世界乐器名, int转换算法中的X)"""
        try:
            return pitched_instrument_list[instrumentID]
        except KeyError:
            return "note.flute", 5

    @staticmethod
    def __bitInst2ID_withX(instrumentID):
        try:
            return percussion_instrument_list[instrumentID]
        except KeyError:
            print("WARN", "无法使用打击乐器列表库，可能是不支持当前环境，打击乐器使用Dislink算法代替。")
            if instrumentID == 55:
                return "note.cow_bell", 5
            elif instrumentID in [41, 43, 45]:
                return "note.hat", 7
            elif instrumentID in [36, 37, 39]:
                return "note.snare", 7
            else:
                return "note.bd", 7

    @staticmethod
    def score2time(score: int):
        return str(int(int(score / 20) / 60)) + ":" + str(int(int(score / 20) % 60))

    def __formProgressBar(
        self,
        maxscore: int,
        scoreboard_name: str,
        progressbar: tuple = (
            r"▶ %%N [ %%s/%^s %%% __________ %%t|%^t ]",
            ("§e=§r", "§7=§r"),
        ),
    ) -> list:

        pgs_style = progressbar[0]
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
        perEach = maxscore / pgs_style.count("_")

        result = []

        if r"%^s" in pgs_style:
            pgs_style = pgs_style.replace(r"%^s", str(maxscore))

        if r"%^t" in pgs_style:
            pgs_style = pgs_style.replace(r"%^t", self.score2time(maxscore))

        sbn_pc = scoreboard_name[:2]
        if r"%%%" in pgs_style:
            result.append(
                'scoreboard objectives add {}PercT dummy "百分比计算"'.format(sbn_pc)
            )
            result.append(
                self.exeHead.format("@a[scores={" + scoreboard_name + "=1..}]")
                + "scoreboard players set MaxScore {} {}".format(
                    scoreboard_name, maxscore
                )
            )
            result.append(
                self.exeHead.format("@a[scores={" + scoreboard_name + "=1..}]")
                + "scoreboard players set n100 {} 100".format(scoreboard_name)
            )
            result.append(
                self.exeHead.format("@a[scores={" + scoreboard_name + "=1..}]")
                + "scoreboard players operation @s {} = @s {}".format(
                    sbn_pc + "PercT", scoreboard_name
                )
            )
            result.append(
                self.exeHead.format("@a[scores={" + scoreboard_name + "=1..}]")
                + "scoreboard players operation @s {} *= n100 {}".format(
                    sbn_pc + "PercT", scoreboard_name
                )
            )
            result.append(
                self.exeHead.format("@a[scores={" + scoreboard_name + "=1..}]")
                + "scoreboard players operation @s {} /= MaxScore {}".format(
                    sbn_pc + "PercT", scoreboard_name
                )
            )

        if r"%%t" in pgs_style:
            result.append(
                'scoreboard objectives add {}TMinT dummy "时间计算：分"'.format(sbn_pc)
            )
            result.append(
                'scoreboard objectives add {}TSecT dummy "时间计算：秒"'.format(sbn_pc)
            )
            result.append(
                self.exeHead.format("@a[scores={" + scoreboard_name + "=1..}]")
                + "scoreboard players set n20 {} 20".format(scoreboard_name)
            )
            result.append(
                self.exeHead.format("@a[scores={" + scoreboard_name + "=1..}]")
                + "scoreboard players set n60 {} 60".format(scoreboard_name)
            )

            result.append(
                self.exeHead.format("@a[scores={" + scoreboard_name + "=1..}]")
                + "scoreboard players operation @s {} = @s {}".format(
                    sbn_pc + "TMinT", scoreboard_name
                )
            )
            result.append(
                self.exeHead.format("@a[scores={" + scoreboard_name + "=1..}]")
                + "scoreboard players operation @s {} /= n20 {}".format(
                    sbn_pc + "TMinT", scoreboard_name
                )
            )
            result.append(
                self.exeHead.format("@a[scores={" + scoreboard_name + "=1..}]")
                + "scoreboard players operation @s {} /= n60 {}".format(
                    sbn_pc + "TMinT", scoreboard_name
                )
            )

            result.append(
                self.exeHead.format("@a[scores={" + scoreboard_name + "=1..}]")
                + "scoreboard players operation @s {} = @s {}".format(
                    sbn_pc + "TSecT", scoreboard_name
                )
            )
            result.append(
                self.exeHead.format("@a[scores={" + scoreboard_name + "=1..}]")
                + "scoreboard players operation @s {} /= n20 {}".format(
                    sbn_pc + "TSecT", scoreboard_name
                )
            )
            result.append(
                self.exeHead.format("@a[scores={" + scoreboard_name + "=1..}]")
                + "scoreboard players operation @s {} %= n60 {}".format(
                    sbn_pc + "TSecT", scoreboard_name
                )
            )

        for i in range(pgs_style.count("_")):
            npg_stl = (
                pgs_style.replace("_", progressbar[1][0], i + 1)
                .replace("_", progressbar[1][1])
                .replace(r"%%N", self.midFileName)
                if r"%%N" in pgs_style
                else pgs_style.replace("_", progressbar[1][0], i + 1).replace(
                    "_", progressbar[1][1]
                )
            )
            if r"%%s" in npg_stl:
                npg_stl = npg_stl.replace(
                    r"%%s",
                    '"},{"score":{"name":"*","objective":"'
                    + scoreboard_name
                    + '"}},{"text":"',
                )
            if r"%%%" in npg_stl:
                npg_stl = npg_stl.replace(
                    r"%%%",
                    r'"},{"score":{"name":"*","objective":"'
                    + sbn_pc
                    + r'PercT"}},{"text":"%',
                )
            if r"%%t" in npg_stl:
                npg_stl = npg_stl.replace(
                    r"%%t",
                    r'"},{"score":{"name":"*","objective":"{-}TMinT"}},{"text":":"},'
                    r'{"score":{"name":"*","objective":"{-}TSecT"}},{"text":"'.replace(
                        r"{-}", sbn_pc
                    ),
                )
            result.append(
                self.exeHead.format(
                    r"@a[scores={"
                    + scoreboard_name
                    + f"={int(i * perEach)}..{math.ceil((i + 1) * perEach)}"
                    + r"}]"
                )
                + r'titleraw @s actionbar {"rawtext":[{"text":"'
                + npg_stl
                + r'"}]}'
            )

        if r"%%%" in pgs_style:
            result.append("scoreboard objectives remove {}PercT".format(sbn_pc))
        if r"%%t" in pgs_style:
            result.append("scoreboard objectives remove {}TMinT".format(sbn_pc))
            result.append("scoreboard objectives remove {}TSecT".format(sbn_pc))

        return result

    def _toCmdList_m1(
        self,
        scoreboard_name: str = "mscplay",
        MaxVolume: float = 1.0,
        speed: float = 1.0,
    ) -> list:
        """
        使用Dislink Sforza的转换思路，将midi转换为我的世界命令列表
        :param scoreboard_name: 我的世界的计分板名称
        :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
        :return: tuple(命令列表, 命令个数, 计分板最大值)
        """
        # :param volume: 音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
        tracks = []
        if speed == 0:
            if self.debugMode:
                raise ZeroSpeedError("播放速度仅可为正实数")
            speed = 1
        MaxVolume = 1 if MaxVolume > 1 else (0.001 if MaxVolume <= 0 else MaxVolume)

        commands = 0
        maxscore = 0

        # 分轨的思路其实并不好，但这个算法就是这样
        # 所以我建议用第二个方法 _toCmdList_m2
        for i, track in enumerate(self.midi.tracks):

            ticks = 0
            instrumentID = 0
            singleTrack = []

            for msg in track:
                ticks += msg.time
                if msg.is_meta:
                    if msg.type == "set_tempo":
                        tempo = msg.tempo
                else:
                    if msg.type == "program_change":
                        instrumentID = msg.program

                    if msg.type == "note_on" and msg.velocity != 0:
                        try:
                            nowscore = round(
                                (ticks * tempo)
                                / ((self.midi.ticks_per_beat * float(speed)) * 50000)
                            )
                        except NameError:
                            raise NotDefineTempoError("计算当前分数时出错 未定义参量 Tempo")
                        maxscore = max(maxscore, nowscore)
                        if msg.channel == 9:
                            soundID, _X = self.__bitInst2ID_withX(instrumentID)
                        else:
                            soundID, _X = self.__Inst2soundID_withX(instrumentID)

                        singleTrack.append(
                            "execute @a[scores={"
                            + str(scoreboard_name)
                            + "="
                            + str(nowscore)
                            + "}"
                            + f"] ~ ~ ~ playsound {soundID} @s ^ ^ ^{1 / MaxVolume - 1} {msg.velocity / 128} "
                            f"{2 ** ((msg.note - 60 - _X) / 12)}"
                        )
                        commands += 1
            if len(singleTrack) != 0:
                tracks.append(singleTrack)

        return [tracks, commands, maxscore]

    # 原本这个算法的转换效果应该和上面的算法相似的
    def _toCmdList_m2(
        self,
        scoreboard_name: str = "mscplay",
        MaxVolume: float = 1.0,
        speed: float = 1.0,
    ) -> list:
        """
        使用神羽和金羿的转换思路，将midi转换为我的世界命令列表
        :param scoreboard_name: 我的世界的计分板名称
        :param MaxVolume: 音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
        :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
        :return: tuple(命令列表, 命令个数, 计分板最大值)
        """

        if speed == 0:
            if self.debugMode:
                raise ZeroSpeedError("播放速度仅可为正实数")
            speed = 1
        MaxVolume = 1 if MaxVolume > 1 else (0.001 if MaxVolume <= 0 else MaxVolume)

        # 一个midi中仅有16个通道 我们通过通道来识别而不是音轨
        channels = {
            0: [],
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
            7: [],
            8: [],
            9: [],
            10: [],
            11: [],
            12: [],
            13: [],
            14: [],
            15: [],
            16: [],
        }

        microseconds = 0

        # 我们来用通道统计音乐信息
        for msg in self.midi:
            # try:
            microseconds += msg.time * 1000  # 任何人都tm不要动这里，这里循环方式不是track，所以，这里的计时方式不一样
                # print(microseconds)
            # except NameError:
            #     if self.debugMode:
            #         raise NotDefineTempoError("计算当前分数时出错 未定义参量 Tempo")
            #     else:
            #         microseconds += (
            #             msg.time * 1000  # 任何人都tm不要动这里，这里循环方式不是track，所以，这里的计时方式不一样
            #         )

            # if msg.is_meta:
            #     if msg.type == "set_tempo":
            #         tempo = msg.tempo
            # else:
            if not msg.is_meta:
                if self.debugMode:
                    try:
                        if msg.channel > 15:
                            raise ChannelOverFlowError(f"当前消息 {msg} 的通道超限(≤15)")
                    except AttributeError:
                        pass

                if msg.type == "program_change":
                    channels[msg.channel].append(("PgmC", msg.program, microseconds))

                elif msg.type == "note_on" and msg.velocity != 0:
                    channels[msg.channel].append(
                        ("NoteS", msg.note, msg.velocity, microseconds)
                    )

                elif (msg.type == "note_on" and msg.velocity == 0) or (
                    msg.type == "note_off"
                ):
                    channels[msg.channel].append(("NoteE", msg.note, microseconds))

        """整合后的音乐通道格式
        每个通道包括若干消息元素其中逃不过这三种：

        1 切换乐器消息
        ("PgmC", 切换后的乐器ID: int, 距离演奏开始的毫秒)

        2 音符开始消息
        ("NoteS", 开始的音符ID, 力度（响度）, 距离演奏开始的毫秒)

        3 音符结束消息
        ("NoteS", 结束的音符ID, 距离演奏开始的毫秒)"""

        tracks = []
        cmdAmount = 0
        maxScore = 0

        # 此处 我们把通道视为音轨
        for i in channels.keys():
            # 如果当前通道为空 则跳过
            if not channels[i]:
                continue

            if i == 9:
                SpecialBits = True
            else:
                SpecialBits = False

            nowTrack = []

            for msg in channels[i]:

                if msg[0] == "PgmC":
                    InstID = msg[1]

                elif msg[0] == "NoteS":
                    try:
                        soundID, _X = (
                            self.__bitInst2ID_withX(InstID)
                            if SpecialBits
                            else self.__Inst2soundID_withX(InstID)
                        )
                    except UnboundLocalError as E:
                        if self.debugMode:
                            raise NotDefineProgramError(f"未定义乐器便提前演奏。\n{E}")
                        else:
                            soundID, _X = (
                                self.__bitInst2ID_withX(-1)
                                if SpecialBits
                                else self.__Inst2soundID_withX(-1)
                            )
                    score_now = round(msg[-1] / float(speed) / 50)
                    maxScore = max(maxScore, score_now)

                    nowTrack.append(
                        self.exeHead.format(
                            "@a[scores=({}={})]".format(scoreboard_name, score_now)
                            .replace("(", r"{")
                            .replace(")", r"}")
                        )
                        + f"playsound {soundID} @s ^ ^ ^{1 / MaxVolume - 1} {msg[2] / 128} "
                        f"{2 ** ((msg[1] - 60 - _X) / 12)}"
                    )

                    cmdAmount += 1

            if nowTrack:
                tracks.append(nowTrack)

        return [tracks, cmdAmount, maxScore]

    def _toCmdList_m3(
        self,
        scoreboard_name: str = "mscplay",
        MaxVolume: float = 1.0,
        speed: float = 1.0,
    ) -> list:
        """
        使用金羿的转换思路，将midi转换为我的世界命令列表
        :param scoreboard_name: 我的世界的计分板名称
        :param MaxVolume: 音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
        :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
        :return: tuple(命令列表, 命令个数, 计分板最大值)
        """

        if speed == 0:
            if self.debugMode:
                raise ZeroSpeedError("播放速度仅可为正实数")
            speed = 1
        MaxVolume = 1 if MaxVolume > 1 else (0.001 if MaxVolume <= 0 else MaxVolume)

        # 一个midi中仅有16个通道 我们通过通道来识别而不是音轨
        channels = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}, 8: {}, 9: {}, 10: {}, 11: {}, 12: {}, 13: {}, 14: {}, 15: {}, 16: {}}

        # 我们来用通道统计音乐信息
        # 但是是用分轨的思路的
        for track_no, track in enumerate(self.midi.tracks):
            
            microseconds = 0

            for msg in track:

                if msg.time != 0:
                    try:
                        microseconds += msg.time * tempo / self.midi.ticks_per_beat
                        # print(microseconds)
                    except NameError:
                        if self.debugMode:
                            raise NotDefineTempoError("计算当前分数时出错 未定义参量 Tempo")
                        else:
                            microseconds += (msg.time * mido.midifiles.midifiles.DEFAULT_TEMPO / self.midi.ticks_per_beat)

                if msg.is_meta:
                    if msg.type == "set_tempo":
                        tempo = msg.tempo
                        if self.debugMode:
                            self.prt(f"TEMPO更改：{tempo}（毫秒每拍）")
                else:

                    if self.debugMode:
                        try:
                            if msg.channel > 15:
                                raise ChannelOverFlowError(f"当前消息 {msg} 的通道超限(≤15)")
                        except AttributeError:
                            pass
                    
                    if not track_no in channels[msg.channel].keys():
                        channels[msg.channel][track_no] = []
                    if msg.type == "program_change":
                        channels[msg.channel][track_no].append(("PgmC", msg.program, microseconds))

                    elif msg.type == "note_on" and msg.velocity != 0:
                        channels[msg.channel][track_no].append(
                            ("NoteS", msg.note, msg.velocity, microseconds)
                        )

                    elif (msg.type == "note_on" and msg.velocity == 0) or (
                        msg.type == "note_off"
                    ):
                        channels[msg.channel][track_no].append(("NoteE", msg.note, microseconds))

        """整合后的音乐通道格式
        每个通道包括若干消息元素其中逃不过这三种：

        1 切换乐器消息
        ("PgmC", 切换后的乐器ID: int, 距离演奏开始的毫秒)

        2 音符开始消息
        ("NoteS", 开始的音符ID, 力度（响度）, 距离演奏开始的毫秒)

        3 音符结束消息
        ("NoteS", 结束的音符ID, 距离演奏开始的毫秒)"""

        tracks = []
        cmdAmount = 0
        maxScore = 0

        # 此处 我们把通道视为音轨
        for i in channels.keys():
            # 如果当前通道为空 则跳过
            if not channels[i]:
                continue
            
            # 第十通道是打击乐通道
            SpecialBits = True if i == 9 else False

            # nowChannel = []

            for track_no,track in channels[i].items():

                nowTrack = []

                for msg in track:
                    if msg[0] == "PgmC":
                        InstID = msg[1]

                    elif msg[0] == "NoteS":
                        try:
                            soundID, _X = (
                                self.__bitInst2ID_withX(InstID)
                                if SpecialBits
                                else self.__Inst2soundID_withX(InstID)
                            )
                        except UnboundLocalError as E:
                            if self.debugMode:
                                raise NotDefineProgramError(f"未定义乐器便提前演奏。\n{E}")
                            else:
                                soundID, _X = (
                                    self.__bitInst2ID_withX(-1)
                                    if SpecialBits
                                    else self.__Inst2soundID_withX(-1)
                                )
                        score_now = round(msg[-1] / float(speed) / 50)
                        maxScore = max(maxScore, score_now)

                        nowTrack.append(
                            self.exeHead.format(
                                "@a[scores=({}={})]".format(scoreboard_name, score_now)
                                .replace("(", r"{")
                                .replace(")", r"}")
                            )
                            + f"playsound {soundID} @s ^ ^ ^{1 / MaxVolume - 1} {msg[2] / 128} "
                            f"{2 ** ((msg[1] - 60 - _X) / 12)}"
                        )

                        cmdAmount += 1

                if nowTrack:
                    tracks.append(nowTrack)

        return [tracks, cmdAmount, maxScore]

    # 简单的单音填充
    def _toCmdList_m4(
        self,
        scoreboard_name: str = "mscplay",
        MaxVolume: float = 1.0,
        speed: float = 1.0,
    ) -> list:
        """
        使用金羿的转换思路，将midi转换为我的世界命令列表，并使用完全填充算法优化音感
        :param scoreboard_name: 我的世界的计分板名称
        :param MaxVolume: 音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
        :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
        :return: tuple(命令列表, 命令个数, 计分板最大值)
        """
        # TODO: 这里的时间转换不知道有没有问题

        if speed == 0:
            if self.debugMode:
                raise ZeroSpeedError("播放速度仅可为正实数")
            speed = 1
        MaxVolume = 1 if MaxVolume > 1 else (0.001 if MaxVolume <= 0 else MaxVolume)

        # 一个midi中仅有16个通道 我们通过通道来识别而不是音轨
        channels = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

        # 我们来用通道统计音乐信息
        for i, track in enumerate(self.midi.tracks):

            microseconds = 0

            for msg in track:

                if msg.time != 0:
                    try:
                        microseconds += msg.time * tempo / self.midi.ticks_per_beat
                    except NameError:
                        raise NotDefineTempoError("计算当前分数时出错 未定义参量 Tempo")

                if msg.is_meta:
                    if msg.type == "set_tempo":
                        tempo = msg.tempo
                else:

                    if self.debugMode:
                        try:
                            if msg.channel > 15:
                                raise ChannelOverFlowError(f"当前消息 {msg} 的通道超限(≤15)")
                        except AttributeError:
                            pass

                    if msg.type == "program_change":
                        channels[msg.channel].append(
                            ("PgmC", msg.program, microseconds)
                        )

                    elif msg.type == "note_on" and msg.velocity != 0:
                        channels[msg.channel].append(
                            ("NoteS", msg.note, msg.velocity, microseconds)
                        )

                    elif (msg.type == "note_on" and msg.velocity == 0) or (
                        msg.type == "note_off"
                    ):
                        channels[msg.channel].append(("NoteE", msg.note, microseconds))

        """整合后的音乐通道格式
        每个通道包括若干消息元素其中逃不过这三种：

        1 切换乐器消息

        ("PgmC", 切换后的乐器ID: int, 距离演奏开始的毫秒)

        2 音符开始消息

        ("NoteS", 开始的音符ID, 力度（响度）, 距离演奏开始的毫秒)

        3 音符结束消息

        ("NoteS", 结束的音符ID, 距离演奏开始的毫秒)"""

        note_channels = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

        # 此处 我们把通道视为音轨
        for i in range(len(channels)):
            # 如果当前通道为空 则跳过

            noteMsgs = []
            MsgIndex = []

            for msg in channels[i]:

                if msg[0] == "PgmC":
                    InstID = msg[1]

                elif msg[0] == "NoteS":
                    noteMsgs.append(msg[1:])
                    MsgIndex.append(msg[1])

                elif msg[0] == "NoteE":
                    if msg[1] in MsgIndex:
                        note_channels[i].append(
                            SingleNote(
                                InstID,
                                msg[1],
                                noteMsgs[MsgIndex.index(msg[1])][1],
                                noteMsgs[MsgIndex.index(msg[1])][2],
                                msg[-1] - noteMsgs[MsgIndex.index(msg[1])][2],
                            )
                        )
                        noteMsgs.pop(MsgIndex.index(msg[1]))
                        MsgIndex.pop(MsgIndex.index(msg[1]))

        tracks = []
        cmdAmount = 0
        maxScore = 0
        CheckFirstChannel = False

        # 临时用的插值计算函数
        def _linearFun(_note: SingleNote) -> list:
            """传入音符数据，返回以半秒为分割的插值列表
            :param _note: SingleNote 音符
            :return list[tuple(int开始时间（毫秒）, int乐器, int音符, int力度（内置）, float音量（播放）),]"""

            result = []

            totalCount = int(_note.lastTime / 500)

            for _i in range(totalCount):
                result.append(
                    (
                        _note.startTime + _i * 500,
                        _note.instrument,
                        _note.pitch,
                        _note.velocity,
                        MaxVolume * ((totalCount - _i) / totalCount),
                    )
                )

            return result

        # 此处 我们把通道视为音轨
        for track in note_channels:
            # 如果当前通道为空 则跳过
            if not track:
                continue

            if note_channels.index(track) == 0:
                CheckFirstChannel = True
                SpecialBits = False
            elif note_channels.index(track) == 9:
                SpecialBits = True
            else:
                CheckFirstChannel = False
                SpecialBits = False

            nowTrack = []

            for note in track:

                for every_note in _linearFun(note):
                    # 应该是计算的时候出了点小问题
                    # 我们应该用一个MC帧作为时间单位而不是半秒

                    if SpecialBits:
                        soundID, _X = self.__bitInst2ID_withX(InstID)
                    else:
                        soundID, _X = self.__Inst2soundID_withX(InstID)

                    score_now = round(every_note[0] / speed / 50000)

                    maxScore = max(maxScore, score_now)

                    nowTrack.append(
                        "execute @a[scores={"
                        + str(scoreboard_name)
                        + "="
                        + str(score_now)
                        + "}"
                        + f"] ~ ~ ~ playsound {soundID} @s ~ ~{1 / every_note[4] - 1} ~ "
                        f"{note.velocity * (0.7 if CheckFirstChannel else 0.9)} {2 ** ((note.pitch - 60 - _X) / 12)}"
                    )

                    cmdAmount += 1
            tracks.append(nowTrack)

        return [tracks, cmdAmount, maxScore]

    def _toCmdList_withDelay_m1(
        self,
        MaxVolume: float = 1.0,
        speed: float = 1.0,
        player: str = "@a",
    ) -> list:
        """
        使用Dislink Sforza的转换思路，将midi转换为我的世界命令列表，并输出每个音符之后的延迟
        :param MaxVolume: 最大播放音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
        :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
        :param player: 玩家选择器，默认为`@a`
        :return: 全部指令列表[ ( str指令, int距离上一个指令的延迟 ),...]
        """
        tracks = {}

        if speed == 0:
            if self.debugMode:
                raise ZeroSpeedError("播放速度仅可为正实数")
            speed = 1

        MaxVolume = 1 if MaxVolume > 1 else (0.001 if MaxVolume <= 0 else MaxVolume)

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
                        now_tick = round(
                            (ticks * tempo)
                            / ((self.midi.ticks_per_beat * float(speed)) * 50000)
                        )
                        soundID, _X = self.__Inst2soundID_withX(instrumentID)
                        try:
                            tracks[now_tick].append(
                                self.exeHead.format(player)
                                + f"playsound {soundID} @s ^ ^ ^{1 / MaxVolume - 1} {msg.velocity / 128} "
                                f"{2 ** ((msg.note - 60 - _X) / 12)}"
                            )
                        except KeyError:
                            tracks[now_tick] = [
                                self.exeHead.format(player)
                                + f"playsound {soundID} @s ^ ^ ^{1 / MaxVolume - 1} {msg.velocity / 128} "
                                f"{2 ** ((msg.note - 60 - _X) / 12)}"
                            ]

        results = []

        all_ticks = list(tracks.keys())

        for i in range(len(all_ticks)):
            if i != 0:
                for j in range(len(tracks[all_ticks[i]])):
                    if j != 0:
                        results.append((tracks[all_ticks[i]][j], 0))
                    else:
                        results.append(
                            (tracks[all_ticks[i]][j], all_ticks[i] - all_ticks[i - 1])
                        )
            else:
                for j in range(len(tracks[all_ticks[i]])):
                    results.append((tracks[all_ticks[i]][j], all_ticks[i]))

        return [results, max(all_ticks)]

    def _toCmdList_withDelay_m2(
        self,
        MaxVolume: float = 1.0,
        speed: float = 1.0,
        player: str = "@a",
    ) -> list:
        """
        使用神羽和金羿的转换思路，将midi转换为我的世界命令列表，并输出每个音符之后的延迟
        :param MaxVolume: 最大播放音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
        :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
        :param player: 玩家选择器，默认为`@a`
        :return: 全部指令列表[ ( str指令, int距离上一个指令的延迟 ),...]
        """
        tracks = {}
        if speed == 0:
            if self.debugMode:
                raise ZeroSpeedError("播放速度仅可为正实数")
            speed = 1

        MaxVolume = 1 if MaxVolume > 1 else (0.001 if MaxVolume <= 0 else MaxVolume)

        # 一个midi中仅有16个通道 我们通过通道来识别而不是音轨
        channels = {
            0: [],
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
            7: [],
            8: [],
            9: [],
            10: [],
            11: [],
            12: [],
            13: [],
            14: [],
            15: [],
            16: [],
        }

        microseconds = 0

        # 我们来用通道统计音乐信息
        for msg in self.midi:
            try:
                microseconds += msg.time * 1000  # 任何人都tm不要动这里，这里循环方式不是track，所以，这里的计时方式不一样

                # print(microseconds)
            except NameError:
                if self.debugMode:
                    raise NotDefineTempoError("计算当前分数时出错 未定义参量 Tempo")
                else:
                    microseconds += msg.time * 1000  # 任何人都tm不要动这里，这里循环方式不是track，所以，这里的计时方式不一样

            if msg.is_meta:
                if msg.type == "set_tempo":
                    tempo = msg.tempo
            else:

                if self.debugMode:
                    try:
                        if msg.channel > 15:
                            raise ChannelOverFlowError(f"当前消息 {msg} 的通道超限(≤15)")
                    except AttributeError:
                        pass

                if msg.type == "program_change":
                    channels[msg.channel].append(("PgmC", msg.program, microseconds))

                elif msg.type == "note_on" and msg.velocity != 0:
                    channels[msg.channel].append(
                        ("NoteS", msg.note, msg.velocity, microseconds)
                    )

                elif (msg.type == "note_on" and msg.velocity == 0) or (
                    msg.type == "note_off"
                ):
                    channels[msg.channel].append(("NoteE", msg.note, microseconds))

        """整合后的音乐通道格式
        每个通道包括若干消息元素其中逃不过这三种：

        1 切换乐器消息
        ("PgmC", 切换后的乐器ID: int, 距离演奏开始的毫秒)

        2 音符开始消息
        ("NoteS", 开始的音符ID, 力度（响度）, 距离演奏开始的毫秒)

        3 音符结束消息
        ("NoteS", 结束的音符ID, 距离演奏开始的毫秒)"""

        results = []

        for i in channels.keys():
            # 如果当前通道为空 则跳过
            if not channels[i]:
                continue

            if i == 9:
                SpecialBits = True
            else:
                SpecialBits = False

            for msg in channels[i]:

                if msg[0] == "PgmC":
                    InstID = msg[1]

                elif msg[0] == "NoteS":
                    try:
                        soundID, _X = (
                            self.__bitInst2ID_withX(InstID)
                            if SpecialBits
                            else self.__Inst2soundID_withX(InstID)
                        )
                    except UnboundLocalError as E:
                        if self.debugMode:
                            raise NotDefineProgramError(f"未定义乐器便提前演奏。\n{E}")
                        else:
                            soundID, _X = (
                                self.__bitInst2ID_withX(-1)
                                if SpecialBits
                                else self.__Inst2soundID_withX(-1)
                            )
                    score_now = round(msg[-1] / float(speed) / 50)

                    try:
                        tracks[score_now].append(
                            self.exeHead.format(player)
                            + f"playsound {soundID} @s ^ ^ ^{1 / MaxVolume - 1} {msg[2] / 128} "
                            f"{2 ** ((msg[1] - 60 - _X) / 12)}"
                        )
                    except KeyError:
                        tracks[score_now] = [
                            self.exeHead.format(player)
                            + f"playsound {soundID} @s ^ ^ ^{1 / MaxVolume - 1} {msg[2] / 128} "
                            f"{2 ** ((msg[1] - 60 - _X) / 12)}"
                        ]

        all_ticks = list(tracks.keys())

        for i in range(len(all_ticks)):
            for j in range(len(tracks[all_ticks[i]])):
                results.append(
                    (
                        tracks[all_ticks[i]][j],
                        (
                            0
                            if j != 0
                            else (
                                all_ticks[i] - all_ticks[i - 1]
                                if i != 0
                                else all_ticks[i]
                            )
                        ),
                    )
                )

        return [results, max(all_ticks)]

    def _toCmdList_withDelay_m3(
        self,
        MaxVolume: float = 1.0,
        speed: float = 1.0,
        player: str = "@a",
    ) -> list:
        """
        使用金羿的转换思路，将midi转换为我的世界命令列表，并输出每个音符之后的延迟
        :param MaxVolume: 最大播放音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
        :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
        :param player: 玩家选择器，默认为`@a`
        :return: 全部指令列表[ ( str指令, int距离上一个指令的延迟 ),...]
        """
        
        if speed == 0:
            if self.debugMode:
                raise ZeroSpeedError("播放速度仅可为正实数")
            speed = 1
        MaxVolume = 1 if MaxVolume > 1 else (0.001 if MaxVolume <= 0 else MaxVolume)

        # 一个midi中仅有16个通道 我们通过通道来识别而不是音轨
        channels = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}, 8: {}, 9: {}, 10: {}, 11: {}, 12: {}, 13: {}, 14: {}, 15: {}, 16: {}}

        # 我们来用通道统计音乐信息
        # 但是是用分轨的思路的
        for track_no, track in enumerate(self.midi.tracks):
            
            microseconds = 0

            for msg in track:

                if msg.time != 0:
                    try:
                        microseconds += msg.time * tempo / self.midi.ticks_per_beat
                        # print(microseconds)
                    except NameError:
                        if self.debugMode:
                            raise NotDefineTempoError("计算当前分数时出错 未定义参量 Tempo")
                        else:
                            microseconds += (msg.time * mido.midifiles.midifiles.DEFAULT_TEMPO / self.midi.ticks_per_beat)

                if msg.is_meta:
                    if msg.type == "set_tempo":
                        tempo = msg.tempo
                        if self.debugMode:
                            self.prt(f"TEMPO更改：{tempo}（毫秒每拍）")
                else:

                    if self.debugMode:
                        try:
                            if msg.channel > 15:
                                raise ChannelOverFlowError(f"当前消息 {msg} 的通道超限(≤15)")
                        except AttributeError:
                            pass
                    
                    if not track_no in channels[msg.channel].keys():
                        channels[msg.channel][track_no] = []
                    if msg.type == "program_change":
                        channels[msg.channel][track_no].append(("PgmC", msg.program, microseconds))

                    elif msg.type == "note_on" and msg.velocity != 0:
                        channels[msg.channel][track_no].append(
                            ("NoteS", msg.note, msg.velocity, microseconds)
                        )

                    elif (msg.type == "note_on" and msg.velocity == 0) or (
                        msg.type == "note_off"
                    ):
                        channels[msg.channel][track_no].append(("NoteE", msg.note, microseconds))

        """整合后的音乐通道格式
        每个通道包括若干消息元素其中逃不过这三种：

        1 切换乐器消息
        ("PgmC", 切换后的乐器ID: int, 距离演奏开始的毫秒)

        2 音符开始消息
        ("NoteS", 开始的音符ID, 力度（响度）, 距离演奏开始的毫秒)

        3 音符结束消息
        ("NoteS", 结束的音符ID, 距离演奏开始的毫秒)"""

        tracks = {}

        # 此处 我们把通道视为音轨
        for i in channels.keys():
            # 如果当前通道为空 则跳过
            if not channels[i]:
                continue
            
            # 第十通道是打击乐通道
            SpecialBits = True if i == 9 else False

            # nowChannel = []

            for track_no,track in channels[i].items():

                for msg in track:

                    if msg[0] == "PgmC":
                        InstID = msg[1]

                    elif msg[0] == "NoteS":
                        try:
                            soundID, _X = (
                                self.__bitInst2ID_withX(InstID)
                                if SpecialBits
                                else self.__Inst2soundID_withX(InstID)
                            )
                        except UnboundLocalError as E:
                            if self.debugMode:
                                raise NotDefineProgramError(f"未定义乐器便提前演奏。\n{E}")
                            else:
                                soundID, _X = (
                                    self.__bitInst2ID_withX(-1)
                                    if SpecialBits
                                    else self.__Inst2soundID_withX(-1)
                                )
                        score_now = round(msg[-1] / float(speed) / 50)

                        try:
                            tracks[score_now].append(
                                self.exeHead.format(player)
                                + f"playsound {soundID} @s ^ ^ ^{1 / MaxVolume - 1} {msg[2] / 128} "
                                f"{2 ** ((msg[1] - 60 - _X) / 12)}"
                            )
                        except KeyError:
                            tracks[score_now] = [
                                self.exeHead.format(player)
                                + f"playsound {soundID} @s ^ ^ ^{1 / MaxVolume - 1} {msg[2] / 128} "
                                f"{2 ** ((msg[1] - 60 - _X) / 12)}"
                            ]

        all_ticks = list(tracks.keys())
        results = []

        for i in range(len(all_ticks)):
            for j in range(len(tracks[all_ticks[i]])):
                results.append(
                    (
                        tracks[all_ticks[i]][j],
                        (0 if j != 0 else (all_ticks[i] - all_ticks[i - 1] if i != 0 else all_ticks[i])),
                    )
                )

        return [results, max(all_ticks)]

    def to_mcpack(
        self,
        method: int = 1,
        volume: float = 1.0,
        speed: float = 1.0,
        progressbar: Union[bool, tuple] = None,
        scoreboard_name: str = "mscplay",
        isAutoReset: bool = False,
    ) -> tuple:
        """
        使用method指定的转换算法，将midi转换为我的世界mcpack格式的包
        :param method: 转换算法
        :param isAutoReset: 是否自动重置计分板
        :param progressbar: 进度条，（当此参数为True时使用默认进度条，为其他的值为真的参数时识别为进度条自定义参数，为其他值为假的时候不生成进度条）
        :param scoreboard_name: 我的世界的计分板名称
        :param volume: 音量，注意：这里的音量范围为(0,1]，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
        :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
        :return 成功与否，成功返回(True,True)，失败返回(False,str失败原因)
        """

        # try:
        cmdlist, maxlen, maxscore = self.methods[method - 1](
            scoreboard_name, volume, speed
        )
        # except:
        #     return (False, f"无法找到算法ID{method}对应的转换算法")

        # 当文件f夹{self.outputPath}/temp/functions存在时清空其下所有项目，然后创建
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
        index_file = open(
            f"{self.outputPath}/temp/functions/index.mcfunction", "w", encoding="utf-8"
        )
        for track in cmdlist:
            index_file.write(
                "function mscplay/track" + str(cmdlist.index(track) + 1) + "\n"
            )
            with open(
                f"{self.outputPath}/temp/functions/mscplay/track{cmdlist.index(track) + 1}.mcfunction",
                "w",
                encoding="utf-8",
            ) as f:
                f.write("\n".join(track))
        index_file.writelines(
            (
                "scoreboard players add @a[scores={"
                + scoreboard_name
                + "=1..}] "
                + scoreboard_name
                + " 1\n",
                (
                    "scoreboard players reset @a[scores={"
                    + scoreboard_name
                    + "="
                    + str(maxscore + 20)
                    + "..}]"
                    + f" {scoreboard_name}\n"
                )
                if isAutoReset
                else "",
                f"function mscplay/progressShow\n" if progressbar else "",
            )
        )

        if progressbar:
            if progressbar:
                with open(
                    f"{self.outputPath}/temp/functions/mscplay/progressShow.mcfunction",
                    "w",
                    encoding="utf-8",
                ) as f:
                    f.writelines(
                        "\n".join(self.__formProgressBar(maxscore, scoreboard_name))
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
                                maxscore, scoreboard_name, progressbar
                            )
                        )
                    )

        index_file.close()

        if os.path.exists(f"{self.outputPath}/{self.midFileName}.mcpack"):
            os.remove(f"{self.outputPath}/{self.midFileName}.mcpack")
        compress_zipfile(
            f"{self.outputPath}/temp/", f"{self.outputPath}/{self.midFileName}.mcpack"
        )

        shutil.rmtree(f"{self.outputPath}/temp/")

        return True, maxlen, maxscore

    def to_BDX_file(
        self,
        method: int = 1,
        volume: float = 1.0,
        speed: float = 1.0,
        progressbar: Union[bool, tuple] = False,
        scoreboard_name: str = "mscplay",
        isAutoReset: bool = False,
        author: str = "Eilles",
        max_height: int = 64,
    ):
        """
        使用method指定的转换算法，将midi转换为BDX结构文件
        :param method: 转换算法
        :param author: 作者名称
        :param progressbar: 进度条，（当此参数为True时使用默认进度条，为其他的值为真的参数时识别为进度条自定义参数，为其他值为假的时候不生成进度条）
        :param max_height: 生成结构最大高度
        :param scoreboard_name: 我的世界的计分板名称
        :param volume: 音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
        :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
        :param isAutoReset: 是否自动重置计分板
        :return 成功与否，成功返回(True,未经过压缩的源,结构占用大小)，失败返回(False,str失败原因)
        """
        # try:
        cmdlist, total_count, maxScore = self.methods[method - 1](
            scoreboard_name, volume, speed
        )
        # except Exception as E:
        #     return (False, f"无法找到算法ID{method}对应的转换算法: {E}")

        if not os.path.exists(self.outputPath):
            os.makedirs(self.outputPath)

        with open(
            os.path.abspath(os.path.join(self.outputPath, f"{self.midFileName}.bdx")),
            "w+",
        ) as f:
            f.write("BD@")

        _bytes = (
            b"BDX\x00"
            + author.encode("utf-8")
            + b" & Musicreater\x00\x01command_block\x00"
        )

        commands = []

        for track in cmdlist:
            commands += track

        if isAutoReset:
            commands.append(
                "scoreboard players reset @a[scores={"
                + scoreboard_name
                + "="
                + str(maxScore + 20)
                + "}] "
                + scoreboard_name,
            )

        cmdBytes, size, finalPos = to_BDX_bytes(
            [(i, 0) for i in commands], max_height - 1
        )
        # 此处是对于仅有 True 的参数和自定义参数的判断
        if progressbar:
            pgbBytes, pgbSize, pgbNowPos = to_BDX_bytes(
                [
                    (i, 0)
                    for i in (
                        self.__formProgressBar(maxScore, scoreboard_name)
                        if progressbar
                        else self.__formProgressBar(
                            maxScore, scoreboard_name, progressbar
                        )
                    )
                ],
                max_height - 1,
            )
            _bytes += pgbBytes
            _bytes += move(y, -pgbNowPos[1])
            _bytes += move(z, -pgbNowPos[2])
            _bytes += move(x, 2)

            size[0] += 2 + pgbSize[0]
            size[1] = max(size[1], pgbSize[1])
            size[2] = max(size[2], pgbSize[2])

        _bytes += cmdBytes

        with open(
            os.path.abspath(os.path.join(self.outputPath, f"{self.midFileName}.bdx")),
            "ab+",
        ) as f:
            f.write(brotli.compress(_bytes + b"XE"))

        return True, total_count, maxScore, size, finalPos

    def to_BDX_file_with_delay(
        self,
        method: int = 1,
        volume: float = 1.0,
        speed: float = 1.0,
        progressbar: Union[bool, tuple] = False,
        player: str = "@a",
        author: str = "Eilles",
        max_height: int = 64,
    ):
        """
        使用method指定的转换算法，将midi转换为BDX结构文件
        :param method: 转换算法
        :param author: 作者名称
        :param progressbar: 进度条，（当此参数为True时使用默认进度条，为其他的值为真的参数时识别为进度条自定义参数，为其他值为假的时候不生成进度条）
        :param max_height: 生成结构最大高度
        :param volume: 音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
        :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
        :param player: 玩家选择器，默认为`@a`
        :return 成功与否，成功返回(True,未经过压缩的源,结构占用大小)，失败返回(False,str失败原因)
        """

        # try:
        cmdlist, max_delay = self.methods_byDelay[method - 1](
            volume,
            speed,
            player,
        )
        # except Exception as E:
        #     return (False, f"无法找到算法ID{method}对应的转换算法\n{E}")

        if not os.path.exists(self.outputPath):
            os.makedirs(self.outputPath)

        with open(
            os.path.abspath(os.path.join(self.outputPath, f"{self.midFileName}.bdx")),
            "w+",
        ) as f:
            f.write("BD@")

        _bytes = (
            b"BDX\x00"
            + author.encode("utf-8")
            + b" & Musicreater\x00\x01command_block\x00"
        )

        # 此处是对于仅有 True 的参数和自定义参数的判断
        if progressbar:
            progressbar = (
                r"▶ %%N [ %%s/%^s %%% __________ %%t|%^t ]",
                ("§e=§r", "§7=§r"),
            )

        cmdBytes, size, finalPos = to_BDX_bytes(cmdlist, max_height - 1)

        if progressbar:
            scb_name = self.midFileName[:5] + "Pgb"
            _bytes += form_command_block_in_BDX_bytes(
                r"scoreboard objectives add {} dummy {}播放用".replace(r"{}", scb_name),
                1,
                customName="初始化进度条",
            )
            _bytes += move(z, 2)
            _bytes += form_command_block_in_BDX_bytes(
                r"scoreboard players add {} {} 1".format(player, scb_name),
                1,
                1,
                customName="显示进度条并加分",
            )
            _bytes += move(y, 1)
            pgbBytes, pgbSize, pgbNowPos = to_BDX_bytes(
                [
                    (i, 0)
                    for i in self.__formProgressBar(max_delay, scb_name, progressbar)
                ],
                max_height - 1,
            )
            _bytes += pgbBytes
            _bytes += move(y, -1 - pgbNowPos[1])
            _bytes += move(z, -2 - pgbNowPos[2])
            _bytes += move(x, 2)
            _bytes += form_command_block_in_BDX_bytes(
                r"scoreboard players reset {} {}".format(player, scb_name),
                1,
                customName="置零进度条",
            )
            _bytes += move(y, 1)
            size[0] += 2 + pgbSize[0]
            size[1] = max(size[1], pgbSize[1])
            size[2] = max(size[2], pgbSize[2])

        size[1] += 1
        _bytes += cmdBytes

        with open(
            os.path.abspath(os.path.join(self.outputPath, f"{self.midFileName}.bdx")),
            "ab+",
        ) as f:
            f.write(brotli.compress(_bytes + b"XE"))

        return True, len(cmdlist), max_delay, size, finalPos

    def toDICT(
        self,
    ) -> dict:
        """
        使用金羿的转换思路，将midi转换为字典
        :return: dict()
        """

        # 一个midi中仅有16个通道 我们通过通道来识别而不是音轨
        channels = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}, 8: {}, 9: {}, 10: {}, 11: {}, 12: {}, 13: {}, 14: {}, 15: {}, 16: {}}

        # 我们来用通道统计音乐信息
        # 但是是用分轨的思路的
        for track_no, track in enumerate(self.midi.tracks):
            
            microseconds = 0

            for msg in track:

                if msg.time != 0:
                    try:
                        microseconds += msg.time * tempo / self.midi.ticks_per_beat
                        # print(microseconds)
                    except NameError:
                        if self.debugMode:
                            raise NotDefineTempoError("计算当前分数时出错 未定义参量 Tempo")
                        else:
                            microseconds += (msg.time * mido.midifiles.midifiles.DEFAULT_TEMPO / self.midi.ticks_per_beat)

                if msg.is_meta:
                    if msg.type == "set_tempo":
                        tempo = msg.tempo
                        if self.debugMode:
                            self.prt(f"TEMPO更改：{tempo}（毫秒每拍）")
                else:

                    if self.debugMode:
                        try:
                            if msg.channel > 15:
                                raise ChannelOverFlowError(f"当前消息 {msg} 的通道超限(≤15)")
                        except AttributeError:
                            pass
                    
                    if not track_no in channels[msg.channel].keys():
                        channels[msg.channel][track_no] = []
                    if msg.type == "program_change":
                        channels[msg.channel][track_no].append(("PgmC", msg.program, microseconds))

                    elif msg.type == "note_on" and msg.velocity != 0:
                        channels[msg.channel][track_no].append(
                            ("NoteS", msg.note, msg.velocity, microseconds)
                        )

                    elif (msg.type == "note_on" and msg.velocity == 0) or (
                        msg.type == "note_off"
                    ):
                        channels[msg.channel][track_no].append(("NoteE", msg.note, microseconds))

        """整合后的音乐通道格式
        每个通道包括若干消息元素其中逃不过这三种：

        1 切换乐器消息
        ("PgmC", 切换后的乐器ID: int, 距离演奏开始的毫秒)

        2 音符开始消息
        ("NoteS", 开始的音符ID, 力度（响度）, 距离演奏开始的毫秒)

        3 音符结束消息
        ("NoteS", 结束的音符ID, 距离演奏开始的毫秒)"""

        return channels
