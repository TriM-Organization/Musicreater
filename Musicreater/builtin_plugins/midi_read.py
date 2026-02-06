# -*- coding: utf-8 -*-

"""
音·创 v3 内置的 Midi 读取插件
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

import mido

from pathlib import Path

from typing import BinaryIO, Optional

from Musicreater import SingleMusic
from Musicreater.plugins import (
    music_input_plugin,
    PluginConfig,
    PluginMetaInformation,
    PluginTypes,
    MusicInputPluginBase,
)


@music_input_plugin("midi_2_music_plugin")
class MidiImport2MusicPlugin(MusicInputPluginBase):
    """Midi 音乐数据导入插件"""

    metainfo = PluginMetaInformation(
        name="Midi 导入插件",
        author="金羿、玉衡Alioth",
        description="从 Midi 文件导入音乐数据",
        version=(0, 0, 1),
        type=PluginTypes.FUNCTION_MUSIC_IMPORT,
        license="Same as Musicreater",
    )

    supported_formats = ("MID", "MIDI")

    def loadbytes(
        self, bytes_buffer_in: BinaryIO, config: PluginConfig | None
    ) -> SingleMusic:
        midi_file = mido.MidiFile(file=bytes_buffer_in)
        return SingleMusic()  # =========================== TODO: 等待制作

    def load(self, file_path: Path, config: Optional[PluginConfig]) -> "SingleMusic":
        """从 Midi 文件导入音乐数据"""
        midi_file = mido.MidiFile(filename=file_path)
        return SingleMusic()  # =========================== TODO: 等待制作
