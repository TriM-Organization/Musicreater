# -*- coding: utf-8 -*-

"""
存放常量与数值性内容
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


x = "x"
"""
x
"""

y = "y"
"""
y
"""

z = "z"
"""
z
"""

DEFAULT_PROGRESSBAR_STYLE = (
    r"▶ %%N [ %%s/%^s %%% __________ %%t|%^t ]",
    ("§e=§r", "§7=§r"),
)
"""
默认的进度条样式组
"""

PITCHED_INSTRUMENT_LIST = {
    0: ("note.harp", 6),
    1: ("note.harp", 6),
    2: ("note.pling", 6),
    3: ("note.harp", 6),
    4: ("note.pling", 6),
    5: ("note.pling", 6),
    6: ("note.harp", 6),
    7: ("note.harp", 6),
    8: ("note.share", 7),  # 打击乐器无音域
    9: ("note.harp", 6),
    10: ("note.didgeridoo", 8),
    11: ("note.harp", 6),
    12: ("note.xylophone", 4),
    13: ("note.chime", 4),
    14: ("note.harp", 6),
    15: ("note.harp", 6),
    16: ("note.bass", 8),
    17: ("note.harp", 6),
    18: ("note.harp", 6),
    19: ("note.harp", 6),
    20: ("note.harp", 6),
    21: ("note.harp", 6),
    22: ("note.harp", 6),
    23: ("note.guitar", 7),
    24: ("note.guitar", 7),
    25: ("note.guitar", 7),
    26: ("note.guitar", 7),
    27: ("note.guitar", 7),
    28: ("note.guitar", 7),
    29: ("note.guitar", 7),
    30: ("note.guitar", 7),
    31: ("note.bass", 8),
    32: ("note.bass", 8),
    33: ("note.bass", 8),
    34: ("note.bass", 8),
    35: ("note.bass", 8),
    36: ("note.bass", 8),
    37: ("note.bass", 8),
    38: ("note.bass", 8),
    39: ("note.bass", 8),
    40: ("note.harp", 6),
    41: ("note.harp", 6),
    42: ("note.harp", 6),
    43: ("note.harp", 6),
    44: ("note.iron_xylophone", 6),
    45: ("note.guitar", 7),
    46: ("note.harp", 6),
    47: ("note.harp", 6),
    48: ("note.guitar", 7),
    49: ("note.guitar", 7),
    50: ("note.bit", 6),
    51: ("note.bit", 6),
    52: ("note.harp", 6),
    53: ("note.harp", 6),
    54: ("note.bit", 6),
    55: ("note.flute", 5),
    56: ("note.flute", 5),
    57: ("note.flute", 5),
    58: ("note.flute", 5),
    59: ("note.flute", 5),
    60: ("note.flute", 5),
    61: ("note.flute", 5),
    62: ("note.flute", 5),
    63: ("note.flute", 5),
    64: ("note.bit", 6),
    65: ("note.bit", 6),
    66: ("note.bit", 6),
    67: ("note.bit", 6),
    68: ("note.flute", 5),
    69: ("note.harp", 6),
    70: ("note.harp", 6),
    71: ("note.flute", 5),
    72: ("note.flute", 5),
    73: ("note.flute", 5),
    74: ("note.harp", 6),
    75: ("note.flute", 5),
    76: ("note.harp", 6),
    77: ("note.harp", 6),
    78: ("note.harp", 6),
    79: ("note.harp", 6),
    80: ("note.bit", 6),
    81: ("note.bit", 6),
    82: ("note.bit", 6),
    83: ("note.bit", 6),
    84: ("note.bit", 6),
    85: ("note.bit", 6),
    86: ("note.bit", 6),
    87: ("note.bit", 6),
    88: ("note.bit", 6),
    89: ("note.bit", 6),
    90: ("note.bit", 6),
    91: ("note.bit", 6),
    92: ("note.bit", 6),
    93: ("note.bit", 6),
    94: ("note.bit", 6),
    95: ("note.bit", 6),
    96: ("note.bit", 6),
    97: ("note.bit", 6),
    98: ("note.bit", 6),
    99: ("note.bit", 6),
    100: ("note.bit", 6),
    101: ("note.bit", 6),
    102: ("note.bit", 6),
    103: ("note.bit", 6),
    104: ("note.harp", 6),
    105: ("note.banjo", 6),
    106: ("note.harp", 6),
    107: ("note.harp", 6),
    108: ("note.harp", 6),
    109: ("note.harp", 6),
    110: ("note.harp", 6),
    111: ("note.guitar", 7),
    112: ("note.harp", 6),
    113: ("note.bell", 4),
    114: ("note.harp", 6),
    115: ("note.cow_bell", 5),
    116: ("note.bd", 7),  # 打击乐器无音域
    117: ("note.bass", 8),
    118: ("note.bit", 6),
    119: ("note.bd", 7),  # 打击乐器无音域
    120: ("note.guitar", 7),
    121: ("note.harp", 6),
    122: ("note.harp", 6),
    123: ("note.harp", 6),
    124: ("note.harp", 6),
    125: ("note.hat", 7),  # 打击乐器无音域
    126: ("note.bd", 7),  # 打击乐器无音域
    127: ("note.snare", 7),  # 打击乐器无音域
}

PERCUSSION_INSTRUMENT_LIST = {
    34: ("note.bd", 7),
    35: ("note.bd", 7),
    36: ("note.hat", 7),
    37: ("note.snare", 7),
    38: ("note.snare", 7),
    39: ("note.snare", 7),
    40: ("note.hat", 7),
    41: ("note.snare", 7),
    42: ("note.hat", 7),
    43: ("note.snare", 7),
    44: ("note.snare", 7),
    45: ("note.bell", 4),
    46: ("note.snare", 7),
    47: ("note.snare", 7),
    48: ("note.bell", 4),
    49: ("note.hat", 7),
    50: ("note.bell", 4),
    51: ("note.bell", 4),
    52: ("note.bell", 4),
    53: ("note.bell", 4),
    54: ("note.bell", 4),
    55: ("note.bell", 4),
    56: ("note.snare", 7),
    57: ("note.hat", 7),
    58: ("note.chime", 4),
    59: ("note.iron_xylophone", 6),
    60: ("note.bd", 7),
    61: ("note.bd", 7),
    62: ("note.xylophone", 4),
    63: ("note.xylophone", 4),
    64: ("note.xylophone", 4),
    65: ("note.hat", 7),
    66: ("note.bell", 4),
    67: ("note.bell", 4),
    68: ("note.hat", 7),
    69: ("note.hat", 7),
    70: ("note.flute", 5),
    71: ("note.flute", 5),
    72: ("note.hat", 7),
    73: ("note.hat", 7),
    74: ("note.xylophone", 4),
    75: ("note.hat", 7),
    76: ("note.hat", 7),
    77: ("note.xylophone", 4),
    78: ("note.xylophone", 4),
    79: ("note.bell", 4),
    80: ("note.bell", 4),
}

INSTRUMENT_BLOCKS_LIST = {
    "note.bass": ("planks",),
    "note.snare": ("sand",),
    "note.hat": ("glass",),
    "note.bd": ("stone",),
    "note.bell": ("gold_block",),
    "note.flute": ("clay",),
    "note.chime": ("packed_ice",),
    "note.guitar": ("wool",),
    "note.xylobone": ("bone_block",),
    "note.iron_xylophone": ("iron_block",),
    "note.cow_bell": ("soul_sand",),
    "note.didgeridoo": ("pumpkin",),
    "note.bit": ("emerald_block",),
    "note.banjo": ("hay_block",),
    "note.pling": ("glowstone",),
    "note.bassattack": ("command_block",),  # 无法找到此音效
    "note.harp": ("glass",),
}


# 即将启用
height2note = {
    0.5: 0,
    0.53: 1,
    0.56: 2,
    0.6: 3,
    0.63: 4,
    0.67: 5,
    0.7: 6,
    0.75: 7,
    0.8: 8,
    0.84: 9,
    0.9: 10,
    0.94: 11,
    1.0: 12,
    1.05: 13,
    1.12: 14,
    1.2: 15,
    1.25: 16,
    1.33: 17,
    1.4: 18,
    1.5: 19,
    1.6: 20,
    1.7: 21,
    1.8: 22,
    1.9: 23,
    2.0: 24,
}
"""音高对照表\n
MC音高:音符盒音调"""
