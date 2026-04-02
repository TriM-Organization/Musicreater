# -*- coding: utf-8 -*-

"""
音·创 v3 内置的乐曲查看器
"""

"""
版权所有 © 2026 金羿
Copyright © 2026 Eilles

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md

from io import BytesIO
from typing import BinaryIO, Optional, Iterator, Generator, Any, Tuple
from pathlib import Path
from dataclasses import dataclass

from TrimMCStruct import Structure

from Musicreater import SingleMusic, SingleTrack
from Musicreater.plugins import (
    PluginConfig,
    PluginMetaInformation,
    PluginTypes,
    MusicOperatePluginBase,
    music_operate_plugin,
)


@dataclass
class TerminalSeekerConfig(PluginConfig):
    """
    终端查看器配置
    """



@music_operate_plugin("music_terminal_seeker")
class TerminalSeekerPlugin(MusicOperatePluginBase):

    metainfo = PluginMetaInformation(
        name="基于终端的音乐查看器",
        author="金羿",
        description="将乐曲信息输出到终端",
        version=(0,0,1),
        type=PluginTypes.FUNCTION_MUSIC_OPERATE,
        license="Same as Musiccreater",
        dependencies=(),
    )

    def process(
        self, data: "SingleMusic", config: TerminalSeekerConfig
    ) -> "SingleMusic":
        ...

