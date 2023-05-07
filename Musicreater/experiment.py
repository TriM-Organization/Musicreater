'''
新版本功能以及即将启用的函数
'''



from .exceptions import *
from .subclass import *
from .utils import *
from .main import midiConvert, mido


# 简单的单音填充
def _toCmdList_m4(
    self: midiConvert,
    scoreboard_name: str = "mscplay",
    MaxVolume: float = 1.0,
    speed: float = 1.0,
) -> list:
    """
    使用金羿的转换思路，将midi转换为我的世界命令列表，并使用完全填充算法优化音感
    :param scoreboard_name: 我的世界的计分板名称
    :param MaxVolume: 音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
    :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
    :return: tuple(命令列表, 命令个数, 计分板最大值)
    """
    # TODO: 这里的时间转换不知道有没有问题

    if speed == 0:
        if self.debug_mode:
            raise ZeroSpeedError("播放速度仅可为正实数")
        speed = 1
    MaxVolume = 1 if MaxVolume > 1 else (0.001 if MaxVolume <= 0 else MaxVolume)

    # 一个midi中仅有16个通道 我们通过通道来识别而不是音轨
    channels = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

    # 我们来用通道统计音乐信息
    for i, track in enumerate(self.midi.tracks):
        microseconds = 0

        for msg in track:
            if msg.time != 0:
                try:
                    microseconds += msg.time * tempo / self.midi.ticks_per_beat
                except NameError:
                    raise NotDefineTempoError("计算当前分数时出错 未定义参量 Tempo")

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
                    channels[msg.channel].append(
                        ("PgmC", msg.program, microseconds)
                    )

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

    note_channels = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

    # 此处 我们把通道视为音轨
    for i in range(len(channels)):
        # 如果当前通道为空 则跳过

        noteMsgs = []
        MsgIndex = []

        for msg in channels[i]:
            if msg[0] == "PgmC":
                InstID = msg[1]

            elif msg[0] == "NoteS":
                noteMsgs.append(msg[1:])
                MsgIndex.append(msg[1])

            elif msg[0] == "NoteE":
                if msg[1] in MsgIndex:
                    note_channels[i].append(
                        SingleNote(
                            InstID,
                            msg[1],
                            noteMsgs[MsgIndex.index(msg[1])][1],
                            noteMsgs[MsgIndex.index(msg[1])][2],
                            msg[-1] - noteMsgs[MsgIndex.index(msg[1])][2],
                        )
                    )
                    noteMsgs.pop(MsgIndex.index(msg[1]))
                    MsgIndex.pop(MsgIndex.index(msg[1]))

    tracks = []
    cmdAmount = 0
    maxScore = 0
    CheckFirstChannel = False

    # 临时用的插值计算函数
    def _linearFun(_note: SingleNote) -> list:
        """传入音符数据，返回以半秒为分割的插值列表
        :param _note: SingleNote 音符
        :return list[tuple(int开始时间（毫秒）, int乐器, int音符, int力度（内置）, float音量（播放）),]"""

        result = []

        totalCount = int(_note.lastTime / 500)

        for _i in range(totalCount):
            result.append(
                (
                    _note.startTime + _i * 500,
                    _note.instrument,
                    _note.pitch,
                    _note.velocity,
                    MaxVolume * ((totalCount - _i) / totalCount),
                )
            )

        return result

    # 此处 我们把通道视为音轨
    for track in note_channels:
        # 如果当前通道为空 则跳过
        if not track:
            continue

        if note_channels.index(track) == 0:
            CheckFirstChannel = True
            SpecialBits = False
        elif note_channels.index(track) == 9:
            SpecialBits = True
        else:
            CheckFirstChannel = False
            SpecialBits = False

        nowTrack = []

        for note in track:
            for every_note in _linearFun(note):
                # 应该是计算的时候出了点小问题
                # 我们应该用一个MC帧作为时间单位而不是半秒

                if SpecialBits:
                    soundID, _X = self.perc_inst_to_soundID_withX(InstID)
                else:
                    soundID, _X = self.inst_to_souldID_withX(InstID)

                score_now = round(every_note[0] / speed / 50000)

                maxScore = max(maxScore, score_now)

                nowTrack.append(
                    "execute @a[scores={"
                    + str(scoreboard_name)
                    + "="
                    + str(score_now)
                    + "}"
                    + f"] ~ ~ ~ playsound {soundID} @s ~ ~{1 / every_note[4] - 1} ~ "
                    f"{note.velocity * (0.7 if CheckFirstChannel else 0.9)} {2 ** ((note.pitch - 60 - _X) / 12)}"
                )

                cmdAmount += 1
        tracks.append(nowTrack)

    return [tracks, cmdAmount, maxScore]



def to_note_list(
    self,
    speed: float = 1.0,
) -> list:
    """
    使用金羿的转换思路，将midi转换为我的世界音符盒所用的音高列表，并输出每个音符之后的延迟

    Parameters
    ----------
    speed: float
        速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed

    Returns
    -------
    tuple( list[tuple(str指令, int距离上一个指令的延迟 ),...], int音乐时长游戏刻 )
    """

    if speed == 0:
        if self.debug_mode:
            raise ZeroSpeedError("播放速度仅可为正实数")
        speed = 1

    # 一个midi中仅有16个通道 我们通过通道来识别而不是音轨
    channels = empty_midi_channels()

    # 我们来用通道统计音乐信息
    # 但是是用分轨的思路的
    for track_no, track in enumerate(self.midi.tracks):
        microseconds = 0

        for msg in track:
            if msg.time != 0:
                try:
                    microseconds += (
                        msg.time * tempo / self.midi.ticks_per_beat / 1000
                    )
                    # print(microseconds)
                except NameError:
                    if self.debug_mode:
                        raise NotDefineTempoError("计算当前分数时出错 未定义参量 Tempo")
                    else:
                        microseconds += (
                            msg.time
                            * mido.midifiles.midifiles.DEFAULT_TEMPO
                            / self.midi.ticks_per_beat
                        ) / 1000

            if msg.is_meta:
                if msg.type == "set_tempo":
                    tempo = msg.tempo
                    if self.debug_mode:
                        self.prt(f"TEMPO更改：{tempo}（毫秒每拍）")
            else:
                try:
                    if msg.channel > 15 and self.debug_mode:
                        raise ChannelOverFlowError(f"当前消息 {msg} 的通道超限(≤15)")
                    if not track_no in channels[msg.channel].keys():
                        channels[msg.channel][track_no] = []
                except AttributeError:
                    pass

                if msg.type == "program_change":
                    channels[msg.channel][track_no].append(
                        ("PgmC", msg.program, microseconds)
                    )

                elif msg.type == "note_on" and msg.velocity != 0:
                    channels[msg.channel][track_no].append(
                        ("NoteS", msg.note, msg.velocity, microseconds)
                    )

                elif (msg.type == "note_on" and msg.velocity == 0) or (
                    msg.type == "note_off"
                ):
                    channels[msg.channel][track_no].append(
                        ("NoteE", msg.note, microseconds)
                    )

    """整合后的音乐通道格式
    每个通道包括若干消息元素其中逃不过这三种：

    1 切换乐器消息
    ("PgmC", 切换后的乐器ID: int, 距离演奏开始的毫秒)

    2 音符开始消息
    ("NoteS", 开始的音符ID, 力度（响度）, 距离演奏开始的毫秒)

    3 音符结束消息
    ("NoteS", 结束的音符ID, 距离演奏开始的毫秒)"""

    tracks = {}

    # 此处 我们把通道视为音轨
    for i in channels.keys():
        # 如果当前通道为空 则跳过
        if not channels[i]:
            continue

        # 第十通道是打击乐通道
        SpecialBits = True if i == 9 else False

        # nowChannel = []

        for track_no, track in channels[i].items():
            for msg in track:
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
                    # print(score_now)

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
    results = []

    for i in range(len(all_ticks)):
        for j in range(len(tracks[all_ticks[i]])):
            results.append(
                (
                    tracks[all_ticks[i]][j],
                    (
                        0
                        if j != 0
                        else (
                            all_ticks[i] - all_ticks[i - 1]
                            if i != 0
                            else all_ticks[i]
                        )
                    ),
                )
            )

    return [results, max(all_ticks)]