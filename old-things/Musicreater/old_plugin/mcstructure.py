# -*- coding: utf-8 -*-
"""
存放有关MCSTRUCTURE结构操作的内容
"""

"""
版权所有 © 2025 金羿 & 诸葛亮与八卦阵
Copyright © 2025 Eilles & bgArray

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md


from typing import List, Literal, Tuple

from TrimMCStruct import Block, Structure, TAG_Byte, TAG_Long

from ..constants import x, y, z
from ..subclass import MineCommand
from .common import bottem_side_length_of_smallest_square_bottom_box


def antiaxis(axis: Literal["x", "z", "X", "Z"]):
    return z if axis == x else x


def forward_IER(forward: bool):
    return 1 if forward else -1


AXIS_PARTICULAR_VALUE = {
    x: {
        True: 5,
        False: 4,
    },
    y: {
        True: 1,
        False: 0,
    },
    z: {
        True: 3,
        False: 2,
    },
}

# 1.19的结构兼容版本号
COMPABILITY_VERSION_119: int = 17959425
"""
Minecraft 1.19 兼容版本号
"""
# 1.17的结构兼容版本号
COMPABILITY_VERSION_117: int = 17879555
"""
Minecraft 1.17 兼容版本号
"""
COMPABILITY_VERSION_121: int = 18168865
"""
Minecraft 1.21 兼容版本号
"""


def command_statevalue(axis_: Literal["x", "y", "z", "X", "Y", "Z"], forward_: bool):
    return AXIS_PARTICULAR_VALUE[axis_.lower()][forward_]


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

    _sideLength = bottem_side_length_of_smallest_square_bottom_box(
        len(commands), max_height
    )

    struct = Structure(
        size=(_sideLength, max_height, _sideLength),  # 声明结构大小
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
                command=command.command_text,
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
                            or (z_forward and (now_z != _sideLength - 1))
                        )
                        else 5
                    )
                ),
                impluse=2,
                condition=False,
                alwaysRun=True,
                tickDelay=command.delay,
                customName=command.annotation_text,
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
                    command=cmd.command_text,
                    coordinate=(pos_now[x], 1, pos_now[z]),
                    particularValue=command_statevalue(extensioon_direction, forward),
                    # impluse= (0 if first_impluse else 2),
                    impluse=0,
                    condition=False,
                    alwaysRun=False,
                    tickDelay=cmd.delay % 2,
                    customName=cmd.annotation_text,
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
                    command=cmd.command_text,
                    coordinate=(now_pos_copy[x], 1, now_pos_copy[z]),
                    particularValue=command_statevalue(extensioon_direction, forward),
                    # impluse= (0 if first_impluse else 2),
                    impluse=0,
                    condition=False,
                    alwaysRun=False,
                    tickDelay=cmd.delay % 2,
                    customName=cmd.annotation_text,
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
