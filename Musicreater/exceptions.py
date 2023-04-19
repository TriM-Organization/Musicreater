# -*- coding: utf-8 -*-


# 睿穆组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 版权所有 金羿("Eilles Wan") & 诸葛亮与八卦阵("bgArray") & 鸣凤鸽子("MingFengPigeon")
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md


"""一个简单的我的世界音频转换库
音·创 (Musicreater)
是一款免费开源的针对《我的世界》的midi音乐转换库
Musicreater(音·创)
A free open source library used for convert midi file into formats that is suitable for **Minecraft**.

版权所有 © 2023 音·创 开发者
Copyright © 2023 all the developers of Musicreater

开源相关声明请见 ../License.md
Terms & Conditions: ../License.md
"""


class MSCTBaseException(Exception):
    """音·创库版本的所有错误均继承于此"""

    def __init__(self, *args):
        super().__init__(*args)

    def miao(
        self,
    ):
        for i in self.args:
            print(i + "喵！")

    def crash_it(self):
        raise self
    

class CrossNoteError(MSCTBaseException):
    """同通道下同音符交叉出现所产生的错误"""

    pass


class NotDefineTempoError(MSCTBaseException):
    """没有Tempo设定导致时间无法计算的错误"""

    pass


class MidiDestroyedError(MSCTBaseException):
    """Midi文件损坏"""

    pass


class ChannelOverFlowError(MSCTBaseException):
    """一个midi中含有过多的通道（数量应≤16）"""

    pass


class NotDefineProgramError(MSCTBaseException):
    """没有Program设定导致没有乐器可以选择的错误"""

    pass


class ZeroSpeedError(MSCTBaseException):
    """以0作为播放速度的错误"""

    pass