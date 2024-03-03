# -*- coding: utf-8 -*-


"""
音·创 (Musicreater)
一款免费开源的针对《我的世界》音乐的支持库
Musicreater (音·创)
A free open source library used for **Minecraft** musics.

版权所有 © 2024 音·创 开发者
Copyright © 2024 all the developers of Musicreater

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 音·创 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库根目录下的 License.md


# BUG退散！BUG退散！                  BUG退散！BUG退散！                   BUG retreat! BUG retreat!
# 异常与错误作乱之时                   異常、誤りが、困った時は               Abnormalities and errors are causing chaos
# 二六字组！万国码合！二六字组！万国码合！ グループ！コード＃！グループ！コード＃！  Words combine! Unicode unite!
# 赶快呼叫 程序员！Let's Go！          直ぐに呼びましょプログラマ レッツゴー！  Hurry to call the programmer! Let's Go!


import math
import os

import mido

from .constants import *
from .exceptions import *
from .subclass import *
from .types import *
from .utils import *

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


# VoidMido = Union[mido.MidiFile, None]  # void mido
# """
# 空Midi类类型
# """
# 已经成为历史了


@dataclass(init=False)
class MusicSequence:
    """
    音乐曲谱序列存储类
    """

    music_name: str
    """乐曲名"""

    channels: MineNoteChannelType
    """频道信息字典"""

    total_note_count: int
    """音符总数"""

    used_instrument: List[str]
    """所使用的乐器"""

    minium_volume: float
    """乐曲最小音量"""

    music_deviation: float
    """乐曲音调偏移"""

    def __init__(
        self,
        name_of_music: str,
        channels_of_notes: MineNoteChannelType,
        music_note_count: Optional[int] = None,
        used_instrument_of_music: Optional[List[str]] = None,
        minium_volume_of_music: float = 0.1,
        deviation: Optional[float] = None,
    ) -> None:
        """
        《我的世界》音符序列类

        Paramaters
        ==========
        name_of_music: str
            乐曲名称
        channels_of_notes: MineNoteChannelType
            音乐音轨
        minium_volume_of_music: float
            音乐最小音量(0,1]
        """

        if minium_volume_of_music > 1 or minium_volume_of_music <= 0:
            raise IllegalMinimumVolumeError(
                "自订的最小音量参数错误：{}，应在 (0,1] 范围内。".format(
                    minium_volume_of_music
                )
            )
        # max_volume = 1 if max_volume > 1 else (0.001 if max_volume <= 0 else max_volume)

        self.music_name = name_of_music
        self.channels = channels_of_notes
        self.minium_volume = minium_volume_of_music

        if used_instrument_of_music is None or music_note_count is None:
            kp = [i.sound_name for j in self.channels.values() for i in j]
            self.total_note_count = (
                len(kp) if music_note_count is None else music_note_count
            )
            self.used_instrument = (
                list(set(kp))
                if used_instrument_of_music is None
                else used_instrument_of_music
            )

        self.music_deviation = (
            self.guess_deviation(
                self.total_note_count,
                len(self.used_instrument),
                music_channels=self.channels,
            )
            if deviation is None
            else deviation
        )

    @classmethod
    def from_mido(
        cls,
        mido_file: mido.MidiFile,
        midi_music_name: str,
        mismatch_error_ignorance: bool = True,
        speed_multiplier: float = 1,
        pitched_note_referance_table: MidiInstrumentTableType = MM_TOUCH_PITCHED_INSTRUMENT_TABLE,
        percussion_note_referance_table: MidiInstrumentTableType = MM_TOUCH_PERCUSSION_INSTRUMENT_TABLE,
        minium_vol: float = 0.1,
        volume_processing_function: FittingFunctionType = natural_curve,
        default_tempo: int = mido.midifiles.midifiles.DEFAULT_TEMPO,
        devation_guess_enabled: bool = True,
    ):
        note_channels, note_count_total, inst_note_count, qualified_inst_note_count = (
            cls.to_music_note_channels(
                midi=mido_file,
                speed=speed_multiplier,
                pitched_note_rtable=pitched_note_referance_table,
                percussion_note_rtable=percussion_note_referance_table,
                default_tempo_value=default_tempo,
                vol_processing_function=volume_processing_function,
                ignore_mismatch_error=mismatch_error_ignorance,
            )
        )
        return cls(
            name_of_music=midi_music_name,
            channels_of_notes=note_channels,
            music_note_count=note_count_total,
            used_instrument_of_music=list(inst_note_count.keys()),
            minium_volume_of_music=minium_vol,
            deviation=(
                cls.guess_deviation(
                    note_count_total,
                    len(inst_note_count),
                    inst_note_count,
                    qualified_inst_note_count,
                )
                if devation_guess_enabled
                else 0
            ),
        )

    def set_min_volume(self, volume_value: int):
        self.minium_volume = volume_value

    def set_deviation(self, deviation_value: int):
        self.music_deviation = deviation_value

    def rename_music(self, new_name: str):
        self.music_name = new_name

    def add_note(self, channel_no: int, note: MineNote, is_sort: bool = False):
        self.channels[channel_no].append(note)
        self.total_note_count += 1
        if is_sort:
            self.channels[channel_no].sort(key=lambda note: note.start_tick)

    @staticmethod
    def guess_deviation(
        total_note_count: int,
        total_instrument_count: int,
        note_count_per_instruments: Optional[Dict[str, int]] = None,
        qualified_note_count_per_instruments: Optional[Dict[str, int]] = None,
        music_channels: Optional[MineNoteChannelType] = None,
    ) -> float:
        if (
            note_count_per_instruments is None
            or qualified_note_count_per_instruments is None
        ):
            if music_channels is None:
                raise ValueError("参数不足，算逑！")
            note_count_per_instruments = {}
            qualified_note_count_per_instruments = {}
            for this_note in [k for j in music_channels.values() for k in j]:
                if this_note.sound_name in note_count_per_instruments.keys():
                    note_count_per_instruments[this_note.sound_name] += 1
                    qualified_note_count_per_instruments[
                        this_note.sound_name
                    ] += is_note_in_diapason(this_note)
                else:
                    note_count_per_instruments[this_note.sound_name] = 1
                    qualified_note_count_per_instruments[this_note.sound_name] = int(
                        is_note_in_diapason(this_note)
                    )
        return (
            sum(
                [
                    (
                        (
                            MM_INSTRUMENT_RANGE_TABLE[inst][-1]
                            * note_count
                            / total_note_count
                            - MM_INSTRUMENT_RANGE_TABLE[inst][-1]
                        )
                        * (note_count - qualified_note_count_per_instruments[inst])
                    )
                    for inst, note_count in note_count_per_instruments.items()
                ]
            )
            / total_instrument_count
            / total_note_count
        )

    @staticmethod
    def to_music_note_channels(
        midi: mido.MidiFile,
        ignore_mismatch_error: bool = True,
        speed: float = 1.0,
        pitched_note_rtable: MidiInstrumentTableType = MM_TOUCH_PITCHED_INSTRUMENT_TABLE,
        percussion_note_rtable: MidiInstrumentTableType = MM_TOUCH_PERCUSSION_INSTRUMENT_TABLE,
        default_tempo_value: int = mido.midifiles.midifiles.DEFAULT_TEMPO,
        vol_processing_function: FittingFunctionType = natural_curve,
    ) -> Tuple[MineNoteChannelType, int, Dict[str, int], Dict[str, int]]:
        """
        将midi解析并转换为频道音符字典

        Returns
        -------
        以频道作为分割的Midi音符列表字典:
        Dict[int,List[SingleNote,]]
        """

        if speed == 0:
            raise ZeroSpeedError("播放速度为 0 ，其需要(0,1]范围内的实数。")

        # if midi is None:
        #     raise MidiUnboundError(
        #         "Midi参量为空。你是否正在使用的是一个由 copy_important 生成的MidiConvert对象？这是不可复用的。"
        #     )

        # 一个midi中仅有16个通道 我们通过通道来识别而不是音轨
        midi_channels: MineNoteChannelType = empty_midi_channels(staff=[])
        tempo = default_tempo_value
        note_count = 0
        note_count_per_instruments: Dict[str, int] = {}
        qualified_note_count_per_instruments: Dict[str, int] = {}

        # 我们来用通道统计音乐信息
        # 但是是用分轨的思路的
        for track_no, track in enumerate(midi.tracks):
            microseconds = 0
            if not track:
                continue

            note_queue_A: Dict[
                int,
                List[
                    Tuple[
                        int,
                        int,
                    ]
                ],
            ] = empty_midi_channels(staff=[])
            note_queue_B: Dict[
                int,
                List[
                    Tuple[
                        int,
                        int,
                    ]
                ],
            ] = empty_midi_channels(staff=[])

            channel_program: Dict[int, int] = empty_midi_channels(staff=-1)

            for msg in track:
                if msg.time != 0:
                    microseconds += msg.time * tempo / midi.ticks_per_beat / 1000

                if msg.is_meta:
                    if msg.type == "set_tempo":
                        tempo = msg.tempo
                else:
                    if msg.type == "program_change":
                        channel_program[msg.channel] = msg.program

                    elif msg.type == "note_on" and msg.velocity != 0:
                        note_queue_A[msg.channel].append(
                            (msg.note, channel_program[msg.channel])
                        )
                        note_queue_B[msg.channel].append((msg.velocity, microseconds))

                    elif (msg.type == "note_off") or (
                        msg.type == "note_on" and msg.velocity == 0
                    ):
                        if (msg.note, channel_program[msg.channel]) in note_queue_A[
                            msg.channel
                        ]:
                            _velocity, _ms = note_queue_B[msg.channel][
                                note_queue_A[msg.channel].index(
                                    (msg.note, channel_program[msg.channel])
                                )
                            ]
                            note_queue_A[msg.channel].remove(
                                (msg.note, channel_program[msg.channel])
                            )
                            note_queue_B[msg.channel].remove((_velocity, _ms))

                            midi_channels[msg.channel].append(
                                that_note := midi_msgs_to_minenote(
                                    inst_=(
                                        msg.note
                                        if msg.channel == 9
                                        else channel_program[msg.channel]
                                    ),
                                    note_=(
                                        channel_program[msg.channel]
                                        if msg.channel == 9
                                        else msg.note
                                    ),
                                    velocity_=_velocity,
                                    start_time_=_ms,
                                    duration_=microseconds - _ms,
                                    track_no_=track_no,
                                    percussive_=(msg.channel == 9),
                                    play_speed=speed,
                                    midi_reference_table=(
                                        percussion_note_rtable
                                        if msg.channel == 9
                                        else pitched_note_rtable
                                    ),
                                    volume_processing_method_=vol_processing_function,
                                )
                            )
                            note_count += 1
                            if (
                                that_note.sound_name
                                in note_count_per_instruments.keys()
                            ):
                                note_count_per_instruments[that_note.sound_name] += 1
                                qualified_note_count_per_instruments[
                                    that_note.sound_name
                                ] += is_note_in_diapason(that_note)
                            else:
                                note_count_per_instruments[that_note.sound_name] = 1
                                qualified_note_count_per_instruments[
                                    that_note.sound_name
                                ] = int(is_note_in_diapason(that_note))
                        else:
                            if ignore_mismatch_error:
                                print(
                                    "[WARRING] MIDI格式错误 音符不匹配 {} 无法在上文中找到与之匹配的音符开音消息".format(
                                        msg
                                    )
                                )
                            else:
                                raise NoteOnOffMismatchError(
                                    "当前的MIDI很可能有损坏之嫌……",
                                    msg,
                                    "无法在上文中找到与之匹配的音符开音消息。",
                                )

        """整合后的音乐通道格式
        每个通道包括若干消息元素其中逃不过这三种：

        1 切换乐器消息
        ("PgmC", 切换后的乐器ID: int, 距离演奏开始的毫秒)

        2 音符开始消息
        ("NoteS", 开始的音符ID, 力度（响度）, 距离演奏开始的毫秒)

        3 音符结束消息
        ("NoteE", 结束的音符ID, 距离演奏开始的毫秒)"""
        del tempo
        channels = dict(
            [
                (channel_no, sorted(channel_notes, key=lambda note: note.start_tick))
                for channel_no, channel_notes in midi_channels.items()
            ]
        )

        return (
            channels,
            note_count,
            note_count_per_instruments,
            qualified_note_count_per_instruments,
        )


class MidiConvert(MusicSequence):
    """
    将Midi文件转换为我的世界内容
    """

    enable_old_exe_format: bool
    """是否启用旧版execute指令格式"""

    execute_cmd_head: str
    """execute指令头部"""

    music_command_list: List[MineCommand]
    """音乐指令列表"""

    progress_bar_command: List[MineCommand]
    """进度条指令列表"""

    @classmethod
    def from_mido_obj(
        cls,
        midi_obj: mido.MidiFile,
        midi_name: str,
        ignore_mismatch_error: bool = True,
        playment_speed: float = 1,
        default_tempo_value: int = mido.midifiles.midifiles.DEFAULT_TEMPO,
        pitched_note_rtable: MidiInstrumentTableType = MM_TOUCH_PITCHED_INSTRUMENT_TABLE,
        percussion_note_rtable: MidiInstrumentTableType = MM_TOUCH_PERCUSSION_INSTRUMENT_TABLE,
        enable_devation_guess: bool = True,
        enable_old_exe_format: bool = False,
        minium_volume: float = 0.1,
        vol_processing_function: FittingFunctionType = natural_curve,
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
        pitched_note_rtable: Dict[int, Tuple[str, int]]
            乐音乐器Midi-MC对照表
        percussion_note_rtable: Dict[int, Tuple[str, int]]
            打击乐器Midi-MC对照表
        """

        cls.enable_old_exe_format: bool = enable_old_exe_format

        cls.execute_cmd_head = (
            "execute {} ~ ~ ~ "
            if enable_old_exe_format
            else "execute as {} at @s positioned ~ ~ ~ run "
        )

        cls.progress_bar_command = cls.music_command_list = []
        cls.channels = {}

        return cls.from_mido(
            mido_file=midi_obj,
            midi_music_name=midi_name,
            speed_multiplier=playment_speed,
            pitched_note_referance_table=pitched_note_rtable,
            percussion_note_referance_table=percussion_note_rtable,
            minium_vol=minium_volume,
            volume_processing_function=vol_processing_function,
            default_tempo=default_tempo_value,
            devation_guess_enabled=enable_devation_guess,
            mismatch_error_ignorance=ignore_mismatch_error,
        )

    @classmethod
    def from_midi_file(
        cls,
        midi_file_path: str,
        mismatch_error_ignorance: bool = True,
        play_speed: float = 1,
        default_tempo: int = mido.midifiles.midifiles.DEFAULT_TEMPO,
        pitched_note_table: MidiInstrumentTableType = MM_TOUCH_PITCHED_INSTRUMENT_TABLE,
        percussion_note_table: MidiInstrumentTableType = MM_TOUCH_PERCUSSION_INSTRUMENT_TABLE,
        devation_guess_enabled: bool = True,
        old_exe_format: bool = False,
        min_volume: float = 0.1,
        vol_processing_func: FittingFunctionType = natural_curve,
    ):
        """
        直接输入文件地址，将midi文件读入

        Parameters
        ----------
        midi_file_path: str
            midi文件地址

        speed: float
            速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
        pitched_note_table: Dict[int, Tuple[str, int]]
            乐音乐器Midi-MC对照表
        percussion_note_table: Dict[int, Tuple[str, int]]
            打击乐器Midi-MC对照表
        enable_old_exe_format: bool
            是否启用旧版(≤1.19)指令格式，默认为否
        min_volume: float
            最小播放音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值
        """

        midi_music_name = os.path.splitext(os.path.basename(midi_file_path))[0].replace(
            " ", "_"
        )
        """文件名，不含路径且不含后缀"""

        try:
            return cls.from_mido_obj(
                midi_obj=mido.MidiFile(
                    midi_file_path,
                    clip=True,
                ),
                midi_name=midi_music_name,
                ignore_mismatch_error=mismatch_error_ignorance,
                playment_speed=play_speed,
                default_tempo_value=default_tempo,
                pitched_note_rtable=pitched_note_table,
                percussion_note_rtable=percussion_note_table,
                enable_devation_guess=devation_guess_enabled,
                enable_old_exe_format=old_exe_format,
                minium_volume=min_volume,
                vol_processing_function=vol_processing_func,
            )
        except (ValueError, TypeError) as E:
            raise MidiDestroyedError(f"文件{midi_file_path}损坏：{E}")
        except FileNotFoundError as E:
            raise FileNotFoundError(f"文件{midi_file_path}不存在：{E}")

        # ……真的那么重要吗
        # 我又几曾何时，知道祂真的会抛下我

    def form_progress_bar(
        self,
        max_score: int,
        scoreboard_name: str,
        progressbar_style: ProgressBarStyle = DEFAULT_PROGRESSBAR_STYLE,
    ) -> List[MineCommand]:
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
        pgs_style = progressbar_style.base_style
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

        result: List[MineCommand] = []

        if r"%^s" in pgs_style:
            pgs_style = pgs_style.replace(r"%^s", str(max_score))

        if r"%^t" in pgs_style:
            pgs_style = pgs_style.replace(r"%^t", mctick2timestr(max_score))

        sbn_pc = scoreboard_name[:2]
        if r"%%%" in pgs_style:
            result.append(
                MineCommand(
                    'scoreboard objectives add {}PercT dummy "百分比计算"'.format(
                        sbn_pc
                    ),
                    annotation="新增临时百分比变量",
                )
            )
            result.append(
                MineCommand(
                    self.execute_cmd_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players set MaxScore {} {}".format(
                        scoreboard_name, max_score
                    ),
                    annotation="设定音乐最大延迟分数",
                )
            )
            result.append(
                MineCommand(
                    self.execute_cmd_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players set n100 {} 100".format(scoreboard_name),
                    annotation="设置常量100",
                )
            )
            result.append(
                MineCommand(
                    self.execute_cmd_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players operation @s {} = @s {}".format(
                        sbn_pc + "PercT", scoreboard_name
                    ),
                    annotation="赋值临时百分比",
                )
            )
            result.append(
                MineCommand(
                    self.execute_cmd_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players operation @s {} *= n100 {}".format(
                        sbn_pc + "PercT", scoreboard_name
                    ),
                    annotation="转换临时百分比之单位至%（扩大精度）",
                )
            )
            result.append(
                MineCommand(
                    self.execute_cmd_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players operation @s {} /= MaxScore {}".format(
                        sbn_pc + "PercT", scoreboard_name
                    ),
                    annotation="计算百分比",
                )
            )

        # 那是假的
        # 一切都并未留下痕迹啊
        # 那梦又是多么的真实……

        if r"%%t" in pgs_style:
            result.append(
                MineCommand(
                    'scoreboard objectives add {}TMinT dummy "时间计算：分"'.format(
                        sbn_pc
                    ),
                    annotation="新增临时分变量",
                )
            )
            result.append(
                MineCommand(
                    'scoreboard objectives add {}TSecT dummy "时间计算：秒"'.format(
                        sbn_pc
                    ),
                    annotation="新增临时秒变量",
                )
            )
            result.append(
                MineCommand(
                    self.execute_cmd_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players set n20 {} 20".format(scoreboard_name),
                    annotation="设置常量20",
                )
            )
            result.append(
                MineCommand(
                    self.execute_cmd_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players set n60 {} 60".format(scoreboard_name),
                    annotation="设置常量60",
                )
            )

            result.append(
                MineCommand(
                    self.execute_cmd_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players operation @s {} = @s {}".format(
                        sbn_pc + "TMinT", scoreboard_name
                    ),
                    annotation="赋值临时分",
                )
            )
            result.append(
                MineCommand(
                    self.execute_cmd_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players operation @s {} /= n20 {}".format(
                        sbn_pc + "TMinT", scoreboard_name
                    ),
                    annotation="转换临时分之单位为秒（缩减精度）",
                )
            )
            result.append(
                MineCommand(
                    self.execute_cmd_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players operation @s {} = @s {}".format(
                        sbn_pc + "TSecT", sbn_pc + "TMinT"
                    ),
                    annotation="赋值临时秒",
                )
            )

            result.append(
                MineCommand(
                    self.execute_cmd_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players operation @s {} /= n60 {}".format(
                        sbn_pc + "TMinT", scoreboard_name
                    ),
                    annotation="转换临时分之单位为分（缩减精度）",
                )
            )

            result.append(
                MineCommand(
                    self.execute_cmd_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players operation @s {} %= n60 {}".format(
                        sbn_pc + "TSecT", scoreboard_name
                    ),
                    annotation="确定临时秒（框定精度区间）",
                )
            )

        for i in range(pgs_style.count("_")):
            npg_stl = (
                pgs_style.replace("_", progressbar_style.played_style, i + 1)
                .replace("_", progressbar_style.to_play_style)
                .replace(r"%%N", self.music_name)
                .replace(
                    r"%%s",
                    '"},{"score":{"name":"*","objective":"'
                    + scoreboard_name
                    + '"}},{"text":"',
                )
                .replace(
                    r"%%%",
                    r'"},{"score":{"name":"*","objective":"'
                    + sbn_pc
                    + r'PercT"}},{"text":"%',
                )
                .replace(
                    r"%%t",
                    r'"},{"score":{"name":"*","objective":"{-}TMinT"}},{"text":":"},'
                    r'{"score":{"name":"*","objective":"{-}TSecT"}},{"text":"'.replace(
                        r"{-}", sbn_pc
                    ),
                )
            )
            result.append(
                MineCommand(
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
                MineCommand(
                    "scoreboard objectives remove {}PercT".format(sbn_pc),
                    annotation="移除临时百分比变量",
                )
            )
        if r"%%t" in pgs_style:
            result.append(
                MineCommand(
                    "scoreboard objectives remove {}TMinT".format(sbn_pc),
                    annotation="移除临时分变量",
                )
            )
            result.append(
                MineCommand(
                    "scoreboard objectives remove {}TSecT".format(sbn_pc),
                    annotation="移除临时秒变量",
                )
            )

        self.progress_bar_command = result
        return result

    def to_command_list_in_score(
        self,
        scoreboard_name: str = "mscplay",
    ) -> Tuple[List[List[MineCommand]], int, int]:
        """
        将midi转换为我的世界命令列表

        Parameters
        ----------
        scoreboard_name: str
            我的世界的计分板名称

        Returns
        -------
        tuple( list[list[SingleCommand指令,... ],... ], int指令数量, int音乐时长游戏刻 )
        """

        command_channels = []
        command_amount = 0
        max_score = 0

        # 此处 我们把通道视为音轨
        for channel in self.channels.values():
            # 如果当前通道为空 则跳过
            if not channel:
                continue

            this_channel = []

            for note in channel:
                max_score = max(max_score, note.start_tick)

                (
                    mc_sound_ID,
                    relative_coordinates,
                    volume_percentage,
                    mc_pitch,
                ) = minenote_to_command_paramaters(
                    note,
                    pitch_deviation=self.music_deviation,
                )

                this_channel.append(
                    MineCommand(
                        (
                            self.execute_cmd_head.format(
                                "@a[scores=({}={})]".format(
                                    scoreboard_name, note.start_tick
                                )
                                .replace("(", r"{")
                                .replace(")", r"}")
                            )
                            + r"playsound {} @s ^{} ^{} ^{} {} {} {}".format(
                                mc_sound_ID,
                                *relative_coordinates,
                                volume_percentage,
                                1.0 if note.percussive else mc_pitch,
                                self.minium_volume,
                            )
                        ),
                        annotation=(
                            "在{}播放噪音{}".format(
                                mctick2timestr(note.start_tick),
                                mc_sound_ID,
                            )
                            if note.percussive
                            else "在{}播放乐音{}".format(
                                mctick2timestr(note.start_tick),
                                "{}:{:.2f}".format(mc_sound_ID, mc_pitch),
                            )
                        ),
                    ),
                )

                command_amount += 1

            if this_channel:
                self.music_command_list.extend(this_channel)
                command_channels.append(this_channel)

        return command_channels, command_amount, max_score

    def to_command_list_in_delay(
        self,
        player_selector: str = "@a",
    ) -> Tuple[List[MineCommand], int, int]:
        """
        将midi转换为我的世界命令列表，并输出每个音符之后的延迟

        Parameters
        ----------
        player_selector: str
            玩家选择器，默认为`@a`

        Returns
        -------
        tuple( list[SingleCommand,...], int音乐时长游戏刻, int最大同时播放的指令数量 )
        """

        notes_list: List[MineNote] = sorted(
            [i for j in self.channels.values() for i in j],
            key=lambda note: note.start_tick,
        )

        # 此处 我们把通道视为音轨
        self.music_command_list = []
        multi = max_multi = 0
        delaytime_previous = 0

        for note in notes_list:
            if (tickdelay := (note.start_tick - delaytime_previous)) == 0:
                multi += 1
            else:
                max_multi = max(max_multi, multi)
                multi = 0

            (
                mc_sound_ID,
                relative_coordinates,
                volume_percentage,
                mc_pitch,
            ) = minenote_to_command_paramaters(
                note,
                pitch_deviation=self.music_deviation,
            )

            self.music_command_list.append(
                MineCommand(
                    command=(
                        self.execute_cmd_head.format(player_selector)
                        + r"playsound {} @s ^{} ^{} ^{} {} {} {}".format(
                            mc_sound_ID,
                            *relative_coordinates,
                            volume_percentage,
                            1.0 if note.percussive else mc_pitch,
                            self.minium_volume,
                        )
                    ),
                    annotation=(
                        "在{}播放噪音{}".format(
                            mctick2timestr(note.start_tick),
                            mc_sound_ID,
                        )
                        if note.percussive
                        else "在{}播放乐音{}".format(
                            mctick2timestr(note.start_tick),
                            "{}:{:.2f}".format(mc_sound_ID, mc_pitch),
                        )
                    ),
                    tick_delay=tickdelay,
                ),
            )
            delaytime_previous = note.start_tick

        return self.music_command_list, notes_list[-1].start_tick, max_multi + 1

    def copy_important(self):
        dst = MidiConvert.from_mido_obj(
            midi_obj=mido.MidiFile(),
            midi_name=self.music_name,
            enable_old_exe_format=self.enable_old_exe_format,
            pitched_note_rtable={},
            percussion_note_rtable={},
            vol_processing_function=lambda a: a,
        )
        dst.music_command_list = [i.copy() for i in self.music_command_list]
        dst.progress_bar_command = [i.copy() for i in self.progress_bar_command]
        return dst
