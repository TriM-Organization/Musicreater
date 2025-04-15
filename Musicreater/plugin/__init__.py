# -*- coding: utf-8 -*-
"""
存放非音·创本体的附加功能件

版权所有 © 2024 金羿 & 诸葛亮与八卦阵
Copyright © 2025 Eilles & bgArray

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md


__all__ = [
    # 通用
    # "ConvertConfig",
    "bottem_side_length_of_smallest_square_bottom_box",
    # 打包
    "compress_zipfile",
    "behavior_mcpack_manifest",
    # MCSTRUCTURE 函数
    "antiaxis",
    "forward_IER",
    "command_statevalue",
    "form_note_block_in_NBT_struct",
    "form_repeater_in_NBT_struct",
    "form_command_block_in_NBT_struct",
    "commands_to_structure",
    "commands_to_redstone_delay_structure",
    # MCSTRUCTURE 常量
    "AXIS_PARTICULAR_VALUE",
    "COMPABILITY_VERSION_117",
    "COMPABILITY_VERSION_119",
    # BDX 函数
    "bdx_move",
    "form_command_block_in_BDX_bytes",
    "commands_to_BDX_bytes",
    # BDX 常量
    "BDX_MOVE_KEY",
]
__author__ = (("金羿", "Eilles"), ("诸葛亮与八卦阵", "bgArray"))

# from .main import ConvertConfig

from .archive import compress_zipfile, behavior_mcpack_manifest

from .bdx import (
    BDX_MOVE_KEY,
    bdx_move,
    form_command_block_in_BDX_bytes,
    commands_to_BDX_bytes,
)

from .common import bottem_side_length_of_smallest_square_bottom_box

from .mcstructure import (
    antiaxis,
    forward_IER,
    AXIS_PARTICULAR_VALUE,
    COMPABILITY_VERSION_119,
    COMPABILITY_VERSION_117,
    command_statevalue,
    form_note_block_in_NBT_struct,
    form_repeater_in_NBT_struct,
    form_command_block_in_NBT_struct,
    commands_to_structure,
    commands_to_redstone_delay_structure,
)
