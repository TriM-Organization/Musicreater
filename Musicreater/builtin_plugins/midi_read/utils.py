
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



def velocity_2_distance_natural(
    vol: float,
) -> float:
    """
    midi力度值拟合成的距离函数

    Parameters
    ----------
    vol: int
        midi 音符力度值

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


def velocity_2_distance_straight(vol: float) -> float:
    """
    midi力度值拟合成的距离函数

    Parameters
    ----------
    vol: int
        midi 音符力度值

    Returns
    -------
    float播放中心到玩家的距离
    """
    return vol / -8 + 16


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

