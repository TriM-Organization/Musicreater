# -*- coding: utf-8 -*-
"""
版权所有 © 2023 音·创 开发者
Copyright © 2023 all the developers of Musicreater

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿穆组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md

import os

from ...exceptions import CommandFormatError
from ...main import MidiConvert
from ..main import ConvertConfig
from ..mcstructure import commands_to_structure


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
    tuple[tuple[int,]结构大小, int音乐总延迟]
    """

    if midi_cvt.enable_old_exe_format:
        raise CommandFormatError("使用mcstructure结构文件导出时不支持旧版本的指令格式。")

    cmd_list, max_delay = midi_cvt.to_command_list_in_delay(
        data_cfg.volume_ratio,
        data_cfg.speed_multiplier,
        player,
    )

    if not os.path.exists(data_cfg.dist_path):
        os.makedirs(data_cfg.dist_path)

    struct, size, end_pos = commands_to_structure(cmd_list, max_height - 1)

    with open(
        os.path.abspath(
            os.path.join(data_cfg.dist_path, f"{midi_cvt.midi_music_name}.mcstructure")
        ),
        "wb+",
    ) as f:
        struct.dump(f)

    return size, max_delay


def to_mcstructure_file_in_redstone(
    midi_cvt: MidiConvert,
    data_cfg: ConvertConfig,):
    pass