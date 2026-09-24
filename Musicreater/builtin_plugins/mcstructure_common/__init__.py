# -*- coding: utf-8 -*-
"""
音·创 v3 内置的 MCSTRUCTURE 共享原语库插件
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


from Musicreater.plugins import (
    library_plugin,
    PluginMetaInformation,
    PluginTypes,
    LibraryPluginBase,
)

from .constants import (
    x,
    y,
    z,
    COMPABILITY_VERSION_117,
    COMPABILITY_VERSION_119,
    COMPABILITY_VERSION_121,
    AXIS_PARTICULAR_VALUE,
)
from .blocks import (
    form_command_block_in_NBT_struct,
    form_note_block_in_NBT_struct,
    form_repeater_in_NBT_struct,
)
from .structure import (
    antiaxis,
    forward_IER,
    command_statevalue,
    bottem_side_length_of_smallest_square_bottom_box,
    commands_to_structure,
    commands_to_redstone_delay_structure,
)
from .packaging import (
    compress_zipfile,
    behavior_mcpack_manifest,
)


@library_plugin("mcstructure_common_lib")
class McstructureCommonLibPlugin(LibraryPluginBase):
    metainfo = PluginMetaInformation(
        name="MCSTRUCTURE 共享结构原语库",
        author="金羿、玉衡Alioth",
        description="为结构生成类插件提供共享的方块生成、结构组装与打包辅助函数",
        version=(0, 0, 1),
        type=PluginTypes.LIBRARY,
        license="Same as Musicreater",
    )


__all__ = [
    "x",
    "y",
    "z",
    "COMPABILITY_VERSION_117",
    "COMPABILITY_VERSION_119",
    "COMPABILITY_VERSION_121",
    "AXIS_PARTICULAR_VALUE",
    "form_command_block_in_NBT_struct",
    "form_note_block_in_NBT_struct",
    "form_repeater_in_NBT_struct",
    "antiaxis",
    "forward_IER",
    "command_statevalue",
    "bottem_side_length_of_smallest_square_bottom_box",
    "commands_to_structure",
    "commands_to_redstone_delay_structure",
    "compress_zipfile",
    "behavior_mcpack_manifest",
]
