# -*- coding: utf-8 -*-

"""
音·创 v3 内置的 指令生成插件
"""

"""
版权所有 © 2026 金羿、玉衡Alioth
Copyright © 2026 Eilles, YuhengAlioth

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md


from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import BinaryIO, Optional, Dict, List, Callable, Tuple, Mapping
from math import ceil

from Musicreater import SingleMusic, SingleTrack, SingleNote, SoundAtmos, MineNote
from Musicreater.plugins import (
    library_plugin,
    PluginConfig,
    PluginMetaInformation,
    PluginTypes,
    LibraryPluginBase,
)
from Musicreater.exceptions import ZeroSpeedError, IllegalMinimumVolumeError
from Musicreater._utils import enumerated_stuffcopy_dictionary

from .progressbar import ProgressBarStyle, DEFAULT_PROGRESSBAR_STYLE, mctick2timestr
from .utils import minenote_to_command_parameters

# @dataclass
# class CommandConvertionConfig(PluginConfig):
#     execute_command_head: str = "execute as {} at @s positioned ~ ~ ~ run "


@dataclass
class MineCommand:
    """存储单个指令的类"""

    command: str
    """指令文本"""
    conditional: bool = False
    """执行是否有条件"""
    delay: int = 0
    """执行的延迟"""
    annotation: str = ""
    """指令注释"""

    def copy(self):
        return MineCommand(
            command=self.command,
            conditional=self.conditional,
            delay=self.delay,
            annotation=self.annotation,
        )

    @property
    def mcfunction_command_string(self) -> str:
        """
        我的世界函数字符串（包含注释）
        """
        return self.__str__()

    def __str__(self) -> str:
        """
        转为我的世界函数文件格式（包含注释）
        """
        return "# {cdt}<{delay}> {ant}\n{cmd}".format(
            cdt="[CDT]" if self.conditional else "",
            delay=self.delay,
            ant=self.annotation,
            cmd=self.command,
        )

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            # 不比较注释内容
            return (
                (self.command == other.command)
                and (self.conditional == other.conditional)
                and (self.delay == other.delay)
            )
        else:
            return False


@library_plugin("notedata_to_command_plugin")
class NoteDataConvert2CommandPlugin(LibraryPluginBase):
    metainfo = PluginMetaInformation(
        name="音符数据的基岩版指令支持",
        author="金羿、玉衡Alioth",
        description="从音符数据转换为我的世界指令相关格式",
        version=(0, 0, 1),
        type=PluginTypes.LIBRARY,
        license="Same as Musicreater",
    )

    @staticmethod
    def generate_progressbar(
        max_score: int,
        scoreboard_name: str,
        music_name: str = "",
        progressbar_style: ProgressBarStyle = DEFAULT_PROGRESSBAR_STYLE,
        execute_command_head: str = "execute as {} at @s positioned ~ ~ ~ run ",
    ) -> List[MineCommand]:
        """
        生成进度条

        Parameters
        ----------
        max_score: int
            最大的积分值
        scoreboard_name: str
            所使用的计分板名称
        progressbar_style: ProgressBarStyle
            此参数详见 ../docs/库的生成与功能文档.md#进度条自定义

        Returns
        -------
        list[MineCommand,]
        """
        orignal_style_string = progressbar_style.style_base_string
        """用于被替换的进度条原始样式"""

        """
        | 标识符   | 指定的可变量     |
        |---------|----------------|
        | `%%N`   | 乐曲名          |
        | `%^s`   | 计分板最大值     |
        | `%^t`   | 曲目总时长       |
        | `%%s`   | 当前计分板值     |
        | `%%t`   | 当前播放时间     |
        | `%%%`   | 当前进度比率     |
        | `_`     | 用以表示进度条占位|
        | `%*%`   | 指定*的动画内容   |
        """
        per_value_in_each = max_score / orignal_style_string.count("_")
        """每个进度条代表的分值"""

        result: List[MineCommand] = []

        orignal_style_string = (
            orignal_style_string.replace("%%N", music_name)
            .replace("%^s", str(max_score))
            .replace("%^t", mctick2timestr(max_score))
        )

        scoreboard_name_part = scoreboard_name[:2]
        if "%%%" in orignal_style_string:
            result.append(
                MineCommand(
                    'scoreboard objectives add {}PercT dummy "百分比计算"'.format(
                        scoreboard_name_part
                    ),
                    annotation="新增临时百分比变量",
                )
            )
            result.append(
                MineCommand(
                    execute_command_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players set MaxScore {} {}".format(
                        scoreboard_name, max_score
                    ),
                    annotation="设定音乐最大延迟分数",
                )
            )
            result.append(
                MineCommand(
                    execute_command_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players set n100 {} 100".format(scoreboard_name),
                    annotation="设置常量100",
                )
            )
            result.append(
                MineCommand(
                    execute_command_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players operation @s {} = @s {}".format(
                        scoreboard_name_part + "PercT", scoreboard_name
                    ),
                    annotation="赋值当前进度",
                )
            )
            result.append(
                MineCommand(
                    execute_command_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players operation @s {} *= n100 {}".format(
                        scoreboard_name_part + "PercT", scoreboard_name
                    ),
                    annotation="转换当前进度之单位至百分比（扩大精度）",
                )
            )
            result.append(
                MineCommand(
                    execute_command_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players operation @s {} /= MaxScore {}".format(
                        scoreboard_name_part + "PercT", scoreboard_name
                    ),
                    annotation="计算进度百分比",
                )
            )

        if "%%t" in orignal_style_string:
            result.append(
                MineCommand(
                    'scoreboard objectives add {}TMinT dummy "时间计算：分"'.format(
                        scoreboard_name_part
                    ),
                    annotation="新增临时分变量",
                )
            )
            result.append(
                MineCommand(
                    'scoreboard objectives add {}TSecT dummy "时间计算：秒"'.format(
                        scoreboard_name_part
                    ),
                    annotation="新增临时秒变量",
                )
            )
            result.append(
                MineCommand(
                    execute_command_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players set n20 {} 20".format(scoreboard_name),
                    annotation="设置常量 20",
                )
            )
            result.append(
                MineCommand(
                    execute_command_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players set n60 {} 60".format(scoreboard_name),
                    annotation="设置常量 60",
                )
            )

            result.append(
                MineCommand(
                    execute_command_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players operation @s {} = @s {}".format(
                        scoreboard_name_part + "TMinT", scoreboard_name
                    ),
                    annotation="赋值临时分变量",
                )
            )
            result.append(
                MineCommand(
                    execute_command_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players operation @s {} /= n20 {}".format(
                        scoreboard_name_part + "TMinT", scoreboard_name
                    ),
                    annotation="转换临时分变量之单位为秒（缩减精度）",
                )
            )
            result.append(
                MineCommand(
                    execute_command_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players operation @s {} = @s {}".format(
                        scoreboard_name_part + "TSecT", scoreboard_name_part + "TMinT"
                    ),
                    annotation="赋值临时秒",
                )
            )

            result.append(
                MineCommand(
                    execute_command_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players operation @s {} /= n60 {}".format(
                        scoreboard_name_part + "TMinT", scoreboard_name
                    ),
                    annotation="转换临时分变量之单位为分（缩减精度）",
                )
            )

            result.append(
                MineCommand(
                    execute_command_head.format(
                        "@a[scores={" + scoreboard_name + "=1..}]"
                    )
                    + "scoreboard players operation @s {} %= n60 {}".format(
                        scoreboard_name_part + "TSecT", scoreboard_name
                    ),
                    annotation="确定临时秒（框定精度区间）",
                )
            )

        if progressbar_style.is_animate_autoloop and progressbar_style.animate_circle:

            result.append(
                MineCommand(
                    'scoreboard objectives add {}AniC dummy "动画循环控制"'.format(
                        scoreboard_name_part
                    ),
                    annotation="新增动画循环控制变量",
                )
            )
            for animate_placeholder in progressbar_style.animate_circle:
                max_loop_score = max(
                    progressbar_style.animate_circle[animate_placeholder].keys()
                )
                if ("%%%" not in orignal_style_string or max_loop_score != 100) and (
                    "%%t" not in orignal_style_string or max_loop_score not in (60, 20)
                ):
                    result.append(
                        MineCommand(
                            execute_command_head.format(
                                "@a[scores={" + scoreboard_name + "=1..}]"
                            )
                            + "scoreboard players set n{num} {sbn} {num}".format(
                                sbn=scoreboard_name,
                                num=max_loop_score,
                            ),
                            annotation="设置常量 {num}".format(num=max_loop_score),
                        )
                    )

                result.append(
                    MineCommand(
                        execute_command_head.format(
                            "@a[scores={" + scoreboard_name + "=1..}]"
                        )
                        + "scoreboard players operation @s {sbnp}AniC = @s {sbn}".format(
                            sbnp=scoreboard_name_part, sbn=scoreboard_name
                        ),
                    )
                )
                result.append(
                    MineCommand(
                        execute_command_head.format(
                            "@a[scores={" + scoreboard_name + "=1..}]"
                        )
                        + "scoreboard players operation @s {sbnp}AniC %= n{num} {sbn}".format(
                            sbnp=scoreboard_name_part,
                            num=max_loop_score,
                            sbn=scoreboard_name,
                        ),
                    )
                )

        for i in range(orignal_style_string.count("_")):
            npg_stl = (
                orignal_style_string.replace(
                    "%%s",
                    '"},{"score":{"name":"*","objective":"'
                    + scoreboard_name
                    + '"}},{"text":"',
                )
                .replace(
                    "%%t",
                    '"},{"score":{"name":"*","objective":"{-}TMinT"}},{"text":":"},'
                    '{"score":{"name":"*","objective":"{-}TSecT"}},{"text":"'.replace(
                        "{-}", scoreboard_name_part
                    ),
                )
                .replace(
                    "%%%",
                    '"},{"score":{"name":"*","objective":"'
                    + scoreboard_name_part
                    + 'PercT"}},{"text":"%',
                )
                .replace("_", progressbar_style.progress_played, i + 1)
                .replace("_", progressbar_style.progress_toplay)
            )
            for animate_placeholder in progressbar_style.animate_circle:
                animation_start_tick = 0
                npg_stl = npg_stl.replace(
                    animate_placeholder,
                    '"},{"translate": "%%'
                    + str(
                        len(progressbar_style.animate_circle[animate_placeholder]) + 1
                    )
                    + '","with":{"rawtext":['
                    + (
                        ",".join(
                            (
                                '{"selector":"@s[scores={{-}={*}..{&}}]"}'.replace(
                                    "{*}", str(animation_start_tick)
                                ).replace("{&}", str(animation_start_tick := end_tick))
                                for end_tick in progressbar_style.animate_circle[
                                    animate_placeholder
                                ].keys()
                            )
                        ).replace(
                            "{-}",
                            (
                                (scoreboard_name_part + "AniC")
                                if progressbar_style.is_animate_autoloop
                                else scoreboard_name
                            ),
                        )
                    )
                    + ","
                    + ",".join(
                        (
                            '{"text":"' + animation_text + '"}'
                            for animation_text in progressbar_style.animate_circle[
                                animate_placeholder
                            ].values()
                        )
                    )
                    + ',{"text":"NaN"}]}},{"text":"',
                )
            result.append(
                MineCommand(
                    execute_command_head.format(
                        "@a[scores={"
                        + scoreboard_name
                        + f"={int(i * per_value_in_each)}..{ceil((i + 1) * per_value_in_each)}"
                        + "}]"
                    )
                    + 'titleraw @s actionbar {"rawtext":[{"text":"'
                    + npg_stl
                    + '"}]}',
                    annotation="进度条显示",
                )
            )

        if "%%%" in orignal_style_string:
            result.append(
                MineCommand(
                    "scoreboard objectives remove {}PercT".format(scoreboard_name_part),
                    annotation="移除临时百分比变量",
                )
            )
        if "%%t" in orignal_style_string:
            result.append(
                MineCommand(
                    "scoreboard objectives remove {}TMinT".format(scoreboard_name_part),
                    annotation="移除临时分变量",
                )
            )
            result.append(
                MineCommand(
                    "scoreboard objectives remove {}TSecT".format(scoreboard_name_part),
                    annotation="移除临时秒变量",
                )
            )
        if progressbar_style.is_animate_autoloop and progressbar_style.animate_circle:
            result.append(
                MineCommand(
                    "scoreboard objectives remove {}AniC".format(scoreboard_name_part),
                    annotation="移除临时动画循环控制变量",
                )
            )

        return result

    @staticmethod
    def to_command_list_in_score(
        music: SingleMusic,
        music_deviation: float = 0,
        minimum_volume: float = 0.01,
        scoreboard_name: str = "mscplay",
        execute_command_head: str = "execute as {} at @s positioned ~ ~ ~ run ",
    ) -> Tuple[List[List[MineCommand]], int, int]:
        """
        将midi转换为我的世界命令列表

        Parameters
        ----------
        scoreboard_name: str
            我的世界的计分板名称

        Returns
        -------
        tuple( list[list[MineCommand指令,... ],... ], int指令数量, int音乐时长游戏刻 )
        """

        command_channels: List[List[MineCommand]] = []
        command_amount = 0
        max_score = 0

        for track in music.music_tracks:
            # 如果当前轨道为空 则跳过
            if not track:
                continue

            this_channel = []

            for note in track.minenotes:
                max_score = max(max_score, note.start_tick)

                (
                    relative_coordinates,
                    mc_pitch,
                ) = minenote_to_command_parameters(
                    note,
                    pitch_deviation=music_deviation,
                )

                this_channel.append(
                    MineCommand(
                        (
                            execute_command_head.format(
                                "@a[scores=({}={})]".format(
                                    scoreboard_name, note.start_tick
                                )
                                .replace("(", r"{")
                                .replace(")", r"}")
                            )
                            + "playsound {} @s ^{} ^{} ^{} 3.0 {} {}".format(
                                track.instrument,
                                *relative_coordinates,
                                1.0 if note.percussive else mc_pitch,
                                minimum_volume,
                            )
                        ),
                        annotation=(
                            "[{}] 打击乐音符{}".format(
                                mctick2timestr(note.start_tick),
                                note.instrument,
                            )
                            if note.percussive
                            else "[{}] 音符{}:{:.2f}".format(
                                mctick2timestr(note.start_tick),
                                note.instrument,
                                mc_pitch,
                            )
                        ),
                    ),
                )

                command_amount += 1

            if this_channel:
                command_channels.append(this_channel)

        return command_channels, command_amount, max_score

    @staticmethod
    def to_command_list_in_delay(
        music: SingleMusic,
        music_deviation: float = 0,
        minimum_volume: float = 0.01,
        player_selector: str = "@a",
        execute_command_head: str = "execute as {} at @s positioned ~ ~ ~ run ",
    ) -> Tuple[List[MineCommand], int, int]:
        """
        将midi转换为我的世界命令列表，并输出每个音符之后的延迟

        Parameters
        ----------
        player_selector: str
            玩家选择器，默认为`@a`

        Returns
        -------
        tuple( list[MineCommand指令,...], int音乐时长游戏刻, int最大同时播放的指令数量 )
        """

        # 音轨判断
        music_command_list = []
        multi = max_multi = 0
        delaytime_previous = 0
        last_note: MineNote

        for note in music.get_minenotes(
            start_time=0,
        ):
            if (tickdelay := (note.precise_tick - delaytime_previous)) == 0:
                multi += 1
            else:
                max_multi = max(max_multi, multi)
                multi = 0

            (
                relative_coordinates,
                mc_pitch,
            ) = minenote_to_command_parameters(
                note,
                pitch_deviation=music_deviation,
            )

            music_command_list.append(
                MineCommand(
                    command=(
                        execute_command_head.format(player_selector)
                        + "playsound {} @s ^{} ^{} ^{} 3.0 {} {}".format(
                            note.instrument,
                            *relative_coordinates,
                            1.0 if note.percussive else mc_pitch,
                            minimum_volume,
                        )
                    ),
                    annotation=(
                        "[{}] 打击乐音符{}".format(
                            mctick2timestr(note.start_tick),
                            note.instrument,
                        )
                        if note.percussive
                        else "[{}] 音符{}:{:.2f}".format(
                            mctick2timestr(note.start_tick),
                            note.instrument,
                            mc_pitch,
                        )
                    ),
                    delay=int(tickdelay),
                ),
            )
            delaytime_previous = note.precise_tick
            last_note = note
        if music_command_list:
            return (
                music_command_list,
                last_note.start_tick + last_note.duration_tick,
                max_multi + 1,
            )
        else:
            return [], 0, 0
