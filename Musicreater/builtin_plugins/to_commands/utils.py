# -*- coding: utf-8 -*-

"""
音·创 v3 内置的指令生成插件的功能方法
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

from typing import (
    BinaryIO,
    Optional,
    Dict,
    List,
    Callable,
    Tuple,
    Mapping,
    Union,
    Literal,
)

from Musicreater import MineNote, SingleNote
from Musicreater.constants import MM_INSTRUMENT_DEVIATION_TABLE


# 这个函数可以直接被优化成一个只处理音调参数的，没必要完整留着
def minenote_to_command_parameters(
    mine_note: MineNote,
    pitch_deviation: float = 0,
) -> Tuple[
    Tuple[float, float, float],
    Union[float, Literal[None]],
]:
    """
    将 MineNote 对象转为《我的世界》音符播放所需之参数

    参数
    ----
    mine_note: MineNote
        我的世界音符对象
    pitch_deviation: float
        音调偏移量

    返回
    ----
    tuple[float, float, float], float
        播放视角坐标, 指令音调参数
    """

    return (
        mine_note.position.position_displacement,
        (
            None
            if mine_note.percussive
            else (
                2
                ** (
                    (
                        mine_note.pitch
                        - 60
                        - MM_INSTRUMENT_DEVIATION_TABLE.get(mine_note.instrument, 6)
                        + pitch_deviation
                    )
                    / 12
                )
            )
        ),
    )


def calculate_minecraft_pitch(
    note: MineNote, pitch_deviation: float = 0
) -> Optional[float]:
    """
    计算音符的音调参数

    参数
    ----
    note: MineNote
        我的世界音符对象
    deviation: float
        音调偏移量

    返回
    ----
    Optional[float]
        音调参数, 当为打击乐器时为 None
    """
    return (
        None
        if note.percussive
        else (
            2
            ** (
                (
                    note.pitch
                    - 60
                    - MM_INSTRUMENT_DEVIATION_TABLE.get(note.instrument, 6)
                    + pitch_deviation
                )
                / 12
            )
        )
    )
