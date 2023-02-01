import math
import os
import brotli
from exceptions import *

key = {
    "x": [b"\x0f", b"\x0e", b"\x1c", b"\x14", b"\x15"],
    "y": [b"\x11", b"\x10", b"\x1d", b"\x16", b"\x17"],
    "z": [b"\x13", b"\x12", b"\x1e", b"\x18", b"\x19"],
}
"""key存储了方块移动指令的数据，其中可以用key[x|y|z][0|1]来表示xyz的减或增
而key[][2+]是用来增加指定数目的"""

x = "x"
y = "y"
z = "z"


def move(axis: str, value: int):
    if value == 0:
        return b""
    if abs(value) == 1:
        return key[axis][0 if value == -1 else 1]

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

    return key[axis][pointer] + value.to_bytes(2 ** (pointer - 2), "big", signed=True)


def makeZip(sourceDir, outFilename, compression=8, exceptFile=None):
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


def formCMD_blk(
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
        执行第一个已选项(循环指令方块是否激活后立即执行，若为False，则从激活时起延迟后第一次执行)
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


def __fillSquareSideLength(total: int, max_height: int):
    """给定总方块数量和最大高度，返回所构成的图形外切正方形的边长
    :param total: 总方块数量
    :param max_height: 最大高度
    :return: 外切正方形的边长 int"""
    return math.ceil(math.sqrt(math.ceil(total / max_height)))


axisParticularValue = {
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


def toLineBDX_bytes(
    commands: list,
    axis: str,
    forward: bool,
):
    _bytes = b""
    impluse = 2
    needRedstone = False
    customName = ""
    executeOnFirstTick = False
    trackOutput = True
    for cmd, condition in commands:
        _bytes += formCMD_blk(
            cmd,
            axisParticularValue[axis][forward],
            impluse=impluse,
            condition=condition,
            needRedstone=needRedstone,
            customName=customName,
            executeOnFirstTick=executeOnFirstTick,
            trackOutput=trackOutput,
        ) + move(axis, 1 if forward else -1)
    return _bytes


def toBDX_bytes(
    commands: list,
    max_height: int = 64,
):
    """
    :param commands: 指令列表(指令, 条件)
    :param max_height: 生成结构最大高度
    :return 成功与否，成功返回(True,未经过压缩的源,结构占用大小)，失败返回(False,str失败原因)
    """

    _sideLength = __fillSquareSideLength(len(commands), max_height)
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
        _bytes += formCMD_blk(
            cmd,
            (1 if y_forward else 0)
            if (
                ((now_y != 0) and (not y_forward))
                or (y_forward and (now_y != (max_height - 1)))
            )
            else (3 if z_forward else 2)
            if (
                ((now_z != 0) and (not z_forward))
                or (z_forward and (now_z != _sideLength))
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

            if ((now_z > _sideLength) and z_forward) or (
                (now_z < 0) and (not z_forward)
            ):
                now_z -= 1 if z_forward else -1
                z_forward = not z_forward
                _bytes += key[x][1]
                now_x += 1
            else:

                _bytes += key[z][int(z_forward)]

        else:

            _bytes += key[y][int(y_forward)]

    return (
        _bytes,
        [
            now_x + 1,
            max_height if now_x or now_z else now_y,
            _sideLength if now_x else now_z,
        ],
        [now_x, now_y, now_z],
    )


def toBDXfile(
    funcList: list,
    author: str = "Eilles",
    max_height: int = 64,
    outfile: str = "./test.bdx",
):
    """
    :param funcList: 指令集列表： 指令系统[  指令集[  单个指令( str指令, bool条件性 ),  ],  ]
    :param author: 作者名称
    :param max_height: 生成结构最大高度
    :param outfile: str 输出文件
    :return 成功与否，指令总长度，指令总延迟，指令结构总大小，画笔最终坐标
    """

    with open(os.path.abspath(outfile), "w+", encoding="utf-8") as f:
        f.write("BD@")

    _bytes = (
        b"BDX\x00" + author.encode("utf-8") + b" & Musicreater\x00\x01command_block\x00"
    )
    totalSize = {x: 0, y: 0, z: 0}
    totalLen = 0
    for func in funcList:
        totalLen += len(func)
        cmdBytes, size, finalPos = toBDX_bytes(func, max_height)
        _bytes += cmdBytes
        _bytes += move(x, 2)
        _bytes += move(y, -finalPos[1])
        _bytes += move(z, -finalPos[2])
        totalSize[x] += size[0] + 2
        totalSize[y] = max(totalSize[y], size[1])
        totalSize[z] = max(totalSize[z], size[2])

    with open(
        os.path.abspath(outfile),
        "ab+",
    ) as f:
        f.write(brotli.compress(_bytes + b"XE"))

    return True, totalLen, 0, list(totalSize.values()), finalPos


def toLineBDXfile(
    funcList: list,
    axis_: str,
    forward_: bool,
    author: str = "Eilles",
    outfile: str = "./test.bdx",
):
    """
    :param funcList: 指令集列表： 指令系统[  指令集[  单个指令( str指令, bool条件性 ),  ],  ]
    :param axis_:
    :param forward_:
    :param author: 作者名称
    :param outfile: str 输出文件
    :return 成功与否，指令总长度，指令总延迟，指令结构总大小，画笔最终坐标
    """

    with open(os.path.abspath(outfile), "w+", encoding="utf-8") as f:
        f.write("BD@")

    _bytes = (
        b"BDX\x00" + author.encode("utf-8") + b" & Musicreater\x00\x01command_block\x00"
    )
    totalSize = {x: 0, y: 0, z: 0}
    totalLen = 0
    for func in funcList:
        totalLen += len(func)
        _bytes += toLineBDX_bytes(func, axis_, forward_)
        _bytes += move(z if axis_ == x else x, 2)

        totalSize[z if axis_ == x else x] += 2
        totalSize[axis_] = max(totalSize[axis_], len(func))

    with open(
        os.path.abspath(outfile),
        "ab+",
    ) as f:
        f.write(brotli.compress(_bytes + b"XE"))

    return True, totalLen, 0, list(totalSize.values())


def format_ipt(notice: str, fun, err_note: str = "", *extraArg):
    """循环输入，以某种格式
    notice: 输入时的提示
    fun: 格式函数
    err_note: 输入不符格式时的提示
    *extraArg: 对于函数的其他参数"""
    while True:
        result = input(notice)
        try:
            fun_result = fun(result, *extraArg)
            break
        except ValueError:
            print(err_note)
            continue
    return result, fun_result
