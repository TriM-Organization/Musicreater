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

from TrimMCStruct import Structure

from ...exceptions import CommandFormatError
from ...main import MidiConvert
from ..archive import behavior_mcpack_manifest, compress_zipfile
from ..main import ConvertConfig
from ..mcstructure import (
    commands_to_structure,
    form_command_block_in_NBT_struct,
    commands_to_redstone_delay_structure,
    COMPABILITY_VERSION_117,
    COMPABILITY_VERSION_119,
)


def to_mcstructure_addon_in_delay(
    midi_cvt: MidiConvert,
    data_cfg: ConvertConfig,
    player: str = "@a",
    max_height: int = 64,
):
    """
    将midi以延迟播放器形式转换为mcstructure结构文件后打包成附加包，并在附加包中生成相应地导入函数

    Parameters
    ----------
    midi_cvt: MidiConvert 对象
        用于转换的MidiConvert对象
    data_cfg: ConvertConfig 对象
        部分转换通用参数
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
        data_cfg.volume_ratio,
        data_cfg.speed_multiplier,
        player,
    )[:2]

    if not os.path.exists(data_cfg.dist_path):
        os.makedirs(data_cfg.dist_path)

    # 当文件f夹{self.outputPath}/temp/存在时清空其下所有项目，然后创建
    if os.path.exists(f"{data_cfg.dist_path}/temp/"):
        shutil.rmtree(f"{data_cfg.dist_path}/temp/")
    os.makedirs(f"{data_cfg.dist_path}/temp/functions/")
    os.makedirs(f"{data_cfg.dist_path}/temp/structures/")

    # 写入manifest.json
    with open(f"{data_cfg.dist_path}/temp/manifest.json", "w", encoding="utf-8") as f:
        json.dump(
            behavior_mcpack_manifest(
                pack_description=f"{midi_cvt.midi_music_name} 音乐播放包，MCSTRUCTURE(MCPACK) 延迟播放器 - 由 音·创 生成",
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

    struct, size, end_pos = commands_to_structure(
        command_list,
        max_height - 1,
        compability_version_=compability_ver,
    )
    with open(
        os.path.abspath(
            os.path.join(
                data_cfg.dist_path,
                "temp/structures/",
                f"{midi_cvt.midi_music_name}_main.mcstructure",
            )
        ),
        "wb+",
    ) as f:
        struct.dump(f)

    del struct

    if data_cfg.progressbar_style:
        scb_name = midi_cvt.midi_music_name[:3] + "Pgb"
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
                    data_cfg.dist_path,
                    "temp/structures/",
                    f"{midi_cvt.midi_music_name}_start.mcstructure",
                )
            ),
            "wb+",
        ) as f:
            struct_a.dump(f)

        index_file.write(f"structure load {midi_cvt.midi_music_name}_start ~ ~ ~1\n")

        pgb_struct, pgbSize, pgbNowPos = commands_to_structure(
            midi_cvt.form_progress_bar(max_delay, scb_name, data_cfg.progressbar_style),
            max_height - 1,
            compability_version_=compability_ver,
        )

        with open(
            os.path.abspath(
                os.path.join(
                    data_cfg.dist_path,
                    "temp/structures/",
                    f"{midi_cvt.midi_music_name}_pgb.mcstructure",
                )
            ),
            "wb+",
        ) as f:
            pgb_struct.dump(f)

        index_file.write(f"structure load {midi_cvt.midi_music_name}_pgb ~ ~1 ~1\n")

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
                    data_cfg.dist_path,
                    "temp/structures/",
                    f"{midi_cvt.midi_music_name}_reset.mcstructure",
                )
            ),
            "wb+",
        ) as f:
            struct_a.dump(f)

        del struct_a, pgb_struct

        index_file.write(
            f"structure load {midi_cvt.midi_music_name}_reset ~{pgbSize[0] + 2} ~ ~1\n"
        )

        index_file.write(
            f"structure load {midi_cvt.midi_music_name}_main ~{pgbSize[0] + 2} ~1 ~1\n"
        )

    else:
        index_file.write(f"structure load {midi_cvt.midi_music_name}_main ~ ~ ~1\n")

    index_file.close()

    if os.path.exists(f"{data_cfg.dist_path}/{midi_cvt.midi_music_name}.mcpack"):
        os.remove(f"{data_cfg.dist_path}/{midi_cvt.midi_music_name}.mcpack")
    compress_zipfile(
        f"{data_cfg.dist_path}/temp/",
        f"{data_cfg.dist_path}/{midi_cvt.midi_music_name}.mcpack",
    )

    shutil.rmtree(f"{data_cfg.dist_path}/temp/")

    return len(command_list), max_delay




def to_mcstructure_addon_in_redstone_cd(
    midi_cvt: MidiConvert,
    data_cfg: ConvertConfig,
    player: str = "@a",
    max_height: int = 65,
):
    """
    将midi以延迟播放器形式转换为mcstructure结构文件后打包成附加包，并在附加包中生成相应地导入函数

    Parameters
    ----------
    midi_cvt: MidiConvert 对象
        用于转换的MidiConvert对象
    data_cfg: ConvertConfig 对象
        部分转换通用参数
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

    command_list, max_delay,max_together = midi_cvt.to_command_list_in_delay(
        data_cfg.volume_ratio,
        data_cfg.speed_multiplier,
        player,
    )

    if not os.path.exists(data_cfg.dist_path):
        os.makedirs(data_cfg.dist_path)

    # 当文件f夹{self.outputPath}/temp/存在时清空其下所有项目，然后创建
    if os.path.exists(f"{data_cfg.dist_path}/temp/"):
        shutil.rmtree(f"{data_cfg.dist_path}/temp/")
    os.makedirs(f"{data_cfg.dist_path}/temp/functions/")
    os.makedirs(f"{data_cfg.dist_path}/temp/structures/")

    # 写入manifest.json
    with open(f"{data_cfg.dist_path}/temp/manifest.json", "w", encoding="utf-8") as f:
        json.dump(
            behavior_mcpack_manifest(
                pack_description=f"{midi_cvt.midi_music_name} 音乐播放包，MCSTRUCTURE(MCPACK) 延迟播放器 - 由 音·创 生成",
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

    struct, size, end_pos = commands_to_redstone_delay_structure(
        command_list,
        max_delay,
        max_together,
        compability_version_=compability_ver,
    )
    with open(
        os.path.abspath(
            os.path.join(
                data_cfg.dist_path,
                "temp/structures/",
                f"{midi_cvt.midi_music_name}_main.mcstructure",
            )
        ),
        "wb+",
    ) as f:
        struct.dump(f)

    del struct

    if data_cfg.progressbar_style:
        scb_name = midi_cvt.midi_music_name[:3] + "Pgb"
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
                    data_cfg.dist_path,
                    "temp/structures/",
                    f"{midi_cvt.midi_music_name}_start.mcstructure",
                )
            ),
            "wb+",
        ) as f:
            struct_a.dump(f)

        index_file.write(f"structure load {midi_cvt.midi_music_name}_start ~ ~ ~1\n")

        pgb_struct, pgbSize, pgbNowPos = commands_to_structure(
            midi_cvt.form_progress_bar(max_delay, scb_name, data_cfg.progressbar_style),
            max_height - 1,
            compability_version_=compability_ver,
        )

        with open(
            os.path.abspath(
                os.path.join(
                    data_cfg.dist_path,
                    "temp/structures/",
                    f"{midi_cvt.midi_music_name}_pgb.mcstructure",
                )
            ),
            "wb+",
        ) as f:
            pgb_struct.dump(f)

        index_file.write(f"structure load {midi_cvt.midi_music_name}_pgb ~ ~1 ~1\n")

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
                    data_cfg.dist_path,
                    "temp/structures/",
                    f"{midi_cvt.midi_music_name}_reset.mcstructure",
                )
            ),
            "wb+",
        ) as f:
            struct_a.dump(f)

        del struct_a, pgb_struct

        index_file.write(
            f"structure load {midi_cvt.midi_music_name}_reset ~{pgbSize[0] + 2} ~ ~1\n"
        )

        index_file.write(
            f"structure load {midi_cvt.midi_music_name}_main ~{pgbSize[0] + 2} ~1 ~1\n"
        )

    else:
        index_file.write(f"structure load {midi_cvt.midi_music_name}_main ~ ~ ~1\n")

    index_file.close()

    if os.path.exists(f"{data_cfg.dist_path}/{midi_cvt.midi_music_name}.mcpack"):
        os.remove(f"{data_cfg.dist_path}/{midi_cvt.midi_music_name}.mcpack")
    compress_zipfile(
        f"{data_cfg.dist_path}/temp/",
        f"{data_cfg.dist_path}/{midi_cvt.midi_music_name}.mcpack",
    )

    shutil.rmtree(f"{data_cfg.dist_path}/temp/")

    return len(command_list), max_delay
