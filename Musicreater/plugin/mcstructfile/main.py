# -*- coding: utf-8 -*-
"""
版权所有 © 2024 音·创 开发者
Copyright © 2024 all the developers of Musicreater

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md

import os
from typing import Literal

# from ...exceptions import CommandFormatError
from ...main import MidiConvert
from ..main import ConvertConfig
from ...subclass import SingleCommand
from ..mcstructure import (
    COMPABILITY_VERSION_117,
    COMPABILITY_VERSION_119,
    commands_to_redstone_delay_structure,
    commands_to_structure,
)


def to_mcstructure_file_in_delay(
    midi_cvt: MidiConvert,
    data_cfg: ConvertConfig,
    player: str = "@a",
    max_height: int = 64,
):
    """
    将midi以延迟播放器形式转换为mcstructure结构文件

    Parameters
    ----------
    midi_cvt: MidiConvert 对象
        用于转换的MidiConvert对象
    data_cfg: ConvertConfig 对象
        部分转换通用参数
    player: str
        玩家选择器，默认为`@a`
    max_height: int
        生成结构最大高度

    Returns
    -------
    tuple[tuple[int,int,int]结构大小, int音乐总延迟]
    """

    compability_ver = (
        COMPABILITY_VERSION_117
        if midi_cvt.enable_old_exe_format
        else COMPABILITY_VERSION_119
    )

    cmd_list, max_delay = midi_cvt.to_command_list_in_delay(
        data_cfg.volume_ratio,
        data_cfg.speed_multiplier,
        player,
    )[:2]

    if not os.path.exists(data_cfg.dist_path):
        os.makedirs(data_cfg.dist_path)

    struct, size, end_pos = commands_to_structure(
        cmd_list, max_height - 1, compability_version_=compability_ver
    )

    with open(
        os.path.abspath(
            os.path.join(data_cfg.dist_path, f"{midi_cvt.music_name}.mcstructure")
        ),
        "wb+",
    ) as f:
        struct.dump(f)

    return size, max_delay


def to_mcstructure_file_in_score(
    midi_cvt: MidiConvert,
    data_cfg: ConvertConfig,
    scoreboard_name: str = "mscplay",
    auto_reset: bool = False,
    max_height: int = 64,
):
    """
    将midi以延迟播放器形式转换为mcstructure结构文件

    Parameters
    ----------
    midi_cvt: MidiConvert 对象
        用于转换的MidiConvert对象
    data_cfg: ConvertConfig 对象
        部分转换通用参数
    scoreboard_name: str
        我的世界的计分板名称
    auto_reset: bool
        是否自动重置计分板
    max_height: int
        生成结构最大高度

    Returns
    -------
    tuple[tuple[int,int,int]结构大小, int音乐总延迟, int指令数量
    """

    compability_ver = (
        COMPABILITY_VERSION_117
        if midi_cvt.enable_old_exe_format
        else COMPABILITY_VERSION_119
    )

    cmd_list, cmd_count, max_delay = midi_cvt.to_command_list_in_score(
        scoreboard_name,
        data_cfg.volume_ratio,
        data_cfg.speed_multiplier,
    )

    if not os.path.exists(data_cfg.dist_path):
        os.makedirs(data_cfg.dist_path)

    struct, size, end_pos = commands_to_structure(
        midi_cvt.music_command_list+(
            [
                SingleCommand(
                    command="scoreboard players reset @a[scores={"
                    + scoreboard_name
                    + "="
                    + str(max_delay + 20)
                    + "}] "
                    + scoreboard_name,
                    annotation="自动重置计分板",
                )
            ]
            if auto_reset
            else []
        ), max_height - 1, compability_version_=compability_ver
    )

    with open(
        os.path.abspath(
            os.path.join(data_cfg.dist_path, f"{midi_cvt.music_name}.mcstructure")
        ),
        "wb+",
    ) as f:
        struct.dump(f)

    return size, max_delay, cmd_count


def to_mcstructure_file_in_repeater(
    midi_cvt: MidiConvert,
    data_cfg: ConvertConfig,
    player: str = "@a",
    axis_side: Literal["z+", "z-", "Z+", "Z-", "x+", "x-", "X+", "X-"] = "z+",
    basement_block: str = "concrete",
):
    """
    将midi以延迟播放器形式转换为mcstructure结构文件

    Parameters
    ----------
    midi_cvt: MidiConvert 对象
        用于转换的MidiConvert对象
    data_cfg: ConvertConfig 对象
        部分转换通用参数
    player: str
        玩家选择器，默认为`@a`
    axis_side: Literal["z+","z-","Z+","Z-","x+","x-","X+","X-"]
        生成结构的延展方向
    basement_block: str
        结构的基底方块

    Returns
    -------
    tuple[tuple[int,int,int]结构大小, int音乐总延迟]
    """

    compability_ver = (
        COMPABILITY_VERSION_117
        if midi_cvt.enable_old_exe_format
        else COMPABILITY_VERSION_119
    )

    cmd_list, max_delay, max_multiple_cmd = midi_cvt.to_command_list_in_delay(
        data_cfg.volume_ratio,
        data_cfg.speed_multiplier,
        player,
    )

    if not os.path.exists(data_cfg.dist_path):
        os.makedirs(data_cfg.dist_path)

    struct, size, end_pos = commands_to_redstone_delay_structure(
        cmd_list,
        max_delay,
        max_multiple_cmd,
        basement_block,
        axis_side,
        compability_version_=compability_ver,
    )

    with open(
        os.path.abspath(
            os.path.join(data_cfg.dist_path, f"{midi_cvt.music_name}.mcstructure")
        ),
        "wb+",
    ) as f:
        struct.dump(f)

    return size, max_delay
