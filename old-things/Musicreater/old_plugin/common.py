# -*- coding: utf-8 -*-
"""
存放通用的普遍性的插件内容
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


import math

x = "x"
y = "y"
z = "z"


def bottem_side_length_of_smallest_square_bottom_box(
    _total_block_count: int, _max_height: int
):
    """
    给定结构的总方块数量和规定的最大高度，返回该结构应当构成的图形，在底面的外切正方形之边长

    Parameters
    ------------
    _total_block_count: int
        总方块数量
    _max_height: int
        规定的结构最大高度

    Returns
    ---------
    int
        外切正方形的边长
    """
    return math.ceil(math.sqrt(math.ceil(_total_block_count / _max_height)))
