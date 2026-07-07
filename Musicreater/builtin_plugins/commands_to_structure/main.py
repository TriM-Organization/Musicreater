# -*- coding: utf-8 -*-

"""
音·创 v3 内置的 Minecraft 结构生成插件
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
    music_output_plugin,
    MusicOutputPluginBase,
    track_output_plugin,
    TrackOutputPluginBase,
)

from Musicreater.builtin_plugins.to_commands import (
    MineCommand,
    NoteDataConvert2CommandPlugin,
)

from .mcstructure import (
    COMPABILITY_VERSION_117,
    COMPABILITY_VERSION_119,
    commands_to_structure,
    commands_to_redstone_delay_structure,
)


@dataclass
class McstructureExportConfig(PluginConfig):
    """
    导出 MCSTRUCTURE 结构插件的配置类
    """

    music_deviation: float = 0
    """
    全曲音调偏移调整，单位为 Midi Pitch
    """
    minimum_volume: float = 0.01
    """
    指令参数：最小音量
    """
    player_selector: str = "@a"
    """
    玩家选择器
    """
    max_height: int = 64
    """
    生成结构的最大高度
    """
    enable_old_execute_format: bool = False
    """
    是否使用旧版指令格式
    """

    @property
    def execute_command_head(self) -> str:
        return (
            "execute {} ~ ~ ~ "
            if self.enable_old_execute_format
            else "execute as {} at @s positioned ~ ~ ~ run "
        )


@music_output_plugin("music_to_mcstructure_in_delay_plugin")
class MusicExportToMcstructureWithDelayPlayerPlugin(MusicOutputPluginBase):

    metainfo = PluginMetaInformation(
        name="导出全曲至结构（mcstructure结构、延迟播放器）",
        author="金羿、玉衡Alioth",
        description="将音·创 v3 的整首音乐数据，以指令方块延迟的播放形式，导出为基岩版 MCSTRUCTURE 结构",
        version=(0, 0, 1),
        type=PluginTypes.FUNCTION_MUSIC_EXPORT,
        license="Same as Musicreater",
        dependencies=("notedata_to_command_plugin",),
    )

    supported_formats = ("MCSTRUCTURE",)

    @staticmethod
    def _go_convertion(
        data: SingleMusic, config: McstructureExportConfig
    ) -> Tuple[Structure, Tuple[int, int, int], int]:

        command_list, max_delay = (
            NoteDataConvert2CommandPlugin.to_command_list_in_delay(
                music=data,
                music_deviation=config.music_deviation,
                minimum_volume=config.minimum_volume,
                player_selector=config.player_selector,
                execute_command_head=config.execute_command_head,
            )[:2]
        )

        struct, size, end_pos = commands_to_structure(
            command_list,
            config.max_height - 1,
            compability_version_=(
                COMPABILITY_VERSION_117
                if config.enable_old_execute_format
                else COMPABILITY_VERSION_119
            ),
        )

        return struct, size, max_delay

    def dump(self, data: SingleMusic, file_path: Path, config: McstructureExportConfig):

        struct, size, max_delay = self._go_convertion(data, config)

        file_path.parent.mkdir(parents=True, exist_ok=True)

        with file_path.open("wb") as f:
            struct.dump(f)

        return size, max_delay

    def stream_dump(
        self, data: SingleMusic, config: McstructureExportConfig
    ) -> Iterator[bytes]:
        struct, size, max_delay = self._go_convertion(data, config)

        b_out = BytesIO()
        struct.dump(b_out)
        b_out.seek(0)

        yield from b_out
