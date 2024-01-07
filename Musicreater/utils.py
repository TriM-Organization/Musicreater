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

from .constants import PERCUSSION_INSTRUMENT_TABLE, PITCHED_INSTRUMENT_TABLE
from typing import Any, Dict, Tuple


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
        return PITCHED_INSTRUMENT_TABLE[instrumentID]
    except KeyError:
        return "note.flute", 5


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
        return PERCUSSION_INSTRUMENT_TABLE[instrumentID]
    except KeyError:
        return "note.bd", 7

    # 明明已经走了
    # 凭什么还要在我心里留下缠绵缱绻


def volume2distance(vol: float) -> float:
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
