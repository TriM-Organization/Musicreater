# -*- coding: utf-8 -*-

"""
音·创 v3 内置的 红石-混合指令音乐链 生成插件
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
from io import BytesIO
from pathlib import Path
from typing import BinaryIO, Optional, Iterator, Tuple

from Musicreater import SingleMusic
from Musicreater.plugins import (
    PluginConfig,
    PluginMetaInformation,
    PluginTypes,
    music_output_plugin,
    MusicOutputPluginBase,
)

from .redstone_chain import RedstoneBlockSpec, notes_to_redstone_specs
from Musicreater.builtin_plugins.mcstructure_common.constants import (
    COMPABILITY_VERSION_117,
    COMPABILITY_VERSION_119,
)


@dataclass
class RedstoneMixedExportConfig(PluginConfig):
    """
    导出 红石-混合指令音乐链 插件的配置类
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

    max_segment_length: int = 48
    """
    沿链轴方向切分结构的阈值长度
    """

    axis_: str = "z+"
    """
    红石链的传播方向
    """

    base_block: str = "concrete"
    """
    结构基础方块类型
    """

    enable_old_execute_format: bool = False
    """
    是否使用旧版指令格式
    """

    scoreboard_name: str = "mscply"
    """
    玩家位置计时器所用记分板名称
    """

    @property
    def execute_command_head(self) -> str:
        return (
            "execute {} ~ ~ ~ "
            if self.enable_old_execute_format
            else "execute as {} at @s positioned ~ ~ ~ run "
        )


@music_output_plugin("music_to_redstone_mixed_structure_plugin")
class MusicExportToRedstoneMixedStructurePlugin(MusicOutputPluginBase):

    metainfo = PluginMetaInformation(
        name="导出全曲至红石-混合指令音乐链（mcpack）",
        author="金羿、玉衡Alioth",
        description="将整首音乐以红石中继器为时序骨架、音符盒与指令方块混合的方式，导出为可一键导入的 mcpack 行为包",
        version=(0, 0, 1),
        type=PluginTypes.FUNCTION_MUSIC_EXPORT,
        license="Same as Musicreater",
        dependencies=("mcstructure_common_lib", "notedata_to_command_plugin"),
    )

    supported_formats = ("MCPACK",)

    def _build(self, data: SingleMusic, config: RedstoneMixedExportConfig):
        """
        执行完整的 转换→分段→加载器→打包 流水线，返回 mcpack 字节内容。

        流程：
          1. notes_to_redstone_specs ：音符 → 红石链规格
          2. split_redstone_chain    ：规格 → 红石链结构并按 max_segment_length 切分
          3. build_loader_structure  ：分段 → 加载器指令方块列
          4. assemble_mcpack         ：装载 manifest / structures / functions 并打包
        """
        from .segment import split_redstone_chain
        from .loader import build_loader_structure
        from .pack import assemble_mcpack

        specs = notes_to_redstone_specs(
            data,
            music_deviation=config.music_deviation,
            minimum_volume=config.minimum_volume,
            player_selector=config.player_selector,
            execute_command_head=config.execute_command_head,
        )
        compability = (
            COMPABILITY_VERSION_117
            if config.enable_old_execute_format
            else COMPABILITY_VERSION_119
        )
        segments, _full, _full_size = split_redstone_chain(
            specs,
            max_segment_length=config.max_segment_length,
            axis_=config.axis_,
            base_block=config.base_block,
            compability_version_=compability,
        )
        loader_struct, _loader_size = build_loader_structure(
            segments,
            player_selector=config.player_selector,
            axis_=config.axis_,
            marker_name="mscply_origin",
            scoreboard_name=config.scoreboard_name,
            compability_version_=compability,
        )
        return assemble_mcpack(data, segments, loader_struct, config)

    def dump(
        self,
        data: SingleMusic,
        file_path: Path,
        config: RedstoneMixedExportConfig,
    ):
        mcpack_bytes = self._build(data, config)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("wb") as f:
            f.write(mcpack_bytes)

    def stream_dump(
        self,
        data: SingleMusic,
        config: RedstoneMixedExportConfig,
    ) -> Iterator[bytes]:
        mcpack_bytes = self._build(data, config)
        yield from BytesIO(mcpack_bytes)
