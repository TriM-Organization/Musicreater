# -*- coding: utf-8 -*-

"""
存储 音·创 v3 定义的一些数据类型，可以用于类型检查器
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


from typing import Callable, Dict, List, Literal, Mapping, Tuple, Union

FittingFunctionType = Callable[[float], float]
"""
拟合函数类型
"""
