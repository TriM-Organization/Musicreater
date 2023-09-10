# -*- coding: utf-8 -*-
"""
新版本功能以及即将启用的函数
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

import random
from typing import Dict, List, Tuple, Union

from .constants import INSTRUMENT_BLOCKS_TABLE
from .exceptions import *
from .main import MidiConvert
from .subclass import *
from .utils import *


class FutureMidiConvertRSNB(MidiConvert):
    """
    加入红石音乐适配
    """

    music_command_list: Dict[int, SingleNoteBox]
    """音乐指令列表"""

    @staticmethod
    def soundID_to_block(sound_id: str, random_select: bool = False) -> str:
        """
        将我的世界乐器名改作音符盒所需的对应方块名称

        Parameters
        ----------
        sound_id: str
            将我的世界乐器名
        random_select: bool
            是否随机选取对应方块

        Returns
        -------
        str方块名称
        """
        try:
            if random_select:
                return random.choice(INSTRUMENT_BLOCKS_TABLE[sound_id])
            else:
                return INSTRUMENT_BLOCKS_TABLE[sound_id][0]
        except KeyError:
            return "air"

    def to_note_list_in_delay(
        self,
    ) -> Tuple[Dict[int, SingleNoteBox], int]:
        """
        使用金羿的转换思路，将midi转换为我的世界音符盒音高、乐器及延迟列表，并输出每个音符之后的延迟

        Returns
        -------
        tuple( Dict[int, SingleNoteBox], int音乐时长游戏刻 )
        """

        self.to_music_channels()

        tracks = {}
        note_range = {}
        InstID = -1
        # cmd_amount = 0

        # 此处 我们把通道视为音轨
        for i in self.channels.keys():
            # 如果当前通道为空 则跳过
            if not self.channels[i]:
                continue

            # 第十通道是打击乐通道
            SpecialBits = True if i == 9 else False

            for track_no, track in self.channels[i].items():
                for msg in track:
                    if msg[0] == "PgmC":
                        InstID = msg[1]

                    elif msg[0] == "NoteS":
                        # block_id = self.soundID_to_block((
                        #     self.perc_inst_to_soundID_withX(msg[1])
                        #     if SpecialBits
                        #     else self.inst_to_souldID_withX(InstID)
                        # )[0])

                        # delaytime_now = round(msg[-1] / 50)

                        note_ = 2 ** ((msg[1] - 60) / 12)

                        try:
                            tracks[msg[-1]].append(
                                (
                                    InstID,
                                    note_,
                                )
                            )
                        except KeyError:
                            tracks[msg[-1]] = [(InstID, note_)]

                        try:
                            note_range[InstID]["max"] = max(
                                note_range[InstID]["max"], note_
                            )
                            note_range[InstID]["min"] = min(
                                note_range[InstID]["min"], note_
                            )
                        except KeyError:
                            note_range[InstID] = {"max": note_, "min": note_}

        del InstID
        all_ticks = list(tracks.keys())
        all_ticks.sort()
        results = []
        print(note_range)

        exit()

        for i in range(len(all_ticks)):
            for j in range(len(tracks[all_ticks[i]])):
                results.append(
                    SingleCommand(
                        tracks[all_ticks[i]][j],
                        tick_delay=(
                            0
                            if j != 0
                            else (
                                all_ticks[i] - all_ticks[i - 1]
                                if i != 0
                                else all_ticks[i]
                            )
                        ),
                        annotation="在{}播放{}%的{}音".format(
                            mctick2timestr(i), max_volume * 100, ""
                        ),
                    )
                )

        self.music_command_list = results
        self.music_tick_num = max(all_ticks)
        return results, self.music_tick_num


class FutureMidiConvertM4(MidiConvert):
    """
    加入插值算法优化音感
    : 经测试，生成效果已经达到，感觉良好
    """

    # 临时用的插值计算函数
    @staticmethod
    def _linear_note(
        _note: SingleNote,
        _apply_time_division: int = 100,
    ) -> List[Tuple[int, int, int, int, float],]:
        """传入音符数据，返回以半秒为分割的插值列表
        :param _note: SingleNote 音符
        :return list[tuple(int开始时间（毫秒）, int乐器, int音符, int力度（内置）, float音量（播放）),]"""

        totalCount = int(_note.duration / _apply_time_division)
        
        if totalCount == 0:
            return [
                (_note.start_time, _note.inst, _note.pitch, _note.velocity, 1),
            ]
        # print(totalCount)

        result: List[Tuple[int, int, int, int, float],] = []

        for _i in range(totalCount):
            result.append(
                (
                    _note.start_time + _i * _apply_time_division,
                    _note.instrument,
                    _note.pitch,
                    _note.velocity,
                    ((totalCount - _i) / totalCount),
                )
            )

        return result

    # 简单的单音填充
    def to_command_list_in_score(
        self,
        scoreboard_name: str = "mscplay",
        max_volume: float = 1.0,
        speed: float = 1.0,
    ) -> Tuple[List[List[SingleCommand]], int, int]:
        """
        使用金羿的转换思路，使用完全填充算法优化音感后，将midi转换为我的世界命令列表

        Parameters
        ----------
        scoreboard_name: str
            我的世界的计分板名称
        max_volume: float
            最大播放音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放
        speed: float
            速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed

        Returns
        -------
        tuple( list[list[SingleCommand指令,... ],... ], int指令数量, int音乐时长游戏刻 )
        """

        if speed == 0:
            raise ZeroSpeedError("播放速度仅可为正实数")
        max_volume = 1 if max_volume > 1 else (0.001 if max_volume <= 0 else max_volume)

        self.to_music_channels()

        note_channels: Dict[int, List[SingleNote]] = empty_midi_channels(staff=[])
        InstID = -1

        # 此处 我们把通道视为音轨
        for i in self.channels.keys():
            # 如果当前通道为空 则跳过
            if not self.channels[i]:
                continue

            # nowChannel = []
            for track_no, track in self.channels[i].items():
                noteMsgs = []
                MsgIndex = []

                for msg in track:
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
                                    track_number=track_no,
                                )
                            )
                            noteMsgs.pop(MsgIndex.index(msg[1]))
                            MsgIndex.pop(MsgIndex.index(msg[1]))

        del InstID

        tracks = []
        cmd_amount = 0
        max_score = 0

        # 此处 我们把通道视为音轨
        for no, track in note_channels.items():
            # 如果当前通道为空 则跳过
            if not track:
                continue

            SpecialBits = True if no == 9 else False

            track_now = []

            for note in track:
                for every_note in self._linear_note(
                    note, 100 if note.track_no == 0 else 500
                ):
                    soundID, _X = (
                        self.perc_inst_to_soundID_withX(note.pitch)
                        if SpecialBits
                        else self.inst_to_souldID_withX(note.inst)
                    )

                    score_now = round(every_note[0] / speed / 50)

                    max_score = max(max_score, score_now)
                    mc_pitch = 2 ** ((note.pitch - 60 - _X) / 12)
                    blockmeter = (
                        1
                        / (1 if note.track_no == 0 else 0.9)
                        / max_volume
                        / every_note[4]
                        - 1
                    )

                    track_now.append(
                        SingleCommand(
                            self.execute_cmd_head.format(
                                "@a[scores=({}={})]".format(scoreboard_name, score_now)
                                .replace("(", r"{")
                                .replace(")", r"}")
                            )
                            + "playsound {} @s ^ ^ ^{} {} {}".format(
                                soundID,
                                blockmeter,
                                note.velocity / 128,
                                "" if SpecialBits else mc_pitch,
                            ),
                            annotation="在{}播放{}%({}BM)的{}音".format(
                                mctick2timestr(score_now),
                                max_volume * 100,
                                blockmeter,
                                "{}:{}".format(soundID, note.pitch),
                            ),
                        ),
                    )

                    cmd_amount += 1

            if track_now:
                self.music_command_list.extend(track_now)
                tracks.append(track_now)

        self.music_tick_num = max_score
        return (tracks, cmd_amount, max_score)

    # 简单的单音填充的延迟应用
    def to_command_list_in_delay(
        self,
        max_volume: float = 1.0,
        speed: float = 1.0,
        player_selector: str = "@a",
    ) -> Tuple[List[SingleCommand], int, int]:
        """
        使用金羿的转换思路，使用完全填充算法优化音感后，将midi转换为我的世界命令列表，并输出每个音符之后的延迟

        Parameters
        ----------
        max_volume: float
            最大播放音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
        speed: float
            速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
        player_selector: str
            玩家选择器，默认为`@a`

        Returns
        -------
        tuple( list[SingleCommand,...], int音乐时长游戏刻, int最大同时播放的指令数量 )
        """

        if speed == 0:
            raise ZeroSpeedError("播放速度仅可为正实数")
        max_volume = 1 if max_volume > 1 else (0.001 if max_volume <= 0 else max_volume)

        self.to_music_channels()

        note_channels: Dict[int, List[SingleNote]] = empty_midi_channels(staff=[])
        InstID = -1

        # 此处 我们把通道视为音轨
        for i in self.channels.keys():
            # 如果当前通道为空 则跳过
            if not self.channels[i]:
                continue

            # nowChannel = []
            for track_no, track in self.channels[i].items():
                noteMsgs = []
                MsgIndex = []

                for msg in track:
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
                                    track_number=track_no,
                                )
                            )
                            noteMsgs.pop(MsgIndex.index(msg[1]))
                            MsgIndex.pop(MsgIndex.index(msg[1]))

        del InstID

        tracks = {}
        InstID = -1
        # open("RES.TXT", "w", encoding="utf-8").write(str(note_channels))

        # 此处 我们把通道视为音轨
        for no, track in note_channels.items():
            # 如果当前通道为空 则跳过
            if not track:
                continue

            SpecialBits = True if no == 9 else False

            for note in track:
                liner_list = self._linear_note(
                    note, 100 if note.track_no == 0 else 500
                )
                for every_note in liner_list:
                    soundID, _X = (
                        self.perc_inst_to_soundID_withX(note.pitch)
                        if SpecialBits
                        else self.inst_to_souldID_withX(note.inst)
                    )

                    score_now = round(every_note[0] / speed / 50)

                    try:
                        tracks[score_now].append(
                            self.execute_cmd_head.format(player_selector)
                            + f"playsound {soundID} @s ^ ^ ^{1 / (1 if note.track_no == 0 else 0.9) / max_volume / every_note[4] - 1} {note.velocity / 128} "
                            + (
                                ""
                                if SpecialBits
                                else f"{2 ** ((note.pitch - 60 - _X) / 12)}"
                            )
                        )
                    except KeyError:
                        tracks[score_now] = [
                            self.execute_cmd_head.format(player_selector)
                            + f"playsound {soundID} @s ^ ^ ^{1 / (1 if note.track_no == 0 else 0.9) / max_volume / every_note[4] - 1} {note.velocity / 128} "
                            + (
                                ""
                                if SpecialBits
                                else f"{2 ** ((note.pitch - 60 - _X) / 12)}"
                            )
                        ]

        all_ticks = list(tracks.keys())
        all_ticks.sort()
        results:List[SingleCommand] = []
        max_multi = 0
        now_multi_delay = 0
        now_multi = 0

        for i in range(len(all_ticks)):
            l = len(tracks[all_ticks[i]])
            for j in range(l):
                results.append(
                    SingleCommand(
                        tracks[all_ticks[i]][j],
                        tick_delay=(
                            0
                            if j != 0
                            else (
                                all_ticks[i] - all_ticks[i - 1]
                                if i != 0
                                else all_ticks[i]
                            )
                        ),
                        annotation="由 音·创 生成",
                    )
                )
                if results[-1].delay + now_multi_delay <= 1:
                    now_multi += 1
                    now_multi_delay += results[-1].delay
                else:
                    max_multi = max(max_multi, now_multi)
                    now_multi = 0
                    now_multi_delay = 0

        self.music_command_list = results
        self.music_tick_num = max(all_ticks)
        return results, self.music_tick_num, max_multi


class FutureMidiConvertM5(MidiConvert):
    """
    加入同刻偏移算法优化音感
    """

    # 神奇的偏移音
    def to_command_list_in_delay(
        self,
        max_volume: float = 1.0,
        speed: float = 1.0,
        player_selector: str = "@a",
    ) -> Tuple[List[SingleCommand], int]:
        """
        使用金羿的转换思路，使用同刻偏移算法优化音感后，将midi转换为我的世界命令列表，并输出每个音符之后的延迟

        Parameters
        ----------
        max_volume: float
            最大播放音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
        speed: float
            速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
        player_selector: str
            玩家选择器，默认为`@a`

        Returns
        -------
        tuple( list[SingleCommand,...], int音乐时长游戏刻 )
        """

        if speed == 0:
            raise ZeroSpeedError("播放速度仅可为正实数")
        max_volume = 1 if max_volume > 1 else (0.001 if max_volume <= 0 else max_volume)

        self.to_music_channels()

        tracks = {}
        InstID = -1

        # 此处 我们把通道视为音轨
        for i in self.channels.keys():
            # 如果当前通道为空 则跳过
            if not self.channels[i]:
                continue

            # 第十通道是打击乐通道
            SpecialBits = True if i == 9 else False

            # nowChannel = []

            for track_no, track in self.channels[i].items():
                for msg in track:
                    if msg[0] == "PgmC":
                        InstID = msg[1]

                    elif msg[0] == "NoteS":
                        soundID, _X = (
                            self.perc_inst_to_soundID_withX(msg[1])
                            if SpecialBits
                            else self.inst_to_souldID_withX(InstID)
                        )

                        score_now = round(msg[-1] / float(speed) / 50)
                        # print(score_now)

                        try:
                            tracks[score_now].append(
                                self.execute_cmd_head.format(player_selector)
                                + f"playsound {soundID} @s ^ ^ ^{128 / max_volume / msg[2] - 1} {msg[2] / 128} "
                                + (
                                    ""
                                    if SpecialBits
                                    else f"{2 ** ((msg[1] - 60 - _X) / 12)}"
                                )
                            )
                        except KeyError:
                            tracks[score_now] = [
                                self.execute_cmd_head.format(player_selector)
                                + f"playsound {soundID} @s ^ ^ ^{128 / max_volume / msg[2] - 1} {msg[2] / 128} "
                                + (
                                    ""
                                    if SpecialBits
                                    else f"{2 ** ((msg[1] - 60 - _X) / 12)}"
                                )
                            ]

        all_ticks = list(tracks.keys())
        all_ticks.sort()
        results = []

        for i in range(len(all_ticks)):
            for j in range(len(tracks[all_ticks[i]])):
                results.append(
                    SingleCommand(
                        tracks[all_ticks[i]][j],
                        tick_delay=(
                            (
                                0
                                if (
                                    (all_ticks[i + 1] - all_ticks[i])
                                    / len(tracks[all_ticks[i]])
                                    < 1
                                )
                                else 1
                            )
                            if j != 0
                            else (
                                (
                                    all_ticks[i]
                                    - all_ticks[i - 1]
                                    - (
                                        0
                                        if (
                                            (all_ticks[i] - all_ticks[i - 1])
                                            / len(tracks[all_ticks[i - 1]])
                                            < 1
                                        )
                                        else (len(tracks[all_ticks[i - 1]]) - 1)
                                    )
                                )
                                if i != 0
                                else all_ticks[i]
                            )
                        ),
                        annotation="在{}播放{}%的{}音".format(
                            mctick2timestr(
                                i + 0
                                if (
                                    (all_ticks[i + 1] - all_ticks[i])
                                    / len(tracks[all_ticks[i]])
                                    < 1
                                )
                                else j
                            ),
                            max_volume * 100,
                            "",
                        ),
                    )
                )

        self.music_command_list = results
        self.music_tick_num = max(all_ticks)
        return results, self.music_tick_num


class FutureMidiConvertM6(MidiConvert):
    """
    加入插值算法优化音感，但仅用于第一音轨
    """

    # TODO 没写完的！！！！
