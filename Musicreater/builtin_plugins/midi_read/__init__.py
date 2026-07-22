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


from .main import MidiImportConfig, MidiImport2MusicPlugin


from .constants import (
    MIDI_DEFAULT_PROGRAM_VALUE,
    MIDI_DEFAULT_VOLUME_VALUE,
    MM_CLASSIC_PITCHED_INSTRUMENT_TABLE,
    MM_CLASSIC_PERCUSSION_INSTRUMENT_TABLE,
    MM_DEFAULT_PITCHED_INSTRUMENT_TABLE,
    MM_DEFAULT_PERCUSSION_INSTRUMENT_TABLE,
    MM_DISLINK_PITCHED_INSTRUMENT_TABLE,
    MM_DISLINK_PERCUSSION_INSTRUMENT_TABLE,
    MM_NBS_PITCHED_INSTRUMENT_TABLE,
    MM_NBS_PERCUSSION_INSTRUMENT_TABLE,
)

from .utils import panning_2_rotation_linear, panning_2_rotation_trigonometric

__all__ = [
    # 插件参数和插件本体类
    "MidiImportConfig",
    "MidiImport2MusicPlugin",
    # 内置的拟合函数
    "panning_2_rotation_linear",
    "panning_2_rotation_trigonometric",
    # Midi 相关默认值
    "MIDI_DEFAULT_PROGRAM_VALUE",
    "MIDI_DEFAULT_VOLUME_VALUE",
    # Midi 与 游戏内容 的对照表
    "MM_CLASSIC_PITCHED_INSTRUMENT_TABLE",
    "MM_CLASSIC_PERCUSSION_INSTRUMENT_TABLE",
    "MM_DEFAULT_PITCHED_INSTRUMENT_TABLE",
    "MM_DEFAULT_PERCUSSION_INSTRUMENT_TABLE",
    "MM_DISLINK_PITCHED_INSTRUMENT_TABLE",
    "MM_DISLINK_PERCUSSION_INSTRUMENT_TABLE",
    "MM_NBS_PITCHED_INSTRUMENT_TABLE",
    "MM_NBS_PERCUSSION_INSTRUMENT_TABLE",
]
