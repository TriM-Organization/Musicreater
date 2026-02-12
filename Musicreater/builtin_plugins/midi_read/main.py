# -*- coding: utf-8 -*-

"""
音·创 v3 内置的 Midi 读取插件
"""

"""
版权所有 © 2026 金羿、玉衡Alioth、偷吃不是Touch
Copyright © 2026 Eilles, YuhengAlioth, Touch

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md

import mido

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import BinaryIO, Optional, Dict, List, Callable, Tuple, Mapping

from Musicreater import SingleMusic, SingleTrack, SingleNote, SoundAtmos
from Musicreater.plugins import (
    music_input_plugin,
    PluginConfig,
    PluginMetaInformation,
    PluginTypes,
    MusicInputPluginBase,
)
from Musicreater.exceptions import ZeroSpeedError, IllegalMinimumVolumeError
from Musicreater._utils import enumerated_stuffcopy_dictionary

from .constants import (
    MIDI_DEFAULT_PROGRAM_VALUE,
    MIDI_DEFAULT_VOLUME_VALUE,
    MM_TOUCH_PERCUSSION_INSTRUMENT_TABLE,
    MM_TOUCH_PITCHED_INSTRUMENT_TABLE,
)
from .exceptions import (
    MidiFormatError,
    NoteOnOffMismatchError,
    ChannelOverFlowError,
    LyricMismatchError,
)
from .utils import (
    volume_2_distance_natural,
    panning_2_rotation_trigonometric,
    midi_msgs_to_noteinfo,
)


@dataclass
class MidiImportConfig(PluginConfig):
    """Midi 音乐数据导入插件配置"""

    # 系统设置
    ignore_errors: bool = True

    # 处理设置
    speed_multiplier: float = 1.0

    # 兼容不良 Midi 所定义的默认值
    default_program_value: int = MIDI_DEFAULT_PROGRAM_VALUE
    default_volume_value: int = MIDI_DEFAULT_VOLUME_VALUE
    default_tempo_value: int = mido.midifiles.midifiles.DEFAULT_TEMPO

    # 对照表
    pitched_note_reference_table: Mapping[int, str] = None  # type: ignore
    percussion_note_reference_table: Mapping[int, str] = None  # type: ignore
    note_replacement_table: Mapping[str, str] = None  # type: ignore

    # 参数转换函数
    volume_process_function: Callable[[float], float] = volume_2_distance_natural
    panning_processing_function: Callable[[float], float] = (
        panning_2_rotation_trigonometric
    )

    # 分轨方式
    divide_tracks_by_miditrack: bool = True
    divide_tracks_by_midichannel: bool = False
    divide_tracks_by_soundname: bool = True
    divide_tracks_by_volume: bool = False
    divide_tracks_by_panning: bool = False

    def __post_init__(self):
        self.pitched_note_reference_table = (
            self.pitched_note_reference_table
            if self.pitched_note_reference_table
            else MM_TOUCH_PITCHED_INSTRUMENT_TABLE
        )
        self.percussion_note_reference_table = (
            self.percussion_note_reference_table
            if self.percussion_note_reference_table
            else MM_TOUCH_PERCUSSION_INSTRUMENT_TABLE
        )
        self.note_replacement_table = (
            self.note_replacement_table if self.note_replacement_table else {}
        )


class ControlerKeys(Enum):
    MIDI_PROGRAM = "midi_program"
    MIDI_VOLUME = "midi_volume"
    MIDI_PAN = "midi_pan"


class TrackDivisionDict(
    Dict[
        Tuple[
            Optional[int],
            Optional[int],
            Optional[str],
            Optional[float],
            Optional[Tuple[float, float]],
        ],
        SingleTrack,
    ]
):
    """
    音轨分轨字典
    """

    division_by_miditrack: bool = True
    division_by_midichannel: bool = False
    division_by_soundname: bool = True
    division_by_volume: bool = False
    division_by_panning: bool = False

    def __init__(
        self,
        *args,
        midi_import_config: MidiImportConfig = MidiImportConfig(),
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.division_by_miditrack = midi_import_config.divide_tracks_by_miditrack
        self.division_by_midichannel = midi_import_config.divide_tracks_by_midichannel
        self.division_by_soundname = midi_import_config.divide_tracks_by_soundname
        self.division_by_volume = midi_import_config.divide_tracks_by_volume
        self.division_by_panning = midi_import_config.divide_tracks_by_panning

    def __getitem__(
        self,
        key: Tuple[
            Optional[int],
            Optional[int],
            Optional[str],
            Optional[float],
            Optional[Tuple[float, float]],
        ],
    ) -> SingleTrack:
        key = (
            key[0] if self.division_by_miditrack else None,
            key[1] if self.division_by_midichannel else None,
            key[2] if self.division_by_soundname else None,
            key[3] if self.division_by_volume else None,
            key[4] if self.division_by_panning else None,
        )
        try:
            return super().__getitem__(key)
        except KeyError:
            self[key] = SingleTrack()
            return self[key]


@music_input_plugin("midi_2_music_plugin")
class MidiImport2MusicPlugin(MusicInputPluginBase):
    """Midi 音乐数据导入插件"""

    metainfo = PluginMetaInformation(
        name="Midi 导入插件",
        author="金羿、玉衡Alioth",
        description="从 Midi 文件导入音乐数据",
        version=(0, 0, 1),
        type=PluginTypes.FUNCTION_MUSIC_IMPORT,
        license="Same as Musicreater",
    )

    supported_formats = ("MID", "MIDI")

    def loadbytes(
        self,
        bytes_buffer_in: BinaryIO,
        config: Optional[MidiImportConfig] = MidiImportConfig(),
    ) -> SingleMusic:
        return self.midifile_2_singlemusic(
            mido.MidiFile(file=bytes_buffer_in),
            config if config else MidiImportConfig(),
        )

    def load(
        self, file_path: Path, config: Optional[MidiImportConfig] = MidiImportConfig()
    ) -> SingleMusic:
        """从 Midi 文件导入音乐数据"""
        return self.midifile_2_singlemusic(
            mido.MidiFile(filename=file_path), config if config else MidiImportConfig()
        )

    @staticmethod
    def midifile_2_singlemusic(
        midi: mido.MidiFile,
        config: MidiImportConfig = MidiImportConfig(),
    ) -> SingleMusic:
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
        Tuple[SingleMusic, int, Dict[str, int]]
            以通道作为分割的Midi音符列表字典, 音符总数, 乐器使用统计
        """

        if config.speed_multiplier == 0:
            raise ZeroSpeedError("播放速度不得为零，应为 (0,1] 范围内的实数。")

        # 一个midi中仅有16个通道 我们通过通道来识别而不是音轨
        divided_tracks: TrackDivisionDict = TrackDivisionDict(midi_import_config=config)

        value_controler_per_channel: Dict[int, Dict[ControlerKeys, int]] = (
            enumerated_stuffcopy_dictionary(
                staff={
                    ControlerKeys.MIDI_PROGRAM: config.default_program_value,
                    ControlerKeys.MIDI_VOLUME: config.default_volume_value,
                    ControlerKeys.MIDI_PAN: 64,
                }
            )
        )

        midi_tempo = config.default_tempo_value
        """微秒每拍"""
        note_count = 0
        """音符计数"""
        note_count_per_instrument: Dict[str, int] = {}
        """乐器使用统计"""
        microseconds = 0
        """当前的微妙时间"""

        note_queue_A: Dict[int, List[Tuple[int, int]]] = (
            enumerated_stuffcopy_dictionary(staff=[])
        )
        """音符队列甲 Dict[通道, List[Tuple[int音高, int乐器, int轨道]]]"""
        note_queue_B: Dict[int, List[Tuple[int, int, int]]] = (
            enumerated_stuffcopy_dictionary(staff=[])
        )
        """音符队列乙 Dict[通道, List[Tuple[int音高, int微秒时间]]]"""

        midi_lyric_cache: List[Tuple[int, str]] = []
        """歌词缓存 List[Tuple[int微秒时间, str歌词内容]]"""

        midi_text_list: List[str] = []
        """Midi 附加文本列表"""
        midi_copyright_list: List[str] = []
        """Midi 版权列表"""
        midi_track_name_dict: Dict[int, str] = {}
        """轨道名称字典 Dict[int轨道编号, str轨道名称]"""

        for track_no, message_track in enumerate(midi.tracks):
            for msg in message_track:
                if msg.type == "set_tempo":
                    midi_tempo = msg.tempo

                if msg.time != 0:
                    # 微秒
                    # 通常情况下，tempo 是 500000，tpb 在
                    microseconds += msg.time * midi_tempo / midi.ticks_per_beat

                if msg.type == "program_change":
                    # 检测 乐器变化 之 midi 事件
                    value_controler_per_channel[msg.channel][
                        ControlerKeys.MIDI_PROGRAM
                    ] = msg.program

                elif msg.is_cc(7):
                    # Control Change 更改当前通道的 音量 的事件（大幅度，最高有效位）
                    value_controler_per_channel[msg.channel][
                        ControlerKeys.MIDI_VOLUME
                    ] = msg.value
                elif msg.is_cc(10):
                    # Control Change 更改当前通道的 音调偏移 的事件（大幅度，最高有效位）
                    value_controler_per_channel[msg.channel][
                        ControlerKeys.MIDI_PAN
                    ] = msg.value

                elif msg.type == "lyrics":
                    # 歌词事件
                    midi_lyric_cache.append((microseconds, msg.text))
                    # print(lyric_cache, flush=True)
                elif msg.type == "text":
                    # 检测文本事件
                    midi_text_list.append(msg.text)
                elif msg.type == "copyright":
                    # 检测版权事件
                    midi_copyright_list.append(msg.text)
                elif msg.type == "track_name":
                    # 检测轨道名称事件
                    midi_track_name_dict[track_no] = msg.name
                elif msg.type == "note_on" and msg.velocity != 0:
                    # 一个音符开始弹奏

                    # 加入音符队列甲（按通道分隔）
                    # (音高, 轨道)
                    note_queue_A[msg.channel].append((msg.note, track_no))
                    # 音符队列乙（按通道分隔）
                    # (乐器, 力度, 微秒)
                    note_queue_B[msg.channel].append(
                        (
                            value_controler_per_channel[msg.channel][
                                ControlerKeys.MIDI_PROGRAM
                            ],
                            msg.velocity,
                            microseconds,
                        )
                    )

                elif (msg.type == "note_off") or (
                    msg.type == "note_on" and msg.velocity == 0
                ):
                    # 一个音符结束弹奏

                    if (
                        msg.note,
                        value_controler_per_channel[msg.channel][
                            ControlerKeys.MIDI_PROGRAM
                        ],
                    ) in note_queue_A[msg.channel]:
                        # 在甲队列中发现了同一个 音高和乐器且在同轨道 的音符

                        # 获取其音符力度和微秒数
                        _velocity, _program, _ms = note_queue_B[msg.channel][
                            note_queue_A[msg.channel].index((msg.note, track_no))
                        ]

                        # 在队列中删除此音符
                        note_queue_A[msg.channel].remove((msg.note, track_no))
                        note_queue_B[msg.channel].remove((_velocity, _program, _ms))

                        _lyric = ""
                        # 找一找歌词吧
                        if midi_lyric_cache:
                            for i in range(len(midi_lyric_cache)):
                                if midi_lyric_cache[i][0] >= _ms:
                                    _lyric = midi_lyric_cache.pop(i)[1]
                                    break

                        # 更新结果信息

                        that_note, sound_name, orign_distance, sound_rotation = (
                            midi_msgs_to_noteinfo(
                                inst=(
                                    msg.note
                                    if (_is_percussion := (msg.channel == 9))
                                    else _program
                                ),
                                note=(_program if _is_percussion else msg.note),
                                percussive=_is_percussion,
                                volume=value_controler_per_channel[msg.channel][
                                    ControlerKeys.MIDI_VOLUME
                                ],
                                velocity=_velocity,
                                panning=value_controler_per_channel[msg.channel][
                                    ControlerKeys.MIDI_PAN
                                ],
                                start_time=_ms,  # 微秒
                                duration=microseconds - _ms,  # 微秒
                                play_speed=config.speed_multiplier,
                                midi_reference_table=(
                                    config.percussion_note_reference_table
                                    if _is_percussion
                                    else config.pitched_note_reference_table
                                ),
                                volume_processing_method=config.volume_process_function,
                                panning_processing_method=config.panning_processing_function,
                                note_table_replacement=config.note_replacement_table,
                                lyric_line=_lyric,
                            )
                        )

                        divided_tracks[
                            (
                                track_no,
                                msg.channel,
                                sound_name,
                                orign_distance,
                                sound_rotation,
                            )
                        ].add(that_note)

                        # 更新统计信息
                        note_count += 1
                        if sound_name in note_count_per_instrument.keys():
                            note_count_per_instrument[sound_name] += 1
                        else:
                            note_count_per_instrument[sound_name] = 1

                    else:
                        # 什么？找不到 note on 消息？？
                        if config.ignore_errors:
                            print(
                                "[WARRING] MIDI格式错误 音符不匹配`{}`无法在上文`{}`中找到与之匹配的音符开音消息".format(
                                    msg, note_queue_A[msg.channel]
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

        del midi_tempo

        if midi_lyric_cache:
            # 怎么有歌词多啊
            if config.ignore_errors:
                print(
                    "[WARRING] MIDI 解析错误 歌词对应错误，以下歌词未能填入音符之中，已经填入的仍可能有误 {}".format(
                        midi_lyric_cache
                    )
                )
            else:
                raise LyricMismatchError(
                    "MIDI 解析产生错误",
                    "歌词解析过程中无法对应音符，已填入的音符仍可能有误",
                    midi_lyric_cache,
                )

        final_music = SingleMusic(
            credits="; ".join(midi_copyright_list),
            extra_information={
                "MIDI_TEXT_LIST": midi_text_list,
                "NOTE_COUNT": note_count,
                "NOTE_COUNT_PER_INSTRUMENT": note_count_per_instrument,
            },
        )
        for track_properties, every_single_track in divided_tracks.items():
            if track_properties[0] and (
                track_name := midi_track_name_dict.get(track_properties[0])
            ):
                every_single_track.track_name = track_name
            if track_properties[2]:
                every_single_track.track_instrument = track_properties[2]
            if track_properties[3]:
                every_single_track.sound_position.sound_distance = track_properties[3]
            if track_properties[4]:
                every_single_track.sound_position.sound_azimuth = track_properties[4]
            final_music.append(every_single_track)

        return final_music
