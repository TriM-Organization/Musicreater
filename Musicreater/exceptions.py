# -*- coding: utf-8 -*-

"""
存放一些报错类型
"""

"""
版权所有 © 2025 金羿 & 诸葛亮与八卦阵
Copyright © 2025 Eilles & bgArray

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md


class MSCTBaseException(Exception):
    """音·创 的所有错误均继承于此"""

    def __init__(self, *args):
        """音·创 的所有错误均继承于此"""
        super().__init__("音·创", *args)

    def meow(
        self,
    ):
        for i in self.args:
            print(i + "喵！")

    def crash_it(self):
        raise self


class MidiFormatException(MSCTBaseException):
    """音·创 的所有MIDI格式错误均继承于此"""

    def __init__(self, *args):
        """音·创 的所有MIDI格式错误均继承于此"""
        super().__init__("MIDI 格式错误", *args)


class MidiDestroyedError(MSCTBaseException):
    """Midi文件损坏"""

    def __init__(self, *args):
        """Midi文件损坏"""
        super().__init__("MIDI文件损坏：无法读取 MIDI 文件", *args)


# class MidiUnboundError(MSCTBaseException):
#     """未定义Midi对象（无用）"""

#     def __init__(self, *args):
#         """未绑定Midi对象"""
#         super().__init__("未定义MidiFile对象：你甚至没有对象就想要生孩子？", *args)
# 此错误在本版本内已经不再使用


class CommandFormatError(MSCTBaseException, RuntimeError):
    """指令格式与目标格式不匹配而引起的错误"""

    def __init__(self, *args):
        """指令格式与目标格式不匹配而引起的错误"""
        super().__init__("指令格式不匹配", *args)


# class CrossNoteError(MidiFormatException):
#     """同通道下同音符交叉出现所产生的错误"""

#     def __init__(self, *args):
#         """同通道下同音符交叉出现所产生的错误"""
#         super().__init__("同通道下同音符交叉", *args)
# 这TM是什么错误？
# 我什么时候写的这玩意？
# 我哪知道这说的是啥？
# ！！！
# 我知道这是什么了 —— 金羿 2025 0401
# 两个其他属性相同的音符在同一个通道，出现连续两个开音信息和连续两个停止信息
# 那么这两个音符的音长无法判断。这是个好问题，但是不是我现在能解决的，也不是我们现在想解决的问题


class NotDefineTempoError(MidiFormatException):
    """没有Tempo设定导致时间无法计算的错误"""

    def __init__(self, *args):
        """没有Tempo设定导致时间无法计算的错误"""
        super().__init__("在曲目开始时没有声明 Tempo（未指定拍长）", *args)


class ChannelOverFlowError(MidiFormatException):
    """一个midi中含有过多的通道"""

    def __init__(self, max_channel=16, *args):
        """一个midi中含有过多的通道"""
        super().__init__("含有过多的通道（数量应≤{}）".format(max_channel), *args)


class NotDefineProgramError(MidiFormatException):
    """没有Program设定导致没有乐器可以选择的错误"""

    def __init__(self, *args):
        """没有Program设定导致没有乐器可以选择的错误"""
        super().__init__("未指定演奏乐器", *args)


class NoteOnOffMismatchError(MidiFormatException):
    """音符开音和停止不匹配的错误"""

    def __init__(self, *args):
        """音符开音和停止不匹配的错误"""
        super().__init__("音符不匹配", *args)


class LyricMismatchError(MSCTBaseException):
    """歌词匹配解析错误"""

    def __init__(self, *args):
        """有可能产生了错误的歌词解析"""
        super().__init__("歌词解析错误", *args)


class ZeroSpeedError(MSCTBaseException, ZeroDivisionError):
    """以0作为播放速度的错误"""

    def __init__(self, *args):
        """以0作为播放速度的错误"""
        super().__init__("播放速度为零", *args)


class IllegalMinimumVolumeError(MSCTBaseException, ValueError):
    """最小播放音量有误的错误"""

    def __init__(self, *args):
        """最小播放音量错误"""
        super().__init__("最小播放音量超出范围", *args)


class MusicSequenceDecodeError(MSCTBaseException):
    """音乐序列解码错误"""

    def __init__(self, *args):
        """音乐序列无法正确解码的错误"""
        super().__init__("解码音符序列文件时出现问题", *args)


class MusicSequenceTypeError(MSCTBaseException):
    """音乐序列类型错误"""

    def __init__(self, *args):
        """无法识别音符序列字节码的类型"""
        super().__init__("错误的音符序列字节类型", *args)


class MusicSequenceVerificationFailed(MusicSequenceDecodeError):
    """音乐序列校验失败"""

    def __init__(self, *args):
        """音符序列文件与其校验值不一致"""
        super().__init__("音符序列文件校验失败", *args)
