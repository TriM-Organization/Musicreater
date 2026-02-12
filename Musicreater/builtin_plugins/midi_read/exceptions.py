# -*- coding: utf-8 -*-

"""
音·创 v3 内置的 Midi 读取插件用到的一些报错类型
"""

"""
版权所有 © 2026 金羿 & 玉衡Alioth
Copyright © 2026 Eilles & YuhengAlioth

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md



from Musicreater.exceptions import MusicreaterOuterlyError


class MidiFormatError(MusicreaterOuterlyError):
    """音·创 的所有MIDI格式错误均继承于此"""

    def __init__(self, *args):
        """音·创 的所有MIDI格式错误均继承于此"""
        super().__init__("MIDI 格式错误 - ", *args)


class NotDefineTempoError(MidiFormatError):
    """没有Tempo设定导致时间无法计算的错误"""

    def __init__(self, *args):
        """没有Tempo设定导致时间无法计算的错误"""
        super().__init__("在曲目开始时没有声明 Tempo（未指定拍长）：", *args)


class ChannelOverFlowError(MidiFormatError):
    """一个midi中含有过多的通道"""

    def __init__(self, max_channel=16, *args):
        """一个midi中含有过多的通道"""
        super().__init__("含有过多的通道（数量应≤{}）：".format(max_channel), *args)


class NotDefineProgramError(MidiFormatError):
    """没有Program设定导致没有乐器可以选择的错误"""

    def __init__(self, *args):
        """没有Program设定导致没有乐器可以选择的错误"""
        super().__init__("未指定演奏乐器：", *args)


class NoteOnOffMismatchError(MidiFormatError):
    """音符开音和停止不匹配的错误"""

    def __init__(self, *args):
        """音符开音和停止不匹配的错误"""
        super().__init__("音符不匹配：", *args)


class LyricMismatchError(MidiFormatError):
    """歌词匹配解析错误"""

    def __init__(self, *args):
        """有可能产生了错误的歌词解析"""
        super().__init__("歌词解析错误：", *args)
