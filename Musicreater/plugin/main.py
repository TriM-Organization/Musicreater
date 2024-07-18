# -*- coding: utf-8 -*-
"""
存放附加内容功能
"""

"""
版权所有 © 2024 金羿 & 诸葛亮与八卦阵
Copyright © 2024 EillesWan & bgArray

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md


# from dataclasses import dataclass
# from typing import Literal, Tuple, Union

# from ..subclass import DEFAULT_PROGRESSBAR_STYLE, ProgressBarStyle


# @dataclass(init=False)
# class ConvertConfig: # 必定要改
#     """
#     转换通用设置存储类
#     """

#     progressbar_style: Union[ProgressBarStyle, None]
#     """进度条样式"""

#     dist_path: str
#     """输出目录"""

#     def __init__(
#         self,
#         output_path: str,
#         progressbar: Union[bool, Tuple[str, Tuple[str, str]], ProgressBarStyle] = True,
#         ignore_progressbar_param_error: bool = False,
#     ):
#         """
#         将已经转换好的数据内容指令载入MC可读格式

#         Parameters
#         ----------
#         output_path: str
#             生成内容的输出目录
#         volume: float
#             音量比率，范围为(0,1]，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
#         speed: float
#             速度倍率，注意：这里的速度指的是播放速度倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
#         progressbar: bool|tuple[str, Tuple[str,]]
#             进度条，当此参数为 `True` 时使用默认进度条，为其他的**值为真**的参数时识别为进度条自定义参数，为其他**值为假**的时候不生成进度条

#         """

#         self.dist_path = output_path
#         """输出目录"""

#         if progressbar:
#             # 此处是对于仅有 True 的参数和自定义参数的判断
#             # 改这一段没🐎
#             if progressbar is True:
#                 self.progressbar_style = DEFAULT_PROGRESSBAR_STYLE
#                 """进度条样式"""
#                 return
#             elif isinstance(progressbar, ProgressBarStyle):
#                 self.progressbar_style = progressbar
#                 """进度条样式"""
#                 return
#             elif isinstance(progressbar, tuple):
#                 if isinstance(progressbar[0], str) and isinstance(
#                     progressbar[1], tuple
#                 ):
#                     if isinstance(progressbar[1][0], str) and isinstance(
#                         progressbar[1][1], str
#                     ):
#                         self.progressbar_style = ProgressBarStyle(
#                             progressbar[0], progressbar[1][0], progressbar[1][1]
#                         )
#                         return
#             if not ignore_progressbar_param_error:
#                 raise TypeError(
#                     "参数 {} 的类型 {} 与所需类型 Union[bool, Tuple[str, Tuple[str, str]], ProgressBarStyle] 不符。".format(
#                         progressbar, type(progressbar)
#                     )
#                 )

#         self.progressbar_style = None
#         """进度条样式组"""
