"""
版权所有 © 2024 金羿 & 诸葛亮与八卦阵
Copyright © 2025 Eilles & bgArray

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

import os
import shutil

from typing import Optional, Tuple


import Musicreater.experiment
from Musicreater.plugin.archive import compress_zipfile


def to_zip_pack_in_score(
    midi_cvt: Musicreater.experiment.FutureMidiConvertJavaE,
    dist_path: str,
    progressbar_style: Optional[Musicreater.experiment.ProgressBarStyle],
    scoreboard_name: str = "mscplay",
    sound_source: str = "ambient",
    auto_reset: bool = False,
) -> Tuple[int, int]:
    """
    将midi以计分播放器形式转换为我的世界函数附加包

    Parameters
    ----------
    midi_cvt: MidiConvert 对象
        用于转换的MidiConvert对象
    dist_path: str
        转换结果输出的目标路径
    progressbar_style: ProgressBarStyle 对象
        进度条对象
    scoreboard_name: str
        我的世界的计分板名称
    auto_reset: bool
        是否自动重置计分板

    Returns
    -------
    tuple[int指令数量, int音乐总延迟]
    """

    cmdlist, maxlen, maxscore = midi_cvt.to_command_list_in_java_score(
        scoreboard_name=scoreboard_name,
        source_of_sound=sound_source,
    )

    # 当文件f夹{self.outputPath}/temp/mscplyfuncs存在时清空其下所有项目，然后创建
    if os.path.exists(f"{dist_path}/temp/mscplyfuncs/"):
        shutil.rmtree(f"{dist_path}/temp/mscplyfuncs/")
    os.makedirs(f"{dist_path}/temp/mscplyfuncs/mscplay")

    # 写入stop.mcfunction
    with open(
        f"{dist_path}/temp/mscplyfuncs/stop.mcfunction", "w", encoding="utf-8"
    ) as f:
        f.write("scoreboard players reset @a {}".format(scoreboard_name))

    # 将命令列表写入文件
    index_file = open(
        f"{dist_path}/temp/mscplyfuncs/index.mcfunction", "w", encoding="utf-8"
    )
    for i in range(len(cmdlist)):
        index_file.write(f"function mscplyfuncs:mscplay/track{i + 1}\n")
        with open(
            f"{dist_path}/temp/mscplyfuncs/mscplay/track{i + 1}.mcfunction",
            "w",
            encoding="utf-8",
        ) as f:
            f.write("\n".join([single_cmd.cmd for single_cmd in cmdlist[i]]))
    index_file.writelines(
        (
            "scoreboard players add @a[score_{0}_min=1] {0} 1\n".format(
                scoreboard_name
            ),
            (
                "scoreboard players reset @a[score_{0}_min={1}] {0}\n".format(
                    scoreboard_name, maxscore + 20
                )
                if auto_reset
                else ""
            ),
            f"function mscplyfuncs:mscplay/progressShow\n" if progressbar_style else "",
        )
    )

    if progressbar_style:
        with open(
            f"{dist_path}/temp/mscplyfuncs/mscplay/progressShow.mcfunction",
            "w",
            encoding="utf-8",
        ) as f:
            f.writelines(
                "\n".join(
                    [
                        single_cmd.cmd
                        for single_cmd in midi_cvt.form_java_progress_bar(
                            maxscore, scoreboard_name, progressbar_style
                        )
                    ]
                )
            )

    index_file.close()

    if os.path.exists(f"{dist_path}/{midi_cvt.music_name}.zip"):
        os.remove(f"{dist_path}/{midi_cvt.music_name}.zip")
    compress_zipfile(
        f"{dist_path}/temp/",
        f"{dist_path}/{midi_cvt.music_name}[JEscore].zip",
    )

    shutil.rmtree(f"{dist_path}/temp/")

    return maxlen, maxscore


print(
    to_zip_pack_in_score(
        Musicreater.experiment.FutureMidiConvertJavaE.from_midi_file(
            input("midi路径："),
            play_speed=float(input("播放速度：")),
            old_exe_format=True,
            note_table_replacement={
                "note.iron_xylophone": "note.xylophone",
                "note.cow_bell": "note.xylophone",
                "note.didgeridoo": "note.guitar",
                "note.bit": "note.harp",
                "note.banjo": "note.flute",
                "note.pling": "note.harp",
            },
            # pitched_note_table=Musicreater.MM_NBS_PITCHED_INSTRUMENT_TABLE,
        ),
        input("输出路径："),
        Musicreater.experiment.ProgressBarStyle(),
        # Musicreater.plugin.ConvertConfig(input("输出路径:"),),
        scoreboard_name=input("计分板名称："),
        sound_source=input("发音源："),
        auto_reset=True,
    )
)
