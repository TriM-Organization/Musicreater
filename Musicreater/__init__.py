# -*- coding: utf-8 -*-
"""一个简单的我的世界音频转换库
音·创 (Musicreater)
是一款免费开源的针对《我的世界》的midi音乐转换库
Musicreater(音·创)
A free open source library used for convert midi file into formats that is suitable for **Minecraft**.

版权所有 © 2023 音·创 开发者
Copyright © 2023 all the developers of Musicreater

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿穆组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md


__version__ = "1.4.2"
__vername__ = "优质的红石音乐生成&更好的线性插值算法"
__author__ = (
    ("金羿", "Eilles Wan"),
    ("诸葛亮与八卦阵", "bgArray"),
    ("偷吃不是Touch", "Touch"),
    ("鸣凤鸽子", "MingFengPigeon"),
)
__all__ = [
    # 主要类
    "MidiConvert",
    # 附加类
    # "SingleNote",
    "SingleCommand",
    # "TimeStamp", 未来功能
]

from .main import *
