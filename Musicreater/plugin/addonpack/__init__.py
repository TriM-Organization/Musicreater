# -*- coding: utf-8 -*-
"""
用以生成附加包的附加功能

版权所有 © 2023 音·创 开发者
Copyright © 2023 all the developers of Musicreater

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿穆组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md


__all__ = [
    "to_addon_pack_in_delay",
    "to_addon_pack_in_score",
    "to_addon_pack_in_repeater",
]
__author__ = (("金羿", "Eilles Wan"),)

from .main import (
    to_addon_pack_in_delay,
    to_addon_pack_in_repeater,
    to_addon_pack_in_score,
)
