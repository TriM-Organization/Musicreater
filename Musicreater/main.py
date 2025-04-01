# -*- coding: utf-8 -*-


"""
音·创 (Musicreater)
是一款免费开源的《我的世界》数字音频支持库。
Musicreater (音·创)
A free open source library used for dealing with **Minecraft** digital musics.

版权所有 © 2024 金羿 & 诸葛亮与八卦阵
Copyright © 2025 Eilles & bgArray

音·创（“本项目”）的协议颁发者为 金羿、诸葛亮与八卦阵
The Licensor of Musicreater("this project") is Eilles Wan, bgArray.

本项目根据 第一版 汉钰律许可协议（“本协议”）授权。
任何人皆可从以下地址获得本协议副本：https://gitee.com/EillesWan/YulvLicenses。
若非因法律要求或经过了特殊准许，此作品在根据本协议“原样”提供的基础上，不予提供任何形式的担保、任何明示、任何暗示或类似承诺。也就是说，用户将自行承担因此作品的质量或性能问题而产生的全部风险。
详细的准许和限制条款请见原协议文本。
"""

# 音·创 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库根目录下的 License.md


# BUG退散！BUG退散！                  BUG退散！BUG退散！                   BUG retreat! BUG retreat!
# 异常与错误作乱之时                   異常、誤りが、困った時は               Abnormalities and errors are causing chaos
# 二六字组！万国码合！二六字组！万国码合！ グループ！コード＃！グループ！コード＃！  Words combine! Unicode unite!
# 赶快呼叫 程序员！Let's Go！          直ぐに呼びましょプログラマ レッツゴー！  Hurry to call the programmer! Let's Go!


import os
import math

import mido
from xxhash import xxh3_64, xxh3_128

from .constants import *
from .exceptions import *
from .subclass import *
from .types import *
from .utils import *

"""
学习笔记：
tempo:  microseconds per quarter note 毫秒每四分音符，换句话说就是一拍占多少微秒
tick:  midi帧
ticks_per_beat:  帧每拍，即一拍多少帧

那么：

tick / ticks_per_beat => amount_of_beats 拍数(四分音符数)

tempo * amount_of_beats => 微秒数

所以：

tempo * tick / ticks_per_beat => 微秒数

###########

seconds per tick:
(tempo / 1000000.0) / ticks_per_beat

seconds:
tick * tempo / 1000000.0 / ticks_per_beat

milliseconds:
tick * tempo / 1000.0 / ticks_per_beat

gameticks:
tick * tempo / 1000000.0 / ticks_per_beat * 一秒多少游戏刻


"""


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

    note_count_per_instrument: Dict[str, int]
    """所使用的乐器"""

    minimum_volume: float
    """乐曲最小音量"""

    music_deviation: float
    """全曲音调偏移"""

    def __init__(
        self,
        name_of_music: str,
        channels_of_notes: MineNoteChannelType,
        music_note_count: Optional[int] = None,
        note_used_per_instrument: Optional[Dict[str, int]] = None,
        minimum_volume_of_music: float = 0.1,
        deviation_value: Optional[float] = None,
    ) -> None:
        """
        音符序列类

        Paramaters
        ==========
        name_of_music: str
            乐曲名称
        channels_of_notes: MineNoteChannelType
            音乐音轨
        music_note_count: int
            总音符数
        note_used_per_instrument: Dict[str, int]
            全曲乐器使用统计
        minimum_volume_of_music: float
            音乐最小音量(0,1]
        deviation_value: float
            全曲音调偏移值
        """

        if minimum_volume_of_music > 1 or minimum_volume_of_music <= 0:
            raise IllegalMinimumVolumeError(
                "自订的最小音量参数错误：{}，应在 (0,1] 范围内。".format(
                    minimum_volume_of_music
                )
            )
        # max_volume = 1 if max_volume > 1 else (0.001 if max_volume <= 0 else max_volume)

        self.music_name = name_of_music
        self.channels = channels_of_notes
        self.minimum_volume = minimum_volume_of_music

        if (note_used_per_instrument is None) or (music_note_count is None):
            kp = [i.sound_name for j in self.channels.values() for i in j]
            self.total_note_count = (
                len(kp) if music_note_count is None else music_note_count
            )
            self.note_count_per_instrument = (
                dict([(it, kp.count(it)) for it in set(kp)])
                if note_used_per_instrument is None
                else note_used_per_instrument
            )
        else:
            self.total_note_count = music_note_count
            self.note_count_per_instrument = note_used_per_instrument

        self.music_deviation = 0 if deviation_value is None else deviation_value

    @classmethod
    def from_mido(
        cls,
        mido_file: Optional[mido.MidiFile],
        midi_music_name: str,
        mismatch_error_ignorance: bool = True,
        speed_multiplier: float = 1,
        default_tempo: int = mido.midifiles.midifiles.DEFAULT_TEMPO,
        pitched_note_referance_table: MidiInstrumentTableType = MM_TOUCH_PITCHED_INSTRUMENT_TABLE,
        percussion_note_referance_table: MidiInstrumentTableType = MM_TOUCH_PERCUSSION_INSTRUMENT_TABLE,
        minimum_vol: float = 0.1,
        volume_processing_function: FittingFunctionType = natural_curve,
        deviation: float = 0,
    ):
        """
        自mido对象导入一个音符序列类

        Paramaters
        ==========
        mido_file: mido.MidiFile 对象
            需要处理的midi对象
        midi_music_name: str
            音乐名称
        mismatch_error_ignorance bool
            是否在导入时忽略音符不匹配错误
        speed_multiplier: float
            音乐播放速度倍数
        default_tempo: int
            默认的MIDI TEMPO值
        pitched_note_referance_table: Dict[int, Tuple[str, int]]
            乐音乐器Midi-MC对照表
        percussion_note_referance_table: Dict[int, Tuple[str, int]]
            打击乐器Midi-MC对照表
        minimum_vol: float
            播放的最小音量 应为 (0,1] 范围内的小数
        volume_processing_function: Callable[[float], float]
            声像偏移拟合函数
        deviation: float
            全曲音调偏移值
        """
        if mido_file:
            (
                note_channels,
                note_count_total,
                inst_note_count,
            ) = cls.to_music_note_channels(
                midi=mido_file,
                speed=speed_multiplier,
                default_program_value=-1,  # TODO 默认音色可调
                pitched_note_rtable=pitched_note_referance_table,
                percussion_note_rtable=percussion_note_referance_table,
                default_tempo_value=default_tempo,
                vol_processing_function=volume_processing_function,
                ignore_mismatch_error=mismatch_error_ignorance,
            )
        else:
            note_channels = {}
            note_count_total = 0
            inst_note_count = {}
        return cls(
            name_of_music=midi_music_name,
            channels_of_notes=note_channels,
            music_note_count=note_count_total,
            note_used_per_instrument=inst_note_count,
            minimum_volume_of_music=minimum_vol,
            deviation_value=deviation,
        )

    @classmethod
    def load_decode(
        cls,
        bytes_buffer_in: bytes,
        verify: bool = True,
    ):
        """从字节码导入音乐序列"""

        group_1 = int.from_bytes(bytes_buffer_in[4:6], "big")
        group_2 = int.from_bytes(bytes_buffer_in[6:8], "big", signed=False)

        high_quantity = bool(group_2 & 0b1000000000000000)
        # print(group_2, high_quantity)

        music_name_ = bytes_buffer_in[8 : (stt_index := 8 + (group_1 >> 10))].decode(
            "GB18030"
        )
        channels_: MineNoteChannelType = empty_midi_channels(default_staff=[])
        total_note_count = 0
        if verify:
            _header_index = stt_index
            _total_verify_code = 0

        for channel_index in channels_.keys():
            channel_note_count = 0
            _channel_start_index = stt_index

            for i in range(
                int.from_bytes(
                    bytes_buffer_in[stt_index : (stt_index := stt_index + 4)], "big"
                )
            ):
                try:
                    end_index = (
                        stt_index
                        + 13
                        + high_quantity
                        + (bytes_buffer_in[stt_index] >> 2)
                    )
                    channels_[channel_index].append(
                        MineNote.decode(
                            code_buffer=bytes_buffer_in[stt_index:end_index],
                            is_high_time_precision=high_quantity,
                        )
                    )
                    channel_note_count += 1
                    stt_index = end_index
                except Exception as _err:
                    print(channels_)
                    raise MusicSequenceDecodeError(_err)
            if verify:
                if (
                    _count_verify := xxh3_64(
                        channel_note_count.to_bytes(4, "big", signed=False),
                        seed=3,
                    )
                ).digest() != (
                    _original_code := bytes_buffer_in[stt_index : stt_index + 8]
                ):
                    raise MusicSequenceVerificationFailed(
                        "通道 {} 音符数量校验失败：{} -> `{}`；原始为 `{}`".format(
                            channel_index,
                            channel_note_count,
                            _count_verify.digest(),
                            _original_code,
                        )
                    )
                if (
                    _channel_verify := xxh3_64(
                        bytes_buffer_in[_channel_start_index:stt_index],
                        seed=channel_note_count,
                    )
                ).digest() != (
                    _original_code := bytes_buffer_in[stt_index + 8 : stt_index + 16]
                ):
                    raise MusicSequenceVerificationFailed(
                        "通道 {} 音符数据校验失败：`{}`；原始为 `{}`".format(
                            channel_index,
                            _channel_verify.digest(),
                            _original_code,
                        )
                    )
                _total_verify_code ^= (
                    _count_verify.intdigest() ^ _channel_verify.intdigest()
                )
            total_note_count += channel_note_count
            stt_index += 16

        if verify:
            if (
                _total_verify_res := xxh3_128(
                    _total_verify := (
                        xxh3_64(
                            bytes_buffer_in[0:_header_index],
                            seed=total_note_count,
                        ).intdigest()
                        ^ _total_verify_code
                    ).to_bytes(8, "big"),
                    seed=total_note_count,
                ).digest()
            ) != (_original_code := bytes_buffer_in[stt_index:]):
                raise MusicSequenceVerificationFailed(
                    "全曲最终校验失败。全曲音符数：{}，全曲校验码异或和：`{}` -> `{}`；原始为 `{}`".format(
                        total_note_count,
                        _total_verify,
                        _total_verify_res,
                        _original_code,
                    )
                )

        return cls(
            name_of_music=music_name_,
            channels_of_notes=channels_,
            minimum_volume_of_music=(group_1 & 0b1111111111) / 1000,
            deviation_value=(
                (-1 if group_2 & 0b100000000000000 else 1)
                * (group_2 & 0b11111111111111)
                / 1000
            ),
        )

    def encode_dump(
        self,
        high_time_precision: bool = True,
    ) -> bytes:
        """将音乐序列转为二进制字节码"""

        # （已废弃）
        # 第一版的码头： MSQ#  字串编码： UTF-8
        # 第一版格式
        # 音乐名称长度 6 位 支持到 63
        # 最小音量 minimum_volume 10 位 最大支持 1023 即三位小数
        # 共 16 位 合 2 字节
        # +++
        # 总音调偏移 music_deviation 16 位 最大支持 -32768 ~ 32767 即 三位小数
        # 共 16 位 合 2 字节
        # +++
        # 音乐名称 music_name 长度最多63 支持到 21 个中文字符 或 63 个西文字符

        # bytes_buffer = (
        #     b"MSQ#"
        #     + (
        #         (len(r := self.music_name.encode("utf-8")) << 10)
        #         + round(self.minimum_volume * 1000)
        #     ).to_bytes(2, "big")
        #     + round(self.music_deviation * 1000).to_bytes(2, "big", signed=True)
        #     + r
        # )

        # for channel_index, note_list in self.channels.items():
        #     bytes_buffer += len(note_list).to_bytes(4, "big")
        #     for note_ in note_list:
        #         bytes_buffer += note_.encode()

        # （已废弃）
        # 第二版的码头： MSQ@  字串编码： GB18030

        # 第三版的码头： MSQ!  字串编码： GB18030  大端字节序

        # 音乐名称长度 6 位 支持到 63
        # 最小音量 minimum_volume 10 位 最大支持 1023 即三位小数
        # 共 16 位 合 2 字节
        # +++
        # 是否启用“高精度”音符时间控制 1 位
        # 总音调偏移 music_deviation 15 位 最大支持 -16383 ~ 16383 即 三位小数
        # 共 16 位 合 2 字节
        # +++
        # 音乐名称 music_name 长度最多 63 支持到 31 个中文字符 或 63 个西文字符

        bytes_buffer = (
            b"MSQ!"
            + (
                (len(r := self.music_name.encode("GB18030")) << 10)  # 音乐名称长度
                + round(self.minimum_volume * 1000)  # 最小音量
            ).to_bytes(2, "big")
            + (
                (
                    (
                        (high_time_precision << 1)  # 是否启用“高精度”音符时间控制
                        + (
                            1 if (k := round(self.music_deviation * 1000)) < 0 else 0
                        )  # 总音调偏移的正负位
                    )
                    << 14
                )
                + abs(k)  # 总音调偏移
            ).to_bytes(2, "big", signed=False)
            + r
        )

        # 此上是音符序列的元信息，接下来是多通道的音符序列

        # 每个通道的开头是 32 位的 序列长度 共 4 字节
        # 接下来根据这个序列的长度来读取音符数据

        # 若启用“高精度”，则每个音符皆添加一个字节，用于存储音符时间控制精度偏移
        # 此值每增加 1，则音符向后播放时长增加 1/1250 秒
        # 高精度功能在 MineNote 类实现

        # （第三版新增）每个通道结尾包含一个 128 位的 XXHASH 校验值，用以标识该通道结束
        # 在这 128 位里，前 64 位是该通道音符数的 XXHASH64 校验值，以 3 作为种子值
        # 后 64 位是整个通道全部字节串的 XXHASH64 校验值（包括通道开头的音符数），以 该通道音符数 作为种子值
        _final_hash_codec = xxh3_64(
            bytes_buffer, seed=self.total_note_count
        ).intdigest()

        for channel_index, note_list in self.channels.items():
            channel_buffer = len_buffer = len(note_list).to_bytes(
                4, "big", signed=False
            )
            for note_ in note_list:
                channel_buffer += note_.encode(
                    is_high_time_precision=high_time_precision
                )
            _now_hash_codec_spliter = xxh3_64(len_buffer, seed=3)
            _now_hash_codec_verifier = xxh3_64(
                channel_buffer, seed=int.from_bytes(len_buffer, "big", signed=False)
            )

            bytes_buffer += channel_buffer
            bytes_buffer += (
                _now_hash_codec_spliter.digest() + _now_hash_codec_verifier.digest()
            )

            _final_hash_codec ^= (
                _now_hash_codec_spliter.intdigest()
                ^ _now_hash_codec_verifier.intdigest()
            )

        # 在所有音符通道表示完毕之后，由一个 128 位的 XXHASH 校验值，用以标识文件结束并校验
        # 该 128 位的校验值是对于前述所有校验值的异或所得值之 XXHASH128 校验值，以 全曲音符总数 作为种子值
        bytes_buffer += xxh3_128(
            _final_hash_codec.to_bytes(8, "big"), seed=self.total_note_count
        ).digest()

        return bytes_buffer

    def set_min_volume(self, volume_value: int):
        """重新设置全曲最小音量"""
        if volume_value > 1 or volume_value <= 0:
            raise IllegalMinimumVolumeError(
                "自订的最小音量参数错误：{}，应在 (0,1] 范围内。".format(volume_value)
            )
        self.minimum_volume = volume_value

    def set_deviation(self, deviation_value: int):
        """重新设置全曲音调偏移"""
        self.music_deviation = deviation_value

    def rename_music(self, new_name: str):
        """重命名此音乐"""
        self.music_name = new_name

    def add_note(self, channel_no: int, note: MineNote, is_sort: bool = False):
        """在指定通道添加一个音符"""
        self.channels[channel_no].append(note)
        self.total_note_count += 1
        if note.sound_name in self.note_count_per_instrument.keys():
            self.note_count_per_instrument[note.sound_name] += 1
        else:
            self.note_count_per_instrument[note.sound_name] = 1
        if is_sort:
            self.channels[channel_no].sort(key=lambda note: note.start_tick)

    @staticmethod
    def to_music_note_channels(
        midi: mido.MidiFile,
        ignore_mismatch_error: bool = True,
        speed: float = 1.0,
        default_program_value: int = -1,
        default_tempo_value: int = mido.midifiles.midifiles.DEFAULT_TEMPO,
        pitched_note_rtable: MidiInstrumentTableType = MM_TOUCH_PITCHED_INSTRUMENT_TABLE,
        percussion_note_rtable: MidiInstrumentTableType = MM_TOUCH_PERCUSSION_INSTRUMENT_TABLE,
        vol_processing_function: FittingFunctionType = natural_curve,
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
        default_tempo_value: int
            默认的 MIDI TEMPO 值
        pitched_note_rtable: Dict[int, Tuple[str, int]]
            乐音乐器Midi-MC对照表
        percussion_note_rtable: Dict[int, Tuple[str, int]]
            打击乐器Midi-MC对照表
        vol_processing_function: Callable[[float], float]
            声像偏移拟合函数

        Returns
        -------
        以频道作为分割的Midi音符列表字典, 音符总数, 乐器使用统计:
        Tuple[MineNoteChannelType, int, Dict[str, int]]
        """

        if speed == 0:
            raise ZeroSpeedError("播放速度为 0 ，其需要(0,1]范围内的实数。")

        # 一个midi中仅有16个通道 我们通过通道来识别而不是音轨
        midi_channels: MineNoteChannelType = empty_midi_channels(default_staff=[])
        channel_program: Dict[int, int] = empty_midi_channels(
            default_staff=default_program_value
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
        ] = empty_midi_channels(default_staff=[])
        note_queue_B: Dict[
            int,
            List[
                Tuple[
                    int,
                    int,
                ]
            ],
        ] = empty_midi_channels(default_staff=[])

        # 直接使用mido.midifiles.tracks.merge_tracks转为单轨
        # 采用的时遍历信息思路
        for msg in midi.merged_track:
            if msg.time != 0:
                # 微秒
                microseconds += msg.time * tempo / midi.ticks_per_beat

            # 简化
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
                                start_time_=_ms,  # 微秒
                                duration_=microseconds - _ms,  # 微秒
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
        midi_obj: Optional[mido.MidiFile],
        midi_name: str,
        ignore_mismatch_error: bool = True,
        playment_speed: float = 1,
        default_tempo_value: int = mido.midifiles.midifiles.DEFAULT_TEMPO,
        pitched_note_rtable: MidiInstrumentTableType = MM_TOUCH_PITCHED_INSTRUMENT_TABLE,
        percussion_note_rtable: MidiInstrumentTableType = MM_TOUCH_PERCUSSION_INSTRUMENT_TABLE,
        enable_old_exe_format: bool = False,
        minimum_volume: float = 0.1,
        vol_processing_function: FittingFunctionType = natural_curve,
    ):
        """
        简单的midi转换类，将midi对象转换为我的世界结构或者包

        Parameters
        ----------
        midi_obj: mido.MidiFile 对象
            需要处理的midi对象
        midi_name: str
            此音乐之名称
        ignore_mismatch_error： bool
            是否在导入时忽略音符不匹配错误
        playment_speed: float
            音乐播放速度倍数
        default_tempo_value: int
            默认的MIDI TEMPO值
        pitched_note_rtable: Dict[int, Tuple[str, int]]
            乐音乐器Midi-MC对照表
        percussion_note_rtable: Dict[int, Tuple[str, int]]
            打击乐器Midi-MC对照表
        enable_old_exe_format: bool
            是否启用旧版(≤1.19)指令格式，默认为否
        minimum_volume: float
            最小播放音量
        vol_processing_function: Callable[[float], float]
            声像偏移拟合函数
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
            minimum_vol=minimum_volume,
            volume_processing_function=vol_processing_function,
            default_tempo=default_tempo_value,
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
        mismatch_error_ignorance bool
            是否在导入时忽略音符不匹配错误
        play_speed: float
            音乐播放速度倍数
        default_tempo: int
            默认的MIDI TEMPO值
        pitched_note_table: Dict[int, Tuple[str, int]]
            乐音乐器Midi-MC对照表
        percussion_note_table: Dict[int, Tuple[str, int]]
            打击乐器Midi-MC对照表
        old_exe_format: bool
            是否启用旧版(≤1.19)指令格式，默认为否
        min_volume: float
            最小播放音量
        vol_processing_func: Callable[[float], float]
            声像偏移拟合函数
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
                enable_old_exe_format=old_exe_format,
                minimum_volume=min_volume,
                vol_processing_function=vol_processing_func,
            )
        except (ValueError, TypeError) as E:
            raise MidiDestroyedError(f"文件{midi_file_path}可能损坏：{E}")
        except FileNotFoundError as E:
            raise FileNotFoundError(f"文件{midi_file_path}不存在：{E}")

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

    def redefine_execute_format(
        self, is_old_exe_cmd_using: bool = False
    ) -> "MidiConvert":
        """
        根据是否使用旧版执行命令格式，重新定义执行命令的起始格式。

        此方法用于处理 Minecraft 中的执行命令的格式差异。在 Minecraft 的命令系统中，
        "execute" 命令的用法在不同版本间有所变化。此方法允许动态选择使用旧版还是新版
        的命令格式，以便适应不同的 Minecraft 版本。

        Parameters
        ----------
        is_old_exe_cmd_using: bool
            是否使用旧版执行命令格式。

        Returns
        -------
        MidiConvert修改后的实例，允许链式调用
        """

        # 根据 is_old_exe_cmd_using 的值选择合适的执行命令头格式
        self.execute_cmd_head = (
            "execute {} ~ ~ ~ "  # 旧版执行命令格式
            if is_old_exe_cmd_using
            else "execute as {} at @s positioned ~ ~ ~ run "  # 新版执行命令格式
        )

        # 返回修改后的实例，支持链式调用
        return self

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

        return self.music_command_list, notes_list[-1].start_tick, max_multi + 1

    def to_command_list_in_delay_devided_by_instrument(
        self,
        player_selector: str = "@a",
    ) -> Tuple[Dict[str, List[MineCommand]], int, Dict[str, int]]:
        """
        将midi转换为我的世界命令列表，并输出每个音符之后的延迟

        Parameters
        ----------
        player_selector: str
            玩家选择器，默认为`@a`

        Returns
        -------
        Tuple[Dict[str, List[MineCommand指令]], int音乐时长游戏刻, int最大同时播放的指令数量 )
        """

        notes_list: List[MineNote] = sorted(
            [i for j in self.channels.values() for i in j],
            key=lambda note: note.start_tick,
        )

        command_dict: Dict[str, List[MineCommand]] = dict(
            [(inst, []) for inst in self.note_count_per_instrument.keys()]
        )
        multi: Dict[str, int] = dict(
            [(inst, 0) for inst in self.note_count_per_instrument.keys()]
        )
        max_multi: Dict[str, int] = dict(
            [(inst, 0) for inst in self.note_count_per_instrument.keys()]
        )
        delaytime_previous: Dict[str, int] = dict(
            [(inst, 0) for inst in self.note_count_per_instrument.keys()]
        )

        for note in notes_list:
            if (
                tickdelay := (note.start_tick - delaytime_previous[note.sound_name])
            ) == 0:
                multi[note.sound_name] += 1
            else:
                max_multi[note.sound_name] = max(
                    max_multi[note.sound_name], multi[note.sound_name]
                )
                multi[note.sound_name] = 0

            (
                mc_sound_ID,
                relative_coordinates,
                volume_percentage,
                mc_pitch,
            ) = minenote_to_command_paramaters(
                note,
                pitch_deviation=self.music_deviation,
            )

            command_dict[note.sound_name].append(
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
            delaytime_previous[note.sound_name] = note.start_tick

        self.music_command_list = [j for i in command_dict.values() for j in i]
        return command_dict, notes_list[-1].start_tick, max_multi

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
