# -*- coding: utf-8 -*-
"""
存放通用的普遍性的插件内容
"""

"""
版权所有 © 2023 音·创 开发者
Copyright © 2023 all the developers of Musicreater

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿穆组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md


import math


def bottem_side_length_of_smallest_square_bottom_box(total: int, maxHeight: int):
    """给定总方块数量和最大高度，返回所构成的图形外切正方形的边长
    :param total: 总方块数量
    :param maxHeight: 最大高度
    :return: 外切正方形的边长 int"""
    return math.ceil(math.sqrt(math.ceil(total / maxHeight)))


