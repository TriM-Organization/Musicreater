# -*- coding: utf-8 -*-

"""
音·创 v3 内置的 Midi 读取插件的功能方法
"""

"""
版权所有 © 2026 金羿、玉衡Alioth
Copyright © 2026 Eilles, YuhengAlioth

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md


import math

from typing import Callable, Dict, List, Optional, Sequence, Tuple, Mapping

from Musicreater import SingleNote, SoundAtmos



def panning_2_rotation_linear(pan_: float) -> float:
    """
    Midi 左右平衡偏移值线性转为声源旋转角度

    Parameters
    ----------
    pan_: int
        Midi 左右平衡偏移值
        注：此参数为int，范围从 0 到 127，当为 64 时，声源居中

    Returns
    -------
    float
        声源旋转角度
    """
    return (pan_ - 64) * 90 / 63


def panning_2_rotation_trigonometric(pan_: float) -> float:
    """
    Midi 左右平衡偏移值，依照圆的声场定位，转为声源旋转角度

    Parameters
    ----------
    pan_: int
        Midi 左右平衡偏移值
        注：此参数为int，范围从 0 到 127，当为 64 时，声源居中

    Returns
    -------
    float
        声源旋转角度
    """
    if pan_ <= 0:
        return -90
    elif pan_ >= 127:
        return 90
    else:
        return math.degrees(math.acos((64 - pan_) / 63)) - 90


def midi_inst_to_mc_sound(
    instrumentID: int,
    reference_table: Mapping[int, str],
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


def midi_msgs_to_noteinfo(
    inst: int,  # 乐器编号
    note: int,
    percussive: bool,  # 是否作为打击乐器启用
    volume: int,
    master_volume: int,
    velocity: int,
    panning: int,
    start_time: int,
    duration: int,
    play_speed: float,
    midi_reference_table: Mapping[int, str],
    panning_processing_method: Callable[[float], float],
    note_table_replacement: Mapping[str, str] = {},
    lyric_line: str = "",
) -> Tuple[SingleNote, str, Tuple[float, float]]:
    """
    将 Midi信息转为音符对象

    Parameters
    ------------
    inst: int
        乐器编号
    note: int
        音高编号（音符编号）
    percussive: bool
        是否作为打击乐器启用
    volume: int
        音量
    master_volume: int
        主音量
    velocity: int
        力度
    panning: int
        声相偏移
    start_time: int
        音符起始时间（微秒）
    duration: int
        音符持续时间（微秒）
    play_speed: float
        曲目播放速度
    midi_reference_table: Dict[int, str]
        转换对照表
    panning_processing_method: Callable[[float], float]
        立体声相偏移处理函数
    note_table_replacement: Dict[str, str]
        音符替换表，定义 Minecraft 音符字串的替换
    lyric_line: str
        该音符的歌词

    Returns
    ---------
    Tuple[
        MineNote我的世界音符对象,
        str我的世界声音名,
        Tuple[float, float]声源旋转角度
    ]
    """
    mc_sound_ID = midi_inst_to_mc_sound(
        inst,
        midi_reference_table,
        "note.bd" if percussive else "note.flute",
    )

    return (
        SingleNote(
            note_pitch=note,
            start_tick=(tk := int(start_time / float(play_speed) / 50000)),
            keep_tick=round(duration / float(play_speed) / 50000),
            mass_precision_time=round(
                (start_time / float(play_speed) - tk * 50000) / 200
            ),
            extra_information={
                "LYRIC_TEXT": lyric_line,
                "VELOCITY_VALUE": velocity,
                "VOLUME_VALUE": volume,
                "MASTER_VOLUME_VALUE": master_volume,
                "PIN_VALUE": panning,
            },
        ),
        note_table_replacement.get(mc_sound_ID, mc_sound_ID),
        (panning_processing_method(panning), 0),
    )
