# -*- coding: utf-8 -*-
"""
存放有关MCSTRUCTURE结构操作的内容
"""

"""
版权所有 © 2023 音·创 开发者
Copyright © 2023 all the developers of Musicreater

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿穆组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md


from typing import List

from TrimMCStruct import Block, Structure, TAG_Byte, TAG_Long

from ..subclass import SingleCommand
from .common import bottem_side_length_of_smallest_square_bottom_box


def form_note_block_in_NBT_struct(
    note: int, coordinate: tuple, instrument: str = "note.harp", powered: bool = False
):
    """生成音符盒方块
    :param note: `int`(0~24)
        音符的音高
    :param coordinate: `tuple[int,int,int]`
        此方块所在之相对坐标
    :param instrument: `str`
        音符盒的乐器
    :param powered: `bool`
        是否已被激活
    :return Block
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
            }
        },
    )


def form_repeater_in_NBT_struct(delay: int, facing: int):
    """生成中继器方块
    :param facing:
    :param delay: 1~4
    :return Block()"""

    return Block(
        "minecraft",
        "unpowered_repeater",
        {
            "repeater_delay": delay,
            "direction": facing,
        },
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
):
    """
    使用指定项目返回指定的指令方块结构
    :param command: `str`
        指令
    :param coordinate: `tuple[int,int,int]`
        此方块所在之相对坐标
    :param particularValue:
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
    :param impluse: `int 0|1|2`
        方块类型
            0脉冲 1循环 2连锁
    :param condition: `bool`
        是否有条件
    :param alwaysRun: `bool`
        是否始终执行
    :param tickDelay: `int`
        执行延时
    :param customName: `str`
        悬浮字
    :param executeOnFirstTick: `bool`
        首刻执行(循环指令方块是否激活后立即执行，若为False，则从激活时起延迟后第一次执行)
    :param trackOutput: `bool`
        是否输出

    :return:str
    """

    return Block(
        "minecraft",
        "command_block"
        if impluse == 0
        else ("repeating_command_block" if impluse == 1 else "chain_command_block"),
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
                "Version": 25,
                "auto": alwaysRun,
                "conditionMet": False,  # 是否已经满足条件
                "conditionalMode": condition,
                "id": "CommandBlock",
                "isMovable": True,
                "powered": False,  # 是否已激活
                "x": coordinate[0],
                "y": coordinate[1],
                "z": coordinate[2],
            }
        },
        compability_version=17959425,
    )


def commands_to_structure(
    commands: List[SingleCommand],
    max_height: int = 64,
):
    """
    :param commands: 指令列表
    :param max_height: 生成结构最大高度
    :return 结构类,结构占用大小,终点坐标
    """

    _sideLength = bottem_side_length_of_smallest_square_bottom_box(
        len(commands), max_height
    )

    struct = Structure(
        (_sideLength, max_height, _sideLength),  # 声明结构大小
    )

    y_forward = True
    z_forward = True

    now_y = 0
    now_z = 0
    now_x = 0

    for command in commands:
        coordinate = (now_x, now_y, now_z)
        struct.set_block(
            coordinate,
            form_command_block_in_NBT_struct(
                command=command.command_text,
                coordinate=coordinate,
                particularValue=(1 if y_forward else 0)
                if (
                    ((now_y != 0) and (not y_forward))
                    or (y_forward and (now_y != (max_height - 1)))
                )
                else (
                    (3 if z_forward else 2)
                    if (
                        ((now_z != 0) and (not z_forward))
                        or (z_forward and (now_z != _sideLength - 1))
                    )
                    else 5
                ),
                impluse=2,
                condition=False,
                alwaysRun=True,
                tickDelay=command.delay,
                customName=command.annotation_text,
                executeOnFirstTick=False,
                trackOutput=True,
            ),
        )

        now_y += 1 if y_forward else -1

        if ((now_y >= max_height) and y_forward) or ((now_y < 0) and (not y_forward)):
            now_y -= 1 if y_forward else -1

            y_forward = not y_forward

            now_z += 1 if z_forward else -1

            if ((now_z >= _sideLength) and z_forward) or (
                (now_z < 0) and (not z_forward)
            ):
                now_z -= 1 if z_forward else -1
                z_forward = not z_forward
                now_x += 1

    return (
        struct,
        (
            now_x + 1,
            max_height if now_x or now_z else now_y,
            _sideLength if now_x else now_z,
        ),
        (now_x, now_y, now_z),
    )
