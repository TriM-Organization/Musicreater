'''
存放有关BDX结构操作的内容
'''


from .common import bottem_side_length_of_smallest_square_bottom_box
from ..constants import x,y,z


bdx_key = {
    "x": [b"\x0f", b"\x0e", b"\x1c", b"\x14", b"\x15"],
    "y": [b"\x11", b"\x10", b"\x1d", b"\x16", b"\x17"],
    "z": [b"\x13", b"\x12", b"\x1e", b"\x18", b"\x19"],
}
"""key存储了方块移动指令的数据，其中可以用key[x|y|z][0|1]来表示xyz的减或增
而key[][2+]是用来增加指定数目的"""


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


