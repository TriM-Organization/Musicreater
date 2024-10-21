# -*- coding: utf-8 -*-
"""一个简单的我的世界音频转换库
音·创 (Musicreater)
是一款免费开源的《我的世界》数字音频支持库。
Musicreater(音·创)
A free open source library used for dealing with **Minecraft** digital musics.

版权所有 © 2024 金羿 & 诸葛亮与八卦阵
Copyright © 2024 EillesWan & bgArray

音·创（“本项目”）的协议颁发者为 金羿、诸葛亮与八卦阵
The Licensor of Musicreater("this project") is Eilles Wan, bgArray.

本项目根据 第一版 汉钰律许可协议（“本协议”）授权。
任何人皆可从以下地址获得本协议副本：https://gitee.com/EillesWan/YulvLicenses。
若非因法律要求或经过了特殊准许，此作品在根据本协议“原样”提供的基础上，不予提供任何形式的担保、任何明示、任何暗示或类似承诺。也就是说，用户将自行承担因此作品的质量或性能问题而产生的全部风险。
详细的准许和限制条款请见原协议文本。
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md


__version__ = "2.2.2.1"
__vername__ = "部分API小幅度新增内容"
__author__ = (
    ("金羿", "Eilles Wan"),
    ("诸葛亮与八卦阵", "bgArray"),
    ("鱼旧梦", "ElapsingDreams"),
    ("偷吃不是Touch", "Touch"),
)
__all__ = [
    # 主要类
    "MusicSequence",
    "MidiConvert",
    # 附加类
    # "SingleNote",
    "MineNote",
    "MineCommand",
    "SingleNoteBox",
    "ProgressBarStyle",
    # "TimeStamp", 未来功能
    # 默认值
    "DEFAULT_PROGRESSBAR_STYLE",
    "MM_INSTRUMENT_RANGE_TABLE",
    "MM_CLASSIC_PITCHED_INSTRUMENT_TABLE",
    "MM_CLASSIC_PERCUSSION_INSTRUMENT_TABLE",
    "MM_TOUCH_PITCHED_INSTRUMENT_TABLE",
    "MM_TOUCH_PERCUSSION_INSTRUMENT_TABLE",
]

from .main import *
