# -*- coding: utf-8 -*-

"""
音·创 v3 内置的 指令生成插件
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


from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import BinaryIO, Optional, Dict, List, Callable, Tuple, Mapping

from Musicreater import SingleMusic, SingleTrack, SingleNote, SoundAtmos
from Musicreater.plugins import (
    library_plugin,
    PluginConfig,
    PluginMetaInformation,
    PluginTypes,
    LibraryPluginBase,
)
from Musicreater.exceptions import ZeroSpeedError, IllegalMinimumVolumeError
from Musicreater._utils import enumerated_stuffcopy_dictionary


@dataclass
class CommandConvertionConfig(PluginConfig): ...


@library_plugin("notedata_2_command_plugin")
class NoteDataConvert2CommandPlugin(LibraryPluginBase):
    metainfo = PluginMetaInformation(
        name="音符数据指令支持插件",
        author="金羿、玉衡Alioth",
        description="从音符数据转换为我的世界指令相关格式",
        version=(0, 0, 1),
        type=PluginTypes.LIBRARY,
        license="Same as Musicreater",
    )
