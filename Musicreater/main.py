# -*- coding: utf-8 -*-


"""
音·创 (Musicreater)
是一款免费开源的针对《我的世界》的midi音乐转换库
Musicreater (音·创)
A free open source library used for convert midi file into formats that is suitable for **Minecraft**.

版权所有 © 2023 音·创 开发者
Copyright © 2023 all the developers of Musicreater

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 音·创 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库根目录下的 License.md


import os
import math
from typing import Tuple, List

import mido

from .exceptions import *
from .constants import *
from .utils import *
from .subclass import *

VM = TypeVar("VM", mido.MidiFile, None)  # void mido
"""
空Midi类类型
"""

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


@dataclass(init=False)
class MidiConvert:
    """
    将Midi文件转换为我的世界内容
    """

    midi: VM
    """MidiFile对象"""

    midi_music_name: str
    """Midi乐曲名"""

    enable_old_exe_format: bool
    """是否启用旧版execute指令格式"""

    execute_cmd_head: str
    """execute指令头部"""

    music_command_list: List[SingleCommand]
    """音乐指令列表"""

    music_tick_num: int
    """音乐总延迟"""

    progress_bar_command: List[SingleCommand]
    """进度条指令列表"""

    def __init__(
        self,
        midi_obj: VM,
        midi_name: str,
        enable_old_exe_format: bool = False,
    ):
        """
        简单的midi转换类，将midi对象转换为我的世界结构或者包

        Parameters
        ----------
        midi_obj: mido.MidiFile 对象
            需要处理的midi对象
        midi_name: MIDI乐曲名称
            此音乐之名
        enable_old_exe_format: bool
            是否启用旧版(≤1.19)指令格式，默认为否
        """

        self.midi: VM = midi_obj

        self.midi_music_name: str = midi_name

        self.enable_old_exe_format: bool = enable_old_exe_format

        self.execute_cmd_head = (
            "execute {} ~ ~ ~ "
            if enable_old_exe_format
            else "execute as {} at @s positioned ~ ~ ~ run "
        )

        self.progress_bar_command = self.music_command_list = []
        self.music_tick_num = 0

    @classmethod
    def from_midi_file(
        cls,
        midi_file_path: str,
        old_exe_format: bool = False,
    ):
        """
        直接输入文件地址，将midi文件读入

        Parameters
        ----------
        midi_file: str
            midi文件地址
        enable_old_exe_format: bool
            是否启用旧版(≤1.19)指令格式，默认为否
        """

        midi_music_name = os.path.splitext(os.path.basename(midi_file_path))[0]
        """文件名，不含路径且不含后缀"""

        try:
            return cls(mido.MidiFile(midi_file_path), midi_music_name, old_exe_format)
        except (ValueError, TypeError) as E:
            raise MidiDestroyedError(f"文件{midi_file_path}损坏：{E}")
        except FileNotFoundError as E:
            raise FileNotFoundError(f"文件{midi_file_path}不存在：{E}")

    @staticmethod
    def inst_to_souldID_withX(
        instrumentID: int,
    ) -> Tuple[str, int]:
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
    def perc_inst_to_soundID_withX(instrumentID: int) -> Tuple[str, int]:
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
    ) -> List[SingleCommand]:
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
        list[SingleCommand,]
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
        """每个进度条代表的分值"""

        result: List[SingleCommand] = []

        if r"%^s" in pgs_style:
            pgs_style = pgs_style.replace(r"%^s", str(max_score))

        if r"%^t" in pgs_style:
            pgs_style = pgs_style.replace(r"%^t", mctick2timestr(max_score))

        sbn_pc = scoreboard_name[:2]
        if r"%%%" in pgs_style:
            result.append(
                SingleCommand(
                    'scoreboard objectives add {}PercT dummy "百分比计算"'.format(sbn_pc),
                    annotation="新增临时计算用计分板（百分比）",
                )
            )
            result.append(
                SingleCommand(
                    self.execute_cmd_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players set MaxScore {} {}".format(
                        scoreboard_name, max_score
                    ),
                    annotation="设定此音乐最大计分",
                )
            )
            result.append(
                SingleCommand(
                    self.execute_cmd_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players set n100 {} 100".format(scoreboard_name),
                    annotation="设置常量100",
                )
            )
            result.append(
                SingleCommand(
                    self.execute_cmd_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players operation @s {} = @s {}".format(
                        sbn_pc + "PercT", scoreboard_name
                    ),
                    annotation="为临时变量赋值",
                )
            )
            result.append(
                SingleCommand(
                    self.execute_cmd_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players operation @s {} *= n100 {}".format(
                        sbn_pc + "PercT", scoreboard_name
                    ),
                    annotation="改变临时变量的单位为百分比（扩大精度）",
                )
            )
            result.append(
                SingleCommand(
                    self.execute_cmd_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players operation @s {} /= MaxScore {}".format(
                        sbn_pc + "PercT", scoreboard_name
                    ),
                    annotation="使用临时变量计算百分比",
                )
            )

        if r"%%t" in pgs_style:
            result.append(
                SingleCommand(
                    'scoreboard objectives add {}TMinT dummy "时间计算：分"'.format(sbn_pc),
                    annotation="新增临时计算计分板（分）",
                )
            )
            result.append(
                SingleCommand(
                    'scoreboard objectives add {}TSecT dummy "时间计算：秒"'.format(sbn_pc),
                    annotation="新增临时计算计分板（秒）",
                )
            )
            result.append(
                SingleCommand(
                    self.execute_cmd_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players set n20 {} 20".format(scoreboard_name),
                    annotation="设置常量20",
                )
            )
            result.append(
                SingleCommand(
                    self.execute_cmd_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players set n60 {} 60".format(scoreboard_name),
                    annotation="设置常量60",
                )
            )

            result.append(
                SingleCommand(
                    self.execute_cmd_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players operation @s {} = @s {}".format(
                        sbn_pc + "TMinT", scoreboard_name
                    ),
                    annotation="为临时变量（分）赋值",
                )
            )
            result.append(
                SingleCommand(
                    self.execute_cmd_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players operation @s {} /= n20 {}".format(
                        sbn_pc + "TMinT", scoreboard_name
                    ),
                    annotation="将临时变量转换单位为秒（缩减精度）",
                )
            )
            result.append(
                SingleCommand(
                    self.execute_cmd_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players operation @s {} = @s {}".format(
                        sbn_pc + "TSecT", sbn_pc + "TMinT"
                    ),
                    annotation="为临时变量（秒）赋值",
                )
            )

            result.append(
                SingleCommand(
                    self.execute_cmd_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players operation @s {} /= n60 {}".format(
                        sbn_pc + "TMinT", scoreboard_name
                    ),
                    annotation="将临时变量（分）转换单位为分（缩减精度）",
                )
            )

            result.append(
                SingleCommand(
                    self.execute_cmd_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players operation @s {} %= n60 {}".format(
                        sbn_pc + "TSecT", scoreboard_name
                    ),
                    annotation="将临时变量（秒）确定下来（框定精度区间）",
                )
            )

        for i in range(pgs_style.count("_")):
            npg_stl = (
                pgs_style.replace("_", progressbar_style[1][0], i + 1)
                .replace("_", progressbar_style[1][1])
                .replace(r"%%N", self.midi_music_name)
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
                SingleCommand(
                    self.execute_cmd_head.format(
                        r"@a[scores={"
                        + scoreboard_name
                        + f"={int(i * perEach)}..{math.ceil((i + 1) * perEach)}"
                        + r"}]"
                    )
                    + r'titleraw @s actionbar {"rawtext":[{"text":"'
                    + npg_stl
                    + r'"}]}',
                    annotation="进度条显示",
                )
            )

        if r"%%%" in pgs_style:
            result.append(
                SingleCommand(
                    "scoreboard objectives remove {}PercT".format(sbn_pc),
                    annotation="移除临时计算计分板（百分比）",
                )
            )
        if r"%%t" in pgs_style:
            result.append(
                SingleCommand(
                    "scoreboard objectives remove {}TMinT".format(sbn_pc),
                    annotation="移除临时计算计分板（分）",
                )
            )
            result.append(
                SingleCommand(
                    "scoreboard objectives remove {}TSecT".format(sbn_pc),
                    annotation="移除临时计算计分板（秒）",
                )
            )

        self.progress_bar_command = result
        return result

    def to_command_list_in_score(
        self,
        scoreboard_name: str = "mscplay",
        max_volume: float = 1.0,
        speed: float = 1.0,
    ) -> Tuple[List[List[SingleCommand]], int, int]:
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
        tuple( list[list[SingleCommand指令,... ],... ], int指令数量, int音乐时长游戏刻 )
        """

        if speed == 0:
            raise ZeroSpeedError("播放速度仅可为正实数")
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
                        # raise NotDefineTempoError("计算当前分数时出错 未定义参量 Tempo")
                        microseconds += (
                            msg.time
                            * mido.midifiles.midifiles.DEFAULT_TEMPO
                            / self.midi.ticks_per_beat
                        ) / 1000

                if msg.is_meta:
                    if msg.type == "set_tempo":
                        tempo = msg.tempo
                else:
                    # 曾用于调试模式
                    #     try:
                    #         if msg.channel > 15:
                    #             raise ChannelOverFlowError(f"当前消息 {msg} 的通道超限(≤15)")
                    #     except AttributeError:
                    #         pass

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
                            # raise NotDefineProgramError(f"未定义乐器便提前演奏。\n{E}")
                            soundID, _X = (
                                self.perc_inst_to_soundID_withX(-1)
                                if SpecialBits
                                else self.inst_to_souldID_withX(-1)
                            )
                        score_now = round(msg[-1] / float(speed) / 50)
                        maxScore = max(maxScore, score_now)

                        nowTrack.append(
                            SingleCommand(
                                self.execute_cmd_head.format(
                                    "@a[scores=({}={})]".format(
                                        scoreboard_name, score_now
                                    )
                                    .replace("(", r"{")
                                    .replace(")", r"}")
                                )
                                + f"playsound {soundID} @s ^ ^ ^{1 / max_volume - 1} {msg[2] / 128} "
                                f"{2 ** ((msg[1] - 60 - _X) / 12)}",
                                annotation="在{}播放{}%的{}音".format(
                                    mctick2timestr(score_now), max_volume * 100, ""
                                ),
                            ),
                        )

                        cmdAmount += 1

                if nowTrack:
                    self.music_command_list.extend(nowTrack)
                    tracks.append(nowTrack)

        self.music_tick_num = maxScore
        return (tracks, cmdAmount, maxScore)

    def to_command_list_in_delay(
        self,
        max_volume: float = 1.0,
        speed: float = 1.0,
        player_selector: str = "@a",
    ) -> Tuple[List[SingleCommand], int]:
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
        tuple( list[SingleCommand,...], int音乐时长游戏刻 )
        """

        if speed == 0:
            raise ZeroSpeedError("播放速度仅可为正实数")
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
                        # raise NotDefineTempoError("计算当前分数时出错 未定义参量 Tempo")
                        microseconds += (
                            msg.time
                            * mido.midifiles.midifiles.DEFAULT_TEMPO
                            / self.midi.ticks_per_beat
                        ) / 1000

                if msg.is_meta:
                    if msg.type == "set_tempo":
                        tempo = msg.tempo
                else:
                    try:
                        # 曾用于调试模式
                        # if msg.channel > 15:
                            # raise ChannelOverFlowError(f"当前消息 {msg} 的通道超限(≤15)")
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
                            # raise NotDefineProgramError(f"未定义乐器便提前演奏。\n{E}")
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
                    SingleCommand(
                        tracks[all_ticks[i]][j],
                        tick_delay=(
                            0
                            if j != 0
                            else (
                                all_ticks[i] - all_ticks[i - 1]
                                if i != 0
                                else all_ticks[i]
                            )
                        ),
                        annotation="在{}播放{}%的{}音".format(
                            mctick2timestr(i), max_volume * 100, ""
                        ),
                    )
                )

        self.music_command_list = results
        self.music_tick_num = max(all_ticks)
        return [results, self.music_tick_num]


    def to_dict(
        self,
    ) -> dict:
        """
        使用金羿的转换思路，将midi转换为字典
        :return: dict()
        """

        
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
                        # raise NotDefineTempoError("计算当前分数时出错 未定义参量 Tempo")
                        microseconds += (
                            msg.time
                            * mido.midifiles.midifiles.DEFAULT_TEMPO
                            / self.midi.ticks_per_beat
                        ) / 1000

                if msg.is_meta:
                    if msg.type == "set_tempo":
                        tempo = msg.tempo
                else:
                    try:
                        # 曾用于调试模式
                        # if msg.channel > 15:
                            # raise ChannelOverFlowError(f"当前消息 {msg} 的通道超限(≤15)")
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

        return channels


    def copy_important(self):
        dst = MidiConvert(
            midi_obj=None,
            midi_name=self.midi_music_name,
            enable_old_exe_format=self.enable_old_exe_format,
        )
        dst.music_command_list = [i.copy() for i in self.music_command_list]
        dst.progress_bar_command = [i.copy() for i in self.progress_bar_command]
        dst.music_tick_num = self.music_tick_num
        return dst

