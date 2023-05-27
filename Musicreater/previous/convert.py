# -*- coding: utf-8 -*-
"""
旧版本转换功能以及已经弃用的函数
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


from ..exceptions import *
from ..main import MidiConvert


def to_command_list_method1(
    self: MidiConvert,
    scoreboard_name: str = "mscplay",
    MaxVolume: float = 1.0,
    speed: float = 1.0,
) -> list:
    """
    使用Dislink Sforza的转换思路，将midi转换为我的世界命令列表
    :param scoreboard_name: 我的世界的计分板名称
    :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
    :return: tuple(命令列表, 命令个数, 计分板最大值)
    """
    # :param volume: 音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
    tracks = []
    if speed == 0:
        if self.debug_mode:
            raise ZeroSpeedError("播放速度仅可为正实数")
        speed = 1
    MaxVolume = 1 if MaxVolume > 1 else (0.001 if MaxVolume <= 0 else MaxVolume)

    commands = 0
    maxscore = 0

    # 分轨的思路其实并不好，但这个算法就是这样
    # 所以我建议用第二个方法 _toCmdList_m2
    for i, track in enumerate(self.midi.tracks):
        ticks = 0
        instrumentID = 0
        singleTrack = []

        for msg in track:
            ticks += msg.time
            if msg.is_meta:
                if msg.type == "set_tempo":
                    tempo = msg.tempo
            else:
                if msg.type == "program_change":
                    instrumentID = msg.program

                if msg.type == "note_on" and msg.velocity != 0:
                    try:
                        nowscore = round(
                            (ticks * tempo)
                            / ((self.midi.ticks_per_beat * float(speed)) * 50000)
                        )
                    except NameError:
                        raise NotDefineTempoError("计算当前分数时出错 未定义参量 Tempo")
                    maxscore = max(maxscore, nowscore)
                    if msg.channel == 9:
                        soundID, _X = self.perc_inst_to_soundID_withX(instrumentID)
                    else:
                        soundID, _X = self.inst_to_souldID_withX(instrumentID)

                    singleTrack.append(
                        "execute @a[scores={"
                        + str(scoreboard_name)
                        + "="
                        + str(nowscore)
                        + "}"
                        + f"] ~ ~ ~ playsound {soundID} @s ^ ^ ^{1 / MaxVolume - 1} {msg.velocity / 128} "
                        f"{2 ** ((msg.note - 60 - _X) / 12)}"
                    )
                    commands += 1
        if len(singleTrack) != 0:
            tracks.append(singleTrack)

    return [tracks, commands, maxscore]


# 原本这个算法的转换效果应该和上面的算法相似的
def _toCmdList_m2(
    self: MidiConvert,
    scoreboard_name: str = "mscplay",
    MaxVolume: float = 1.0,
    speed: float = 1.0,
) -> list:
    """
    使用神羽和金羿的转换思路，将midi转换为我的世界命令列表
    :param scoreboard_name: 我的世界的计分板名称
    :param MaxVolume: 音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
    :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
    :return: tuple(命令列表, 命令个数, 计分板最大值)
    """

    if speed == 0:
        if self.debug_mode:
            raise ZeroSpeedError("播放速度仅可为正实数")
        speed = 1
    MaxVolume = 1 if MaxVolume > 1 else (0.001 if MaxVolume <= 0 else MaxVolume)

    # 一个midi中仅有16个通道 我们通过通道来识别而不是音轨
    channels = {
        0: [],
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [],
        8: [],
        9: [],
        10: [],
        11: [],
        12: [],
        13: [],
        14: [],
        15: [],
        16: [],
    }

    microseconds = 0

    # 我们来用通道统计音乐信息
    for msg in self.midi:
        microseconds += msg.time * 1000  # 任何人都tm不要动这里，这里循环方式不是track，所以，这里的计时方式不一样
        if not msg.is_meta:
            if self.debug_mode:
                try:
                    if msg.channel > 15:
                        raise ChannelOverFlowError(f"当前消息 {msg} 的通道超限(≤15)")
                except AttributeError:
                    pass

            if msg.type == "program_change":
                channels[msg.channel].append(("PgmC", msg.program, microseconds))

            elif msg.type == "note_on" and msg.velocity != 0:
                channels[msg.channel].append(
                    ("NoteS", msg.note, msg.velocity, microseconds)
                )

            elif (msg.type == "note_on" and msg.velocity == 0) or (
                msg.type == "note_off"
            ):
                channels[msg.channel].append(("NoteE", msg.note, microseconds))

    """整合后的音乐通道格式
    每个通道包括若干消息元素其中逃不过这三种：

    1 切换乐器消息
    ("PgmC", 切换后的乐器ID: int, 距离演奏开始的毫秒)

    2 音符开始消息
    ("NoteS", 开始的音符ID, 力度（响度）, 距离演奏开始的毫秒)

    3 音符结束消息
    ("NoteS", 结束的音符ID, 距离演奏开始的毫秒)"""

    tracks = []
    cmdAmount = 0
    maxScore = 0

    # 此处 我们把通道视为音轨
    for i in channels.keys():
        # 如果当前通道为空 则跳过
        if not channels[i]:
            continue

        if i == 9:
            SpecialBits = True
        else:
            SpecialBits = False

        nowTrack = []

        for msg in channels[i]:
            if msg[0] == "PgmC":
                InstID = msg[1]

            elif msg[0] == "NoteS":
                try:
                    soundID, _X = (
                        self.perc_inst_to_soundID_withX(InstID)
                        if SpecialBits
                        else self.inst_to_souldID_withX(InstID)
                    )
                except UnboundLocalError as E:
                    if self.debug_mode:
                        raise NotDefineProgramError(f"未定义乐器便提前演奏。\n{E}")
                    else:
                        soundID, _X = (
                            self.perc_inst_to_soundID_withX(-1)
                            if SpecialBits
                            else self.inst_to_souldID_withX(-1)
                        )
                score_now = round(msg[-1] / float(speed) / 50)
                maxScore = max(maxScore, score_now)

                nowTrack.append(
                    self.execute_cmd_head.format(
                        "@a[scores=({}={})]".format(scoreboard_name, score_now)
                        .replace("(", r"{")
                        .replace(")", r"}")
                    )
                    + f"playsound {soundID} @s ^ ^ ^{1 / MaxVolume - 1} {msg[2] / 128} "
                    f"{2 ** ((msg[1] - 60 - _X) / 12)}"
                )

                cmdAmount += 1

        if nowTrack:
            tracks.append(nowTrack)

    return [tracks, cmdAmount, maxScore]


def _toCmdList_withDelay_m1(
    self: MidiConvert,
    MaxVolume: float = 1.0,
    speed: float = 1.0,
    player: str = "@a",
) -> list:
    """
    使用Dislink Sforza的转换思路，将midi转换为我的世界命令列表，并输出每个音符之后的延迟
    :param MaxVolume: 最大播放音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
    :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
    :param player: 玩家选择器，默认为`@a`
    :return: 全部指令列表[ ( str指令, int距离上一个指令的延迟 ),...]
    """
    tracks = {}

    if speed == 0:
        if self.debug_mode:
            raise ZeroSpeedError("播放速度仅可为正实数")
        speed = 1

    MaxVolume = 1 if MaxVolume > 1 else (0.001 if MaxVolume <= 0 else MaxVolume)

    for i, track in enumerate(self.midi.tracks):
        instrumentID = 0
        ticks = 0

        for msg in track:
            ticks += msg.time
            if msg.is_meta:
                if msg.type == "set_tempo":
                    tempo = msg.tempo
            else:
                if msg.type == "program_change":
                    instrumentID = msg.program
                if msg.type == "note_on" and msg.velocity != 0:
                    now_tick = round(
                        (ticks * tempo)
                        / ((self.midi.ticks_per_beat * float(speed)) * 50000)
                    )
                    soundID, _X = self.inst_to_souldID_withX(instrumentID)
                    try:
                        tracks[now_tick].append(
                            self.execute_cmd_head.format(player)
                            + f"playsound {soundID} @s ^ ^ ^{1 / MaxVolume - 1} {msg.velocity / 128} "
                            f"{2 ** ((msg.note - 60 - _X) / 12)}"
                        )
                    except KeyError:
                        tracks[now_tick] = [
                            self.execute_cmd_head.format(player)
                            + f"playsound {soundID} @s ^ ^ ^{1 / MaxVolume - 1} {msg.velocity / 128} "
                            f"{2 ** ((msg.note - 60 - _X) / 12)}"
                        ]

    results = []

    all_ticks = list(tracks.keys())
    all_ticks.sort()

    for i in range(len(all_ticks)):
        if i != 0:
            for j in range(len(tracks[all_ticks[i]])):
                if j != 0:
                    results.append((tracks[all_ticks[i]][j], 0))
                else:
                    results.append(
                        (tracks[all_ticks[i]][j], all_ticks[i] - all_ticks[i - 1])
                    )
        else:
            for j in range(len(tracks[all_ticks[i]])):
                results.append((tracks[all_ticks[i]][j], all_ticks[i]))

    return [results, max(all_ticks)]


def _toCmdList_withDelay_m2(
    self: MidiConvert,
    MaxVolume: float = 1.0,
    speed: float = 1.0,
    player: str = "@a",
) -> list:
    """
    使用神羽和金羿的转换思路，将midi转换为我的世界命令列表，并输出每个音符之后的延迟
    :param MaxVolume: 最大播放音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
    :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
    :param player: 玩家选择器，默认为`@a`
    :return: 全部指令列表[ ( str指令, int距离上一个指令的延迟 ),...]
    """
    tracks = {}
    if speed == 0:
        if self.debug_mode:
            raise ZeroSpeedError("播放速度仅可为正实数")
        speed = 1

    MaxVolume = 1 if MaxVolume > 1 else (0.001 if MaxVolume <= 0 else MaxVolume)

    # 一个midi中仅有16个通道 我们通过通道来识别而不是音轨
    channels = {
        0: [],
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [],
        8: [],
        9: [],
        10: [],
        11: [],
        12: [],
        13: [],
        14: [],
        15: [],
        16: [],
    }

    microseconds = 0

    # 我们来用通道统计音乐信息
    for msg in self.midi:
        try:
            microseconds += msg.time * 1000  # 任何人都tm不要动这里，这里循环方式不是track，所以，这里的计时方式不一样

            # print(microseconds)
        except NameError:
            if self.debug_mode:
                raise NotDefineTempoError("计算当前分数时出错 未定义参量 Tempo")
            else:
                microseconds += (
                    msg.time * 1000
                )  # 任何人都tm不要动这里，这里循环方式不是track，所以，这里的计时方式不一样

        if msg.is_meta:
            if msg.type == "set_tempo":
                tempo = msg.tempo
        else:
            if self.debug_mode:
                try:
                    if msg.channel > 15:
                        raise ChannelOverFlowError(f"当前消息 {msg} 的通道超限(≤15)")
                except AttributeError:
                    pass

            if msg.type == "program_change":
                channels[msg.channel].append(("PgmC", msg.program, microseconds))

            elif msg.type == "note_on" and msg.velocity != 0:
                channels[msg.channel].append(
                    ("NoteS", msg.note, msg.velocity, microseconds)
                )

            elif (msg.type == "note_on" and msg.velocity == 0) or (
                msg.type == "note_off"
            ):
                channels[msg.channel].append(("NoteE", msg.note, microseconds))

    """整合后的音乐通道格式
    每个通道包括若干消息元素其中逃不过这三种：

    1 切换乐器消息
    ("PgmC", 切换后的乐器ID: int, 距离演奏开始的毫秒)

    2 音符开始消息
    ("NoteS", 开始的音符ID, 力度（响度）, 距离演奏开始的毫秒)

    3 音符结束消息
    ("NoteS", 结束的音符ID, 距离演奏开始的毫秒)"""

    results = []

    for i in channels.keys():
        # 如果当前通道为空 则跳过
        if not channels[i]:
            continue

        if i == 9:
            SpecialBits = True
        else:
            SpecialBits = False

        for msg in channels[i]:
            if msg[0] == "PgmC":
                InstID = msg[1]

            elif msg[0] == "NoteS":
                try:
                    soundID, _X = (
                        self.perc_inst_to_soundID_withX(InstID)
                        if SpecialBits
                        else self.inst_to_souldID_withX(InstID)
                    )
                except UnboundLocalError as E:
                    if self.debug_mode:
                        raise NotDefineProgramError(f"未定义乐器便提前演奏。\n{E}")
                    else:
                        soundID, _X = (
                            self.perc_inst_to_soundID_withX(-1)
                            if SpecialBits
                            else self.inst_to_souldID_withX(-1)
                        )
                score_now = round(msg[-1] / float(speed) / 50)

                try:
                    tracks[score_now].append(
                        self.execute_cmd_head.format(player)
                        + f"playsound {soundID} @s ^ ^ ^{1 / MaxVolume - 1} {msg[2] / 128} "
                        f"{2 ** ((msg[1] - 60 - _X) / 12)}"
                    )
                except KeyError:
                    tracks[score_now] = [
                        self.execute_cmd_head.format(player)
                        + f"playsound {soundID} @s ^ ^ ^{1 / MaxVolume - 1} {msg[2] / 128} "
                        f"{2 ** ((msg[1] - 60 - _X) / 12)}"
                    ]

    all_ticks = list(tracks.keys())
    all_ticks.sort()

    for i in range(len(all_ticks)):
        for j in range(len(tracks[all_ticks[i]])):
            results.append(
                (
                    tracks[all_ticks[i]][j],
                    (
                        0
                        if j != 0
                        else (
                            all_ticks[i] - all_ticks[i - 1] if i != 0 else all_ticks[i]
                        )
                    ),
                )
            )

    return [results, max(all_ticks)]
