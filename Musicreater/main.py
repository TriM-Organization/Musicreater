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


# BUG退散！BUG退散！                    BUG退散！BUG退散！
# 异常、错误作乱之时                     異常、誤りが、困った時は
# 二六字组！万国码合！二六字组！万国码合！   グループ！コード＃！グループ！コード＃！
# 赶快呼叫 程序员！Let's Go！            直ぐに呼びましょプログラマ レッツゴー！


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


VoidMido = Union[mido.MidiFile, None]  # void mido
"""
空Midi类类型
"""


@dataclass(init=False)
class MidiConvert:
    """
    将Midi文件转换为我的世界内容
    """

    midi: VoidMido
    """MidiFile对象"""

    pitched_note_reference_table: MidiInstrumentTableType
    """乐音乐器Midi-MC对照表"""

    percussion_note_referrence_table: MidiInstrumentTableType
    """打击乐器Midi-MC对照表"""

    volume_processing_function: FittingFunctionType
    """音量处理函数"""

    midi_music_name: str
    """Midi乐曲名"""

    enable_old_exe_format: bool
    """是否启用旧版execute指令格式"""

    execute_cmd_head: str
    """execute指令头部"""

    channels: Union[ChannelType, NoteChannelType]
    """频道信息字典"""

    music_command_list: List[SingleCommand]
    """音乐指令列表"""

    music_tick_num: int
    """音乐总延迟"""

    progress_bar_command: List[SingleCommand]
    """进度条指令列表"""

    def __init__(
        self,
        midi_obj: VoidMido,
        midi_name: str,
        enable_old_exe_format: bool = False,
        pitched_note_rtable: MidiInstrumentTableType = MM_TOUCH_PITCHED_INSTRUMENT_TABLE,
        percussion_note_rtable: MidiInstrumentTableType = MM_TOUCH_PERCUSSION_INSTRUMENT_TABLE,
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

        self.midi: VoidMido = midi_obj

        self.midi_music_name: str = midi_name

        self.enable_old_exe_format: bool = enable_old_exe_format

        self.execute_cmd_head = (
            "execute {} ~ ~ ~ "
            if enable_old_exe_format
            else "execute as {} at @s positioned ~ ~ ~ run "
        )

        self.pitched_note_reference_table = pitched_note_rtable
        self.percussion_note_referrence_table = percussion_note_rtable
        self.volume_processing_function = vol_processing_function

        self.progress_bar_command = self.music_command_list = []
        self.channels = {}
        self.music_tick_num = 0

    @classmethod
    def from_midi_file(
        cls,
        midi_file_path: str,
        old_exe_format: bool = False,
        pitched_note_table: MidiInstrumentTableType = MM_TOUCH_PITCHED_INSTRUMENT_TABLE,
        percussion_note_table: MidiInstrumentTableType = MM_TOUCH_PERCUSSION_INSTRUMENT_TABLE,
        vol_processing_func: FittingFunctionType = natural_curve,
    ):
        """
        直接输入文件地址，将midi文件读入

        Parameters
        ----------
        midi_file: str
            midi文件地址
        enable_old_exe_format: bool
            是否启用旧版(≤1.19)指令格式，默认为否
        pitched_note_table: Dict[int, Tuple[str, int]]
            乐音乐器Midi-MC对照表
        percussion_note_table: Dict[int, Tuple[str, int]]
            打击乐器Midi-MC对照表
        """

        midi_music_name = os.path.splitext(os.path.basename(midi_file_path))[0].replace(
            " ", "_"
        )
        """文件名，不含路径且不含后缀"""

        try:
            return cls(
                mido.MidiFile(midi_file_path, clip=True),
                midi_music_name,
                old_exe_format,
                pitched_note_table,
                percussion_note_table,
                vol_processing_func,
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

        result: List[SingleCommand] = []

        if r"%^s" in pgs_style:
            pgs_style = pgs_style.replace(r"%^s", str(max_score))

        if r"%^t" in pgs_style:
            pgs_style = pgs_style.replace(r"%^t", mctick2timestr(max_score))

        sbn_pc = scoreboard_name[:2]
        if r"%%%" in pgs_style:
            result.append(
                SingleCommand(
                    'scoreboard objectives add {}PercT dummy "百分比计算"'.format(
                        sbn_pc
                    ),
                    annotation="新增临时百分比变量",
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
                    annotation="设定音乐最大延迟分数",
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
                    annotation="赋值临时百分比",
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
                    annotation="转换临时百分比之单位至%（扩大精度）",
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
                    annotation="计算百分比",
                )
            )

        # 那是假的
        # 一切都并未留下痕迹啊
        # 那梦又是多么的真实……

        if r"%%t" in pgs_style:
            result.append(
                SingleCommand(
                    'scoreboard objectives add {}TMinT dummy "时间计算：分"'.format(
                        sbn_pc
                    ),
                    annotation="新增临时分变量",
                )
            )
            result.append(
                SingleCommand(
                    'scoreboard objectives add {}TSecT dummy "时间计算：秒"'.format(
                        sbn_pc
                    ),
                    annotation="新增临时秒变量",
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
                    annotation="赋值临时分",
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
                    annotation="转换临时分之单位为秒（缩减精度）",
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
                    annotation="赋值临时秒",
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
                    annotation="转换临时分之单位为分（缩减精度）",
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
                    annotation="确定临时秒（框定精度区间）",
                )
            )

        for i in range(pgs_style.count("_")):
            npg_stl = (
                pgs_style.replace("_", progressbar_style.played_style, i + 1)
                .replace("_", progressbar_style.to_play_style)
                .replace(r"%%N", self.midi_music_name)
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
                    annotation="移除临时百分比变量",
                )
            )
        if r"%%t" in pgs_style:
            result.append(
                SingleCommand(
                    "scoreboard objectives remove {}TMinT".format(sbn_pc),
                    annotation="移除临时分变量",
                )
            )
            result.append(
                SingleCommand(
                    "scoreboard objectives remove {}TSecT".format(sbn_pc),
                    annotation="移除临时秒变量",
                )
            )

        self.progress_bar_command = result
        return result

    def to_music_note_channels(
        self,
        default_tempo_value: int = mido.midifiles.midifiles.DEFAULT_TEMPO,
        ignore_mismatch_error: bool = True,
    ) -> NoteChannelType:
        """
        将midi解析并转换为频道音符字典

        Returns
        -------
        以频道作为分割的Midi音符列表字典:
        Dict[int,List[SingleNote,]]
        """

        if self.midi is None:
            raise MidiUnboundError(
                "你是否正在使用的是一个由 copy_important 生成的MidiConvert对象？这是不可复用的。"
            )

        # 一个midi中仅有16个通道 我们通过通道来识别而不是音轨
        midi_channels: NoteChannelType = empty_midi_channels(staff=[])
        tempo = default_tempo_value

        # 我们来用通道统计音乐信息
        # 但是是用分轨的思路的
        for track_no, track in enumerate(self.midi.tracks):
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
                    microseconds += msg.time * tempo / self.midi.ticks_per_beat / 1000

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
                                SingleNote(
                                    instrument=msg.note,
                                    pitch=channel_program[msg.channel],
                                    velocity=_velocity,
                                    startime=_ms,
                                    lastime=microseconds - _ms,
                                    track_number=track_no,
                                    is_percussion=True,
                                )
                                if msg.channel == 9
                                else SingleNote(
                                    instrument=channel_program[msg.channel],
                                    pitch=msg.note,
                                    velocity=_velocity,
                                    startime=_ms,
                                    lastime=microseconds - _ms,
                                    track_number=track_no,
                                    is_percussion=False,
                                )
                            )
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
        del tempo, self.channels
        self.channels = dict(
            [
                (channel_no, sorted(channel_notes, key=lambda note: note.start_time))
                for channel_no, channel_notes in midi_channels.items()
            ]
        )

        return self.channels

    def to_command_list_in_score(
        self,
        scoreboard_name: str = "mscplay",
        max_volume: float = 1.0,
        speed: float = 1.0,
    ) -> Tuple[List[List[SingleCommand]], int, int]:
        """
        将midi转换为我的世界命令列表

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
            raise ZeroSpeedError("播放速度仅可为(0,1]范围内的正实数")
        max_volume = 1 if max_volume > 1 else (0.001 if max_volume <= 0 else max_volume)

        command_channels = []
        command_amount = 0
        max_score = 0

        # 此处 我们把通道视为音轨
        for channel in self.to_music_note_channels().values():
            # 如果当前通道为空 则跳过
            if not channel:
                continue

            this_channel = []

            for note in channel:
                score_now = round(note.start_time / float(speed) / 50)
                max_score = max(max_score, score_now)

                (
                    mc_sound_ID,
                    mc_distance_volume,
                    volume_percentage,
                    mc_pitch,
                ) = note_to_command_parameters(
                    note,
                    (
                        self.percussion_note_referrence_table
                        if note.percussive
                        else self.pitched_note_reference_table
                    ),
                    (max_volume) if note.track_no == 0 else (max_volume * 0.9),
                    self.volume_processing_function,
                )

                this_channel.append(
                    SingleCommand(
                        (
                            self.execute_cmd_head.format(
                                "@a[scores=({}={})]".format(scoreboard_name, score_now)
                                .replace("(", r"{")
                                .replace(")", r"}")
                            )
                            + (
                                r"playsound {} @s ^ ^ ^{} {}".format(
                                    mc_sound_ID, mc_distance_volume, volume_percentage
                                )
                                if note.percussive
                                else r"playsound {} @s ^ ^ ^{} {} {}".format(
                                    mc_sound_ID,
                                    mc_distance_volume,
                                    volume_percentage,
                                    mc_pitch,
                                )
                            )
                        ),
                        annotation=(
                            "在{}播放{}%的{}噪音".format(
                                mctick2timestr(score_now),
                                max_volume * 100,
                                mc_sound_ID,
                            )
                            if note.percussive
                            else "在{}播放{}%的{}乐音".format(
                                mctick2timestr(score_now),
                                max_volume * 100,
                                "{}:{:.2f}".format(mc_sound_ID, mc_pitch),
                            )
                        ),
                    ),
                )

                command_amount += 1

            if this_channel:
                self.music_command_list.extend(this_channel)
                command_channels.append(this_channel)

        self.music_tick_num = max_score
        return (command_channels, command_amount, max_score)

    def to_command_list_in_delay(
        self,
        max_volume: float = 1.0,
        speed: float = 1.0,
        player_selector: str = "@a",
    ) -> Tuple[List[SingleCommand], int, int]:
        """
        将midi转换为我的世界命令列表，并输出每个音符之后的延迟

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
        tuple( list[SingleCommand,...], int音乐时长游戏刻, int最大同时播放的指令数量 )
        """

        if speed == 0:
            raise ZeroSpeedError("播放速度仅可为(0,1]范围内的正实数")
        max_volume = 1 if max_volume > 1 else (0.001 if max_volume <= 0 else max_volume)

        notes_list: List[SingleNote] = []

        # 此处 我们把通道视为音轨
        for channel in self.to_music_note_channels().values():
            notes_list.extend(channel)

        notes_list.sort(key=lambda a: a.start_time)

        self.music_command_list = []
        multi = max_multi = 0
        delaytime_previous = 0

        for note in notes_list:
            delaytime_now = round(note.start_time / speed / 50)
            if (tickdelay := (delaytime_now - delaytime_previous)) == 0:
                multi += 1
            else:
                max_multi = max(max_multi, multi)
                multi = 0

            (
                mc_sound_ID,
                mc_distance_volume,
                volume_percentage,
                mc_pitch,
            ) = note_to_command_parameters(
                note,
                (
                    self.percussion_note_referrence_table
                    if note.percussive
                    else self.pitched_note_reference_table
                ),
                (max_volume) if note.track_no == 0 else (max_volume * 0.9),
                self.volume_processing_function,
            )

            self.music_command_list.append(
                SingleCommand(
                    command=(
                        self.execute_cmd_head.format(player_selector)
                        + (
                            r"playsound {} @s ^ ^ ^{} {}".format(
                                mc_sound_ID, mc_distance_volume, volume_percentage
                            )
                            if note.percussive
                            else r"playsound {} @s ^ ^ ^{} {} {}".format(
                                mc_sound_ID,
                                mc_distance_volume,
                                volume_percentage,
                                mc_pitch,
                            )
                        )
                    ),
                    annotation=(
                        "在{}播放{}%的{}噪音".format(
                            mctick2timestr(delaytime_now),
                            max_volume * 100,
                            mc_sound_ID,
                        )
                        if note.percussive
                        else "在{}播放{}%的{}乐音".format(
                            mctick2timestr(delaytime_now),
                            max_volume * 100,
                            "{}:{:.2f}".format(mc_sound_ID, mc_pitch),
                        )
                    ),
                    tick_delay=tickdelay,
                ),
            )
            delaytime_previous = delaytime_now

        self.music_tick_num = round(notes_list[-1].start_time / speed / 50)
        return self.music_command_list, self.music_tick_num, max_multi + 1

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
