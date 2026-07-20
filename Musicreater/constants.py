# -*- coding: utf-8 -*-

"""
存放常量与数值性内容
"""

"""
版权所有 © 2026 金羿 & 诸葛亮与八卦阵
Copyright © 2026 Eilles & bgArray

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md

# from .types import Dict, List, Tuple, MidiInstrumentTableType, MidiNoteNameTableType
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


# Midi用对照表
MIDI_PITCH_NAME_TABLE: Dict[int, str] = {
    0: "C",  # Midi 最低，C-1
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
    12: "C",  # C0
    13: "C#",
    14: "D",
    15: "D#",
    16: "E",
    17: "F",
    18: "F#",
    19: "G",
    20: "G#",
    21: "A",  # 钢琴最低，A0
    22: "A#",
    23: "B",
    24: "C",  # C1
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
    60: "C",  # 钢琴中央 C，C4
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
    108: "C",  # 钢琴最高，C8
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
    127: "G",  # G9
}
"""Midi音高名称对照表"""


MIDI_PITCHED_NOTE_NAME_GROUP: Dict[int, Tuple[str, str]] = {
    1: ("钢琴", "Piano"),
    9: ("半音阶打击乐器", "Chromatic Percussion"),
    17: ("风琴", "Organ"),
    25: ("吉他", "Guitar"),
    33: ("贝斯", "Bass"),
    41: ("弦乐器", "Strings"),
    49: ("合奏乐器", "Ensemble"),
    57: ("铜管乐器", "Brass"),
    65: ("簧乐器", "Reed"),
    73: ("吹管乐器", "Pipe"),
    81: ("合成主旋律", "Synth Lead"),
    89: ("合成和弦", "Synth Pad"),
    97: ("合成声效", "Synth Effects"),
    105: ("民族乐器", "Ethnic"),
    113: ("打击乐器", "Percussive"),
    121: ("特殊音效", "Sound Effects"),
}
"""Midi乐音乐器分组名称对照表"""

MIDI_PITCHED_NOTE_NAME_TABLE: Dict[int, Tuple[str, str]] = {
    1: ("原声平台钢琴", "Acoustic Grand Piano"),
    2: ("亮音原声钢琴", "Bright Acoustic Piano"),
    3: ("数码电钢琴", "Electric Grand Piano"),
    4: ("酒吧钢琴", "Honky-tonk Piano"),
    5: ("电气电钢琴", "Electric Piano 1(Rhodes Piano)"),
    6: ("合唱效果电钢琴", "Electric Piano 2(Chorused Piano)"),
    7: ("拨弦古钢琴（羽管键琴）", "Harpsichord"),
    8: ("古钢琴", "Clavi"),
    9: ("钢片琴", "Celesta"),
    10: ("钟琴", "Glockenspiel"),
    11: ("八音盒", "Music box"),
    12: ("颤音琴", "Vibraphone"),
    13: ("马林巴琴", "Marimba"),
    14: ("木琴", "Xylophone"),
    15: ("管钟", "Tubular Bells"),
    16: ("扬琴", "Dulcimer"),
    17: ("音栓风琴（击杆风琴）", "Drawbar Organ (Hammond Organ)"),
    18: ("打击风琴", "Percussive Organ"),
    19: ("摇滚管风琴", "Rock Organ"),
    20: ("教堂管风琴", "Church Organ"),
    21: ("簧风琴", "Reed Organ"),
    22: ("手风琴", "Accordion"),
    23: ("口琴", "Harmonica"),
    24: ("探戈手风琴", "Tango Accordion"),
    25: ("尼龙弦吉他", "Acoustic Guitar (nylon)"),
    26: ("钢弦吉他", "Acoustic Guitar (steel)"),
    27: ("爵士电吉他", "Electric Guitar (jazz)"),
    28: ("清音电吉他", "Electric Guitar (clean)"),
    29: ("弱音电吉他", "Electric Guitar (muted)"),
    30: ("过驱电吉他", "Overdriven Guitar"),
    31: ("失真电吉他", "Distortion Guitar"),
    32: ("吉他泛音", "Guitar harmonics"),
    33: ("原声贝斯", "Acoustic Bass"),
    34: ("指奏电贝斯", "Electric Bass (finger)"),
    35: ("拨奏电贝斯", "Electric Bass (pick)"),
    36: ("无品贝斯", "Fretless Bass"),
    37: ("击弦贝斯1", "Slap Bass 1"),
    38: ("击弦贝斯2", "Slap Bass 2"),
    39: ("合成贝斯1", "Synth Bass 1"),
    40: ("合成贝斯2", "Synth Bass 2"),
    41: ("小提琴", "Violin"),
    42: ("中提琴", "Viola"),
    43: ("大提琴", "Cello"),
    44: ("低音提琴", "Contrabass"),
    45: ("颤弓弦乐（弦乐震音）", "Tremolo Strings"),
    46: ("弹拨弦乐（弦乐拨奏）", "Pizzicato Strings"),
    47: ("竖琴", "Orchestral Harp"),
    48: ("定音鼓", "Timpani"),
    49: ("弦乐合奏1", "String Ensemble 1"),
    50: ("弦乐合奏2", "String Ensemble 2"),
    51: ("合成弦乐1", "Synth Strings 1"),
    52: ("合成弦乐2", "Synth Strings 2"),
    53: ("合唱“啊”音", "Choir Aahs"),
    54: ("人声“嘟”音", "Voice Oohs"),
    55: ("合成人声", "Synth Voice"),
    56: ("交响打击乐", "Orchestra Hit"),
    57: ("小号", "Trumpet"),
    58: ("长号", "Trombone"),
    59: ("大号", "Tuba"),
    60: ("弱音小号", "Muted Trumpet"),
    61: ("圆号（法国号）", "French Horn"),
    62: ("铜管乐组", "Brass Section"),
    63: ("合成铜管 1", "Synth Brass 1"),
    64: ("合成铜管 2", "Synth Brass 2"),
    65: ("高音萨克斯", "Soprano Sax"),
    66: ("中音萨克斯", "Alto Sax"),
    67: ("次中音萨克斯", "Tenor Sax"),
    68: ("上低音萨克斯", "Baritone Sax"),
    69: ("双簧管", "Oboe"),
    70: ("英国管", "English Horn"),
    71: ("大管（巴松管）", "Bassoon"),
    72: ("单簧管（黑管）", "Clarinet"),
    73: ("短笛", "Piccolo"),
    74: ("长笛", "Flute"),
    75: ("竖笛", "Recorder"),
    76: ("排笛", "Pan Flute"),
    77: ("瓶笛", "Blown Bottle"),
    78: ("尺八", "Shakuhachi"),
    79: ("哨子", "Whistle"),
    80: ("陶笛", "Ocarina"),
    81: ("合成方波", "Lead 1 (square)"),
    82: ("锯齿波音", "Lead 2 (sawtooth)"),
    83: ("汽笛风琴", "Lead 3 (calliope)"),
    84: ("合成吹管", "Lead 4 (chiff)"),
    85: ("合成电吉他", "Lead 5 (charang)"),
    86: ("人声键盘", "Lead 6 (voice)"),
    87: ("五度音", "Lead 7 (fifths)"),
    88: ("低音与主音", "Lead 8 (bass+lead)"),
    89: ("新纪", "Pad 1 (new age)"),
    90: ("暖温", "Pad 2 (warm)"),
    91: ("复音", "Pad 3 (polysynth)"),
    92: ("合声", "Pad 4 (choir)"),
    93: ("弓弦", "Pad 5 (bowed)"),
    94: ("银铃", "Pad 6 (metallic)"),
    95: ("荣光", "Pad 7 (halo)"),
    96: ("轻扫", "Pad 8 (sweep)"),
    97: ("夏雨", "FX 1 (rain)"),
    98: ("音轨", "FX 2 (soundtrack)"),
    99: ("水晶", "FX 3 (crystal)"),
    100: ("大气", "FX 4 (atmosphere)"),
    101: ("轻曼", "FX 5 (light)"),
    102: ("魅影", "FX 6 (goblins)"),
    103: ("回响", "FX 7 (echoes)"),
    104: ("科幻", "FX 8 (sci-fi)"),
    105: ("西塔琴", "Sitar"),
    106: ("五弦琴（班卓琴）", "Banjo"),
    107: ("三味线", "Shamisen"),
    108: ("日本筝", "Koto"),
    109: ("卡林巴铁片琴", "Kalimba"),
    110: ("苏格兰风笛", "Bagpipe"),
    111: ("古提琴", "Fiddle"),
    112: ("唢呐", "Shanai"),
    113: ("铃铛", "Tinkle Bell"),
    114: ("阿哥铃", "Agogo"),
    115: ("钢鼓", "Steel Drums"),
    116: ("木块", "Woodblock"),
    117: ("太鼓", "Taiko Drum"),
    118: ("古式高音鼓", "Melodic Tom"),
    119: ("合成鼓", "Synth Drum"),
    120: ("铜钹", "Reverse Cymbal"),
    121: ("吉他品格杂音", "Guitar Fret Noise"),
    122: ("呼吸杂音", "Breath Noise"),
    123: ("浪潮", "Seashore"),
    124: ("鸟鸣", "Bird Tweet"),
    125: ("电话", "Telephone"),
    126: ("直升机", "Helicopter"),
    127: ("鼓掌", "Applause"),
    128: ("射击", "Gunshot"),
}
"""Midi乐音乐器名称对照表"""

MIDI_PERCUSSION_NOTE_NAME_TABLE: Dict[int, Tuple[str, str]] = {
    35: ("原声大鼓", "Acoustic Bass Drum"),
    36: ("大鼓", "Bass Drum 1"),
    37: ("小鼓鼓边", "Side Stick"),
    38: ("原声小军鼓", "Acoustic Snare"),
    39: ("拍手", "Hand Clap"),
    40: ("电子小军鼓", "Electric Snare"),
    41: ("低音落地桶鼓", "Low Floor Tom"),
    42: ("闭镲", "Closed Hi-Hat"),
    43: ("高音落地桶鼓", "High Floor Tom"),
    44: ("脚踏踩镲", "Pedal Hi-Hat"),
    45: ("低桶鼓", "Low Tom"),
    46: ("开镲", "Open Hi-Hat"),
    47: ("低音中桶鼓", "Low-Mid Tom"),
    48: ("高音中桶鼓", "Hi Mid Tom 2"),
    49: ("强音钹1", "Crash Cymbal 1"),
    50: ("高桶鼓", "High Tom"),
    51: ("打点钹1", "Ride Cymbal 1"),
    52: ("铙钹", "Chinese Cymbal"),
    53: ("圆铃", "Ride Bell"),
    54: ("铃鼓", "Tambourine"),
    55: ("小钹铜钹", "Splash Cymbal"),
    56: ("牛铃", "Cowbell"),
    57: ("强音钹2", "Crash Cymbal 2"),
    58: ("颤音器", "Vibra-Slap"),
    59: ("打点钹2", "Ride Cymbal 2"),
    60: ("高音邦加鼓", "Hi Bongo"),
    61: ("低音邦加鼓", "Low Bongo"),
    62: ("弱音高音康加鼓", "Mute Hi Conga"),
    63: ("强音高音康加鼓", "Open Hi Conga"),
    64: ("低音康加鼓", "Low Conga"),
    65: ("高音天巴鼓", "High Timbale"),
    66: ("低音天巴鼓", "Low Timbale"),
    67: ("高音阿哥铃", "High Agogo"),
    68: ("低音阿哥铃", "Low Agogo"),
    69: ("串珠", "Cabasa"),
    70: ("沙槌", "Maracas"),
    71: ("短口哨", "Short Whistle"),
    72: ("长口哨", "Long Whistle"),
    73: ("短刮壶", "Short Guiro"),
    74: ("长刮壶", "Long Guiro"),
    75: ("梆子", "Claves"),
    76: ("高音木块", "Hi Wood Block"),
    77: ("低音木块", "Low Wood Block"),
    78: ("弱音锯加鼓", "Mute Cuica"),
    79: ("开音锯加鼓", "Open Cuica"),
    80: ("弱音三角铁", "Mute Triangle"),
    81: ("强音三角铁", "Open Triangle"),
}
"""Midi打击乐器名称对照表"""

# Minecraft用对照表

MC_PERCUSSION_INSTRUMENT_LIST: List[str] = [
    "note.snare",
    "note.bd",
    "note.hat",
    "note.basedrum",
    "firework.blast",
    "firework.twinkle",
    "fire.ignite",
    "mob.zombie.wood",
]
"""打击乐器列表"""

MC_PITCHED_INSTRUMENT_LIST: List[str] = [
    "note.harp",
    "note.pling",
    "note.guitar",
    "note.iron_xylophone",
    "note.bell",
    "note.xylophone",
    "note.chime",
    "note.banjo",
    "note.flute",
    "note.bass",
    "note.didgeridoo",
    "note.bit",
    "note.cow_bell",
    "note.trumpet",
    "note.trumpet_exposed",
    "note.trumpet_weathered",
    "note.trumpet_oxidized",
]
"""乐音乐器列表"""

MC_INSTRUMENT_BLOCKS_TABLE: Dict[str, Tuple[str, ...]] = {
    "note.bass": ("planks",),
    "note.bassattack": ("planks",),  # 无法找到此音效
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
    "note.trumpet": ("waxed_copper",),
    "note.trumpet_exposed": ("waxed_exposed_copper",),
    "note.trumpet_weathered": ("waxed_weathered_copper",),
    "note.trumpet_oxidized": ("waxed_oxidized_copper",),
    "note.harp": ("dirt",),
    # 呃……
    "firework.blast": ("sandstone",),
    "firework.twinkle": ("red_sandstone",),
    "fire.ignite": ("concrete_powder",),
    "mob.zombie.wood": ("sand",),
}
"""MC乐器对音符盒下垫方块对照表"""

MC_INSTRUMENT_SOUND_INFO_TABLE: Dict[str, Dict[str, float]] = {
    "note.bass": {"C-LUFS": -1178, "MS": 532.0, "SR": 7218},
    "note.bassattack": {"C-LUFS": -1188, "MS": 484.8, "SR": 7921},
    "note.snare": {"C-LUFS": -1173, "MS": 80.0, "SR": 48000},
    "note.hat": {"C-LUFS": -1480, "MS": 85.3, "SR": 48000},
    "note.bd": {"C-LUFS": -957, "MS": 137.8, "SR": 29718},
    "note.bell": {"C-LUFS": -2510, "MS": 440.7, "SR": 32531},
    "note.flute": {"C-LUFS": -2076, "MS": 618.3, "SR": 19875},
    "note.chime": {"C-LUFS": -2984, "MS": 1106.8, "SR": 38859},
    "note.guitar": {"C-LUFS": -2539, "MS": 567.8, "SR": 24796},
    "note.xylophone": {"C-LUFS": -2419, "MS": 142.4, "SR": 39562},
    "note.iron_xylophone": {"C-LUFS": -2078, "MS": 603.8, "SR": 9328},
    "note.cow_bell": {"C-LUFS": -1427, "MS": 177.2, "SR": 33234},
    "note.didgeridoo": {"C-LUFS": -2062, "MS": 441.5, "SR": 15656},
    "note.bit": {"C-LUFS": -2677, "MS": 384.0, "SR": 48000},
    "note.banjo": {"C-LUFS": -2207, "MS": 466.5, "SR": 31828},
    "note.pling": {"C-LUFS": -1528, "MS": 651.5, "SR": 18468},
    "note.trumpet": {"C-LUFS": -1678, "MS": 277.3, "SR": 48000},
    "note.trumpet_exposed": {"C-LUFS": -1682, "MS": 325.3, "SR": 48000},
    "note.trumpet_oxidized": {"C-LUFS": -2225, "MS": 314.7, "SR": 48000},
    "note.trumpet_weathered": {"C-LUFS": -1875, "MS": 282.7, "SR": 48000},
    "note.harp": {"C-LUFS": -1448, "MS": 588.7, "SR": 15656},
    # 嗯……
    "fire.ignite": {"C-LUFS": -2788, "MS": 426.2, "SR": 40246},
    "firework.blast": {"C-LUFS": -2523, "MS": 1004.3, "SR": 44100},
    "firework.twinkle": {"C-LUFS": -2021, "MS": 1335.1, "SR": 44100},
    "mob.cat.meow-2": {"C-LUFS": -1406, "MS": 648.1, "SR": 33182},
    "mob.cat.meow-4": {"C-LUFS": -1412, "MS": 653.6, "SR": 34467},
    "mob.zombie.wood": {"C-LUFS": -1017, "MS": 940.4, "SR": 44100},
}
"""
MC 乐器对应音效信息表
C-LUFS: 响度，单位`百 LUFS`
MS:     持续时间，单位`毫秒`
SR:     采样率，单位`赫兹`
"""

# 以上的 LUFS 值可以用于计算下面这个倍率
# 我们期望所有的音效的响度都为 -20 LUFS
# 那么需要改变每一个采样的音量大小就需要
# data * (10 ** ((原响度 - 目标响度) / 20))
# 其中 10 ** ((原响度 - 目标响度) / 20) 为倍率
# 上表中的响度单位是 百 LUFS
# 因此实际计算的过程中记得把这一百除回来
# 公式就变成了：
# data * (10 ** ((C_LUFS - 2000) / 2000))
MC_INSTRUMENT_VOLUME_BALANCE_TABLE: Dict[str, float] = {
    "note.bass": 0.3881503659906483,
    "note.bassattack": 0.3926449353995998,
    "note.snare": 0.3859224115947292,
    "note.hat": 0.5495408738576245,
    "note.bd": 0.3009539168873202,
    "note.bell": 1.7988709151287878,
    "note.flute": 1.0914403364487566,
    "note.chime": 3.1045595881283554,
    "note.guitar": 1.8599445632225762,
    "note.xylophone": 1.6199439939036293,
    "note.iron_xylophone": 1.093956366272094,
    "note.cow_bell": 0.517011257968655,
    "note.didgeridoo": 1.0739894123412448,
    "note.bit": 2.1802183971859455,
    "note.banjo": 1.2691121444451907,
    "note.pling": 0.580764417521312,
    "note.trumpet": 0.690239803840242,
    "note.trumpet_exposed": 0.6934258060165691,
    "note.trumpet_oxidized": 1.2956866975170194,
    "note.trumpet_weathered": 0.8659643233600653,
    "note.harp": 0.5296634438916578,
    "fire.ignite": 2.4774220576332855,
    "firework.blast": 1.8259967490749676,
    "firework.twinkle": 1.0244717803103813,
    "mob.cat.meow-2": 0.5046612975635284,
    "mob.cat.meow-4": 0.5081594425605606,
    "mob.zombie.wood": 0.32247793193163765,
}
"""乐器响度平衡表，倍率"""

MC_EILLES_RT261_INSTRUMENT_REPLACE_TABLE: Dict[str, str] = {
    "note.trumpet": "note.flute",
    "note.trumpet_exposed": "note.flute",
    "note.trumpet_weathered": "note.banjo",
    "note.trumpet_oxidized": "note.banjo",
}


MC_EILLES_RTJE12_INSTRUMENT_REPLACE_TABLE: Dict[str, str] = {
    "note.iron_xylophone": "note.xylophone",
    "note.cow_bell": "note.xylophone",
    "note.didgeridoo": "note.guitar",
    "note.bit": "note.harp",
    "note.banjo": "note.flute",
    "note.pling": "note.harp",
}
"""在 Minecraft JE 1.12 ~ JE 1.14 的版本中，部分乐器是没有的，这是金羿的乐器替换表"""

MC_EILLES_RTBETA_INSTRUMENT_REPLACE_TABLE: Dict[str, str] = {
    # lt je 12
    "note.bell": "note.harp",
    "note.flute": "note.harp",
    "note.chime": "note.harp",
    "note.guitar": "note.bass",
    "note.xylophone": "note.hat",
    # rt je 12
    "note.iron_xylophone": "note.hat",
    "note.cow_bell": "note.ha",
    "note.didgeridoo": "note.bass",
    "note.bit": "note.harp",
    "note.banjo": "note.harp",
    "note.pling": "note.harp",
}
"""在 Minecraft JE Beta1.2 / BE 0.13.0 ~ JE 1.12 / BE 1.13.0 的版本中，部分乐器是没有的，这是金羿的乐器替换表"""


# Midi对MC通用对照表

MM_INSTRUMENT_RANGE_TABLE: Dict[str, Tuple[Tuple[int, int], int]] = {
    "note.harp": ((42, 66), 54),
    "note.pling": ((42, 66), 54),
    "note.guitar": ((30, 54), 42),
    "note.iron_xylophone": ((42, 66), 54),
    "note.bell": ((66, 90), 78),
    "note.xylophone": ((66, 90), 78),
    "note.chime": ((66, 90), 78),
    "note.banjo": ((42, 66), 54),
    "note.flute": ((54, 78), 66),
    "note.bass": ((18, 42), 30),
    "note.snare": ((-1, 128), 0),  # 实际上是 0~127，此处仅作兼容性处理
    "note.didgeridoo": ((18, 42), 30),
    "mob.zombie.wood": ((-1, 128), 0),
    "note.bit": ((42, 66), 54),
    "note.hat": ((-1, 128), 0),
    "note.bd": ((-1, 128), 0),
    "note.basedrum": ((-1, 128), 0),
    "firework.blast": ((-1, 128), 0),
    "firework.twinkle": ((-1, 128), 0),
    "fire.ignite": ((-1, 128), 0),
    "note.cow_bell": ((54, 78), 66),
    "note.trumpet": ((42, 66), 54),
    "note.trumpet_exposed": ((42, 66), 54),
    "note.trumpet_weathered": ((30, 54), 42),
    "note.trumpet_oxidized": ((30, 54), 42),
}
"""
不同乐器的音域偏离对照表
元组里的是范围，后面的整数是游戏里的默认采样音高
单位是在 Midi 中的音高
"""

MM_INSTRUMENT_DEVIATION_TABLE: Dict[str, int] = {
    "note.harp": 6,
    "note.pling": 6,
    "note.guitar": -6,
    "note.iron_xylophone": 6,
    "note.bell": 30,
    "note.xylophone": 30,
    "note.chime": 30,
    "note.banjo": 6,
    "note.flute": 18,
    "note.bass": -18,
    "note.snare": 0,
    "note.didgeridoo": -18,
    "mob.zombie.wood": 0,
    "note.bit": 6,
    "note.hat": 0,
    "note.bd": 0,
    "firework.blast": 0,
    "firework.twinkle": 0,
    "fire.ignite": 0,
    "note.cow_bell": 6,
    "note.trumpet": 6,
    "note.trumpet_exposed": 6,
    "note.trumpet_weathered": -6,
    "note.trumpet_oxidized": -6,
}
"""
不同乐器的音调偏离对照表  
*注意* 该表中的单位是对于 Midi Pitch 音调（整数）的低音偏移。  
也就是说，该数值越高，则在 Midi Pitch 中的值域越低  
默认的偏移量为 6 ，因为在计算音高时候少减去了 6 个 Pitch 单位
（在表里的数据是用作被减数的，实际计算时默认有 +6，所以在表中默认的 6 最后就会被抵消）
"""


# Midi音高对MC方块对照表

# 金羿ELS 音符方块对照表

MN_EILLES_NOTE_BLOCK_TABLE: Dict[int, str] = {
}



