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

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md

from typing import Dict, List, Tuple

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

MIDI_PITCH_NAME_TABLE: Dict[int, str] = {
    0: "C",
    1: "C#",
    2: "D",
    3: "D#",
    4: "E",
    5: "F",
    6: "F#",
    7: "G",
    8: "G#",
    9: "A",
    10: "A#",
    11: "B",
    12: "C",
    13: "C#",
    14: "D",
    15: "D#",
    16: "E",
    17: "F",
    18: "F#",
    19: "G",
    20: "G#",
    21: "A",
    22: "A#",
    23: "B",
    24: "C",
    25: "C#",
    26: "D",
    27: "D#",
    28: "E",
    29: "F",
    30: "F#",
    31: "G",
    32: "G#",
    33: "A",
    34: "A#",
    35: "B",
    36: "C",
    37: "C#",
    38: "D",
    39: "D#",
    40: "E",
    41: "F",
    42: "F#",
    43: "G",
    44: "G#",
    45: "A",
    46: "A#",
    47: "B",
    48: "C",
    49: "C#",
    50: "D",
    51: "D#",
    52: "E",
    53: "F",
    54: "F#",
    55: "G",
    56: "G#",
    57: "A",
    58: "A#",
    59: "B",
    60: "C",
    61: "C#",
    62: "D",
    63: "D#",
    64: "E",
    65: "F",
    66: "F#",
    67: "G",
    68: "G#",
    69: "A",
    70: "A#",
    71: "B",
    72: "C",
    73: "C#",
    74: "D",
    75: "D#",
    76: "E",
    77: "F",
    78: "F#",
    79: "G",
    80: "G#",
    81: "A",
    82: "A#",
    83: "B",
    84: "C",
    85: "C#",
    86: "D",
    87: "D#",
    88: "E",
    89: "F",
    90: "F#",
    91: "G",
    92: "G#",
    93: "A",
    94: "A#",
    95: "B",
    96: "C",
    97: "C#",
    98: "D",
    99: "D#",
    100: "E",
    101: "F",
    102: "F#",
    103: "G",
    104: "G#",
    105: "A",
    106: "A#",
    107: "B",
    108: "C",
    109: "C#",
    110: "D",
    111: "D#",
    112: "E",
    113: "F",
    114: "F#",
    115: "G",
    116: "G#",
    117: "A",
    118: "A#",
    119: "B",
    120: "C",
    121: "C#",
    122: "D",
    123: "D#",
    124: "E",
    125: "F",
    126: "F#",
    127: "G",
}


# 以下是由 Touch “偷吃” 带来的高准确率音效对照表
# 包括乐音乐器对照和打击乐器对照

PITCHED_INSTRUMENT_TABLE: Dict[int, Tuple[str, int]] = {
    0: ("note.harp", 6),
    1: ("note.harp", 6),
    2: ("note.pling", 6),
    3: ("note.harp", 6),
    4: ("note.pling", 6),
    5: ("note.pling", 6),
    6: ("note.guitar", 7),
    7: ("note.guitar", 7),
    8: ("note.iron_xylophone", 8),
    9: ("note.bell", 4),  # 打击乐器无音域
    10: ("note.iron_xylophone", 6),
    11: ("note.iron_xylophone", 6),
    12: ("note.iron_xylophone", 6),
    13: ("note.xylophone", 4),
    14: ("note.chime", 4),
    15: ("note.banjo", 6),
    16: ("note.xylophone", 6),
    17: ("note.iron_xylophone", 6),
    18: ("note.flute", 5),
    19: ("note.flute", 5),
    20: ("note.flute", 5),
    21: ("note.flute", 5),
    22: ("note.flute", 5),
    23: ("note.flute", 5),
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
    40: ("note.flute", 5),
    41: ("note.flute", 5),
    42: ("note.flute", 5),
    43: ("note.bass", 8),
    44: ("note.flute", 5),
    45: ("note.iron_xylophone", 6),
    46: ("note.harp", 6),
    47: ("note.snare", 7),
    48: ("note.flute", 5),
    49: ("note.flute", 5),
    50: ("note.flute", 5),
    51: ("note.flute", 5),
    52: ("note.didgeridoo", 5),
    53: ("note.flute", 5),  # 合唱“啊”音
    54: ("note.flute", 5),  # 人声“嘟”音
    55: ("mob.zombie.wood", 7),  # 合成人声
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
    69: ("note.bit", 6),
    70: ("note.banjo", 6),
    71: ("note.flute", 5),
    72: ("note.flute", 5),
    73: ("note.flute", 5),
    74: ("note.flute", 5),
    75: ("note.flute", 5),
    76: ("note.iron_xylophone", 6),
    77: ("note.iron_xylophone", 6),
    78: ("note.flute", 5),
    79: ("note.flute", 5),
    80: ("note.bit", 6),
    81: ("note.bit", 6),
    82: ("note.flute", 5),
    83: ("note.flute", 5),
    84: ("note.guitar", 7),
    85: ("note.flute", 5),
    86: ("note.bass", 8),
    87: ("note.bass", 8),
    88: ("note.bit", 6),
    89: ("note.flute", 5),
    90: ("note.bit", 6),
    91: ("note.flute", 5),
    92: ("note.bell", 4),
    93: ("note.guitar", 7),
    94: ("note.flute", 5),
    95: ("note.bit", 6),
    96: ("note.bit", 6),  # 雨声
    97: ("note.flute", 5),
    98: ("note.bell", 4),
    99: ("note.bit", 6),  # 大气
    100: ("note.bit", 6),  # 明亮
    101: ("note.bit", 6),  # 鬼怪
    102: ("note.bit", 6),  # 回声
    103: ("note.bit", 6),  # 科幻
    104: ("note.iron_xylophone", 6),
    105: ("note.banjo", 6),
    106: ("note.harp", 6),
    107: ("note.harp", 6),
    108: ("note.bell", 4),
    109: ("note.flute", 5),
    110: ("note.flute", 5),
    111: ("note.flute", 5),
    112: ("note.bell", 4),
    113: ("note.xylophone", 4),
    114: ("note.flute", 5),
    115: ("note.hat", 7),  # 打击乐器无音域
    116: ("note.snare", 7),  # 打击乐器无音域
    117: ("note.snare", 7),  # 打击乐器无音域
    118: ("note.bd", 7),  # 打击乐器无音域
    119: ("firework.blast", 7),  # 打击乐器无音域
    120: ("note.guitar", 7),  # 吉他还把杂音
    121: ("note.harp", 6),  # 呼吸声
    122: ("note.harp", 6),  # 海浪声
    123: ("note.harp", 6),  # 鸟鸣
    124: ("note.bit", 6),
    125: ("note.hat", 7),  # 直升机
    126: ("firework.twinkle", 7),  # 打击乐器无音域
    127: ("mob.zombie.wood", 7),  # 打击乐器无音域
}

PERCUSSION_INSTRUMENT_TABLE: Dict[int, Tuple[str, int]] = {
    34: ("note.hat", 7),
    35: ("note.bd", 7),
    36: ("note.bd", 7),
    37: ("note.snare", 7),
    38: ("note.snare", 7),
    39: ("fire.ignite", 7),
    40: ("note.snare", 7),
    41: ("note.hat", 7),
    42: ("note.hat", 7),
    43: ("firework.blast", 7),
    44: ("note.hat", 7),
    45: ("note.snare", 4),
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

PERCUSSION_INSTRUMENT_LIST: List[str] = [
    "note.snare",
    "note.bd",
    "note.hat",
    "note.basedrum",
    "firework.blast",
    "firework.twinkle",
    "fire.ignite",
    "mob.zombie.wood",
]

INSTRUMENT_BLOCKS_TABLE: Dict[str, Tuple[str, ...]] = {
    "note.bass": ("planks",),
    "note.snare": ("sand",),
    "note.hat": ("glass",),
    "note.bd": ("stone",),
    "note.basedrum": ("stone",),
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
    "note.harp": ("dirt",),
    # 呃……
    "firework.blast": ("sandstone",),
    "firework.twinkle": ("red_sandstone",),
    "fire.ignite": ("concrete_powder",),
    "mob.zombie.wood": ("sand",),
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
