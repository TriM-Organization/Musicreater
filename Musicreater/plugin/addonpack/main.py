# -*- coding: utf-8 -*-
"""
版权所有 © 2024 音·创 开发者
Copyright © 2024 all the developers of Musicreater

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md

import json
import os
import shutil
from typing import Tuple

from ...main import MidiConvert
from ..archive import behavior_mcpack_manifest, compress_zipfile
from ...subclass import ProgressBarStyle
from ...types import Optional, Literal
from ..mcstructure import (
    Structure,
    COMPABILITY_VERSION_117,
    COMPABILITY_VERSION_119,
    commands_to_redstone_delay_structure,
    commands_to_structure,
    form_command_block_in_NBT_struct,
)


def to_addon_pack_in_score(
    midi_cvt: MidiConvert,
    dist_path: str,
    progressbar_style: Optional[ProgressBarStyle],
    scoreboard_name: str = "mscplay",
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

    cmdlist, maxlen, maxscore = midi_cvt.to_command_list_in_score(
        scoreboard_name=scoreboard_name,
    )

    # 当文件f夹{self.outputPath}/temp/functions存在时清空其下所有项目，然后创建
    if os.path.exists(f"{dist_path}/temp/functions/"):
        shutil.rmtree(f"{dist_path}/temp/functions/")
    os.makedirs(f"{dist_path}/temp/functions/mscplay")

    # 写入manifest.json
    with open(f"{dist_path}/temp/manifest.json", "w", encoding="utf-8") as f:
        json.dump(
            behavior_mcpack_manifest(
                pack_description=f"{midi_cvt.music_name} 音乐播放包，MCFUNCTION(MCPACK) 计分播放器 - 由 音·创 生成",
                pack_name=midi_cvt.music_name + "播放",
                modules_description=f"无 - 由 音·创 生成",
            ),
            fp=f,
            indent=4,
        )

    # 写入stop.mcfunction
    with open(
        f"{dist_path}/temp/functions/stop.mcfunction", "w", encoding="utf-8"
    ) as f:
        f.write("scoreboard players reset @a {}".format(scoreboard_name))

    # 将命令列表写入文件
    index_file = open(
        f"{dist_path}/temp/functions/index.mcfunction", "w", encoding="utf-8"
    )
    for i in range(len(cmdlist)):
        index_file.write(f"function mscplay/track{i + 1}\n")
        with open(
            f"{dist_path}/temp/functions/mscplay/track{i + 1}.mcfunction",
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
                (
                    "scoreboard players reset @a[scores={"
                    + scoreboard_name
                    + "="
                    + str(maxscore + 20)
                    + "..}]"
                    + f" {scoreboard_name}\n"
                )
                if auto_reset
                else ""
            ),
            f"function mscplay/progressShow\n" if progressbar_style else "",
        )
    )

    if progressbar_style:
        with open(
            f"{dist_path}/temp/functions/mscplay/progressShow.mcfunction",
            "w",
            encoding="utf-8",
        ) as f:
            f.writelines(
                "\n".join(
                    [
                        single_cmd.cmd
                        for single_cmd in midi_cvt.form_progress_bar(
                            maxscore, scoreboard_name, progressbar_style
                        )
                    ]
                )
            )

    index_file.close()

    if os.path.exists(f"{dist_path}/{midi_cvt.music_name}.mcpack"):
        os.remove(f"{dist_path}/{midi_cvt.music_name}.mcpack")
    compress_zipfile(
        f"{dist_path}/temp/",
        f"{dist_path}/{midi_cvt.music_name}.mcpack",
    )

    shutil.rmtree(f"{dist_path}/temp/")

    return maxlen, maxscore


def to_addon_pack_in_delay(
    midi_cvt: MidiConvert,
    dist_path: str,
    progressbar_style: Optional[ProgressBarStyle],
    player: str = "@a",
    max_height: int = 64,
) -> Tuple[int, int]:
    """
    将midi以延迟播放器形式转换为mcstructure结构文件后打包成附加包，并在附加包中生成相应地导入函数

    Parameters
    ----------
    midi_cvt: MidiConvert 对象
        用于转换的MidiConvert对象
    dist_path: str
        转换结果输出的目标路径
    progressbar_style: ProgressBarStyle 对象
        进度条对象
    player: str
        玩家选择器，默认为`@a`
    max_height: int
        生成结构最大高度

    Returns
    -------
    tuple[int指令数量, int音乐总延迟]
    """

    compability_ver = (
        COMPABILITY_VERSION_117
        if midi_cvt.enable_old_exe_format
        else COMPABILITY_VERSION_119
    )

    command_list, max_delay = midi_cvt.to_command_list_in_delay(
        player_selector=player,
    )[:2]

    if not os.path.exists(dist_path):
        os.makedirs(dist_path)

    # 当文件f夹{self.outputPath}/temp/存在时清空其下所有项目，然后创建
    if os.path.exists(f"{dist_path}/temp/"):
        shutil.rmtree(f"{dist_path}/temp/")
    os.makedirs(f"{dist_path}/temp/functions/")
    os.makedirs(f"{dist_path}/temp/structures/")

    # 写入manifest.json
    with open(f"{dist_path}/temp/manifest.json", "w", encoding="utf-8") as f:
        json.dump(
            behavior_mcpack_manifest(
                pack_description=f"{midi_cvt.music_name} 音乐播放包，MCSTRUCTURE(MCPACK) 延迟播放器 - 由 音·创 生成",
                pack_name=midi_cvt.music_name + "播放",
                modules_description=f"无 - 由 音·创 生成",
            ),
            fp=f,
            indent=4,
        )

    # 写入stop.mcfunction
    with open(
        f"{dist_path}/temp/functions/stop.mcfunction", "w", encoding="utf-8"
    ) as f:
        f.write(
            "gamerule commandblocksenabled false\ngamerule commandblocksenabled true"
        )

    # 将命令列表写入文件
    index_file = open(
        f"{dist_path}/temp/functions/index.mcfunction", "w", encoding="utf-8"
    )

    struct, size, end_pos = commands_to_structure(
        command_list,
        max_height - 1,
        compability_version_=compability_ver,
    )
    with open(
        os.path.abspath(
            os.path.join(
                dist_path,
                "temp/structures/",
                f"{midi_cvt.music_name}_main.mcstructure",
            )
        ),
        "wb+",
    ) as f:
        struct.dump(f)

    del struct

    if progressbar_style:
        scb_name = midi_cvt.music_name[:3] + "Pgb"
        index_file.write("scoreboard objectives add {0} dummy {0}计\n".format(scb_name))

        struct_a = Structure((1, 1, 1), compability_version=compability_ver)
        struct_a.set_block(
            (0, 0, 0),
            form_command_block_in_NBT_struct(
                r"scoreboard players add {} {} 1".format(player, scb_name),
                (0, 0, 0),
                1,
                1,
                alwaysRun=False,
                customName="显示进度条并加分",
                compability_version_number=compability_ver,
            ),
        )

        with open(
            os.path.abspath(
                os.path.join(
                    dist_path,
                    "temp/structures/",
                    f"{midi_cvt.music_name}_start.mcstructure",
                )
            ),
            "wb+",
        ) as f:
            struct_a.dump(f)

        index_file.write(f"structure load {midi_cvt.music_name}_start ~ ~ ~1\n")

        pgb_struct, pgbSize, pgbNowPos = commands_to_structure(
            midi_cvt.form_progress_bar(max_delay, scb_name, progressbar_style),
            max_height - 1,
            compability_version_=compability_ver,
        )

        with open(
            os.path.abspath(
                os.path.join(
                    dist_path,
                    "temp/structures/",
                    f"{midi_cvt.music_name}_pgb.mcstructure",
                )
            ),
            "wb+",
        ) as f:
            pgb_struct.dump(f)

        index_file.write(f"structure load {midi_cvt.music_name}_pgb ~ ~1 ~1\n")

        struct_a = Structure(
            (1, 1, 1),
        )
        struct_a.set_block(
            (0, 0, 0),
            form_command_block_in_NBT_struct(
                r"scoreboard players reset {} {}".format(player, scb_name),
                (0, 0, 0),
                1,
                0,
                alwaysRun=False,
                customName="重置进度条计分板",
                compability_version_number=compability_ver,
            ),
        )

        with open(
            os.path.abspath(
                os.path.join(
                    dist_path,
                    "temp/structures/",
                    f"{midi_cvt.music_name}_reset.mcstructure",
                )
            ),
            "wb+",
        ) as f:
            struct_a.dump(f)

        del struct_a, pgb_struct

        index_file.write(
            f"structure load {midi_cvt.music_name}_reset ~{pgbSize[0] + 2} ~ ~1\n"
        )

        index_file.write(
            f"structure load {midi_cvt.music_name}_main ~{pgbSize[0] + 2} ~1 ~1\n"
        )

    else:
        index_file.write(f"structure load {midi_cvt.music_name}_main ~ ~ ~1\n")

    index_file.close()

    if os.path.exists(f"{dist_path}/{midi_cvt.music_name}.mcpack"):
        os.remove(f"{dist_path}/{midi_cvt.music_name}.mcpack")
    compress_zipfile(
        f"{dist_path}/temp/",
        f"{dist_path}/{midi_cvt.music_name}.mcpack",
    )

    shutil.rmtree(f"{dist_path}/temp/")

    return len(command_list), max_delay


def to_addon_pack_in_repeater(
    midi_cvt: MidiConvert,
    dist_path: str,
    progressbar_style: Optional[ProgressBarStyle],
    player: str = "@a",
    max_height: int = 65,
) -> Tuple[int, int]:
    """
    将midi以中继器播放器形式转换为mcstructure结构文件后打包成附加包，并在附加包中生成相应地导入函数

    Parameters
    ----------
    midi_cvt: MidiConvert 对象
        用于转换的MidiConvert对象
    dist_path: str
        转换结果输出的目标路径
    progressbar_style: ProgressBarStyle 对象
        进度条对象
    player: str
        玩家选择器，默认为`@a`
    max_height: int
        生成结构最大高度

    Returns
    -------
    tuple[int指令数量, int音乐总延迟]
    """

    compability_ver = (
        COMPABILITY_VERSION_117
        if midi_cvt.enable_old_exe_format
        else COMPABILITY_VERSION_119
    )

    command_list, max_delay, max_together = midi_cvt.to_command_list_in_delay(
        player_selector=player,
    )

    if not os.path.exists(dist_path):
        os.makedirs(dist_path)

    # 当文件f夹{self.outputPath}/temp/存在时清空其下所有项目，然后创建
    if os.path.exists(f"{dist_path}/temp/"):
        shutil.rmtree(f"{dist_path}/temp/")
    os.makedirs(f"{dist_path}/temp/functions/")
    os.makedirs(f"{dist_path}/temp/structures/")

    # 写入manifest.json
    with open(f"{dist_path}/temp/manifest.json", "w", encoding="utf-8") as f:
        json.dump(
            behavior_mcpack_manifest(
                pack_description=f"{midi_cvt.music_name} 音乐播放包，MCSTRUCTURE(MCPACK) 中继器播放器 - 由 音·创 生成",
                pack_name=midi_cvt.music_name + "播放",
                modules_description=f"无 - 由 音·创 生成",
            ),
            fp=f,
            indent=4,
        )

    # 写入stop.mcfunction
    with open(
        f"{dist_path}/temp/functions/stop.mcfunction", "w", encoding="utf-8"
    ) as f:
        f.write(
            "gamerule commandblocksenabled false\ngamerule commandblocksenabled true"
        )

    # 将命令列表写入文件
    index_file = open(
        f"{dist_path}/temp/functions/index.mcfunction", "w", encoding="utf-8"
    )

    struct, size, end_pos = commands_to_redstone_delay_structure(
        command_list,
        max_delay,
        max_together,
        compability_version_=compability_ver,
    )
    with open(
        os.path.abspath(
            os.path.join(
                dist_path,
                "temp/structures/",
                f"{midi_cvt.music_name}_main.mcstructure",
            )
        ),
        "wb+",
    ) as f:
        struct.dump(f)

    del struct

    if progressbar_style:
        scb_name = midi_cvt.music_name[:3] + "Pgb"
        index_file.write("scoreboard objectives add {0} dummy {0}计\n".format(scb_name))

        struct_a = Structure((1, 1, 1), compability_version=compability_ver)
        struct_a.set_block(
            (0, 0, 0),
            form_command_block_in_NBT_struct(
                r"scoreboard players add {} {} 1".format(player, scb_name),
                (0, 0, 0),
                1,
                1,
                alwaysRun=False,
                customName="显示进度条并加分",
                compability_version_number=compability_ver,
            ),
        )

        with open(
            os.path.abspath(
                os.path.join(
                    dist_path,
                    "temp/structures/",
                    f"{midi_cvt.music_name}_start.mcstructure",
                )
            ),
            "wb+",
        ) as f:
            struct_a.dump(f)

        index_file.write(f"structure load {midi_cvt.music_name}_start ~ ~ ~1\n")

        pgb_struct, pgbSize, pgbNowPos = commands_to_structure(
            midi_cvt.form_progress_bar(max_delay, scb_name, progressbar_style),
            max_height - 1,
            compability_version_=compability_ver,
        )

        with open(
            os.path.abspath(
                os.path.join(
                    dist_path,
                    "temp/structures/",
                    f"{midi_cvt.music_name}_pgb.mcstructure",
                )
            ),
            "wb+",
        ) as f:
            pgb_struct.dump(f)

        index_file.write(f"structure load {midi_cvt.music_name}_pgb ~ ~1 ~1\n")

        struct_a = Structure(
            (1, 1, 1),
        )
        struct_a.set_block(
            (0, 0, 0),
            form_command_block_in_NBT_struct(
                r"scoreboard players reset {} {}".format(player, scb_name),
                (0, 0, 0),
                1,
                0,
                alwaysRun=False,
                customName="重置进度条计分板",
                compability_version_number=compability_ver,
            ),
        )

        with open(
            os.path.abspath(
                os.path.join(
                    dist_path,
                    "temp/structures/",
                    f"{midi_cvt.music_name}_reset.mcstructure",
                )
            ),
            "wb+",
        ) as f:
            struct_a.dump(f)

        del struct_a, pgb_struct

        index_file.write(
            f"structure load {midi_cvt.music_name}_reset ~{pgbSize[0] + 2} ~ ~1\n"
        )

        index_file.write(
            f"structure load {midi_cvt.music_name}_main ~{pgbSize[0] + 2} ~1 ~1\n"
        )

    else:
        index_file.write(f"structure load {midi_cvt.music_name}_main ~ ~ ~1\n")

    index_file.close()

    if os.path.exists(f"{dist_path}/{midi_cvt.music_name}.mcpack"):
        os.remove(f"{dist_path}/{midi_cvt.music_name}.mcpack")
    compress_zipfile(
        f"{dist_path}/temp/",
        f"{dist_path}/{midi_cvt.music_name}.mcpack",
    )

    shutil.rmtree(f"{dist_path}/temp/")

    return len(command_list), max_delay


def to_addon_pack_in_repeater_divided_by_instrument(
    midi_cvt: MidiConvert,
    dist_path: str,
    player: str = "@a",
    max_height: int = 65,
    base_block: str = "concrete",
) -> Tuple[int, int]:
    """
    将midi以中继器播放器形式转换为mcstructure结构文件后打包成附加包，并在附加包中生成相应地导入函数

    Parameters
    ----------
    midi_cvt: MidiConvert 对象
        用于转换的MidiConvert对象
    dist_path: str
        转换结果输出的目标路径
    player: str
        玩家选择器，默认为`@a`
    max_height: int
        生成结构最大高度

    Returns
    -------
    tuple[int指令数量, int音乐总延迟]
    """

    compability_ver = (
        COMPABILITY_VERSION_117
        if midi_cvt.enable_old_exe_format
        else COMPABILITY_VERSION_119
    )

    if not os.path.exists(dist_path):
        os.makedirs(dist_path)

    # 当文件f夹{self.outputPath}/temp/存在时清空其下所有项目，然后创建
    if os.path.exists(f"{dist_path}/temp/"):
        shutil.rmtree(f"{dist_path}/temp/")
    os.makedirs(f"{dist_path}/temp/functions/")
    os.makedirs(f"{dist_path}/temp/structures/")

    # 写入manifest.json
    with open(f"{dist_path}/temp/manifest.json", "w", encoding="utf-8") as f:
        json.dump(
            behavior_mcpack_manifest(
                pack_description=f"{midi_cvt.music_name} 音乐播放包，MCSTRUCTURE(MCPACK) 中继器播放器 - 由 音·创 生成",
                pack_name=midi_cvt.music_name + "播放",
                modules_description=f"无 - 由 音·创 生成",
            ),
            fp=f,
            indent=4,
        )

    # 写入stop.mcfunction
    with open(
        f"{dist_path}/temp/functions/stop.mcfunction", "w", encoding="utf-8"
    ) as f:
        f.write(
            "gamerule commandblocksenabled false\ngamerule commandblocksenabled true"
        )

    # 将命令列表写入文件
    index_file = open(
        f"{dist_path}/temp/functions/index.mcfunction", "w", encoding="utf-8"
    )

    cmd_dict, max_delay, max_multiple_cmd_count = (
        midi_cvt.to_command_list_in_delay_devided_by_instrument(
            player_selector=player,
        )
    )

    base_height = 0

    for inst, cmd_list in cmd_dict.items():
        struct, size, end_pos = commands_to_redstone_delay_structure(
            cmd_list,
            max_delay,
            max_multiple_cmd_count[inst],
            base_block,
            "z+",
            compability_version_=compability_ver,
        )

        bkn = "{}_{}".format(midi_cvt.music_name, inst.replace(".", "-"))

        with open(
            os.path.abspath(
                os.path.join(
                    dist_path,
                    "temp/structures/",
                    "{}_main.mcstructure".format(bkn),
                )
            ),
            "wb+",
        ) as f:
            struct.dump(f)

        index_file.write("structure load {}_main ~ ~{} ~3\n".format(bkn, base_height))
        base_height += 2 + size[1]

    index_file.close()

    if os.path.exists(f"{dist_path}/{midi_cvt.music_name}.mcpack"):
        os.remove(f"{dist_path}/{midi_cvt.music_name}.mcpack")
    compress_zipfile(
        f"{dist_path}/temp/",
        f"{dist_path}/{midi_cvt.music_name}.mcpack",
    )

    shutil.rmtree(f"{dist_path}/temp/")

    return midi_cvt.total_note_count, max_delay
