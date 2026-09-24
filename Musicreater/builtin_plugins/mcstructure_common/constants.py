# -*- coding: utf-8 -*-
"""
MCSTRUCTURE 共享结构原语库 - 常量定义
"""

"""
版权所有 © 2026 金羿、玉衡Alioth
Copyright © 2026 Eilles, YuhengAlioth

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md


x = "x"
y = "y"
z = "z"


AXIS_PARTICULAR_VALUE = {
    x: {
        True: 5,
        False: 4,
    },
    y: {
        True: 1,
        False: 0,
    },
    z: {
        True: 3,
        False: 2,
    },
}
"""
指令方块朝向对应特殊值
"""

# 1.17的结构兼容版本号
COMPABILITY_VERSION_117: int = 17879555
"""
Minecraft 1.17 兼容版本号
"""
# 1.19的结构兼容版本号
COMPABILITY_VERSION_119: int = 17959425
"""
Minecraft 1.19 兼容版本号
"""
COMPABILITY_VERSION_121: int = 18168865
"""
Minecraft 1.21 兼容版本号
"""
