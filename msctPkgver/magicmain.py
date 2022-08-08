# -*- coding: utf-8 -*-


# 音·创 开发交流群 861684859
# Email EillesWan2006@163.com W-YI_DoctorYI@outlook.com EillesWan@outlook.com
# 版权所有 金羿("Eilles Wan") & 诸葛亮与八卦阵("bgArray") & 鸣凤鸽子("MingFengPigeon")
# 若需使用或借鉴 请依照 Apache 2.0 许可证进行许可


"""
音·创 库版 (Musicreater Package Version)
是一款免费开源的针对《我的世界：基岩版》的midi音乐转换库
注意！除了此源文件以外，任何属于此仓库以及此项目的文件均依照Apache许可证进行许可
Musicreater pkgver (Package Version 音·创 库版)
A free open source library used for convert midi file into formats that is suitable for **Minecraft: Bedrock Edition**.
Note! Except for this source file, all the files in this repository and this project are licensed under Apache License 2.0

   Copyright 2022 all the developers of Musicreater

   Licensed under the Apache License, Version 2.0 (the 'License');
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an 'AS IS' BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


def _toCmdList_m1(
    self, scoreboardname: str = "mscplay", volume: float = 1.0, speed: float = 1.0
) -> list:
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
                    soundID, _X = self.__Inst2soundIDwithX(instrumentID)
                    singleTrack.append(
                        "execute @a[scores={"
                        + str(scoreboardname)
                        + "="
                        + str(nowscore)
                        + "}"
                        + f"] ~ ~ ~ playsound {soundID} @s ~ ~{1 / volume - 1} ~ {msg.velocity * (0.7 if msg.channel == 0 else 0.9)} {2 ** ((msg.note - 60 - _X) / 12)}"
                    )
                    commands += 1
        if len(singleTrack) != 0:
            tracks.append(singleTrack)

    return tracks, commands, maxscore

