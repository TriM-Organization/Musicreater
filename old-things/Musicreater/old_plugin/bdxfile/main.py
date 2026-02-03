# -*- coding: utf-8 -*-
"""
版权所有 © 2025 金羿 & 诸葛亮与八卦阵
Copyright © 2025 Eilles & bgArray

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md


import os
from typing import Optional

import brotli

from ...old_main import MidiConvert
from ...subclass import MineCommand, ProgressBarStyle
from ..bdx import (
    bdx_move,
    commands_to_BDX_bytes,
    form_command_block_in_BDX_bytes,
    x,
    y,
    z,
)


def to_BDX_file_in_score(
    midi_cvt: MidiConvert,
    dist_path: str,
    progressbar_style: Optional[ProgressBarStyle],
    scoreboard_name: str = "mscplay",
    auto_reset: bool = False,
    author: str = "Eilles",
    max_height: int = 64,
):
    """
    将midi以计分播放器形式转换为BDX结构文件

    Parameters
    ----------
    midi_cvt: MidiConvert 对象
        用于转换的MidiConvert对象
    dist_path: str
        转换结果输出的目标路径
    progressbar_style: ProgressBarStyle 对象
        进度条对象
    scoreboard_name: str
        我的世界的计分板名称
    auto_reset: bool
        是否自动重置计分板
    author: str
        作者名称
    max_height: int
        生成结构最大高度

    Returns
    -------
    tuple[int指令数量, int音乐总延迟, tuple[int,]结构大小, tuple[int,]终点坐标]
    """

    cmdlist, command_count, max_score = midi_cvt.to_command_list_in_score(
        scoreboard_name=scoreboard_name,
    )

    if not os.path.exists(dist_path):
        os.makedirs(dist_path)

    with open(
        os.path.abspath(os.path.join(dist_path, f"{midi_cvt.music_name}[score].bdx")),
        "w+",
    ) as f:
        f.write("BD@")

    _bytes = (
        b"BDX\x00" + author.encode("utf-8") + b" & Musicreater\x00\x01command_block\x00"
    )

    cmdBytes, size, finalPos = commands_to_BDX_bytes(
        midi_cvt.music_command_list
        + (
            [
                MineCommand(
                    command="scoreboard players reset @a[scores={"
                    + scoreboard_name
                    + "="
                    + str(max_score + 20)
                    + "}] "
                    + scoreboard_name,
                    annotation="自动重置计分板",
                )
            ]
            if auto_reset
            else []
        ),
        max_height - 1,
    )

    if progressbar_style:
        pgbBytes, pgbSize, pgbNowPos = commands_to_BDX_bytes(
            midi_cvt.form_progress_bar(max_score, scoreboard_name, progressbar_style),
            max_height - 1,
        )
        _bytes += pgbBytes
        _bytes += bdx_move(y, -pgbNowPos[1])
        _bytes += bdx_move(z, -pgbNowPos[2])
        _bytes += bdx_move(x, 2)

        size[0] += 2 + pgbSize[0]
        size[1] = max(size[1], pgbSize[1])
        size[2] = max(size[2], pgbSize[2])

    _bytes += cmdBytes

    with open(
        os.path.abspath(os.path.join(dist_path, f"{midi_cvt.music_name}[score].bdx")),
        "ab+",
    ) as f:
        f.write(brotli.compress(_bytes + b"XE"))

    return command_count, max_score, size, finalPos


def to_BDX_file_in_delay(
    midi_cvt: MidiConvert,
    dist_path: str,
    progressbar_style: Optional[ProgressBarStyle],
    player: str = "@a",
    author: str = "Eilles",
    max_height: int = 64,
):
    """
    使用method指定的转换算法，将midi转换为BDX结构文件

    Parameters
    ----------
    midi_cvt: MidiConvert 对象
        用于转换的MidiConvert对象
    dist_path: str
        转换结果输出的目标路径
    progressbar_style: ProgressBarStyle 对象
        进度条对象
    player: str
        玩家选择器，默认为`@a`
    author: str
        作者名称
    max_height: int
        生成结构最大高度

    Returns
    -------
    tuple[int指令数量, int音乐总延迟, tuple[int,]结构大小, tuple[int,]终点坐标]
    """

    cmdlist, max_delay = midi_cvt.to_command_list_in_delay(
        player_selector=player,
    )[:2]

    if not os.path.exists(dist_path):
        os.makedirs(dist_path)

    with open(
        os.path.abspath(os.path.join(dist_path, f"{midi_cvt.music_name}[delay].bdx")),
        "w+",
    ) as f:
        f.write("BD@")

    _bytes = (
        b"BDX\x00" + author.encode("utf-8") + b" & Musicreater\x00\x01command_block\x00"
    )

    cmdBytes, size, finalPos = commands_to_BDX_bytes(cmdlist, max_height - 1)

    if progressbar_style:
        scb_name = midi_cvt.music_name[:3] + "Pgb"
        _bytes += form_command_block_in_BDX_bytes(
            r"scoreboard objectives add {} dummy {}计".replace(r"{}", scb_name),
            1,
            customName="初始化进度条",
        )
        _bytes += bdx_move(z, 2)
        _bytes += form_command_block_in_BDX_bytes(
            r"scoreboard players add {} {} 1".format(player, scb_name),
            1,
            1,
            customName="显示进度条并加分",
        )
        _bytes += bdx_move(y, 1)
        pgbBytes, pgbSize, pgbNowPos = commands_to_BDX_bytes(
            midi_cvt.form_progress_bar(max_delay, scb_name, progressbar_style),
            max_height - 1,
        )
        _bytes += pgbBytes
        _bytes += bdx_move(y, -1 - pgbNowPos[1])
        _bytes += bdx_move(z, -2 - pgbNowPos[2])
        _bytes += bdx_move(x, 2)
        _bytes += form_command_block_in_BDX_bytes(
            r"scoreboard players reset {} {}".format(player, scb_name),
            1,
            customName="置零进度条",
        )
        _bytes += bdx_move(y, 1)
        size[0] += 2 + pgbSize[0]
        size[1] = max(size[1], pgbSize[1])
        size[2] = max(size[2], pgbSize[2])

    size[1] += 1
    _bytes += cmdBytes

    with open(
        os.path.abspath(os.path.join(dist_path, f"{midi_cvt.music_name}[delay].bdx")),
        "ab+",
    ) as f:
        f.write(brotli.compress(_bytes + b"XE"))

    return len(cmdlist), max_delay, size, finalPos
