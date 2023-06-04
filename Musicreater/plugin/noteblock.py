# -*- coding: utf-8 -*-
"""
存放有关红石音乐生成操作的内容
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


from ..exceptions import NotDefineProgramError, ZeroSpeedError
from ..main import MidiConvert
from ..subclass import SingleCommand

# 你以为写完了吗？其实并没有


def to_note_list(
    midi_cvt: MidiConvert,
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
        raise ZeroSpeedError("播放速度仅可为正实数")

    midi_channels = (
        midi_cvt.to_music_channels() if not midi_cvt.channels else midi_cvt.channels
    )

    tracks = {}

    # 此处 我们把通道视为音轨
    for i in midi_channels.keys():
        # 如果当前通道为空 则跳过
        if not midi_channels[i]:
            continue

        # 第十通道是打击乐通道
        SpecialBits = True if i == 9 else False

        # nowChannel = []

        for track_no, track in midi_channels[i].items():
            for msg in track:
                if msg[0] == "PgmC":
                    InstID = msg[1]

                elif msg[0] == "NoteS":
                    try:
                        soundID, _X = (
                            midi_cvt.perc_inst_to_soundID_withX(InstID)
                            if SpecialBits
                            else midi_cvt.inst_to_souldID_withX(InstID)
                        )
                    except UnboundLocalError as E:
                        soundID, _X = (
                            midi_cvt.perc_inst_to_soundID_withX(-1)
                            if SpecialBits
                            else midi_cvt.inst_to_souldID_withX(-1)
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
                            all_ticks[i] - all_ticks[i - 1] if i != 0 else all_ticks[i]
                        )
                    ),
                )
            )

    return [results, max(all_ticks)]
