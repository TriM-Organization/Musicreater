# -*- coding: utf-8 -*-
"""
新版本功能以及即将启用的函数
"""


"""
版权所有 © 2025 金羿 & 诸葛亮与八卦阵
Copyright © 2025 Eilles & bgArray

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md

from typing import Dict, List, Tuple

from .old_exceptions import *
from .old_main import (
    MM_CLASSIC_PERCUSSION_INSTRUMENT_TABLE,
    MM_CLASSIC_PITCHED_INSTRUMENT_TABLE,
    MM_TOUCH_PERCUSSION_INSTRUMENT_TABLE,
    MM_TOUCH_PITCHED_INSTRUMENT_TABLE,
    MidiConvert,
    mido,
)

from .constants import MIDI_PAN, MIDI_PROGRAM, MIDI_VOLUME
from .subclass import *
from .old_types import ChannelType, FittingFunctionType
from .utils import *


class FutureMidiConvertLyricSupport(MidiConvert):
    """
    歌词测试支持
    """

    def to_command_list_in_delay(
        self,
        player_selector: str = "@a",
        using_lyric: bool = True,
    ) -> Tuple[List[MineCommand], int, int]:
        """
        将midi转换为我的世界命令列表，并输出每个音符之后的延迟

        Parameters
        ----------
        player_selector: str
            玩家选择器，默认为`@a`

        Returns
        -------
        tuple( list[MineCommand指令,...], int音乐时长游戏刻, int最大同时播放的指令数量 )
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
            ) = minenote_to_command_parameters(
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
                            self.minimum_volume,
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
            if using_lyric and note.extra_info["LYRIC_TEXT"]:
                self.music_command_list.append(
                    MineCommand(
                        self.execute_cmd_head.format(player_selector)
                        + 'title @s title " "'
                    )
                )
                self.music_command_list.append(
                    MineCommand(
                        self.execute_cmd_head.format(player_selector)
                        + "title @s subtitle {}".format(note.extra_info["LYRIC_TEXT"])
                    )
                )
            delaytime_previous = note.start_tick

        return self.music_command_list, notes_list[-1].start_tick, max_multi + 1


class FutureMidiConvertKamiRES(MidiConvert):
    """
    神羽资源包之测试支持
    """

    @staticmethod
    def to_music_note_channels(
        midi: mido.MidiFile,
        ignore_mismatch_error: bool = True,
        speed: float = 1.0,
        default_program_value: int = -1,
        default_volume_value: int = 64,
        default_tempo_value: int = mido.midifiles.midifiles.DEFAULT_TEMPO,
        pitched_note_rtable: MidiInstrumentTableType = MM_TOUCH_PITCHED_INSTRUMENT_TABLE,
        percussion_note_rtable: MidiInstrumentTableType = MM_TOUCH_PERCUSSION_INSTRUMENT_TABLE,
        vol_processing_function: FittingFunctionType = velocity_2_distance_natural,
        pan_processing_function: FittingFunctionType = panning_2_rotation_trigonometric,
        note_rtable_replacement: Dict[str, str] = {},
    ) -> Tuple[MineNoteChannelType, int, Dict[str, int]]:
        """
        将midi解析并转换为频道音符字典

        Parameters
        ----------
        midi: mido.MidiFile 对象
            需要处理的midi对象
        speed: float
            音乐播放速度倍数
        default_program_value: int
            默认的 MIDI 乐器值
        default_volume_value: int
            默认的通道音量值
        default_tempo_value: int
            默认的 MIDI TEMPO 值
        pitched_note_rtable: Dict[int, Tuple[str, int]]
            乐音乐器Midi-MC对照表
        percussion_note_rtable: Dict[int, Tuple[str, int]]
            打击乐器Midi-MC对照表
        vol_processing_function: Callable[[float], float]
            音量对播放距离的拟合函数
        pan_processing_function: Callable[[float], float]
            声像偏移对播放旋转角度的拟合函数
        note_rtable_replacement: Dict[str, str]
            音符名称替换表，此表用于对 Minecraft 乐器名称进行替换，而非 Midi Program 的替换

        Returns
        -------
        以频道作为分割的Midi音符列表字典, 音符总数, 乐器使用统计:
        Tuple[MineNoteChannelType, int, Dict[str, int]]
        """

        if speed == 0:
            raise ZeroSpeedError("播放速度为 0 ，其需要(0,1]范围内的实数。")

        # 一个midi中仅有16个通道 我们通过通道来识别而不是音轨
        midi_channels: MineNoteChannelType = enumerated_stuff_copy(staff=[])

        channel_controler: Dict[int, Dict[str, int]] = enumerated_stuff_copy(
            staff={
                MIDI_PROGRAM: default_program_value,
                MIDI_VOLUME: default_volume_value,
                MIDI_PAN: 64,
            }
        )

        tempo = default_tempo_value
        note_count = 0
        note_count_per_instrument: Dict[str, int] = {}
        microseconds = 0

        note_queue_A: Dict[
            int,
            List[
                Tuple[
                    int,
                    int,
                ]
            ],
        ] = enumerated_stuff_copy(staff=[])
        note_queue_B: Dict[
            int,
            List[
                Tuple[
                    int,
                    int,
                ]
            ],
        ] = enumerated_stuff_copy(staff=[])

        # 直接使用mido.midifiles.tracks.merge_tracks转为单轨
        # 采用的时遍历信息思路
        for msg in midi.merged_track:
            if msg.time != 0:
                # 微秒
                microseconds += msg.time * tempo / midi.ticks_per_beat

            # 简化
            if msg.type == "set_tempo":
                tempo = msg.tempo
            elif msg.type == "program_change":
                channel_controler[msg.channel][MIDI_PROGRAM] = msg.program

            elif msg.is_cc(7):
                channel_controler[msg.channel][MIDI_VOLUME] = msg.value
            elif msg.is_cc(10):
                channel_controler[msg.channel][MIDI_PAN] = msg.value

            elif msg.type == "note_on" and msg.velocity != 0:
                note_queue_A[msg.channel].append(
                    (msg.note, channel_controler[msg.channel][MIDI_PROGRAM])
                )
                note_queue_B[msg.channel].append((msg.velocity, microseconds))

            elif (msg.type == "note_off") or (
                msg.type == "note_on" and msg.velocity == 0
            ):
                if (
                    msg.note,
                    channel_controler[msg.channel][MIDI_PROGRAM],
                ) in note_queue_A[msg.channel]:
                    _velocity, _ms = note_queue_B[msg.channel][
                        note_queue_A[msg.channel].index(
                            (msg.note, channel_controler[msg.channel][MIDI_PROGRAM])
                        )
                    ]
                    note_queue_A[msg.channel].remove(
                        (msg.note, channel_controler[msg.channel][MIDI_PROGRAM])
                    )
                    note_queue_B[msg.channel].remove((_velocity, _ms))

                    midi_channels[msg.channel].append(
                        that_note := midi_msgs_to_minenote_using_kami_respack(
                            inst_=(
                                msg.note
                                if msg.channel == 9
                                else channel_controler[msg.channel][MIDI_PROGRAM]
                            ),
                            note_=(
                                channel_controler[msg.channel][MIDI_PROGRAM]
                                if msg.channel == 9
                                else msg.note
                            ),
                            percussive_=(msg.channel == 9),
                            volume_=channel_controler[msg.channel][MIDI_VOLUME],
                            velocity_=_velocity,
                            panning_=channel_controler[msg.channel][MIDI_PAN],
                            start_time_=_ms,  # 微秒
                            duration_=microseconds - _ms,  # 微秒
                            play_speed=speed,
                            midi_reference_table=(
                                percussion_note_rtable
                                if msg.channel == 9
                                else pitched_note_rtable
                            ),
                            volume_processing_method_=vol_processing_function,
                            panning_processing_method_=pan_processing_function,
                            note_table_replacement=note_rtable_replacement,
                        )
                    )
                    note_count += 1
                    if that_note.sound_name in note_count_per_instrument.keys():
                        note_count_per_instrument[that_note.sound_name] += 1
                    else:
                        note_count_per_instrument[that_note.sound_name] = 1
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
            note_count_per_instrument,
        )

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
        tuple( list[list[MineCommand指令,... ],... ], int指令数量, int音乐时长游戏刻 )
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
                ) = minenote_to_command_parameters(
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
                                1.0,
                                self.minimum_volume,
                            )
                        ),
                        annotation=(
                            "在{}播放{}".format(
                                mctick2timestr(note.start_tick),
                                mc_sound_ID,
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
        tuple( list[MineCommand指令,...], int音乐时长游戏刻, int最大同时播放的指令数量 )
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
            ) = minenote_to_command_parameters(
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
                            1.0,
                            self.minimum_volume,
                        )
                    ),
                    annotation=(
                        "在{}播放音{}".format(
                            mctick2timestr(note.start_tick),
                            mc_sound_ID,
                        )
                    ),
                    tick_delay=tickdelay,
                ),
            )
            delaytime_previous = note.start_tick

        return self.music_command_list, notes_list[-1].start_tick, max_multi + 1


class FutureMidiConvertJavaE(MidiConvert):

    def form_java_progress_bar(
        self,
        max_score: int,
        scoreboard_name: str,
        progressbar_style: ProgressBarStyle = DEFAULT_PROGRESSBAR_STYLE,
    ) -> List[MineCommand]:
        """
        生成进度条

        Parameters
        ----------
        max_score: int
            最大的积分值
        scoreboard_name: str
            所使用的计分板名称
        progressbar_style: ProgressBarStyle
            此参数详见 ../docs/库的生成与功能文档.md#进度条自定义

        Returns
        -------
        list[MineCommand,]
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
                        "@a[score_" + scoreboard_name + "_min=1]"
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
                        "@a[score_" + scoreboard_name + "_min=1]"
                    )
                    + "scoreboard players set n100 {} 100".format(scoreboard_name),
                    annotation="设置常量100",
                )
            )
            result.append(
                MineCommand(
                    self.execute_cmd_head.format(
                        "@a[scores_" + scoreboard_name + "_min=1]"
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
                        "@a[score_" + scoreboard_name + "_min=1]"
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
                        "@a[score_" + scoreboard_name + "_min=1]"
                    )
                    + "scoreboard players operation @s {} /= MaxScore {}".format(
                        sbn_pc + "PercT", scoreboard_name
                    ),
                    annotation="计算百分比",
                )
            )

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
                        "@a[score_" + scoreboard_name + "_min=1]"
                    )
                    + "scoreboard players set n20 {} 20".format(scoreboard_name),
                    annotation="设置常量20",
                )
            )
            result.append(
                MineCommand(
                    self.execute_cmd_head.format(
                        "@a[score_" + scoreboard_name + "_min=1]"
                    )
                    + "scoreboard players set n60 {} 60".format(scoreboard_name),
                    annotation="设置常量60",
                )
            )

            result.append(
                MineCommand(
                    self.execute_cmd_head.format(
                        "@a[score_" + scoreboard_name + "_min=1]"
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
                        "@a[score_" + scoreboard_name + "_min=1]"
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
                        "@a[score_" + scoreboard_name + "_min=1]"
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
                        "@a[score_" + scoreboard_name + "_min=1]"
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
                        "@a[score_" + scoreboard_name + "_min=1]"
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
                        f"@a[score_{scoreboard_name}_min={int(i * perEach)},score_{scoreboard_name}={math.ceil((i + 1) * perEach)}]"
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

    def to_command_list_in_java_score(
        self,
        scoreboard_name: str = "mscplay",
        source_of_sound: str = "ambient",
    ) -> Tuple[List[List[MineCommand]], int, int]:
        """
        将midi转换为 Java 1.12.2 版我的世界命令列表

        Parameters
        ----------
        scoreboard_name: str
            我的世界的计分板名称

        Returns
        -------
        tuple( list[list[MineCommand指令,... ],... ], int指令数量, int音乐时长游戏刻 )
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
                ) = minenote_to_command_parameters(
                    note,
                    pitch_deviation=self.music_deviation,
                )

                this_channel.append(
                    MineCommand(
                        (
                            self.execute_cmd_head.format(
                                "@a[score_{0}_min={1},score_{0}={1}]".format(
                                    scoreboard_name, note.start_tick
                                )
                                .replace("(", r"{")
                                .replace(")", r"}")
                            )
                            + "playsound minecraft:block.{} {} @s ~{} ~{} ~{} {} {} {}".format(
                                mc_sound_ID,
                                source_of_sound,
                                *relative_coordinates,
                                volume_percentage,
                                1.0 if note.percussive else mc_pitch,
                                self.minimum_volume,
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


class FutureMidiConvertRSNB(MidiConvert):
    """
    加入红石音乐适配
    """

    music_command_list: Dict[int, SingleNoteBox]
    """音乐指令列表"""


class FutureMidiConvertM4(MidiConvert):
    """
    加入插值算法优化音感
    : 经测试，生成效果已经达到，感觉良好
    """

    # 临时用的插值计算函数
    @staticmethod
    def _linear_note(
        _note: MineNote,
        _apply_time_division: float = 10,
    ) -> List[MineNote]:
        """
        传入音符数据，返回分割后的插值列表

        Parameters
        ------------
        _note: MineNote
            音符
        _apply_time_division: int
            间隔帧数

        Returns
        ---------
        list[tuple[int, int, int, int, float]]
            分割后的插值列表，每个元素为 (开始时间（毫秒）, 乐器, 音符, 力度（内置）, 音量（播放）)
        """

        if _note.percussive:
            return [
                _note,
            ]

        totalCount = int(_note.duration / _apply_time_division)

        if totalCount == 0 or (
            _note.get_info("PITCH") > 1.89 and _note.sound_name != "note.bass"
        ):

            # 喂喂，这是测试用的，别发版啊！！！

            # from rich import print as prt

            # prt("[INFO] 音符太短或音调太高，无法生成插值")
            # prt(_note)

            return [
                _note,
            ]
        # print(totalCount)

        result: List[MineNote] = []

        _slide = _note.duration / totalCount
        _distance_slide = 20 / totalCount

        for _i in range(totalCount):
            result.append(
                MineNote(
                    mc_sound_name=_note.sound_name,
                    midi_pitch=_note.note_pitch,
                    midi_velocity=_note.velocity,
                    start_time=int(_note.start_tick + _i * _slide),
                    last_time=int(_slide),
                    # track_number=_note.track_no,
                    is_percussion=_note.percussive,
                    distance=_note.sound_distance + _i * _distance_slide,
                    azimuth=(
                        _note.sound_azimuth[0],
                        _note.sound_azimuth[1] + 10 * (random.random() - 0.5),
                    ),
                    extra_information=_note.extra_info,
                )
                # (
                #     _note.start_time + _i * _apply_time_division,
                #     _note.instrument,
                #     _note.pitch,
                #     _note.velocity,
                #     ((totalCount - _i) / totalCount),
                # )
            )

        return result

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

        notes_list: List[MineNote] = []

        # 此处 我们把通道视为音轨
        for channel in self.channels.values():
            for note in channel:
                note.set_info(
                    ["NOTE_ID", "COODINATES", "VOLUME", "PITCH"],
                    minenote_to_command_parameters(
                        note,
                        pitch_deviation=self.music_deviation,
                    ),
                )

                if not note.percussive:
                    notes_list.extend(
                        self._linear_note(note, 2.55 / note.get_info("PITCH"))
                    )
                else:
                    notes_list.append(note)

        notes_list.sort(key=lambda a: a.start_tick)

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
            ) = minenote_to_command_parameters(
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
                            self.minimum_volume,
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

        return (
            self.music_command_list,
            notes_list[-1].start_tick + notes_list[-1].duration,
            max_multi + 1,
        )


class FutureMidiConvertM5(MidiConvert):
    """
    加入同刻偏移算法优化音感
    """

    def to_music_channels(
        self,
        midi: mido.MidiFile,
    ) -> ChannelType:
        """
        使用金羿的转换思路，将midi解析并转换为频道信息字典

        Returns
        -------
        以频道作为分割的Midi信息字典:
        Dict[int,Dict[int,List[Union[Tuple[Literal["PgmC"], int, int],Tuple[Literal["NoteS"], int, int, int],Tuple[Literal["NoteE"], int, int],]],],]
        """

        # if self.midi is None:
        #     raise MidiUnboundError(
        #         "你是否正在使用的是一个由 copy_important 生成的MidiConvert对象？这是不可复用的。"
        #     )

        # 一个midi中仅有16个通道 我们通过通道来识别而不是音轨
        midi_channels: ChannelType = enumerated_stuff_copy()
        tempo = 500000

        # 我们来用通道统计音乐信息
        # 但是是用分轨的思路的
        for track_no, track in enumerate(midi.tracks):
            microseconds = 0
            if not track:
                continue

            note_queue = enumerated_stuff_copy(staff=[])

            for msg in track:
                if msg.time != 0:
                    microseconds += msg.time * tempo / midi.ticks_per_beat / 1000

                if msg.is_meta:
                    if msg.type == "set_tempo":
                        tempo = msg.tempo
                else:
                    try:
                        if not track_no in midi_channels[msg.channel].keys():
                            midi_channels[msg.channel][track_no] = []
                    except AttributeError as E:
                        print(msg, E)

                    if msg.type == "program_change":
                        midi_channels[msg.channel][track_no].append(
                            ("PgmC", msg.program, microseconds)
                        )

                    elif msg.type == "note_on" and msg.velocity != 0:
                        midi_channels[msg.channel][track_no].append(
                            ("NoteS", msg.note, msg.velocity, microseconds)
                        )

                    elif (msg.type == "note_on" and msg.velocity == 0) or (
                        msg.type == "note_off"
                    ):
                        midi_channels[msg.channel][track_no].append(
                            ("NoteE", msg.note, microseconds)
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
        self.channels: ChannelType = midi_channels
        # [print([print(no,tno,sum([True if i[0] == 'NoteS' else False for i in track])) for tno,track in cna.items()]) if cna else False for no,cna in midi_channels.items()]
        return midi_channels

    # 神奇的偏移音
    def to_command_list_in_delay(
        self,
        midi: mido.MidiFile,
        max_volume: float = 1.0,
        speed: float = 1.0,
        player_selector: str = "@a",
    ) -> Tuple[List[MineCommand], int]:
        """
        使用金羿的转换思路，使用同刻偏移算法优化音感后，将midi转换为我的世界命令列表，并输出每个音符之后的延迟

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

        self.to_music_channels(
            midi=midi,
        )

        tracks = {}
        InstID = -1

        # 此处 我们把通道视为音轨
        for i in self.channels.keys():
            # 如果当前通道为空 则跳过
            if not self.channels[i]:
                continue

            # 第十通道是打击乐通道
            SpecialBits = True if i == 9 else False

            # nowChannel = []

            for track_no, track in self.channels[i].items():
                for msg in track:
                    if msg[0] == "PgmC":
                        InstID = msg[1]

                    elif msg[0] == "NoteS":
                        soundID = (
                            midi_inst_to_mc_sound(
                                msg[1], MM_CLASSIC_PERCUSSION_INSTRUMENT_TABLE
                            )
                            if SpecialBits
                            else midi_inst_to_mc_sound(
                                InstID, MM_CLASSIC_PITCHED_INSTRUMENT_TABLE
                            )
                        )

                        score_now = round(msg[-1] / float(speed) / 50)
                        # print(score_now)

                        try:
                            tracks[score_now].append(
                                self.execute_cmd_head.format(player_selector)
                                + f"playsound {soundID} @s ^ ^ ^{128 / max_volume / msg[2] - 1} {msg[2] / 128} "
                                + (
                                    ""
                                    if SpecialBits
                                    else f"{2 ** ((msg[1] - 66) / 12)}"
                                )
                            )
                        except KeyError:
                            tracks[score_now] = [
                                self.execute_cmd_head.format(player_selector)
                                + f"playsound {soundID} @s ^ ^ ^{128 / max_volume / msg[2] - 1} {msg[2] / 128} "
                                + (
                                    ""
                                    if SpecialBits
                                    else f"{2 ** ((msg[1] - 66) / 12)}"
                                )
                            ]

        all_ticks = list(tracks.keys())
        all_ticks.sort()
        results = []

        for i in range(len(all_ticks)):
            for j in range(len(tracks[all_ticks[i]])):
                results.append(
                    MineCommand(
                        tracks[all_ticks[i]][j],
                        tick_delay=(
                            (
                                0
                                if (
                                    (all_ticks[i + 1] - all_ticks[i])
                                    / len(tracks[all_ticks[i]])
                                    < 1
                                )
                                else 1
                            )
                            if j != 0
                            else (
                                (
                                    all_ticks[i]
                                    - all_ticks[i - 1]
                                    - (
                                        0
                                        if (
                                            (all_ticks[i] - all_ticks[i - 1])
                                            / len(tracks[all_ticks[i - 1]])
                                            < 1
                                        )
                                        else (len(tracks[all_ticks[i - 1]]) - 1)
                                    )
                                )
                                if i != 0
                                else all_ticks[i]
                            )
                        ),
                        annotation="在{}播放{}%的{}音".format(
                            mctick2timestr(
                                i + 0
                                if (
                                    (all_ticks[i + 1] - all_ticks[i])
                                    / len(tracks[all_ticks[i]])
                                    < 1
                                )
                                else j
                            ),
                            max_volume * 100,
                            "",
                        ),
                    )
                )

        self.music_command_list = results
        return results, max(all_ticks)


class FutureMidiConvertM6(MidiConvert):
    """
    加入插值算法优化音感，但仅用于第一音轨
    """

    # TODO 没写完的！！！！
