# -*- coding: utf-8 -*-
"""
MCSTRUCTURE 共享结构原语库 - 方块生成函数
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


from typing import Tuple

from TrimMCStruct import Block, TAG_Byte, TAG_Long

from .constants import COMPABILITY_VERSION_119


def form_note_block_in_NBT_struct(
    note: int,
    coordinate: Tuple[int, int, int],
    instrument: str = "note.harp",
    powered: bool = False,
    compability_version_number: int = COMPABILITY_VERSION_119,
) -> Block:
    """
    生成音符盒方块

    Parameters
    ------------
    note: int (0~24)
        音符的音高
    coordinate: tuple[int, int, int]
        此方块所在之相对坐标
    instrument: str
        音符盒的乐器
    powered: bool
        是否已被激活

    Returns
    -------
    Block
        生成的方块对象
    """

    return Block(
        "minecraft",
        "noteblock",
        {
            "instrument": instrument.replace("note.", ""),
            "note": note,
            "powered": powered,
        },
        {
            "block_entity_data": {
                "note": TAG_Byte(note),
                "id": "noteblock",
                "x": coordinate[0],
                "y": coordinate[1],
                "z": coordinate[2],
            }  # type: ignore
        },
        compability_version=compability_version_number,
    )


def form_repeater_in_NBT_struct(
    delay: int,
    facing: int,
    compability_version_number: int = COMPABILITY_VERSION_119,
) -> Block:
    """
    生成中继器方块

    Parameters
    ----------
    facing: int (0~3)
        朝向：
        Z- 北 0
        X- 东 1
        Z+ 南 2
        X+ 西 3
    delay: int (0~3)
        信号延迟

    Returns
    -------
    Block
        生成的方块对象
    """

    return Block(
        "minecraft",
        "unpowered_repeater",
        {
            "repeater_delay": delay,
            "direction": facing,
        },
        compability_version=compability_version_number,
    )


def form_command_block_in_NBT_struct(
    command: str,
    coordinate: tuple,
    particularValue: int,
    impluse: int = 0,
    condition: bool = False,
    alwaysRun: bool = True,
    tickDelay: int = 0,
    customName: str = "",
    executeOnFirstTick: bool = False,
    trackOutput: bool = True,
    compability_version_number: int = COMPABILITY_VERSION_119,
) -> Block:
    """
    使用指定参数生成指令方块


    Parameters
    ----------
    command: str
        指令
    coordinate: tuple[int,int,int]
        此方块所在之相对坐标
    particularValue: int
        方块特殊值，即朝向
        :0	下	无条件
        :1	上	无条件
        :2	z轴负方向	无条件
        :3	z轴正方向	无条件
        :4	x轴负方向	无条件
        :5	x轴正方向	无条件
        :6	下	无条件
        :7	下	无条件
        :8	下	有条件
        :9	上	有条件
        :10	z轴负方向	有条件
        :11	z轴正方向	有条件
        :12	x轴负方向	有条件
        :13	x轴正方向	有条件
        :14	下	有条件
        :14	下	有条件
        注意！此处特殊值中的条件会被下面condition参数覆写
    impluse: int (0|1|2)
        方块类型
        0脉冲 1循环 2连锁
    condition: bool
        是否有条件
    alwaysRun: bool
        是否始终执行
    tickDelay: int
        执行延时
    customName: str
        悬浮字
    executeOnFirstTick: bool
        是否启用首刻执行（循环指令方块是否激活后立即执行，若为False，则从激活时起延迟后第一次执行）
    trackOutput: bool
        是否启用命令方块输出
    compability_version_number: int
        版本兼容代号

    Returns
    -------
    Block
        生成的方块对象
    """

    return Block(
        "minecraft",
        (
            "command_block"
            if impluse == 0
            else ("repeating_command_block" if impluse == 1 else "chain_command_block")
        ),
        states={"conditional_bit": condition, "facing_direction": particularValue},
        extra_data={
            "block_entity_data": {
                "Command": command,
                "CustomName": customName,
                "ExecuteOnFirstTick": executeOnFirstTick,
                "LPCommandMode": 0,
                "LPCondionalMode": False,
                "LPRedstoneMode": False,
                "LastExecution": TAG_Long(0),
                "LastOutput": "",
                "LastOutputParams": [],
                "SuccessCount": 0,
                "TickDelay": tickDelay,
                "TrackOutput": trackOutput,
                "Version": (
                    25 if compability_version_number <= COMPABILITY_VERSION_119 else 43
                ),
                "auto": alwaysRun,
                "conditionMet": False,  # 是否已经满足条件
                "conditionalMode": condition,
                "id": "CommandBlock",
                "isMovable": True,
                "powered": False,  # 是否已激活
                "x": coordinate[0],
                "y": coordinate[1],
                "z": coordinate[2],
            }  # type: ignore
        },
        compability_version=compability_version_number,
    )
