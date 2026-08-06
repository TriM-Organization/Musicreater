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


def get_accurate_deviation(
    instrument: str,
    pitch_deviation: float = 0,
) -> float:
    """
    获取乐器所对应的音调偏移量

    参数
    ----
    instrument: str
        我的世界乐器
    pitch_deviation: float
        人工干预的音调偏移量

    返回
    ----
    tuple[float, float, float], float
        播放视角坐标, 指令音调参数
    """

    return pitch_deviation - MM_INSTRUMENT_DEVIATION_TABLE.get(instrument, 6)
