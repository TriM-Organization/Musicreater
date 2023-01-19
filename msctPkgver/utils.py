import math
import os

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
        return b''
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

    return key[axis][pointer] + value.to_bytes(2 ** (pointer - 2), 'big', signed=True)


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
            arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            zipf.write(pathfile, arcname)
    zipf.close()


def formCMDblk(
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


def __fillSquareSideLength(total: int, maxHeight: int):
    """给定总方块数量和最大高度，返回所构成的图形外切正方形的边长
    :param total: 总方块数量
    :param maxHeight: 最大高度
    :return: 外切正方形的边长 int"""
    return math.ceil(math.sqrt(math.ceil(total / maxHeight)))


def toBDXbytes(
    commands: list,
    maxheight: int = 64,
):
    """
    :param commands: 指令列表(指令, 延迟)
    :param maxheight: 生成结构最大高度
    :return 成功与否，成功返回(True,未经过压缩的源,结构占用大小)，失败返回(False,str失败原因)
    """

    _sideLength = __fillSquareSideLength(len(commands), maxheight)
    _bytes = b''

    yforward = True
    zforward = True

    nowy = 0
    nowz = 0
    nowx = 0

    for cmd, delay in commands:
        _bytes += formCMDblk(
            cmd,
            (1 if yforward else 0)
            if (
                ((nowy != 0) and (not yforward))
                or ((yforward) and (nowy != (maxheight - 1)))
            )
            else (3 if zforward else 2)
            if (
                ((nowz != 0) and (not zforward))
                or ((zforward) and (nowz != _sideLength))
            )
            else 5,
            impluse=2,
            condition=False,
            needRedstone=False,
            tickDelay=delay,
            customName="",
            executeOnFirstTick=False,
            trackOutput=True,
        )

        nowy += 1 if yforward else -1

        if ((nowy >= maxheight) and (yforward)) or ((nowy < 0) and (not yforward)):
            nowy -= 1 if yforward else -1

            yforward = not yforward

            nowz += 1 if zforward else -1

            if ((nowz > _sideLength) and (zforward)) or ((nowz < 0) and (not zforward)):
                nowz -= 1 if zforward else -1
                zforward = not zforward
                _bytes += key[x][1]
                nowx += 1
            else:

                _bytes += key[z][int(zforward)]

        else:

            _bytes += key[y][int(yforward)]

    return (
        _bytes,
        [nowx + 1, maxheight if nowx or nowz else nowy, _sideLength if nowx else nowz],
        [nowx, nowy, nowz],
    )
