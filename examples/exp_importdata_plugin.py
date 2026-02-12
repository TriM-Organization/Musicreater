# -*- coding: utf-8 -*-

"""
示例插件：导入音符数据
"""

"""
版权所有 © 2026 金羿
Copyright © 2026 Eilles
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com

"""
本示例模块开放授权，本文件已开放至公共领域。
请注意：
若是对本文件的直接转载（在形式上没有修改、增删、添加注释，或单纯修改排版、翻译、录屏、截图）
则该使用者需要在转载所及之处，明确在转载的内容开头标注本文之原始著作权人
在当前文件下，该原始著作权人为金羿(Eilles)
如果是对本文进行了一定程度上的修改和补充、或者以不同方式演绎本文件（如制成视频教程等）
则无需标注原作者，允许该使用者自行署名

本声明仅限于包含此声明的本文件，本声明与项目内其他文件无关。
"""

from typing import BinaryIO, Optional
from pathlib import Path
from dataclasses import dataclass

from Musicreater import SingleMusic, SingleTrack
from Musicreater.plugins import (
    PluginConfig,
    PluginMetaInformation,
    PluginTypes,
    music_input_plugin,
    MusicInputPluginBase,
    track_input_plugin,
    TrackInputPluginBase,
)


@dataclass
class ExampleImportConfig(PluginConfig):
    example_config_item3: bool
    example_config_item1: str = "example_config_item"
    example_config_item2: int = 0


@music_input_plugin("something_convert_to_music")
class ExampleImportMusicPlugin(MusicInputPluginBase):
    metainfo = PluginMetaInformation(
        name="示例导入插件·甲",
        author="金羿",
        description="这是一个示例导入插件，演示导入到全曲的插件编写过程",
        version=(0, 0, 1),
        type=PluginTypes.FUNCTION_MUSIC_IMPORT,
        license="The Unlicense",
        dependencies=("something_convertion_library"),
    )

    supported_formats = ("EXP", "EXAMPLE_FORMAT")

    def loadbytes(
        self, bytes_buffer_in: BinaryIO, config: Optional[ExampleImportConfig]
    ) -> "SingleMusic":
        return SingleMusic()

    # 插件可选地定义 load 方法，从文件导入数据。下面展示的是不定义 load 方法时候的实现方式
    def load(
        self, file_path: Path, config: Optional[ExampleImportConfig]
    ) -> "SingleMusic":
        with file_path.open("rb") as f:
            return self.loadbytes(f, config)


@track_input_plugin("something_convert_to_track")
class ExampleImportTrackPlugin(TrackInputPluginBase):
    metainfo = PluginMetaInformation(
        name="示例导入插件·乙",
        author="金羿",
        description="这是一个示例导入插件，演示导入到音轨的插件编写过程",
        version=(0, 0, 1),
        type=PluginTypes.FUNCTION_TRACK_IMPORT,
        license="The Unlicense",
        # 可以缺省依赖，如果不需要的话
    )

    supported_formats = ("EXP", "example_format")

    def loadbytes(
        self, bytes_buffer_in: BinaryIO, config: Optional[ExampleImportConfig]
    ) -> "SingleTrack":
        return SingleTrack()
    
    # 可以缺省 load 方法，会直接用上面展示过的方法读取数据
