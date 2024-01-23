# -*- coding: utf-8 -*-
"""
存放主程序所必须的功能性内容
"""

"""
版权所有 © 2023 音·创 开发者
Copyright © 2023 all the developers of Musicreater

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md

import math
import random

from .constants import MM_INSTRUMENT_DEVIATION_TABLE, MC_INSTRUMENT_BLOCKS_TABLE
from .subclass import SingleNote

from .types import Any, Dict, Tuple, Optional, Callable, Literal, Union, MidiInstrumentTableType


def mctick2timestr(mc_tick: int) -> str:
    """
    将《我的世界》的游戏刻计转为表示时间的字符串
    """
    return str(int(int(mc_tick / 20) / 60)) + ":" + str(int(int(mc_tick / 20) % 60))


def empty_midi_channels(channel_count: int = 17, staff: Any = {}) -> Dict[int, Any]:
    """
    空MIDI通道字典
    """

    return dict(
        (
            i,
            (staff.copy() if isinstance(staff, (dict, list)) else staff),
        )  # 这告诉我们，你不能忽略任何一个复制的序列，因为它真的，我哭死，折磨我一整天，全在这个bug上了
        for i in range(channel_count)
    )


def inst_to_sould_with_deviation(
    instrumentID: int,
    reference_table: MidiInstrumentTableType,
    default_instrument: str = "note.flute",
    default_deviation: Optional[int] = 5,
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
    reference_table: Dict[int, Tuple[str, int]]
        转换乐器参照表

    Returns
    -------
    tuple(str我的世界乐器名, int转换算法中的X)
    """
    return reference_table.get(
        instrumentID,
        (
            default_instrument,
            default_deviation
            if default_deviation
            else MM_INSTRUMENT_DEVIATION_TABLE.get(default_instrument, -1),
        ),
    )

    # 明明已经走了
    # 凭什么还要在我心里留下缠绵缱绻


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


def note_to_command_parameters(
    note_: SingleNote,
    reference_table: MidiInstrumentTableType,
    volume_percentage: float = 1,
    volume_processing_method: Callable[[float], float] = natural_curve,
) -> Tuple[str, float, float, Union[float, Literal[None]],]:
    """
    将音符转为播放的指令
    :param note_:int 音符对象
    :param reference_table:Dict[int, Tuple[str, int]] 转换对照表
    :param volume_percentage:int 音量占比(0,1]
    :param volume_proccessing_method:Callable[[float], float]: 音量处理函数

    :return str[我的世界音符ID], float[播放距离], float[指令音量参数], float[指令音调参数]
    """
    mc_sound_ID, deviation = inst_to_sould_with_deviation(
        note_.inst,
        reference_table,
        "note.bd" if note_.percussive else "note.flute",
    )

    # delaytime_now = round(self.start_time / float(speed) / 50)
    mc_pitch = None if note_.percussive else 2 ** ((note_.note - 60 - deviation) / 12)

    mc_distance_volume = volume_processing_method(note_.velocity * volume_percentage)

    return mc_sound_ID, mc_distance_volume, volume_percentage, mc_pitch


def from_single_note(
    note_: SingleNote, random_select: bool = False, default_block: str = "air"
):
    """
    将我的世界乐器名改作音符盒所需的对应方块名称

    Parameters
    ----------
    note_: SingleNote
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
