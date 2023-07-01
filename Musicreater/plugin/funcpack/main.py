# -*- coding: utf-8 -*-
"""
版权所有 © 2023 音·创 开发者
Copyright © 2023 all the developers of Musicreater

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿穆组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md


import json
import os
import shutil
from typing import Tuple

from ...main import MidiConvert
from ..archive import behavior_mcpack_manifest, compress_zipfile
from ..main import ConvertConfig


def to_function_addon_in_score(
    midi_cvt: MidiConvert,
    data_cfg: ConvertConfig,
    scoreboard_name: str = "mscplay",
    auto_reset: bool = False,
) -> Tuple[int, int]:
    """
    将midi以计分播放器形式转换为我的世界函数附加包

    Parameters
    ----------
    midi_cvt: MidiConvert 对象
        用于转换的MidiConvert对象
    data_cfg: ConvertConfig 对象
        部分转换通用参数
    scoreboard_name: str
        我的世界的计分板名称
    auto_reset: bool
        是否自动重置计分板

    Returns
    -------
    tuple[int指令数量, int音乐总延迟]
    """

    cmdlist, maxlen, maxscore = midi_cvt.to_command_list_in_score(
        scoreboard_name, data_cfg.volume_ratio, data_cfg.speed_multiplier
    )

    # 当文件f夹{self.outputPath}/temp/functions存在时清空其下所有项目，然后创建
    if os.path.exists(f"{data_cfg.dist_path}/temp/functions/"):
        shutil.rmtree(f"{data_cfg.dist_path}/temp/functions/")
    os.makedirs(f"{data_cfg.dist_path}/temp/functions/mscplay")

    # 写入manifest.json
    with open(f"{data_cfg.dist_path}/temp/manifest.json", "w", encoding="utf-8") as f:
        json.dump(
            behavior_mcpack_manifest(
                pack_description=f"{midi_cvt.midi_music_name} 音乐播放包，MCFUNCTION(MCPACK) 计分播放器 - 由 音·创 生成",
                pack_name=midi_cvt.midi_music_name + "播放",
                modules_description=f"无 - 由 音·创 生成",
            ),
            fp=f,
            indent=4,
        )

    # 将命令列表写入文件
    index_file = open(
        f"{data_cfg.dist_path}/temp/functions/index.mcfunction", "w", encoding="utf-8"
    )
    for i in range(len(cmdlist)):
        index_file.write(f"function mscplay/track{i + 1}\n")
        with open(
            f"{data_cfg.dist_path}/temp/functions/mscplay/track{i + 1}.mcfunction",
            "w",
            encoding="utf-8",
        ) as f:
            f.write("\n".join([single_cmd.cmd for single_cmd in cmdlist[i]]))
    index_file.writelines(
        (
            "scoreboard players add @a[scores={"
            + scoreboard_name
            + "=1..}] "
            + scoreboard_name
            + " 1\n",
            (
                "scoreboard players reset @a[scores={"
                + scoreboard_name
                + "="
                + str(maxscore + 20)
                + "..}]"
                + f" {scoreboard_name}\n"
            )
            if auto_reset
            else "",
            f"function mscplay/progressShow\n" if data_cfg.progressbar_style else "",
        )
    )

    if data_cfg.progressbar_style:
        with open(
            f"{data_cfg.dist_path}/temp/functions/mscplay/progressShow.mcfunction",
            "w",
            encoding="utf-8",
        ) as f:
            f.writelines(
                "\n".join(
                    [
                        single_cmd.cmd
                        for single_cmd in midi_cvt.form_progress_bar(
                            maxscore, scoreboard_name, data_cfg.progressbar_style
                        )
                    ]
                )
            )

    index_file.close()

    if os.path.exists(f"{data_cfg.dist_path}/{midi_cvt.midi_music_name}.mcpack"):
        os.remove(f"{data_cfg.dist_path}/{midi_cvt.midi_music_name}.mcpack")
    compress_zipfile(
        f"{data_cfg.dist_path}/temp/",
        f"{data_cfg.dist_path}/{midi_cvt.midi_music_name}.mcpack",
    )

    shutil.rmtree(f"{data_cfg.dist_path}/temp/")

    return maxlen, maxscore
