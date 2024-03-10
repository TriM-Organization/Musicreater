# -*- coding: utf-8 -*-

"""
存放常量与数值性内容
"""

"""
版权所有 © 2024 音·创 开发者
Copyright © 2024 all the developers of Musicreater

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md

from .types import Dict, List, Tuple, MidiInstrumentTableType, MidiNoteNameTableType

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
    65: ("高音萨克斯风", "Soprano Sax"),
    66: ("中音萨克斯风", "Alto Sax"),
    67: ("次中音萨克斯风", "Tenor Sax"),
    68: ("上低音萨克斯风", "Baritone Sax"),
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
]
"""乐音乐器列表"""

MC_INSTRUMENT_BLOCKS_TABLE: Dict[str, Tuple[str, ...]] = {
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
    "note.bassattack": ("stone",),  # 无法找到此音效
    "note.harp": ("dirt",),
    # 呃……
    "firework.blast": ("sandstone",),
    "firework.twinkle": ("red_sandstone",),
    "fire.ignite": ("concrete_powder",),
    "mob.zombie.wood": ("sand",),
}
"""MC乐器对音符盒下垫方块对照表"""

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
    "note.snare": ((-1, 128), 0),  # 实际上是 0~127
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
}
"""不同乐器的音域偏离对照表"""

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
    "note.snare": -1,
    "note.didgeridoo": -18,
    "mob.zombie.wood": -1,
    "note.bit": 6,
    "note.hat": -1,
    "note.bd": -1,
    "firework.blast": -1,
    "firework.twinkle": -1,
    "fire.ignite": -1,
    "note.cow_bell": 6,
}
"""不同乐器的音调偏离对照表"""

# Midi乐器对MC乐器对照表

MM_CLASSIC_PITCHED_INSTRUMENT_TABLE: Dict[int, str] = {
    0: "note.harp",
    1: "note.harp",
    2: "note.pling",
    3: "note.harp",
    4: "note.pling",
    5: "note.pling",
    6: "note.harp",
    7: "note.harp",
    8: "note.snare",
    9: "note.harp",
    10: "note.didgeridoo",
    11: "note.harp",
    12: "note.xylophone",
    13: "note.chime",
    14: "note.harp",
    15: "note.harp",
    16: "note.bass",
    17: "note.harp",
    18: "note.harp",
    19: "note.harp",
    20: "note.harp",
    21: "note.harp",
    22: "note.harp",
    23: "note.guitar",
    24: "note.guitar",
    25: "note.guitar",
    26: "note.guitar",
    27: "note.guitar",
    28: "note.guitar",
    29: "note.guitar",
    30: "note.guitar",
    31: "note.bass",
    32: "note.bass",
    33: "note.bass",
    34: "note.bass",
    35: "note.bass",
    36: "note.bass",
    37: "note.bass",
    38: "note.bass",
    39: "note.bass",
    40: "note.harp",
    41: "note.harp",
    42: "note.harp",
    43: "note.harp",
    44: "note.iron_xylophone",
    45: "note.guitar",
    46: "note.harp",
    47: "note.harp",
    48: "note.guitar",
    49: "note.guitar",
    50: "note.bit",
    51: "note.bit",
    52: "note.harp",
    53: "note.harp",
    54: "note.bit",
    55: "note.flute",
    56: "note.flute",
    57: "note.flute",
    58: "note.flute",
    59: "note.flute",
    60: "note.flute",
    61: "note.flute",
    62: "note.flute",
    63: "note.flute",
    64: "note.bit",
    65: "note.bit",
    66: "note.bit",
    67: "note.bit",
    68: "note.flute",
    69: "note.harp",
    70: "note.harp",
    71: "note.flute",
    72: "note.flute",
    73: "note.flute",
    74: "note.harp",
    75: "note.flute",
    76: "note.harp",
    77: "note.harp",
    78: "note.harp",
    79: "note.harp",
    80: "note.bit",
    81: "note.bit",
    82: "note.bit",
    83: "note.bit",
    84: "note.bit",
    85: "note.bit",
    86: "note.bit",
    87: "note.bit",
    88: "note.bit",
    89: "note.bit",
    90: "note.bit",
    91: "note.bit",
    92: "note.bit",
    93: "note.bit",
    94: "note.bit",
    95: "note.bit",
    96: "note.bit",
    97: "note.bit",
    98: "note.bit",
    99: "note.bit",
    100: "note.bit",
    101: "note.bit",
    102: "note.bit",
    103: "note.bit",
    104: "note.harp",
    105: "note.banjo",
    106: "note.harp",
    107: "note.harp",
    108: "note.harp",
    109: "note.harp",
    110: "note.harp",
    111: "note.guitar",
    112: "note.harp",
    113: "note.bell",
    114: "note.harp",
    115: "note.cow_bell",
    116: "note.bd",
    117: "note.bass",
    118: "note.bit",
    119: "note.bd",
    120: "note.guitar",
    121: "note.harp",
    122: "note.harp",
    123: "note.harp",
    124: "note.harp",
    125: "note.hat",
    126: "note.bd",
    127: "note.snare",
}
"""“经典”乐音乐器对照表"""

MM_CLASSIC_PERCUSSION_INSTRUMENT_TABLE: Dict[int, str] = {
    34: "note.bd",
    35: "note.bd",
    36: "note.hat",
    37: "note.snare",
    38: "note.snare",
    39: "note.snare",
    40: "note.hat",
    41: "note.snare",
    42: "note.hat",
    43: "note.snare",
    44: "note.snare",
    45: "note.bell",
    46: "note.snare",
    47: "note.snare",
    48: "note.bell",
    49: "note.hat",
    50: "note.bell",
    51: "note.bell",
    52: "note.bell",
    53: "note.bell",
    54: "note.bell",
    55: "note.bell",
    56: "note.snare",
    57: "note.hat",
    58: "note.chime",
    59: "note.iron_xylophone",
    60: "note.bd",
    61: "note.bd",
    62: "note.xylophone",
    63: "note.xylophone",
    64: "note.xylophone",
    65: "note.hat",
    66: "note.bell",
    67: "note.bell",
    68: "note.hat",
    69: "note.hat",
    70: "note.snare",
    71: "note.flute",
    72: "note.hat",
    73: "note.hat",
    74: "note.xylophone",
    75: "note.hat",
    76: "note.hat",
    77: "note.xylophone",
    78: "note.xylophone",
    79: "note.bell",
    80: "note.bell",
}
"""“经典”打击乐器对照表"""

# 以下是由 Touch “偷吃” 带来的高准确率音色对照表
# 包括乐音乐器对照和打击乐器对照

MM_TOUCH_PITCHED_INSTRUMENT_TABLE: Dict[int, str] = {
    0: "note.harp",
    1: "note.harp",
    2: "note.pling",
    3: "note.harp",
    4: "note.pling",
    5: "note.pling",
    6: "note.guitar",
    7: "note.guitar",
    8: "note.iron_xylophone",
    9: "note.bell",
    10: "note.iron_xylophone",
    11: "note.iron_xylophone",
    12: "note.iron_xylophone",
    13: "note.xylophone",
    14: "note.chime",
    15: "note.banjo",
    16: "note.xylophone",
    17: "note.iron_xylophone",
    18: "note.flute",
    19: "note.flute",
    20: "note.flute",
    21: "note.flute",
    22: "note.flute",
    23: "note.flute",
    24: "note.guitar",
    25: "note.guitar",
    26: "note.guitar",
    27: "note.guitar",
    28: "note.guitar",
    29: "note.guitar",
    30: "note.guitar",
    31: "note.bass",
    32: "note.bass",
    33: "note.bass",
    34: "note.bass",
    35: "note.bass",
    36: "note.bass",
    37: "note.bass",
    38: "note.bass",
    39: "note.bass",
    40: "note.flute",
    41: "note.flute",
    42: "note.flute",
    43: "note.bass",
    44: "note.flute",
    45: "note.iron_xylophone",
    46: "note.harp",
    47: "note.snare",
    48: "note.flute",
    49: "note.flute",
    50: "note.flute",
    51: "note.flute",
    52: "note.didgeridoo",
    53: "note.flute",
    54: "note.flute",
    55: "mob.zombie.wood",
    56: "note.flute",
    57: "note.flute",
    58: "note.flute",
    59: "note.flute",
    60: "note.flute",
    61: "note.flute",
    62: "note.flute",
    63: "note.flute",
    64: "note.bit",
    65: "note.bit",
    66: "note.bit",
    67: "note.bit",
    68: "note.flute",
    69: "note.bit",
    70: "note.banjo",
    71: "note.flute",
    72: "note.flute",
    73: "note.flute",
    74: "note.flute",
    75: "note.flute",
    76: "note.iron_xylophone",
    77: "note.iron_xylophone",
    78: "note.flute",
    79: "note.flute",
    80: "note.bit",
    81: "note.bit",
    82: "note.flute",
    83: "note.flute",
    84: "note.guitar",
    85: "note.flute",
    86: "note.bass",
    87: "note.bass",
    88: "note.bit",
    89: "note.flute",
    90: "note.bit",
    91: "note.flute",
    92: "note.bell",
    93: "note.guitar",
    94: "note.flute",
    95: "note.bit",
    96: "note.bit",
    97: "note.flute",
    98: "note.bell",
    99: "note.bit",
    100: "note.bit",
    101: "note.bit",
    102: "note.bit",
    103: "note.bit",
    104: "note.iron_xylophone",
    105: "note.banjo",
    106: "note.harp",
    107: "note.harp",
    108: "note.bell",
    109: "note.flute",
    110: "note.flute",
    111: "note.flute",
    112: "note.bell",
    113: "note.xylophone",
    114: "note.flute",
    115: "note.hat",
    116: "note.snare",
    117: "note.snare",
    118: "note.bd",
    119: "firework.blast",
    120: "note.guitar",
    121: "note.harp",
    122: "note.harp",
    123: "note.harp",
    124: "note.bit",
    125: "note.hat",
    126: "firework.twinkle",
    127: "mob.zombie.wood",
}
"""“偷吃”乐音乐器对照表"""

MM_TOUCH_PERCUSSION_INSTRUMENT_TABLE: Dict[int, str] = {
    34: "note.hat",
    35: "note.bd",
    36: "note.bd",
    37: "note.snare",
    38: "note.snare",
    39: "fire.ignite",
    40: "note.snare",
    41: "note.hat",
    42: "note.hat",
    43: "firework.blast",
    44: "note.hat",
    45: "note.snare",
    46: "note.snare",
    47: "note.snare",
    48: "note.bell",
    49: "note.hat",
    50: "note.bell",
    51: "note.bell",
    52: "note.bell",
    53: "note.bell",
    54: "note.bell",
    55: "note.bell",
    56: "note.snare",
    57: "note.hat",
    58: "note.chime",
    59: "note.iron_xylophone",
    60: "note.bd",
    61: "note.bd",
    62: "note.xylophone",
    63: "note.xylophone",
    64: "note.xylophone",
    65: "note.hat",
    66: "note.bell",
    67: "note.bell",
    68: "note.hat",
    69: "note.hat",
    70: "note.snare",
    71: "note.flute",
    72: "note.hat",
    73: "note.hat",
    74: "note.xylophone",
    75: "note.hat",
    76: "note.hat",
    77: "note.xylophone",
    78: "note.xylophone",
    79: "note.bell",
    80: "note.bell",
}
"""“偷吃”打击乐器对照表"""

# 以下是 Dislink “断联” 的音色对照表
# 包括乐音乐器对照和打击乐器对照

MM_DISLINK_PITCHED_INSTRUMENT_TABLE: Dict[int, str] = {
    0: "note.harp",
    1: "note.harp",
    2: "note.pling",
    3: "note.harp",
    4: "note.harp",
    5: "note.harp",
    6: "note.harp",
    7: "note.harp",
    8: "note.iron_xylophone",
    9: "note.bell",
    10: "note.iron_xylophone",
    11: "note.iron_xylophone",
    12: "note.iron_xylophone",
    13: "note.iron_xylophone",
    14: "note.chime",
    15: "note.iron_xylophone",
    16: "note.harp",
    17: "note.harp",
    18: "note.harp",
    19: "note.harp",
    20: "note.harp",
    21: "note.harp",
    22: "note.harp",
    23: "note.harp",
    24: "note.guitar",
    25: "note.guitar",
    26: "note.guitar",
    27: "note.guitar",
    28: "note.guitar",
    29: "note.guitar",
    30: "note.guitar",
    31: "note.guitar",
    32: "note.bass",
    33: "note.bass",
    34: "note.bass",
    35: "note.bass",
    36: "note.bass",
    37: "note.bass",
    38: "note.bass",
    39: "note.bass",
    40: "note.harp",
    41: "note.flute",
    42: "note.flute",
    43: "note.flute",
    44: "note.flute",
    45: "note.harp",
    46: "note.harp",
    47: "note.harp",
    48: "note.harp",
    49: "note.harp",
    50: "note.harp",
    51: "note.harp",
    52: "note.harp",
    53: "note.harp",
    54: "note.harp",
    55: "note.harp",
    56: "note.harp",
    57: "note.harp",
    58: "note.harp",
    59: "note.harp",
    60: "note.harp",
    61: "note.harp",
    62: "note.harp",
    63: "note.harp",
    64: "note.harp",
    65: "note.harp",
    66: "note.harp",
    67: "note.harp",
    68: "note.harp",
    69: "note.harp",
    70: "note.harp",
    71: "note.harp",
    72: "note.flute",
    73: "note.flute",
    74: "note.flute",
    75: "note.flute",
    76: "note.flute",
    77: "note.flute",
    78: "note.flute",
    79: "note.flute",
    80: "note.bit",
    81: "note.bit",
    82: "note.harp",
    83: "note.harp",
    84: "note.harp",
    85: "note.harp",
    86: "note.harp",
    87: "note.harp",
    88: "note.harp",
    89: "note.harp",
    90: "note.harp",
    91: "note.harp",
    92: "note.harp",
    93: "note.harp",
    94: "note.harp",
    95: "note.harp",
    96: "note.harp",
    97: "note.harp",
    98: "note.harp",
    99: "note.harp",
    100: "note.harp",
    101: "note.harp",
    102: "note.harp",
    103: "note.harp",
    104: "note.harp",
    105: "note.banjo",
    106: "note.harp",
    107: "note.harp",
    108: "note.harp",
    109: "note.harp",
    110: "note.harp",
    111: "note.harp",
    112: "note.cow_bell",
    113: "note.harp",
    114: "note.harp",
    115: "note.bd",
    116: "note.bd",
    117: "note.bd",
    118: "note.bd",
    119: "note.harp",
    120: "note.harp",
    121: "note.harp",
    122: "note.harp",
    123: "note.harp",
    124: "note.harp",
    125: "note.harp",
    126: "note.harp",
    127: "note.harp",
}
"""“断联”乐音乐器对照表"""

MM_DISLINK_PERCUSSION_INSTRUMENT_TABLE: Dict[int, str] = {
    34: "note.bd",
    35: "note.bd",
    36: "note.snare",
    37: "note.snare",
    38: "note.bd",
    39: "note.snare",
    40: "note.bd",
    41: "note.hat",
    42: "note.bd",
    43: "note.hat",
    44: "note.bd",
    45: "note.hat",
    46: "note.bd",
    47: "note.bd",
    48: "note.bd",
    49: "note.bd",
    50: "note.bd",
    51: "note.bd",
    52: "note.bd",
    53: "note.bd",
    54: "note.bd",
    55: "note.cow_bell",
    56: "note.bd",
    57: "note.bd",
    58: "note.bd",
    59: "note.bd",
    60: "note.bd",
    61: "note.bd",
    62: "note.bd",
    63: "note.bd",
    64: "note.bd",
    65: "note.bd",
    66: "note.bd",
    67: "note.bd",
    68: "note.bd",
    69: "note.bd",
    70: "note.bd",
    71: "note.bd",
    72: "note.bd",
    73: "note.bd",
    74: "note.bd",
    75: "note.bd",
    76: "note.bd",
    77: "note.bd",
    78: "note.bd",
    79: "note.bd",
    80: "note.bd",
}
"""“断联”打击乐器对照表"""


# 即将启用
# height2note = {
#     0.5: 0,
#     0.53: 1,
#     0.56: 2,
#     0.6: 3,
#     0.63: 4,
#     0.67: 5,
#     0.7: 6,
#     0.75: 7,
#     0.8: 8,
#     0.84: 9,
#     0.9: 10,
#     0.94: 11,
#     1.0: 12,
#     1.05: 13,
#     1.12: 14,
#     1.2: 15,
#     1.25: 16,
#     1.33: 17,
#     1.4: 18,
#     1.5: 19,
#     1.6: 20,
#     1.7: 21,
#     1.8: 22,
#     1.9: 23,
#     2.0: 24,
# }
# """音高对照表\n
# MC音高:音符盒音调"""
