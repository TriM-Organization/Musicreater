# -*- coding: utf-8 -*-

"""
存放数据类型的定义
"""

"""
版权所有 © 2023 音·创 开发者
Copyright © 2023 all the developers of Musicreater

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md

from typing import Any, Dict, List, Literal, Optional, Tuple, Union

import mido

from .subclass import SingleNote

ProgressStyle = Tuple[str, Tuple[str, str]]
"""
进度条样式类型
"""

VoidMido = Union[mido.MidiFile, None]  # void mido
"""
空Midi类类型
"""


NoteChannelType = Dict[
    int,
    List[SingleNote,],
]
"""
频道信息类型

Dict[int,Dict[int,List[SingleNote,],],]
"""


ChannelType = Dict[
    int,
    Dict[
        int,
        List[
            Union[
                Tuple[Literal["PgmC"], int, int],
                Tuple[Literal["NoteS"], int, int, int],
                Tuple[Literal["NoteE"], int, int],
            ]
        ],
    ],
]
"""
以字典所标记的频道信息类型（即将弃用）

Dict[int,Dict[int,List[Union[Tuple[Literal["PgmC"], int, int],Tuple[Literal["NoteS"], int, int, int],Tuple[Literal["NoteE"], int, int],]],],]
"""
