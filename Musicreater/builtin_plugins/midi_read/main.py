# -*- coding: utf-8 -*-

"""
音·创 v3 内置的 Midi 读取插件
"""

"""
版权所有 © 2026 金羿、玉衡Alioth、偷吃不是Touch
Copyright © 2026 Eilles, YuhengAlioth, Touch

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md

import mido

from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Optional, Dict, List

from Musicreater import SingleMusic
from Musicreater.plugins import (
    music_input_plugin,
    PluginConfig,
    PluginMetaInformation,
    PluginTypes,
    MusicInputPluginBase,
)
from Musicreater.types import (
    FittingFunctionType,
)


from .constants import (
    MIDI_DEFAULT_PROGRAM_VALUE,
    MIDI_DEFAULT_VOLUME_VALUE,
    MM_TOUCH_PERCUSSION_INSTRUMENT_TABLE,
    MM_TOUCH_PITCHED_INSTRUMENT_TABLE,
)
from .utils import velocity_2_distance_natural, panning_2_rotation_trigonometric


@dataclass
class MidiImportConfig(PluginConfig):
    """Midi 音乐数据导入插件配置"""

    ignore_mismatch_error: bool = True
    speed: float = 1.0
    default_program_value: int = MIDI_DEFAULT_PROGRAM_VALUE
    default_volume_value: int = MIDI_DEFAULT_VOLUME_VALUE
    default_tempo_value: int = mido.midifiles.midifiles.DEFAULT_TEMPO
    pitched_note_rtable: Dict[int, str] = MM_TOUCH_PITCHED_INSTRUMENT_TABLE
    percussion_note_rtable: Dict[int, str] = MM_TOUCH_PERCUSSION_INSTRUMENT_TABLE
    vol_processing_function: FittingFunctionType = velocity_2_distance_natural
    pan_processing_function: FittingFunctionType = panning_2_rotation_trigonometric
    note_rtable_replacement: Dict[str, str] = {}


@music_input_plugin("midi_2_music_by_tracks")
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
        self, bytes_buffer_in: BinaryIO, config: MidiImportConfig = MidiImportConfig()
    ) -> SingleMusic:
        midi_file = mido.MidiFile(file=bytes_buffer_in)
        return SingleMusic()  # =========================== TODO: 等待制作

    def load(
        self, file_path: Path, config: MidiImportConfig = MidiImportConfig()
    ) -> "SingleMusic":
        """从 Midi 文件导入音乐数据"""
        midi_file = mido.MidiFile(filename=file_path)
        return SingleMusic()  # =========================== TODO: 等待制作
