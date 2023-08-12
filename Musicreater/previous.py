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

from typing import Dict, List, Tuple, Union

from .exceptions import *
from .main import MidiConvert, mido
from .subclass import *
from .utils import *


class ObsoleteMidiConvert(MidiConvert):
    """
    我说一句话：
    这些破烂老代码能跑得起来就是谢天谢地，你们还指望我怎么样？这玩意真的不会再维护了，我发誓！
    """

    def to_command_list_method1(
        self,
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
            raise ZeroSpeedError("播放速度仅可为正实数")
        if not self.midi:
            raise MidiUnboundError(
                "你是否正在使用的是一个由 copy_important 生成的MidiConvert对象？这是不可复用的。"
            )

        MaxVolume = 1 if MaxVolume > 1 else (0.001 if MaxVolume <= 0 else MaxVolume)
        commands = 0
        maxscore = 0
        tempo = mido.midifiles.midifiles.DEFAULT_TEMPO

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
                        nowscore = round(
                            (ticks * tempo)
                            / ((self.midi.ticks_per_beat * float(speed)) * 50000)
                        )
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

    def _toCmdList_m1(
            self,
            scoreboardname: str = "mscplay",
            volume: float = 1.0,
            speed: float = 1.0) -> list:
        """
        使用Dislink Sforza的转换思路，将midi转换为我的世界命令列表
        :param scoreboardname: 我的世界的计分板名称
        :param volume: 音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
        :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
        :return: tuple(命令列表, 命令个数, 计分板最大值)
        """
        tracks = []
        if volume > 1:
            volume = 1
        if volume <= 0:
            volume = 0.001

        commands = 0
        maxscore = 0

        for i, track in enumerate(self.midi.tracks):

            ticks = 0
            instrumentID = 0
            singleTrack = []

            for msg in track:
                ticks += msg.time
                # print(msg)
                if msg.is_meta:
                    if msg.type == "set_tempo":
                        tempo = msg.tempo
                else:
                    if msg.type == "program_change":
                        # print("TT")
                        instrumentID = msg.program
                    if msg.type == "note_on" and msg.velocity != 0:
                        nowscore = round(
                            (ticks * tempo)
                            / ((self.midi.ticks_per_beat * float(speed)) * 50000)
                        )
                        maxscore = max(maxscore, nowscore)
                        soundID, _X = self.__Inst2soundID_withX(instrumentID)
                        singleTrack.append(
                            "execute @a[scores={" +
                            str(scoreboardname) +
                            "=" +
                            str(nowscore) +
                            "}" +
                            f"] ~ ~ ~ playsound {soundID} @s ~ ~{1 / volume - 1} ~ {msg.velocity * (0.7 if msg.channel == 0 else 0.9)} {2 ** ((msg.note - 60 - _X) / 12)}")
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
    ) -> tuple:
        """
        使用神羽和金羿的转换思路，将midi转换为我的世界命令列表
        :param scoreboard_name: 我的世界的计分板名称
        :param MaxVolume: 音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
        :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
        :return: tuple(命令列表, 命令个数, 计分板最大值)
        """

        if speed == 0:
            raise ZeroSpeedError("播放速度仅可为正实数")
        MaxVolume = 1 if MaxVolume > 1 else (0.001 if MaxVolume <= 0 else MaxVolume)

        tracks = []
        cmdAmount = 0
        maxScore = 0
        InstID = -1

        self.to_music_channels()

        # 此处 我们把通道视为音轨
        for i in self.channels.keys():
            # 如果当前通道为空 则跳过
            if not self.channels[i]:
                continue

            if i == 9:
                SpecialBits = True
            else:
                SpecialBits = False

            nowTrack = []

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

        return tracks, cmdAmount, maxScore

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
            raise ZeroSpeedError("播放速度仅可为正实数")
        if not self.midi:
            raise MidiUnboundError(
                "你是否正在使用的是一个由 copy_important 生成的MidiConvert对象？这是不可复用的。"
            )

        MaxVolume = 1 if MaxVolume > 1 else (0.001 if MaxVolume <= 0 else MaxVolume)
        tempo = mido.midifiles.midifiles.DEFAULT_TEMPO

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
            raise ZeroSpeedError("播放速度仅可为正实数")

        MaxVolume = 1 if MaxVolume > 1 else (0.001 if MaxVolume <= 0 else MaxVolume)
        InstID = -1
        self.to_music_channels()

        results = []

        for i in self.channels.keys():
            # 如果当前通道为空 则跳过
            if not self.channels[i]:
                continue

            if i == 9:
                SpecialBits = True
            else:
                SpecialBits = False

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
                                all_ticks[i] - all_ticks[i - 1]
                                if i != 0
                                else all_ticks[i]
                            )
                        ),
                    )
                )

        return [results, max(all_ticks)]
