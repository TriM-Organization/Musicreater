# -*- coding: utf-8 -*-
"""
MCSTRUCTURE 共享结构原语库 - 结构组装函数
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
from typing import List, Literal, Tuple

from TrimMCStruct import Block, Structure

from Musicreater.builtin_plugins.to_commands import MineCommand

from .constants import x, y, z, AXIS_PARTICULAR_VALUE, COMPABILITY_VERSION_119
from .blocks import form_command_block_in_NBT_struct, form_repeater_in_NBT_struct


def antiaxis(axis: Literal["x", "z", "X", "Z"]):
    """
    在 x-z 平面上，返回指定轴的另一个轴
    """

    return z if axis == x else x


def forward_IER(forward: bool):
    """
    把用逻辑值标记的方向值转为正负单位，用以乘上增量
    """
    return 1 if forward else -1


def command_statevalue(axis_: Literal["x", "y", "z", "X", "Y", "Z"], forward_: bool):
    return AXIS_PARTICULAR_VALUE[axis_.lower()][forward_]


def bottem_side_length_of_smallest_square_bottom_box(
    _total_block_count: int, _max_height: int
):
    """
    给定结构的总方块数量和规定的最大高度，返回该结构应当构成的图形在底面的外切正方形之边长

    Parameters
    ------------
    _total_block_count: int
        总方块数量
    _max_height: int
        规定的结构最大高度

    Returns
    ---------
    int
        外切正方形的边长
    """
    return math.ceil(math.sqrt(math.ceil(_total_block_count / _max_height)))


def commands_to_structure(
    commands: List[MineCommand],
    max_height: int = 64,
    compability_version_: int = COMPABILITY_VERSION_119,
):
    """
    由指令列表生成(纯指令方块)结构

    Parameters
    ------------
    commands: list
        指令列表
    max_height: int
        生成结构最大高度

    Returns
    ---------
    Structure, tuple[int, int, int], tuple[int, int, int]
        结构类, 结构占用大小, 终点坐标
    """

    _side_length = bottem_side_length_of_smallest_square_bottom_box(
        len(commands), max_height
    )

    struct = Structure(
        size=(_side_length, max_height, _side_length),  # 声明结构大小
        compability_version=compability_version_,
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
                command=command.command,
                coordinate=coordinate,
                particularValue=(
                    (1 if y_forward else 0)
                    if (
                        ((now_y != 0) and (not y_forward))
                        or (y_forward and (now_y != (max_height - 1)))
                    )
                    else (
                        (3 if z_forward else 2)
                        if (
                            ((now_z != 0) and (not z_forward))
                            or (z_forward and (now_z != _side_length - 1))
                        )
                        else 5
                    )
                ),
                impluse=2,
                condition=False,
                alwaysRun=True,
                tickDelay=command.delay,
                customName=command.annotation,
                executeOnFirstTick=False,
                trackOutput=True,
                compability_version_number=compability_version_,
            ),
        )

        now_y += 1 if y_forward else -1

        if ((now_y >= max_height) and y_forward) or ((now_y < 0) and (not y_forward)):
            now_y -= 1 if y_forward else -1

            y_forward = not y_forward

            now_z += 1 if z_forward else -1

            if ((now_z >= _side_length) and z_forward) or (
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
            _side_length if now_x else now_z,
        ),
        (now_x, now_y, now_z),
    )


def commands_to_redstone_delay_structure(
    commands: List[MineCommand],
    delay_length: int,
    max_multicmd_length: int,
    base_block: str = "concrete",
    axis_: Literal["z+", "z-", "Z+", "Z-", "x+", "x-", "X+", "X-"] = "z+",
    compability_version_: int = COMPABILITY_VERSION_119,
) -> Tuple[Structure, Tuple[int, int, int], Tuple[int, int, int]]:
    """
    由指令列表生成由红石中继器延迟的结构

    Parameters
    ------------
    commands: list
        指令列表
    delay_length: int
        延时总长
    max_multicmd_length: int
        最大同时播放的音符数量
    base_block: Block
        生成结构的基底方块
    axis_: str
        生成结构的延展方向

    Returns
    ---------
    Structure, tuple[int, int, int], tuple[int, int, int]
        结构类, 结构占用大小, 终点坐标
    """
    if axis_ in ["z+", "Z+"]:
        extensioon_direction = z
        aside_direction = x
        repeater_facing = 2
        forward = True
    elif axis_ in ["z-", "Z-"]:
        extensioon_direction = z
        aside_direction = x
        repeater_facing = 0
        forward = False
    elif axis_ in ["x+", "X+"]:
        extensioon_direction = x
        aside_direction = z
        repeater_facing = 3
        forward = True
    elif axis_ in ["x-", "X-"]:
        extensioon_direction = x
        aside_direction = z
        repeater_facing = 1
        forward = False
    else:
        raise ValueError(f"axis_({axis_}) 参数错误。")

    goahead = forward_IER(forward)

    command_actually_length = sum([int(bool(cmd.delay)) for cmd in commands])

    a = 1
    a_max = 0
    total_cmd = 0
    for cmd in commands:
        # print("\r 正在进行处理：",end="")
        if cmd.delay > 2:
            a_max = max(a, a_max)
            total_cmd += (a := 1)
        else:
            a += 1

    struct = Structure(
        size=(
            round(delay_length / 2 + total_cmd) if extensioon_direction == x else a_max,
            3,
            round(delay_length / 2 + total_cmd) if extensioon_direction == z else a_max,
        ),
        fill=Block("minecraft", "air", compability_version=compability_version_),
        compability_version=compability_version_,
    )

    pos_now = {
        x: ((1 if extensioon_direction == x else 0) if forward else struct.size[0]),
        y: 0,
        z: ((1 if extensioon_direction == z else 0) if forward else struct.size[2]),
    }

    chain_list = 0
    # print("结构元信息设定完毕")

    for cmd in commands:
        # print("\r 正在进行处理：",end="")
        if cmd.delay > 1:
            # print("\rdelay > 0",end='')
            single_repeater_value = int(cmd.delay / 2) % 4 - 1
            additional_repeater = int(cmd.delay / 2 // 4)
            for i in range(additional_repeater):
                struct.set_block(
                    tuple(pos_now.values()),  # type: ignore
                    Block(
                        "minecraft",
                        base_block,
                        compability_version=compability_version_,
                    ),
                )
                struct.set_block(
                    (pos_now[x], 1, pos_now[z]),
                    form_repeater_in_NBT_struct(
                        delay=3,
                        facing=repeater_facing,
                        compability_version_number=compability_version_,
                    ),
                )
                pos_now[extensioon_direction] += goahead
            if single_repeater_value >= 0:
                struct.set_block(
                    tuple(pos_now.values()),  # type: ignore
                    Block(
                        "minecraft",
                        base_block,
                        compability_version=compability_version_,
                    ),
                )
                struct.set_block(
                    (pos_now[x], 1, pos_now[z]),
                    form_repeater_in_NBT_struct(
                        delay=single_repeater_value,
                        facing=repeater_facing,
                        compability_version_number=compability_version_,
                    ),
                )
                pos_now[extensioon_direction] += goahead
            struct.set_block(
                (pos_now[x], 1, pos_now[z]),
                form_command_block_in_NBT_struct(
                    command=cmd.command,
                    coordinate=(pos_now[x], 1, pos_now[z]),
                    particularValue=command_statevalue(extensioon_direction, forward),
                    # impluse= (0 if first_impluse else 2),
                    impluse=0,
                    condition=False,
                    alwaysRun=False,
                    tickDelay=cmd.delay % 2,
                    customName=cmd.annotation,
                    compability_version_number=compability_version_,
                ),
            )
            struct.set_block(
                (pos_now[x], 2, pos_now[z]),
                Block(
                    "minecraft",
                    "redstone_wire",
                    compability_version=compability_version_,
                ),
            )
            pos_now[extensioon_direction] += goahead
            chain_list = 1

        else:
            # print(pos_now)
            now_pos_copy = pos_now.copy()
            now_pos_copy[extensioon_direction] -= goahead
            now_pos_copy[aside_direction] += chain_list
            # print(pos_now,"\n=========")
            struct.set_block(
                (now_pos_copy[x], 1, now_pos_copy[z]),
                form_command_block_in_NBT_struct(
                    command=cmd.command,
                    coordinate=(now_pos_copy[x], 1, now_pos_copy[z]),
                    particularValue=command_statevalue(extensioon_direction, forward),
                    # impluse= (0 if first_impluse else 2),
                    impluse=0,
                    condition=False,
                    alwaysRun=False,
                    tickDelay=cmd.delay % 2,
                    customName=cmd.annotation,
                    compability_version_number=compability_version_,
                ),
            )
            struct.set_block(
                (now_pos_copy[x], 2, now_pos_copy[z]),
                Block(
                    "minecraft",
                    "redstone_wire",
                    compability_version=compability_version_,
                ),
            )
            chain_list += 1

    return struct, struct.size, tuple(pos_now.values())  # type: ignore
