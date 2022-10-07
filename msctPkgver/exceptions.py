# -*- coding: utf-8 -*-


# 音·创 开发交流群 861684859
# Email EillesWan2006@163.com W-YI_DoctorYI@outlook.com EillesWan@outlook.com
# 版权所有 金羿("Eilles Wan") & 诸葛亮与八卦阵("bgArray") & 鸣凤鸽子("MingFengPigeon")
# 若需使用或借鉴 请依照 Apache 2.0 许可证进行许可


"""
音·创 库版 (Musicreater Package Version)
是一款免费开源的针对《我的世界：基岩版》的midi音乐转换库
注意！除了此源文件以外，任何属于此仓库以及此项目的文件均依照Apache许可证进行许可
Musicreater pkgver (Package Version 音·创 库版)
A free open source library used for convert midi file into formats that is suitable for **Minecraft: Bedrock Edition**.
Note! Except for this source file, all the files in this repository and this project are licensed under Apache License 2.0

   Copyright 2022 all the developers of Musicreater

   Licensed under the Apache License, Version 2.0 (the 'License');
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an 'AS IS' BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""




class MSCTBaseException(Exception):
    """音·创库版本的所有错误均继承于此"""

    def __init__(self, *args):
        super().__init__(*args)

    def 喵(self,):
        for i in self.args:
            print(i+"喵！")
    
    def crash_it(self):
        raise self


class CrossNoteError(MSCTBaseException):
    '''同通道下同音符交叉出现所产生的错误'''
    pass


class NotDefineTempoError(MSCTBaseException):
    '''没有Tempo设定导致时间无法计算的错误'''
    pass


class MidiDestroyedError(MSCTBaseException):
    '''Midi文件损坏'''
    pass

class ChannelOverFlowError(MSCTBaseException):
    '''一个midi中含有过多的通道（应≤16）'''
    pass



