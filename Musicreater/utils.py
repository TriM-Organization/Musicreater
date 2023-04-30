import math
import os

bdx_key = {
    "x": [b"\x0f", b"\x0e", b"\x1c", b"\x14", b"\x15"],
    "y": [b"\x11", b"\x10", b"\x1d", b"\x16", b"\x17"],
    "z": [b"\x13", b"\x12", b"\x1e", b"\x18", b"\x19"],
}
"""key存储了方块移动指令的数据，其中可以用key[x|y|z][0|1]来表示xyz的减或增
而key[][2+]是用来增加指定数目的"""

x = "x"
y = "y"
z = "z"


def bdx_move(axis: str, value: int):
    if value == 0:
        return b""
    if abs(value) == 1:
        return bdx_key[axis][0 if value == -1 else 1]

    pointer = sum(
        [
            1 if i else 0
            for i in (
            value != -1,
            value < -1 or value > 1,
            value < -128 or value > 127,
            value < -32768 or value > 32767,
        )
        ]
    )

    return bdx_key[axis][pointer] + value.to_bytes(
        2 ** (pointer - 2), "big", signed=True
    )


def compress_zipfile(sourceDir, outFilename, compression=8, exceptFile=None):
    """使用compression指定的算法打包目录为zip文件\n
    默认算法为DEFLATED(8),可用算法如下：\n
    STORED = 0\n
    DEFLATED = 8\n
    BZIP2 = 12\n
    LZMA = 14\n
    """
    import zipfile

    zipf = zipfile.ZipFile(outFilename, "w", compression)
    pre_len = len(os.path.dirname(sourceDir))
    for parent, dirnames, filenames in os.walk(sourceDir):
        for filename in filenames:
            if filename == exceptFile:
                continue
            pathfile = os.path.join(parent, filename)
            arc_name = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            zipf.write(pathfile, arc_name)
    zipf.close()


def form_command_block_in_BDX_bytes(
        command: str,
        particularValue: int,
        impluse: int = 0,
        condition: bool = False,
        needRedstone: bool = True,
        tickDelay: int = 0,
        customName: str = "",
        executeOnFirstTick: bool = False,
        trackOutput: bool = True,
):
    """
    使用指定项目返回指定的指令方块放置指令项
    :param command: `str`
        指令
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
    :param needRedstone: `bool`
        是否需要红石
    :param tickDelay: `int`
        执行延时
    :param customName: `str`
        悬浮字
    lastOutput: `str`
        上次输出字符串，注意此处需要留空
    :param executeOnFirstTick: `bool`
        首刻执行(循环指令方块是否激活后立即执行，若为False，则从激活时起延迟后第一次执行)
    :param trackOutput: `bool`
        是否输出

    :return:str
    """
    block = b"\x24" + particularValue.to_bytes(2, byteorder="big", signed=False)

    for i in [
        impluse.to_bytes(4, byteorder="big", signed=False),
        bytes(command, encoding="utf-8") + b"\x00",
        bytes(customName, encoding="utf-8") + b"\x00",
        bytes("", encoding="utf-8") + b"\x00",
        tickDelay.to_bytes(4, byteorder="big", signed=True),
        executeOnFirstTick.to_bytes(1, byteorder="big"),
        trackOutput.to_bytes(1, byteorder="big"),
        condition.to_bytes(1, byteorder="big"),
        needRedstone.to_bytes(1, byteorder="big"),
    ]:
        block += i
    return block


def bottem_side_length_of_smallest_square_bottom_box(total: int, maxHeight: int):
    """给定总方块数量和最大高度，返回所构成的图形外切正方形的边长
    :param total: 总方块数量
    :param maxHeight: 最大高度
    :return: 外切正方形的边长 int"""
    return math.ceil(math.sqrt(math.ceil(total / maxHeight)))


def commands_to_BDX_bytes(
        commands: list,
        max_height: int = 64,
):
    """
    :param commands: 指令列表(指令, 延迟)
    :param max_height: 生成结构最大高度
    :return 成功与否，成功返回(True,未经过压缩的源,结构占用大小)，失败返回(False,str失败原因)
    """

    _sideLength = bottem_side_length_of_smallest_square_bottom_box(
        len(commands), max_height
    )
    _bytes = b""

    y_forward = True
    z_forward = True

    now_y = 0
    now_z = 0
    now_x = 0

    for cmd, delay in commands:
        impluse = 2
        condition = False
        needRedstone = False
        tickDelay = delay
        customName = ""
        executeOnFirstTick = False
        trackOutput = True
        _bytes += form_command_block_in_BDX_bytes(
            cmd,
            (1 if y_forward else 0)
            if (
                    ((now_y != 0) and (not y_forward))
                    or (y_forward and (now_y != (max_height - 1)))
            )
            else (3 if z_forward else 2)
            if (
                    ((now_z != 0) and (not z_forward))
                    or (z_forward and (now_z != _sideLength - 1))
            )
            else 5,
            impluse=impluse,
            condition=condition,
            needRedstone=needRedstone,
            tickDelay=tickDelay,
            customName=customName,
            executeOnFirstTick=executeOnFirstTick,
            trackOutput=trackOutput,
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
                _bytes += bdx_key[x][1]
                now_x += 1
            else:
                _bytes += bdx_key[z][int(z_forward)]

        else:
            _bytes += bdx_key[y][int(y_forward)]

    return (
        _bytes,
        [
            now_x + 1,
            max_height if now_x or now_z else now_y,
            _sideLength if now_x else now_z,
        ],
        [now_x, now_y, now_z],
    )


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

    from TrimMCStruct import Block, TAG_Byte
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


def form_repeater_in_NBT_struct(
        delay: int, facing: int
):
    """生成中继器方块
    :param facing:
    :param delay: 1~4
    :return Block()"""

    from TrimMCStruct import Block

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

    from TrimMCStruct import Block, TAG_Long

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
        commands: list,
        max_height: int = 64,
):
    """
    :param commands: 指令列表(指令, 延迟)
    :param max_height: 生成结构最大高度
    :return 成功与否，成功返回(结构类,结构占用大小)，失败返回(False,str失败原因)
    """

    from TrimMCStruct import Structure

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

    for cmd, delay in commands:
        coordinate = (now_x, now_y, now_z)
        struct.set_block(
            coordinate,
            form_command_block_in_NBT_struct(
                command=cmd,
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
                tickDelay=delay,
                customName="",
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
