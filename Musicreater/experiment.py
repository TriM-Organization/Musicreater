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

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md


from .exceptions import *
from .subclass import *
from .utils import *
from .main import MidiConvert, MM_CLASSIC_PERCUSSION_INSTRUMENT_TABLE, MM_CLASSIC_PITCHED_INSTRUMENT_TABLE
from .types import Tuple, List, Dict, ChannelType


class FutureMidiConvertRSNB(MidiConvert):
    """
    加入红石音乐适配
    """

    music_command_list: Dict[int, SingleNoteBox]
    """音乐指令列表"""


class FutureMidiConvertM4(MidiConvert):
    """
    加入插值算法优化音感
    : 经测试，生成效果已经达到，感觉良好
    """

    # 临时用的插值计算函数
    @staticmethod
    def _linear_note(
        _note: SingleNote,
        _apply_time_division: float = 100,
    ) -> List[SingleNote]:
        """传入音符数据，返回以半秒为分割的插值列表
        :param _note: SingleNote 音符
        :param _apply_time_division: int 间隔毫秒数
        :return list[tuple(int开始时间（毫秒）, int乐器, int音符, int力度（内置）, float音量（播放）),]"""

        if _note.percussive:
            return [
                _note,
            ]

        totalCount = int(_note.duration / _apply_time_division)

        if totalCount == 0:
            return [
                _note,
            ]
        # print(totalCount)

        result: List[SingleNote] = []

        for _i in range(totalCount):
            result.append(
                SingleNote(
                    instrument=_note.inst,
                    pitch=_note.pitch,
                    velocity=_note.velocity,
                    startime=int(_note.start_time + _i * (_note.duration / totalCount)),
                    lastime=int(_note.duration / totalCount),
                    track_number=_note.track_no,
                    is_percussion=_note.percussive,
                    extra_information=_note.extra_info
                )
                # (
                #     _note.start_time + _i * _apply_time_division,
                #     _note.instrument,
                #     _note.pitch,
                #     _note.velocity,
                #     ((totalCount - _i) / totalCount),
                # )
            )

        return result

    def to_command_list_in_delay(
        self,
        max_volume: float = 1.0,
        speed: float = 1.0,
        player_selector: str = "@a",
    ) -> Tuple[List[SingleCommand], int, int]:
        """
        将midi转换为我的世界命令列表，并输出每个音符之后的延迟

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
            raise ZeroSpeedError("播放速度仅可为(0,1]范围内的正实数")
        max_volume = 1 if max_volume > 1 else (0.001 if max_volume <= 0 else max_volume)

        notes_list: List[SingleNote] = []

        # 此处 我们把通道视为音轨
        for channel in self.to_music_note_channels().values():
            for note in channel:
                note.set_info(note_to_command_parameters(note,self.percussion_note_referrence_table if note.percussive else self.pitched_note_reference_table, (max_volume) if note.track_no == 0 else (max_volume * 0.9),self.volume_processing_function,))
                

                if not note.percussive:
                    notes_list.extend(self._linear_note(note, note.extra_info[3] * 500))
                else:
                    notes_list.append(note)

        notes_list.sort(key=lambda a: a.start_time)

        self.music_command_list = []
        multi = max_multi = 0
        delaytime_previous = 0

        for note in notes_list:
            delaytime_now = round(note.start_time / speed / 50)
            if (tickdelay := (delaytime_now - delaytime_previous)) == 0:
                multi += 1
            else:
                max_multi = max(max_multi, multi)
                multi = 0
            self.music_command_list.append(
                SingleCommand(
                    self.execute_cmd_head.format(player_selector)
                    + r"playsound {} @s ^ ^ ^{} {} {}".format(*note.extra_info),
                    tick_delay=tickdelay,
                    annotation="在{}播放{}%的{}音".format(
                        mctick2timestr(delaytime_now),
                        max_volume * 100,
                        "{}:{}".format(note.extra_info[0], note.extra_info[3]),
                    ),
                )
            )
            delaytime_previous = delaytime_now

        self.music_tick_num = round(notes_list[-1].start_time / speed / 50)
        return self.music_command_list, self.music_tick_num, max_multi + 1


class FutureMidiConvertM5(MidiConvert):
    """
    加入同刻偏移算法优化音感
    """

    def to_music_channels(
        self,
    ) -> ChannelType:
        """
        使用金羿的转换思路，将midi解析并转换为频道信息字典

        Returns
        -------
        以频道作为分割的Midi信息字典:
        Dict[int,Dict[int,List[Union[Tuple[Literal["PgmC"], int, int],Tuple[Literal["NoteS"], int, int, int],Tuple[Literal["NoteE"], int, int],]],],]
        """
        if self.midi is None:
            raise MidiUnboundError(
                "你是否正在使用的是一个由 copy_important 生成的MidiConvert对象？这是不可复用的。"
            )

        # 一个midi中仅有16个通道 我们通过通道来识别而不是音轨
        midi_channels: ChannelType = empty_midi_channels()
        tempo = 500000

        # 我们来用通道统计音乐信息
        # 但是是用分轨的思路的
        for track_no, track in enumerate(self.midi.tracks):
            microseconds = 0
            if not track:
                continue

            note_queue = empty_midi_channels(staff=[])

            for msg in track:
                if msg.time != 0:
                    microseconds += msg.time * tempo / self.midi.ticks_per_beat / 1000

                if msg.is_meta:
                    if msg.type == "set_tempo":
                        tempo = msg.tempo
                else:
                    try:
                        if not track_no in midi_channels[msg.channel].keys():
                            midi_channels[msg.channel][track_no] = []
                    except AttributeError as E:
                        print(msg, E)

                    if msg.type == "program_change":
                        midi_channels[msg.channel][track_no].append(
                            ("PgmC", msg.program, microseconds)
                        )

                    elif msg.type == "note_on" and msg.velocity != 0:
                        midi_channels[msg.channel][track_no].append(
                            ("NoteS", msg.note, msg.velocity, microseconds)
                        )

                    elif (msg.type == "note_on" and msg.velocity == 0) or (
                        msg.type == "note_off"
                    ):
                        midi_channels[msg.channel][track_no].append(
                            ("NoteE", msg.note, microseconds)
                        )

        """整合后的音乐通道格式
        每个通道包括若干消息元素其中逃不过这三种：

        1 切换乐器消息
        ("PgmC", 切换后的乐器ID: int, 距离演奏开始的毫秒)

        2 音符开始消息
        ("NoteS", 开始的音符ID, 力度（响度）, 距离演奏开始的毫秒)

        3 音符结束消息
        ("NoteE", 结束的音符ID, 距离演奏开始的毫秒)"""
        del tempo, self.channels
        self.channels: ChannelType = midi_channels
        # [print([print(no,tno,sum([True if i[0] == 'NoteS' else False for i in track])) for tno,track in cna.items()]) if cna else False for no,cna in midi_channels.items()]
        return midi_channels
    
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
                            inst_to_sould_with_deviation(msg[1],MM_CLASSIC_PERCUSSION_INSTRUMENT_TABLE)
                            if SpecialBits
                            else inst_to_sould_with_deviation(InstID,MM_CLASSIC_PITCHED_INSTRUMENT_TABLE)
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
