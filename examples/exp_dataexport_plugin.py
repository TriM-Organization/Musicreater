# -*- coding: utf-8 -*-

"""
示例插件：导出成其他文件
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

from typing import BinaryIO, Optional, Iterator, Generator, Any, Tuple
from pathlib import Path
from dataclasses import dataclass

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


@dataclass
class ExampleExportConfig(PluginConfig):
    example_config_item3: bool
    example_config_item1: str = "example_config_item"
    example_config_item2: int = 0

    def __iter__(self) -> Generator[Tuple[str, Any], None, None]:
        for k, v in self.to_dict().items():
            yield k, v


@music_output_plugin("convert_music_to_something")
class ExampleExportMusicPlugin(MusicOutputPluginBase):
    metainfo = PluginMetaInformation(
        name="示例导出插件·甲",
        author="金羿",
        description="这是一个示例导出插件，演示整首曲目导出到其他文件格式的插件的编写过程",
        version=(0, 0, 1),
        type=PluginTypes.FUNCTION_MUSIC_EXPORT,
        license="The Unlicense",
        dependencies=("something_convertion_library"),
    )

    supported_formats = ("EXP", "EXAMPLE_FORMAT")

    @staticmethod
    def something_data_convert(*args) -> bytes:
        return b"This is something wonderful"

    def stream_dump(
        self, data: SingleMusic, config: ExampleExportConfig | None
    ) -> Iterator[bytes]:
        if not config:
            config = ExampleExportConfig(True)
        for cfg in config:
            yield self.something_data_convert(cfg)

    # 插件可选地定义 dump 方法，从文件导入数据。下面展示的是不定义 load 方法时候的实现方式
    def dump(
        self, data: SingleMusic, file_path: Path, config: ExampleExportConfig | None
    ):

        with file_path.open("wb") as f:
            for _bytes in self.stream_dump(data, config):
                f.write(_bytes)


@track_output_plugin("convert_track_to_something")
class ExampleImportTrackPlugin(TrackOutputPluginBase):
    metainfo = PluginMetaInformation(
        name="示例导出插件·乙",
        author="金羿",
        description="这是一个示例导出插件，演示从音轨导出的其他格式的插件的编写过程",
        version=(0, 0, 1),
        type=PluginTypes.FUNCTION_TRACK_EXPORT,
        license="The Unlicense",
        # 可以缺省依赖，如果不需要的话
    )

    supported_formats = ("EXP", "example_format")

    def stream_dump(
        self, data: SingleTrack, config: ExampleExportConfig | None
    ) -> Iterator[bytes]:
        if not config:
            config = ExampleExportConfig(True)
        for cfg in config:
            yield ExampleExportMusicPlugin.something_data_convert(cfg)

    # 可以缺省 dump 方法，会直接用上面展示过的方法输出
