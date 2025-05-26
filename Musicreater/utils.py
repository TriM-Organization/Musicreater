# -*- coding: utf-8 -*-
"""
存放主程序所必须的功能性内容
"""

"""
版权所有 © 2024 金羿 & 诸葛亮与八卦阵
Copyright © 2025 Eilles & bgArray

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md

import math
import random

# from io import BytesIO
from typing import (
    Any,
    BinaryIO,
    Callable,
    Dict,
    Generator,
    List,
    Literal,
    Optional,
    Tuple,
    Union,
)

from xxhash import xxh3_64, xxh3_128, xxh32

from .constants import (
    MC_INSTRUMENT_BLOCKS_TABLE,
    MC_PITCHED_INSTRUMENT_LIST,
    MM_INSTRUMENT_DEVIATION_TABLE,
    MM_INSTRUMENT_RANGE_TABLE,
)
from .exceptions import MusicSequenceDecodeError
from .subclass import MineNote, mctick2timestr
from .types import MidiInstrumentTableType, MineNoteChannelType


def empty_midi_channels(
    channel_count: int = 17, default_staff: Any = {}
) -> Dict[int, Any]:
    """
    空MIDI通道字典
    """

    return dict(
        (
            i,
            (
                default_staff.copy()
                if isinstance(default_staff, (dict, list))
                else default_staff
            ),
        )  # 这告诉我们，你不能忽略任何一个复制的序列，因为它真的，我哭死，折磨我一整天，全在这个bug上了
        for i in range(channel_count)
    )


def inst_to_sould_with_deviation(
    instrumentID: int,
    reference_table: MidiInstrumentTableType,
    default_instrument: str = "note.flute",
) -> Tuple[str, int]:
    """
    返回midi的乐器ID对应的我的世界乐器名，对于音域转换算法，如下：
    2**( ( msg.note - 60 - X ) / 12 ) 即为MC的音高

    Parameters
    ----------
    instrumentID: int
        midi的乐器ID
    reference_table: Dict[int, Tuple[str, int]]
        转换乐器参照表
    default_instrument: str
        查无此乐器时的替换乐器

    Returns
    -------
    tuple(str我的世界乐器名, int转换算法中的偏移量)
    """
    sound_id = midi_inst_to_mc_sound(
        instrumentID=instrumentID,
        reference_table=reference_table,
        default_instrument=default_instrument,
    )
    return sound_id, MM_INSTRUMENT_DEVIATION_TABLE.get(
        sound_id,
        MM_INSTRUMENT_DEVIATION_TABLE.get(
            default_instrument, 6 if sound_id in MC_PITCHED_INSTRUMENT_LIST else -1
        ),
    )


def midi_inst_to_mc_sound(
    instrumentID: int,
    reference_table: MidiInstrumentTableType,
    default_instrument: str = "note.flute",
) -> str:
    """
    返回midi的乐器ID对应的我的世界乐器名

    Parameters
    ----------
    instrumentID: int
        midi的乐器ID
    reference_table: Dict[int, Tuple[str, int]]
        转换乐器参照表
    default_instrument: str
        查无此乐器时的替换乐器

    Returns
    -------
    str我的世界乐器名
    """
    return reference_table.get(
        instrumentID,
        default_instrument,
    )


def natural_curve(
    vol: float,
) -> float:
    """
    midi力度值拟合成的距离函数

    Parameters
    ----------
    vol: int
        midi音符力度值

    Returns
    -------
    float播放中心到玩家的距离
    """
    return (
        -8.081720684086314
        * math.log(
            vol + 14.579508825070013,
        )
        + 37.65806375944386
        if vol < 60.64
        else 0.2721359356095803 * ((vol + 2592.272889454798) ** 1.358571233418649)
        + -6.313841334963396 * (vol + 2592.272889454798)
        + 4558.496367823575
    )


def straight_line(vol: float) -> float:
    """
    midi力度值拟合成的距离函数

    Parameters
    ----------
    vol: int
        midi音符力度值

    Returns
    -------
    float播放中心到玩家的距离
    """
    return vol / -8 + 16


def minenote_to_command_paramaters(
    note_: MineNote,
    pitch_deviation: float = 0,
) -> Tuple[
    str,
    Tuple[float, float, float],
    float,
    Union[float, Literal[None]],
]:
    """
    将MineNote对象转为《我的世界》音符播放所需之参数
    :param note_:MineNote 音符对象
    :param deviation:float 音调偏移量

    :return str[我的世界音符ID], Tuple[float,float,float]播放视角坐标, float[指令音量参数], float[指令音调参数]
    """

    return (
        note_.sound_name,
        note_.position_displacement,
        note_.velocity / 127,
        (
            None
            if note_.percussive
            else (
                2
                ** (
                    (
                        note_.note_pitch
                        - 60
                        - MM_INSTRUMENT_DEVIATION_TABLE.get(note_.sound_name, 6)
                        + pitch_deviation
                    )
                    / 12
                )
            )
        ),
    )


# def single_note_to_command_parameters(
#     note_: SingleNote,
#     reference_table: MidiInstrumentTableType,
#     deviation: float = 0,
#     volume_processing_method: Callable[[float], float] = natural_curve,
# ) -> Tuple[
#     str,
#     Tuple[float, float, float],
#     float,
#     Union[float, Literal[None]],
# ]:
#     """
#     将音符转为播放的指令之参数
#     :param note_:int 音符对象
#     :param reference_table:Dict[int, str] 转换对照表
#     :param deviation:float 音调偏移量
#     :param volume_proccessing_method:Callable[[float], float] 音量处理函数

#     :return str[我的世界音符ID], Tuple[float,float,float]播放视角坐标, float[指令音量参数], float[指令音调参数]
#     """

#     mc_sound_ID, _X = inst_to_sould_with_deviation(
#         note_.inst,
#         reference_table,
#         "note.bd" if note_.percussive else "note.flute",
#     )

#     mc_distance_volume = volume_processing_method(note_.velocity)

#     return (
#         mc_sound_ID,
#         (0, mc_distance_volume, 0),
#         note_.velocity / 127,
#         None if note_.percussive else 2 ** ((note_.pitch - 60 - _X + deviation) / 12),
#     )


def midi_msgs_to_minenote(
    inst_: int,  # 乐器编号
    note_: int,
    percussive_: bool,  # 是否作为打击乐器启用
    velocity_: int,
    start_time_: int,
    duration_: int,
    play_speed: float,
    midi_reference_table: MidiInstrumentTableType,
    volume_processing_method_: Callable[[float], float],
    note_table_replacement: Dict[str, str] = {},
) -> MineNote:
    """
    将Midi信息转为我的世界音符对象
    :param inst_: int 乐器编号
    :param note_: int 音高编号（音符编号）
    :param percussive_: bool 是否作为打击乐器启用
    :param velocity_: int 力度(响度)
    :param start_time_: int 音符起始时间（微秒）
    :param duration_: int 音符持续时间（微秒）
    :param play_speed: float 曲目播放速度
    :param midi_reference_table: Dict[int, str] 转换对照表
    :param volume_proccessing_method_: Callable[[float], float] 音量处理函数
    :param note_table_replacement: Dict[str, str] 音符替换表，定义 Minecraft 音符字串的替换

    :return MineNote我的世界音符对象
    """
    mc_sound_ID = midi_inst_to_mc_sound(
        inst_,
        midi_reference_table,
        "note.bd" if percussive_ else "note.flute",
    )

    mc_distance_volume = volume_processing_method_(velocity_)

    return MineNote(
        mc_sound_name=note_table_replacement.get(mc_sound_ID, mc_sound_ID),
        midi_pitch=note_,
        midi_velocity=velocity_,
        start_time=(tk := int(start_time_ / float(play_speed) / 50000)),
        last_time=round(duration_ / float(play_speed) / 50000),
        mass_precision_time=round((start_time_ / float(play_speed) - tk * 50000) / 800),
        is_percussion=percussive_,
        displacement=(0, mc_distance_volume, 0),
    )


def midi_msgs_to_minenote_using_kami_respack(
    inst_: int,  # 乐器编号
    note_: int,
    percussive_: bool,  # 是否作为打击乐器启用
    velocity_: int,
    start_time_: int,
    duration_: int,
    play_speed: float,
    midi_reference_table: MidiInstrumentTableType,
    volume_processing_method_: Callable[[float], float],
    note_table_replacement: Dict[str, str] = {},
) -> MineNote:
    """
    将Midi信息转为我的世界音符对象
    :param inst_: int 乐器编号
    :param note_: int 音高编号（音符编号）
    :param percussive_: bool 是否作为打击乐器启用
    :param velocity_: int 力度(响度)
    :param start_time_: int 音符起始时间（微秒）
    :param duration_: int 音符持续时间（微秒）
    :param play_speed: float 曲目播放速度
    :param midi_reference_table: Dict[int, str] 转换对照表
    :param volume_proccessing_method_: Callable[[float], float] 音量处理函数
    :param note_table_replacement: Dict[str, str] 音符替换表，定义 Minecraft 音符字串的替换

    :return MineNote我的世界音符对象
    """

    using_original = False
    if not percussive_ and (0 <= inst_ <= 119):
        mc_sound_ID = "{}{}.{}".format(
            inst_, "d" if duration_ < 500_000 else "c", note_
        )
    elif percussive_ and (27 <= inst_ <= 87):
        mc_sound_ID = "-1d.{}".format(inst_)
    else:
        using_original = True
        mc_sound_ID = midi_inst_to_mc_sound(
            inst_,
            midi_reference_table,
            "note.bd" if percussive_ else "note.flute",
        )

    mc_distance_volume = volume_processing_method_(velocity_)

    return MineNote(
        mc_sound_name=note_table_replacement.get(mc_sound_ID, mc_sound_ID),
        midi_pitch=note_ if using_original else 1,
        midi_velocity=velocity_,
        start_time=(tk := int(start_time_ / float(play_speed) / 50000)),
        last_time=round(duration_ / float(play_speed) / 50000),
        mass_precision_time=round((start_time_ / float(play_speed) - tk * 50000) / 800),
        is_percussion=percussive_,
        displacement=(0, mc_distance_volume, 0),
        extra_information={
            "USING_ORIGINAL_SOUND": using_original,  # 判断 extra_information 中是否有 USING_ORIGINAL_SOUND 键是判断是否使用神羽资源包解析的一个显著方法
            "INST_VALUE": note_ if percussive_ else inst_,
            "NOTE_VALUE": inst_ if percussive_ else note_,
        },
    )


# def single_note_to_minenote(
#     note_: SingleNote,
#     reference_table: MidiInstrumentTableType,
#     play_speed: float = 0,
#     volume_processing_method: Callable[[float], float] = natural_curve,
# ) -> MineNote:
#     """
#     将音符转为我的世界音符对象
#     :param note_:SingleNote 音符对象
#     :param reference_table:Dict[int, str] 转换对照表
#     :param play_speed:float 播放速度
#     :param volume_proccessing_method:Callable[[float], float] 音量处理函数

#     :return MineNote我的世界音符对象
#     """
#     mc_sound_ID = midi_inst_to_mc_sound(
#         note_.inst,
#         reference_table,
#         "note.bd" if note_.percussive else "note.flute",
#     )

#     mc_distance_volume = volume_processing_method(note_.velocity)

#     return MineNote(
#         mc_sound_name=mc_sound_ID,
#         midi_pitch=note_.pitch,
#         midi_velocity=note_.velocity,
#         start_time=round(note_.start_time / float(play_speed) / 50),
#         last_time=round(note_.duration / float(play_speed) / 50),
#         is_percussion=note_.percussive,
#         displacement=(0, mc_distance_volume, 0),
#         extra_information=note_.extra_info,
#     )


def is_in_diapason(note_pitch: float, instrument: str) -> bool:
    note_range = MM_INSTRUMENT_RANGE_TABLE.get(instrument, ((-1, 128), 0))[0]
    return note_pitch >= note_range[0] and note_pitch <= note_range[1]


def is_note_in_diapason(
    note_: MineNote,
) -> bool:
    note_range = MM_INSTRUMENT_RANGE_TABLE.get(note_.sound_name, ((-1, 128), 0))[0]
    return note_.note_pitch >= note_range[0] and note_.note_pitch <= note_range[1]


def note_to_redstone_block(
    note_: MineNote, random_select: bool = False, default_block: str = "air"
):
    """
    将我的世界乐器名改作音符盒所需的对应方块名称

    Parameters
    ----------
    note_: MineNote
        音符类
    random_select: bool
        是否随机选取对应方块
    default_block: str
        查表查不到怎么办？默认一个！

    Returns
    -------
    str方块名称
    """
    pass
    # return SingleNoteBox()  # TO-DO


@staticmethod
def soundID_to_blockID(
    sound_id: str, random_select: bool = False, default_block: str = "air"
) -> str:
    """
    将我的世界乐器名改作音符盒所需的对应方块名称

    Parameters
    ----------
    sound_id: str
        将我的世界乐器名
    random_select: bool
        是否随机选取对应方块
    default_block: str
        查表查不到怎么办？默认一个！

    Returns
    -------
    str方块名称
    """
    if random_select:
        return random.choice(MC_INSTRUMENT_BLOCKS_TABLE.get(sound_id, (default_block,)))
    else:
        return MC_INSTRUMENT_BLOCKS_TABLE.get(sound_id, (default_block,))[0]


def load_decode_musicsequence_metainfo(
    buffer_in: BinaryIO,
) -> Tuple[str, float, float, bool, int]:
    """
    以流的方式解码音乐序列元信息

    Parameters
    ----------
    buffer_in: BytesIO
        MSQ格式的字节流

    Returns
    -------
    Tuple[str, float, float, bool, int]
        音乐名称，最小音量，音调偏移，是否启用高精度，最后的流指针位置

    """
    buffer_in.seek(4, 0)
    group_1 = int.from_bytes(buffer_in.read(2), "big")
    group_2 = int.from_bytes(buffer_in.read(2), "big", signed=False)

    # high_quantity = bool(group_2 & 0b1000000000000000)
    # print(group_2, high_quantity)

    music_name_ = buffer_in.read(stt_index := (group_1 >> 10)).decode("GB18030")

    return (
        music_name_,
        (group_1 & 0b1111111111) / 1000,
        (
            (-1 if group_2 & 0b100000000000000 else 1)
            * (group_2 & 0b11111111111111)
            / 1000
        ),
        bool(group_2 & 0b1000000000000000),
        stt_index + 8,
    )


def load_decode_fsq_flush_release(
    buffer_in: BinaryIO,
    starter_index: int,
    high_quantity_note: bool,
) -> Generator[MineNote, Any, None]:
    """
    以流的方式解码FSQ音乐序列的音符序列并流式返回

    Parameters
    ----------
    buffer_in : BytesIO
        输入的MSQ格式二进制字节流
    starter_index : int
        字节流中，音符序列的起始索引
    high_quantity_note : bool
        是否启用高精度音符解析

    Returns
    -------
    Generator[MineNote, Any, None]
        以流的方式返回解码后的音符序列，每次返回一个元组
        元组中包含两个元素，第一个元素为音符所在通道的索引，第二个元素为音符对象

    Raises
    ------
    MusicSequenceDecodeError
        当解码过程中出现错误，抛出异常
    """

    if buffer_in.tell() != starter_index:
        buffer_in.seek(starter_index, 0)

    total_note_count = int.from_bytes(
        buffer_in.read(5),
        "big",
        signed=False,
    )

    for i in range(total_note_count):
        if (i % 100 == 0) and i:
            buffer_in.read(4)

        try:
            _note_bytes_length = (
                12 + high_quantity_note + ((_first_byte := (buffer_in.read(1)))[0] >> 2)
            )

            yield MineNote.decode(
                code_buffer=_first_byte + buffer_in.read(_note_bytes_length),
                is_high_time_precision=high_quantity_note,
            )
        except Exception as _err:
            # print(bytes_buffer_in[stt_index:end_index])
            raise MusicSequenceDecodeError(
                _err,
                "所截取的音符码之首个字节：",
                _first_byte,
            )


def load_decode_msq_flush_release(
    buffer_in: BinaryIO,
    starter_index: int,
    high_quantity_note: bool,
) -> Generator[Tuple[int, MineNote], Any, None]:
    """以流的方式解码MSQ音乐序列的音符序列并流式返回

    Parameters
    ----------
    buffer_in : BytesIO
        输入的MSQ格式二进制字节流
    starter_index : int
        字节流中，音符序列的起始索引
    high_quantity_note : bool
        是否启用高精度音符解析

    Returns
    -------
    Generator[Tuple[int, MineNote], Any, None]
        以流的方式返回解码后的音符序列，每次返回一个元组
        元组中包含两个元素，第一个元素为音符所在通道的索引，第二个元素为音符对象

    Raises
    ------
    MusicSequenceDecodeError
        当解码过程中出现错误，抛出异常

    """

    # _total_verify = xxh3_64(buffer_in.read(starter_index), seed=total_note_count)

    # buffer_in.seek(starter_index, 0)
    if buffer_in.tell() != starter_index:
        buffer_in.seek(starter_index, 0)
    _bytes_buffer_in = buffer_in.read()
    # int.from_bytes(_bytes_buffer_in[0 : 4], "big")

    _now_channel_starter_index = 0

    _total_note_count = 1

    _channel_infos = empty_midi_channels(
        default_staff={"NOW_INDEX": 0, "NOTE_COUNT": 0, "HAVE_READ": 0, "END_INDEX": -1}
    )

    for __channel_index in _channel_infos.keys():
        # _channel_note_count = 0

        _now_channel_ender_sign = xxh3_64(
            _bytes_buffer_in[
                _now_channel_starter_index : _now_channel_starter_index + 4
            ],
            seed=3,
        ).digest()

        # print(
        #     "[DEBUG] 索引取得：",
        #     _bytes_buffer_in[
        #         _now_channel_starter_index : _now_channel_starter_index + 4
        #     ],
        #     "校验索引",
        #     _now_channel_ender_sign,
        # )

        _now_channel_ender_index = _bytes_buffer_in.find(_now_channel_ender_sign)

        # print("[DEBUG] 索引取得：", _now_channel_ender_index,)

        _channel_note_count = int.from_bytes(
            _bytes_buffer_in[
                _now_channel_starter_index : _now_channel_starter_index + 4
            ],
            "big",
        )

        if _channel_note_count == 0:
            continue

        while (
            xxh3_64(
                _bytes_buffer_in[_now_channel_starter_index:_now_channel_ender_index],
                seed=_channel_note_count,
            ).digest()
            != _bytes_buffer_in[
                _now_channel_ender_index + 8 : _now_channel_ender_index + 16
            ]
        ):
            _now_channel_ender_index += 8 + _bytes_buffer_in[
                _now_channel_ender_index + 8 :
            ].find(_now_channel_ender_sign)

            # print(
            #     "[WARNING] XXHASH 无法匹配，当前序列",
            #     __channel_index,
            #     "当前全部序列字节串",
            #     _bytes_buffer_in[
            #             _now_channel_starter_index:_now_channel_ender_index
            #         ],
            #         "校验值",
            #     xxh3_64(
            #         _bytes_buffer_in[
            #             _now_channel_starter_index:_now_channel_ender_index
            #         ],
            #         seed=_channel_note_count,
            #     ).digest(),
            #     _bytes_buffer_in[
            #         _now_channel_ender_index + 8 : _now_channel_ender_index + 16
            #     ],
            #     "改变结尾索引",
            #     _now_channel_ender_index,
            # )

        _channel_infos[__channel_index]["NOW_INDEX"] = _now_channel_starter_index + 4
        _channel_infos[__channel_index]["END_INDEX"] = _now_channel_ender_index
        _channel_infos[__channel_index]["NOTE_COUNT"] = _channel_note_count

        # print(
        #     "[DEBUG] 当前序列", __channel_index, "值", _channel_infos[__channel_index]
        # )

        _total_note_count += _channel_note_count

        _now_channel_starter_index = _now_channel_ender_index + 16
        # for i in range(
        #     int.from_bytes(
        #         bytes_buffer_in[stt_index : (stt_index := stt_index + 4)], "big"
        #     )
        # ):
    _to_yield_note_list: List[Tuple[MineNote, int]] = []

    # {"NOW_INDEX": 0, "NOTE_COUNT": 0, "HAVE_READ": 0, "END_INDEX": -1}

    while _total_note_count:
        _read_in_note_list: List[Tuple[MineNote, int]] = []
        for __channel_index in _channel_infos.keys():
            if (
                _channel_infos[__channel_index]["HAVE_READ"]
                < _channel_infos[__channel_index]["NOTE_COUNT"]
            ):
                # print("当前已读", _channel_infos[__channel_index]["HAVE_READ"])
                try:
                    _end_index = (
                        (_stt_index := _channel_infos[__channel_index]["NOW_INDEX"])
                        + 13
                        + high_quantity_note
                        + (_bytes_buffer_in[_stt_index] >> 2)
                    )
                    # print("读取音符字节串", _bytes_buffer_in[_stt_index:_end_index])
                    _read_in_note_list.append(
                        (
                            MineNote.decode(
                                code_buffer=_bytes_buffer_in[_stt_index:_end_index],
                                is_high_time_precision=high_quantity_note,
                            ),
                            __channel_index,
                        )
                    )
                    _channel_infos[__channel_index]["HAVE_READ"] += 1
                    _channel_infos[__channel_index]["NOW_INDEX"] = _end_index
                    _total_note_count -= 1
                except Exception as _err:
                    # print(channels_)
                    raise MusicSequenceDecodeError("难以定位的解码错误", _err)
        if not _read_in_note_list:
            break
            # _note_list.append
        min_stt_note: MineNote = min(_read_in_note_list, key=lambda x: x[0].start_tick)[
            0
        ]
        for i in range(len(_to_yield_note_list)):
            __note, __channel_index = _to_yield_note_list[i]
            if __note.start_tick >= min_stt_note.start_tick:
                break
            else:
                yield __channel_index, __note
                _to_yield_note_list.pop(i)

        _to_yield_note_list.extend(_read_in_note_list)
        _to_yield_note_list.sort(key=lambda x: x[0].start_tick)

    for __note, __channel_index in sorted(
        _to_yield_note_list, key=lambda x: x[0].start_tick
    ):
        yield __channel_index, __note
    # 俺寻思能用


def guess_deviation(
    total_note_count: int,
    total_instrument_count: int,
    note_count_per_instrument: Optional[Dict[str, int]] = None,
    qualified_note_count_per_instrument: Optional[Dict[str, int]] = None,
    music_channels: Optional[MineNoteChannelType] = None,
) -> float:
    """
    通过乐器权重来计算一首歌的音调偏移
    这个方法未经验证，但理论有效，金羿首创

    Parameters
    ----------
    total_note_count: int
        歌曲总音符数
    total_instrument_count: int
        歌曲乐器总数
    note_count_per_instrument: Dict[str, int]
        乐器名称与乐器音符数对照表
    qualified_note_count_per_instrument: Dict[str, int]
        每个乐器中，符合该乐器的音调范围的音符数
    music_channels: MineNoteChannelType
        MusicSequence类的音乐通道字典

    Returns
    -------
    float估测的音调偏移值
    """
    if note_count_per_instrument is None or qualified_note_count_per_instrument is None:
        if music_channels is None:
            raise ValueError("参数不足，算逑！")
        note_count_per_instrument = {}
        qualified_note_count_per_instrument = {}
        for this_note in [k for j in music_channels.values() for k in j]:
            if this_note.sound_name in note_count_per_instrument.keys():
                note_count_per_instrument[this_note.sound_name] += 1
                qualified_note_count_per_instrument[
                    this_note.sound_name
                ] += is_note_in_diapason(this_note)
            else:
                note_count_per_instrument[this_note.sound_name] = 1
                qualified_note_count_per_instrument[this_note.sound_name] = int(
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
                    * (note_count - qualified_note_count_per_instrument[inst])
                )
                for inst, note_count in note_count_per_instrument.items()
            ]
        )
        / total_instrument_count
        / total_note_count
    )
