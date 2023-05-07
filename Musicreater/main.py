# -*- coding: utf-8 -*-


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

import os
import math
import json
import shutil
import uuid
from typing import TypeVar, Union, Tuple

import mido

from .exceptions import *
from .constants import *
from .utils import *
from .subclass import *

VM = TypeVar("VM", mido.MidiFile, None)  # void mido
'''
空Midi类类型
'''

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
    def __init__(self, enable_old_exe_format: bool = False, debug: bool = False):
        """
        简单的midi转换类，将midi文件转换为我的世界结构或者包
        
        Parameters
        ----------
        enable_old_exe_format: bool
            是否启用旧版(≤1.19)指令格式，默认为否
        debug: bool
            是否启用调试模式，默认为否
        """

        self.debug_mode: bool = debug
        """是否开启调试模式"""

        self.midi_file: str = ""
        """Midi文件路径"""

        self.midi: VM = None
        """MidiFile对象"""

        self.output_path: str = ""
        """输出路径"""

        self.mid_file_name: str = ""
        """文件名，不含路径且不含后缀"""

        self.execute_cmd_head = ""
        """execute 指令的执行开头，用于被format"""

        self.enable_old_exe_format = enable_old_exe_format
        """是否启用旧版指令格式"""

        self.execute_cmd_head = (
            "execute {} ~ ~ ~ "
            if enable_old_exe_format
            else "execute as {} at @s positioned ~ ~ ~ run "
        )
        """execute指令头部"""

    def convert(self, midi_file: str, output_path: str):
        """转换前需要先运行此函数来获取基本信息"""

        self.midi_file = midi_file
        """midi文件路径"""

        try:
            self.midi = mido.MidiFile(self.midi_file)
            """MidiFile对象"""
        except Exception as E:
            raise MidiDestroyedError(f"文件{self.midi_file}损坏：{E}")

        self.output_path = os.path.abspath(output_path)
        """输出路径"""
        # 将self.midiFile的文件名，不含路径且不含后缀存入self.midiFileName
        self.mid_file_name = os.path.splitext(os.path.basename(self.midi_file))[0]
        """文件名，不含路径且不含后缀"""

    @staticmethod
    def inst_to_souldID_withX(
        instrumentID: int,
    ):
        """
        返回midi的乐器ID对应的我的世界乐器名，对于音域转换算法，如下：
        2**( ( msg.note - 60 - X ) / 12 ) 即为MC的音高，其中
        X的取值随乐器不同而变化：
        竖琴harp、电钢琴pling、班卓琴banjo、方波bit、颤音琴iron_xylophone 的时候为6
        吉他的时候为7
        贝斯bass、迪吉里杜管didgeridoo的时候为8
        长笛flute、牛铃cou_bell的时候为5
        钟琴bell、管钟chime、木琴xylophone的时候为4
        而存在一些打击乐器bd(basedrum)、hat、snare，没有音域，则没有X，那么我们返回7即可

        Parameters
        ----------
        instrumentID: int
            midi的乐器ID

        Returns
        -------
        tuple(str我的世界乐器名, int转换算法中的X)
        """
        try:
            return PITCHED_INSTRUMENT_LIST[instrumentID]
        except KeyError:
            return "note.flute", 5

    @staticmethod
    def perc_inst_to_soundID_withX(instrumentID: int):
        """
        对于Midi第10通道所对应的打击乐器，返回我的世界乐器名

        Parameters
        ----------
        instrumentID: int
            midi的乐器ID

        Returns
        -------
        tuple(str我的世界乐器名, int转换算法中的X)
        """
        try:
            return PERCUSSION_INSTRUMENT_LIST[instrumentID]
        except KeyError:
            print("WARN", f"无法使用打击乐器列表库，或者使用了不存在的乐器，打击乐器使用Dislink算法代替。{instrumentID}")
            if instrumentID == 55:
                return "note.cow_bell", 5
            elif instrumentID in [41, 43, 45]:
                return "note.hat", 7
            elif instrumentID in [36, 37, 39]:
                return "note.snare", 7
            else:
                return "note.bd", 7

    def form_progress_bar(
        self,
        max_score: int,
        scoreboard_name: str,
        progressbar_style: tuple = DEFAULT_PROGRESSBAR_STYLE,
    ) -> list:
        """
        生成进度条

        Parameters
        ----------
        maxscore: int
            midi的乐器ID

        scoreboard_name: str
            所使用的计分板名称

        progressbar_style: tuple
            此参数详见 ../docs/库的生成与功能文档.md#进度条自定义

        Returns
        -------
        list[str"指令",]
        """
        pgs_style = progressbar_style[0]
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
        perEach = max_score / pgs_style.count("_")
        '''每个进度条代表的分值'''

        result = []

        if r"%^s" in pgs_style:
            pgs_style = pgs_style.replace(r"%^s", str(max_score))

        if r"%^t" in pgs_style:
            pgs_style = pgs_style.replace(r"%^t", self.mctick2timestr(max_score))

        sbn_pc = scoreboard_name[:2]
        if r"%%%" in pgs_style:
            result.append(
                'scoreboard objectives add {}PercT dummy "百分比计算"'.format(sbn_pc)
            )
            result.append(
                self.execute_cmd_head.format("@a[scores={" + scoreboard_name + "=1..}]")
                + "scoreboard players set MaxScore {} {}".format(
                    scoreboard_name, max_score
                )
            )
            result.append(
                self.execute_cmd_head.format("@a[scores={" + scoreboard_name + "=1..}]")
                + "scoreboard players set n100 {} 100".format(scoreboard_name)
            )
            result.append(
                self.execute_cmd_head.format("@a[scores={" + scoreboard_name + "=1..}]")
                + "scoreboard players operation @s {} = @s {}".format(
                    sbn_pc + "PercT", scoreboard_name
                )
            )
            result.append(
                self.execute_cmd_head.format("@a[scores={" + scoreboard_name + "=1..}]")
                + "scoreboard players operation @s {} *= n100 {}".format(
                    sbn_pc + "PercT", scoreboard_name
                )
            )
            result.append(
                self.execute_cmd_head.format("@a[scores={" + scoreboard_name + "=1..}]")
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
                self.execute_cmd_head.format("@a[scores={" + scoreboard_name + "=1..}]")
                + "scoreboard players set n20 {} 20".format(scoreboard_name)
            )
            result.append(
                self.execute_cmd_head.format("@a[scores={" + scoreboard_name + "=1..}]")
                + "scoreboard players set n60 {} 60".format(scoreboard_name)
            )

            result.append(
                self.execute_cmd_head.format("@a[scores={" + scoreboard_name + "=1..}]")
                + "scoreboard players operation @s {} = @s {}".format(
                    sbn_pc + "TMinT", scoreboard_name
                )
            )
            result.append(
                self.execute_cmd_head.format("@a[scores={" + scoreboard_name + "=1..}]")
                + "scoreboard players operation @s {} /= n20 {}".format(
                    sbn_pc + "TMinT", scoreboard_name
                )
            )
            result.append(
                self.execute_cmd_head.format("@a[scores={" + scoreboard_name + "=1..}]")
                + "scoreboard players operation @s {} /= n60 {}".format(
                    sbn_pc + "TMinT", scoreboard_name
                )
            )

            result.append(
                self.execute_cmd_head.format("@a[scores={" + scoreboard_name + "=1..}]")
                + "scoreboard players operation @s {} = @s {}".format(
                    sbn_pc + "TSecT", scoreboard_name
                )
            )
            result.append(
                self.execute_cmd_head.format("@a[scores={" + scoreboard_name + "=1..}]")
                + "scoreboard players operation @s {} /= n20 {}".format(
                    sbn_pc + "TSecT", scoreboard_name
                )
            )
            result.append(
                self.execute_cmd_head.format("@a[scores={" + scoreboard_name + "=1..}]")
                + "scoreboard players operation @s {} %= n60 {}".format(
                    sbn_pc + "TSecT", scoreboard_name
                )
            )

        for i in range(pgs_style.count("_")):
            npg_stl = (
                pgs_style.replace("_", progressbar_style[1][0], i + 1)
                .replace("_", progressbar_style[1][1])
                .replace(r"%%N", self.mid_file_name)
                if r"%%N" in pgs_style
                else pgs_style.replace("_", progressbar_style[1][0], i + 1).replace(
                    "_", progressbar_style[1][1]
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
                self.execute_cmd_head.format(
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

    def to_command_list(
        self,
        scoreboard_name: str = "mscplay",
        max_volume: float = 1.0,
        speed: float = 1.0,
    ) -> list:
        """
        使用金羿的转换思路，将midi转换为我的世界命令列表

        Parameters
        ----------
        scoreboard_name: str
            我的世界的计分板名称
        max_volume: float
            最大播放音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放
        speed: float
            速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed

        Returns
        -------
        tuple( list[list[str指令,... ],... ], int指令数量, int最大计分 )
        """

        if speed == 0:
            if self.debug_mode:
                raise ZeroSpeedError("播放速度仅可为正实数")
            speed = 1
        max_volume = 1 if max_volume > 1 else (0.001 if max_volume <= 0 else max_volume)

        # 一个midi中仅有16个通道 我们通过通道来识别而不是音轨
        channels = empty_midi_channels()

        # 我们来用通道统计音乐信息
        # 但是是用分轨的思路的
        for track_no, track in enumerate(self.midi.tracks):
            microseconds = 0

            for msg in track:
                if msg.time != 0:
                    try:
                        microseconds += (
                            msg.time * tempo / self.midi.ticks_per_beat / 1000
                        )
                        # print(microseconds)
                    except NameError:
                        if self.debug_mode:
                            raise NotDefineTempoError("计算当前分数时出错 未定义参量 Tempo")
                        else:
                            microseconds += (
                                msg.time
                                * mido.midifiles.midifiles.DEFAULT_TEMPO
                                / self.midi.ticks_per_beat
                            ) / 1000

                if msg.is_meta:
                    if msg.type == "set_tempo":
                        tempo = msg.tempo
                        if self.debug_mode:
                            self.prt(f"TEMPO更改：{tempo}（毫秒每拍）")
                else:
                    if self.debug_mode:
                        try:
                            if msg.channel > 15:
                                raise ChannelOverFlowError(f"当前消息 {msg} 的通道超限(≤15)")
                        except AttributeError:
                            pass

                    if not track_no in channels[msg.channel].keys():
                        channels[msg.channel][track_no] = []
                    if msg.type == "program_change":
                        channels[msg.channel][track_no].append(
                            ("PgmC", msg.program, microseconds)
                        )

                    elif msg.type == "note_on" and msg.velocity != 0:
                        channels[msg.channel][track_no].append(
                            ("NoteS", msg.note, msg.velocity, microseconds)
                        )

                    elif (msg.type == "note_on" and msg.velocity == 0) or (
                        msg.type == "note_off"
                    ):
                        channels[msg.channel][track_no].append(
                            ("NoteE", msg.note, microseconds)
                        )

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

            for track_no, track in channels[i].items():
                nowTrack = []

                for msg in track:
                    if msg[0] == "PgmC":
                        InstID = msg[1]

                    elif msg[0] == "NoteS":
                        try:
                            soundID, _X = (
                                self.perc_inst_to_soundID_withX(InstID)
                                if SpecialBits
                                else self.inst_to_souldID_withX(InstID)
                            )
                        except UnboundLocalError as E:
                            if self.debug_mode:
                                raise NotDefineProgramError(f"未定义乐器便提前演奏。\n{E}")
                            else:
                                soundID, _X = (
                                    self.perc_inst_to_soundID_withX(-1)
                                    if SpecialBits
                                    else self.inst_to_souldID_withX(-1)
                                )
                        score_now = round(msg[-1] / float(speed) / 50)
                        maxScore = max(maxScore, score_now)

                        nowTrack.append(
                            self.execute_cmd_head.format(
                                "@a[scores=({}={})]".format(scoreboard_name, score_now)
                                .replace("(", r"{")
                                .replace(")", r"}")
                            )
                            + f"playsound {soundID} @s ^ ^ ^{1 / max_volume - 1} {msg[2] / 128} "
                            f"{2 ** ((msg[1] - 60 - _X) / 12)}"
                        )

                        cmdAmount += 1

                if nowTrack:
                    tracks.append(nowTrack)

        return [tracks, cmdAmount, maxScore]


    def to_command_list_with_delay(
        self,
        max_volume: float = 1.0,
        speed: float = 1.0,
        player_selector: str = "@a",
    ) -> list:
        """
        使用金羿的转换思路，将midi转换为我的世界命令列表，并输出每个音符之后的延迟

        Parameters
        ----------
        max_volume: float
            最大播放音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
        speed: float
            速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
        player_selector: str
            玩家选择器，默认为`@a`

        Returns
        -------
        tuple( list[tuple(str指令, int距离上一个指令的延迟 ),...], int音乐时长游戏刻 )
        """

        if speed == 0:
            if self.debug_mode:
                raise ZeroSpeedError("播放速度仅可为正实数")
            speed = 1
        max_volume = 1 if max_volume > 1 else (0.001 if max_volume <= 0 else max_volume)

        # 一个midi中仅有16个通道 我们通过通道来识别而不是音轨
        channels = empty_midi_channels()

        # 我们来用通道统计音乐信息
        # 但是是用分轨的思路的
        for track_no, track in enumerate(self.midi.tracks):
            microseconds = 0

            for msg in track:
                if msg.time != 0:
                    try:
                        microseconds += (
                            msg.time * tempo / self.midi.ticks_per_beat / 1000
                        )
                        # print(microseconds)
                    except NameError:
                        if self.debug_mode:
                            raise NotDefineTempoError("计算当前分数时出错 未定义参量 Tempo")
                        else:
                            microseconds += (
                                msg.time
                                * mido.midifiles.midifiles.DEFAULT_TEMPO
                                / self.midi.ticks_per_beat
                            ) / 1000

                if msg.is_meta:
                    if msg.type == "set_tempo":
                        tempo = msg.tempo
                        if self.debug_mode:
                            self.prt(f"TEMPO更改：{tempo}（毫秒每拍）")
                else:
                    try:
                        if msg.channel > 15 and self.debug_mode:
                            raise ChannelOverFlowError(f"当前消息 {msg} 的通道超限(≤15)")
                        if not track_no in channels[msg.channel].keys():
                            channels[msg.channel][track_no] = []
                    except AttributeError:
                        pass

                    if msg.type == "program_change":
                        channels[msg.channel][track_no].append(
                            ("PgmC", msg.program, microseconds)
                        )

                    elif msg.type == "note_on" and msg.velocity != 0:
                        channels[msg.channel][track_no].append(
                            ("NoteS", msg.note, msg.velocity, microseconds)
                        )

                    elif (msg.type == "note_on" and msg.velocity == 0) or (
                        msg.type == "note_off"
                    ):
                        channels[msg.channel][track_no].append(
                            ("NoteE", msg.note, microseconds)
                        )

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

            for track_no, track in channels[i].items():
                for msg in track:
                    if msg[0] == "PgmC":
                        InstID = msg[1]

                    elif msg[0] == "NoteS":
                        try:
                            soundID, _X = (
                                self.perc_inst_to_soundID_withX(InstID)
                                if SpecialBits
                                else self.inst_to_souldID_withX(InstID)
                            )
                        except UnboundLocalError as E:
                            if self.debug_mode:
                                raise NotDefineProgramError(f"未定义乐器便提前演奏。\n{E}")
                            else:
                                soundID, _X = (
                                    self.perc_inst_to_soundID_withX(-1)
                                    if SpecialBits
                                    else self.inst_to_souldID_withX(-1)
                                )
                        score_now = round(msg[-1] / float(speed) / 50)
                        # print(score_now)

                        try:
                            tracks[score_now].append(
                                self.execute_cmd_head.format(player_selector)
                                + f"playsound {soundID} @s ^ ^ ^{1 / max_volume - 1} {msg[2] / 128} "
                                f"{2 ** ((msg[1] - 60 - _X) / 12)}"
                            )
                        except KeyError:
                            tracks[score_now] = [
                                self.execute_cmd_head.format(player_selector)
                                + f"playsound {soundID} @s ^ ^ ^{1 / max_volume - 1} {msg[2] / 128} "
                                f"{2 ** ((msg[1] - 60 - _X) / 12)}"
                            ]

        all_ticks = list(tracks.keys())
        all_ticks.sort()
        results = []

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


    def to_mcpack(
        self,
        volume: float = 1.0,
        speed: float = 1.0,
        progressbar: Union[bool, Tuple[str, Tuple[str,]]] = None,
        scoreboard_name: str = "mscplay",
        auto_reset: bool = False,
    ) -> tuple:
        """
        将midi转换为我的世界mcpack格式的包

        Parameters
        ----------
        volume: float
            音量，注意：这里的音量范围为(0,1]，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
        speed: float
            速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
        progressbar: bool|tuple[str, Tuple[str,]]
            进度条，当此参数为 `True` 时使用默认进度条，为其他的**值为真**的参数时识别为进度条自定义参数，为其他**值为假**的时候不生成进度条
        scoreboard_name: str
            我的世界的计分板名称
        auto_reset: bool
            是否自动重置计分板
        
        Returns
        -------
        tuple(int指令长度, int最大计分)
        """

        cmdlist, maxlen, maxscore = self.to_command_list(scoreboard_name, volume, speed)

        # 当文件f夹{self.outputPath}/temp/functions存在时清空其下所有项目，然后创建
        if os.path.exists(f"{self.output_path}/temp/functions/"):
            shutil.rmtree(f"{self.output_path}/temp/functions/")
        os.makedirs(f"{self.output_path}/temp/functions/mscplay")

        # 写入manifest.json
        if not os.path.exists(f"{self.output_path}/temp/manifest.json"):
            with open(
                f"{self.output_path}/temp/manifest.json", "w", encoding="utf-8"
            ) as f:
                f.write(
                    '{\n  "format_version": 1,\n  "header": {\n    "description": "'
                    + self.mid_file_name
                    + ' Pack : behavior pack",\n    "version": [ 0, 0, 1 ],\n    "name": "'
                    + self.mid_file_name
                    + 'Pack",\n    "uuid": "'
                    + str(uuid.uuid4())
                    + '"\n  },\n  "modules": [\n    {\n      "description": "'
                    + f"the Player of the Music {self.mid_file_name}"
                    + '",\n      "type": "data",\n      "version": [ 0, 0, 1 ],\n      "uuid": "'
                    + str(uuid.uuid4())
                    + '"\n    }\n  ]\n}'
                )
        else:
            with open(
                f"{self.output_path}/temp/manifest.json", "r", encoding="utf-8"
            ) as manifest:
                data = json.loads(manifest.read())
                data["header"][
                    "description"
                ] = f"the Player of the Music {self.mid_file_name}"
                data["header"]["name"] = self.mid_file_name
                data["header"]["uuid"] = str(uuid.uuid4())
                data["modules"][0]["description"] = "None"
                data["modules"][0]["uuid"] = str(uuid.uuid4())
                manifest.close()
            open(f"{self.output_path}/temp/manifest.json", "w", encoding="utf-8").write(
                json.dumps(data)
            )

        # 将命令列表写入文件
        index_file = open(
            f"{self.output_path}/temp/functions/index.mcfunction", "w", encoding="utf-8"
        )
        for track in cmdlist:
            index_file.write(
                "function mscplay/track" + str(cmdlist.index(track) + 1) + "\n"
            )
            with open(
                f"{self.output_path}/temp/functions/mscplay/track{cmdlist.index(track) + 1}.mcfunction",
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
                if auto_reset
                else "",
                f"function mscplay/progressShow\n" if progressbar else "",
            )
        )

        if progressbar:
            # 此处是对于仅有 True 的参数和自定义参数的判断
            # 改这一行没🐎
            if progressbar is True:
                with open(
                    f"{self.output_path}/temp/functions/mscplay/progressShow.mcfunction",
                    "w",
                    encoding="utf-8",
                ) as f:
                    f.writelines(
                        "\n".join(self.form_progress_bar(maxscore, scoreboard_name))
                    )
            else:
                with open(
                    f"{self.output_path}/temp/functions/mscplay/progressShow.mcfunction",
                    "w",
                    encoding="utf-8",
                ) as f:
                    f.writelines(
                        "\n".join(
                            self.form_progress_bar(
                                maxscore, scoreboard_name, progressbar
                            )
                        )
                    )

        index_file.close()

        if os.path.exists(f"{self.output_path}/{self.mid_file_name}.mcpack"):
            os.remove(f"{self.output_path}/{self.mid_file_name}.mcpack")
        compress_zipfile(
            f"{self.output_path}/temp/",
            f"{self.output_path}/{self.mid_file_name}.mcpack",
        )

        shutil.rmtree(f"{self.output_path}/temp/")

        return maxlen, maxscore

    def to_mcpack_with_delay(
        self,
        method: int = 1,
        volume: float = 1.0,
        speed: float = 1.0,
        progressbar: Union[bool, tuple] = False,
        player: str = "@a",
        max_height: int = 64,
    ):
        """
        使用method指定的转换算法，将midi转换为mcstructure结构文件后打包成mcpack文件
        :param method: 转换算法
        :param author: 作者名称
        :param progressbar: 进度条，（当此参数为True时使用默认进度条，为其他的值为真的参数时识别为进度条自定义参数，为其他值为假的时候不生成进度条）
        :param max_height: 生成结构最大高度
        :param volume: 音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
        :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
        :param player: 玩家选择器，默认为`@a`
        :return 成功与否，成功返回(True,未经过压缩的源,结构占用大小)，失败返回(False,str失败原因)
        """

        from TrimMCStruct import Structure

        if self.enable_old_exe_format:
            raise CommandFormatError("使用mcstructure结构文件导出时不支持旧版本的指令格式。")

        command_list, max_delay = self.methods_byDelay[method - 1](
            volume,
            speed,
            player,
        )

        # 此处是对于仅有 True 的参数和自定义参数的判断
        # 改这一行没🐎
        if progressbar is True:
            progressbar = DEFAULT_PROGRESSBAR_STYLE

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        # 当文件f夹{self.outputPath}/temp/存在时清空其下所有项目，然后创建
        if os.path.exists(f"{self.output_path}/temp/"):
            shutil.rmtree(f"{self.output_path}/temp/")
        os.makedirs(f"{self.output_path}/temp/functions/")
        os.makedirs(f"{self.output_path}/temp/structures/")

        # 写入manifest.json
        with open(f"{self.output_path}/temp/manifest.json", "w", encoding="utf-8") as f:
            json.dump(
                {
                    "format_version": 1,
                    "header": {
                        "description": f"the Music {self.mid_file_name}",
                        "version": [0, 0, 1],
                        "name": self.mid_file_name,
                        "uuid": str(uuid.uuid4()),
                    },
                    "modules": [
                        {
                            "description": "Ryoun mub Pack : behavior pack",
                            "type": "data",
                            "version": [0, 0, 1],
                            "uuid": str(uuid.uuid4()),
                        }
                    ],
                },
                fp=f,
            )

        # 将命令列表写入文件
        index_file = open(
            f"{self.output_path}/temp/functions/index.mcfunction", "w", encoding="utf-8"
        )

        struct, size, end_pos = commands_to_structure(command_list, max_height - 1)
        with open(
            os.path.abspath(
                os.path.join(
                    self.output_path,
                    "temp/structures/",
                    f"{self.mid_file_name}_main.mcstructure",
                )
            ),
            "wb+",
        ) as f:
            struct.dump(f)

        del struct

        if progressbar:
            scb_name = self.mid_file_name[:5] + "Pgb"
            index_file.write(
                "scoreboard objectives add {0} dummy {0}计\n".format(scb_name)
            )

            struct_a = Structure(
                (1, 1, 1),
            )
            struct_a.set_block(
                (0, 0, 0),
                form_command_block_in_NBT_struct(
                    r"scoreboard players add {} {} 1".format(player, scb_name),
                    (0, 0, 0),
                    1,
                    1,
                    alwaysRun=False,
                    customName="显示进度条并加分",
                ),
            )

            with open(
                os.path.abspath(
                    os.path.join(
                        self.output_path,
                        "temp/structures/",
                        f"{self.mid_file_name}_start.mcstructure",
                    )
                ),
                "wb+",
            ) as f:
                struct_a.dump(f)

            index_file.write(f"structure load {self.mid_file_name}_start ~ ~ ~1\n")

            pgb_struct, pgbSize, pgbNowPos = commands_to_structure(
                [
                    (i, 0)
                    for i in self.form_progress_bar(max_delay, scb_name, progressbar)
                ],
                max_height - 1,
            )

            with open(
                os.path.abspath(
                    os.path.join(
                        self.output_path,
                        "temp/structures/",
                        f"{self.mid_file_name}_pgb.mcstructure",
                    )
                ),
                "wb+",
            ) as f:
                pgb_struct.dump(f)

            index_file.write(f"structure load {self.mid_file_name}_pgb ~ ~1 ~1\n")

            struct_a = Structure(
                (1, 1, 1),
            )
            struct_a.set_block(
                (0, 0, 0),
                form_command_block_in_NBT_struct(
                    r"scoreboard players reset {} {}".format(player, scb_name),
                    (0, 0, 0),
                    1,
                    0,
                    alwaysRun=False,
                    customName="重置进度条计分板",
                ),
            )

            with open(
                os.path.abspath(
                    os.path.join(
                        self.output_path,
                        "temp/structures/",
                        f"{self.mid_file_name}_reset.mcstructure",
                    )
                ),
                "wb+",
            ) as f:
                struct_a.dump(f)

            del struct_a, pgb_struct

            index_file.write(
                f"structure load {self.mid_file_name}_reset ~{pgbSize[0] + 2} ~ ~1\n"
            )

            index_file.write(
                f"structure load {self.mid_file_name}_main ~{pgbSize[0] + 2} ~1 ~1\n"
            )

        else:
            index_file.write(f"structure load {self.mid_file_name}_main ~ ~ ~1\n")

        index_file.close()

        if os.path.exists(f"{self.output_path}/{self.mid_file_name}.mcpack"):
            os.remove(f"{self.output_path}/{self.mid_file_name}.mcpack")
        compress_zipfile(
            f"{self.output_path}/temp/",
            f"{self.output_path}/{self.mid_file_name}.mcpack",
        )

        shutil.rmtree(f"{self.output_path}/temp/")

        return True, len(command_list), max_delay

    def to_mcstructure_file_with_delay(
        self,
        method: int = 1,
        volume: float = 1.0,
        speed: float = 1.0,
        player: str = "@a",
        max_height: int = 64,
    ):
        """
        使用method指定的转换算法，将midi转换为mcstructure结构文件
        :param method: 转换算法
        :param author: 作者名称
        :param progressbar: 进度条，（当此参数为True时使用默认进度条，为其他的值为真的参数时识别为进度条自定义参数，为其他值为假的时候不生成进度条）
        :param max_height: 生成结构最大高度
        :param volume: 音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
        :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
        :param player: 玩家选择器，默认为`@a`
        :return 成功与否，成功返回(True,未经过压缩的源,结构占用大小)，失败返回(False,str失败原因)
        """

        if self.enable_old_exe_format:
            raise CommandFormatError("使用mcstructure结构文件导出时不支持旧版本的指令格式。")

        cmd_list, max_delay = self.methods_byDelay[method - 1](
            volume,
            speed,
            player,
        )

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        struct, size, end_pos = commands_to_structure(cmd_list, max_height - 1)

        with open(
            os.path.abspath(
                os.path.join(self.output_path, f"{self.mid_file_name}.mcstructure")
            ),
            "wb+",
        ) as f:
            struct.dump(f)

        return True, size, max_delay

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

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        with open(
            os.path.abspath(
                os.path.join(self.output_path, f"{self.mid_file_name}.bdx")
            ),
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

        cmdBytes, size, finalPos = commands_to_BDX_bytes(
            [(i, 0) for i in commands], max_height - 1
        )

        if progressbar:
            pgbBytes, pgbSize, pgbNowPos = commands_to_BDX_bytes(
                [
                    (i, 0)
                    for i in (
                        self.form_progress_bar(maxScore, scoreboard_name)
                        # 此处是对于仅有 True 的参数和自定义参数的判断
                        # 改这一行没🐎
                        if progressbar is True
                        else self.form_progress_bar(
                            maxScore, scoreboard_name, progressbar
                        )
                    )
                ],
                max_height - 1,
            )
            _bytes += pgbBytes
            _bytes += bdx_move(y, -pgbNowPos[1])
            _bytes += bdx_move(z, -pgbNowPos[2])
            _bytes += bdx_move(x, 2)

            size[0] += 2 + pgbSize[0]
            size[1] = max(size[1], pgbSize[1])
            size[2] = max(size[2], pgbSize[2])

        _bytes += cmdBytes

        with open(
            os.path.abspath(
                os.path.join(self.output_path, f"{self.mid_file_name}.bdx")
            ),
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

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        with open(
            os.path.abspath(
                os.path.join(self.output_path, f"{self.mid_file_name}.bdx")
            ),
            "w+",
        ) as f:
            f.write("BD@")

        _bytes = (
            b"BDX\x00"
            + author.encode("utf-8")
            + b" & Musicreater\x00\x01command_block\x00"
        )

        # 此处是对于仅有 True 的参数和自定义参数的判断
        # 改这一行没🐎
        if progressbar is True:
            progressbar = DEFAULT_PROGRESSBAR_STYLE

        cmdBytes, size, finalPos = commands_to_BDX_bytes(cmdlist, max_height - 1)

        if progressbar:
            scb_name = self.mid_file_name[:5] + "Pgb"
            _bytes += form_command_block_in_BDX_bytes(
                r"scoreboard objectives add {} dummy {}计".replace(r"{}", scb_name),
                1,
                customName="初始化进度条",
            )
            _bytes += bdx_move(z, 2)
            _bytes += form_command_block_in_BDX_bytes(
                r"scoreboard players add {} {} 1".format(player, scb_name),
                1,
                1,
                customName="显示进度条并加分",
            )
            _bytes += bdx_move(y, 1)
            pgbBytes, pgbSize, pgbNowPos = commands_to_BDX_bytes(
                [
                    (i, 0)
                    for i in self.form_progress_bar(max_delay, scb_name, progressbar)
                ],
                max_height - 1,
            )
            _bytes += pgbBytes
            _bytes += bdx_move(y, -1 - pgbNowPos[1])
            _bytes += bdx_move(z, -2 - pgbNowPos[2])
            _bytes += bdx_move(x, 2)
            _bytes += form_command_block_in_BDX_bytes(
                r"scoreboard players reset {} {}".format(player, scb_name),
                1,
                customName="置零进度条",
            )
            _bytes += bdx_move(y, 1)
            size[0] += 2 + pgbSize[0]
            size[1] = max(size[1], pgbSize[1])
            size[2] = max(size[2], pgbSize[2])

        size[1] += 1
        _bytes += cmdBytes

        with open(
            os.path.abspath(
                os.path.join(self.output_path, f"{self.mid_file_name}.bdx")
            ),
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
        channels = {
            0: {},
            1: {},
            2: {},
            3: {},
            4: {},
            5: {},
            6: {},
            7: {},
            8: {},
            9: {},
            10: {},
            11: {},
            12: {},
            13: {},
            14: {},
            15: {},
            16: {},
        }

        # 我们来用通道统计音乐信息
        # 但是是用分轨的思路的
        for track_no, track in enumerate(self.midi.tracks):
            microseconds = 0

            for msg in track:
                if msg.time != 0:
                    try:
                        microseconds += (
                            msg.time * tempo / self.midi.ticks_per_beat / 1000
                        )
                        # print(microseconds)
                    except NameError:
                        if self.debug_mode:
                            raise NotDefineTempoError("计算当前分数时出错 未定义参量 Tempo")
                        else:
                            microseconds += (
                                msg.time
                                * mido.midifiles.midifiles.DEFAULT_TEMPO
                                / self.midi.ticks_per_beat
                            ) / 1000

                if msg.is_meta:
                    if msg.type == "set_tempo":
                        tempo = msg.tempo
                        if self.debug_mode:
                            self.prt(f"TEMPO更改：{tempo}（毫秒每拍）")
                else:
                    try:
                        if msg.channel > 15 and self.debug_mode:
                            raise ChannelOverFlowError(f"当前消息 {msg} 的通道超限(≤15)")
                        if not track_no in channels[msg.channel].keys():
                            channels[msg.channel][track_no] = []
                    except AttributeError:
                        pass

                    if msg.type == "program_change":
                        channels[msg.channel][track_no].append(
                            ("PgmC", msg.program, microseconds)
                        )

                    elif msg.type == "note_on" and msg.velocity != 0:
                        channels[msg.channel][track_no].append(
                            ("NoteS", msg.note, msg.velocity, microseconds)
                        )

                    elif (msg.type == "note_on" and msg.velocity == 0) or (
                        msg.type == "note_off"
                    ):
                        channels[msg.channel][track_no].append(
                            ("NoteE", msg.note, microseconds)
                        )

        """整合后的音乐通道格式
        每个通道包括若干消息元素其中逃不过这三种：

        1 切换乐器消息
        ("PgmC", 切换后的乐器ID: int, 距离演奏开始的毫秒)

        2 音符开始消息
        ("NoteS", 开始的音符ID, 力度（响度）, 距离演奏开始的毫秒)

        3 音符结束消息
        ("NoteS", 结束的音符ID, 距离演奏开始的毫秒)"""
