# -*- coding: utf-8 -*-

"""
音·创 v3 内置的 红石-混合指令音乐链 生成插件 - mcpack 打包
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


import json
import os
import shutil
import tempfile
import zipfile
from io import BytesIO
from typing import List

from Musicreater import SingleMusic
from Musicreater.builtin_plugins.mcstructure_common.packaging import (
    behavior_mcpack_manifest,
)

from .segment import RedstoneSegment
from .loader import (
    build_loader_structure,  # noqa: F401  保留以供外部按规格导入
    _axis_load_relative_coord,  # noqa: F401
    _axis_tp_delta,  # noqa: F401
)


def _trigger_coord(axis_: str) -> str:
    """
    返回 index.mcfunction 中 setblock 红石块的相对坐标（用以触发链首播放）。

    约定（最佳近似，已记录假设）：
    - "z+" : ~ ~1 ~    （红石块置于链首上方 y+1）
    - "z-" : ~ ~1 ~1   （链首在 z 负方向，红石块置于 z+1 处上方）
    - "x+" : ~ ~1 ~
    - "x-" : ~1 ~1 ~   （链首在 x 负方向，红石块置于 x+1 处上方）
    """
    axis_lower = str(axis_).lower()
    if axis_lower == "z+":
        return "~ ~1 ~"
    elif axis_lower == "z-":
        return "~ ~1 ~1"
    elif axis_lower == "x+":
        return "~ ~1 ~"
    elif axis_lower == "x-":
        return "~1 ~1 ~"
    else:
        raise ValueError("axis_({}) 参数错误。".format(axis_))


def _generate_index_mcfunction(
    segments: List[RedstoneSegment],
    player_selector: str,
    axis_: str,
    marker_name: str,
    scoreboard_name: str,
) -> str:
    """
    生成 functions/index.mcfunction 内容。

    流程：
      1. 在玩家处召唤标记实体（armor_stand，作为固定原点）
      2. 添加常加载区以保证加载器区域始终被加载
      3. 加载载入器结构 redstone_loader
      4. 加载第一段红石链（seg0，通常位于原点）
      5. setblock 红石块于链首触发播放
      6. 初始化计分板计时器

    注意：本函数产出的指令为“最佳近似”——标记实体选择器直接以
    marker_name 占位（与 loader.py 保持一致），实际部署时可替换为
    @e[name=<marker_name>] 形式的选择器。
    """

    lines: List[str] = ["# 由 to_redstone_mixed_structure 生成"]

    # 1. 召唤标记实体（带名、无重力、隐形的标记型 armor_stand）
    lines.append(
        'summon armor_stand ~ ~ ~ {{CustomName:"{n}",Marker:1b,NoGravity:1b,'
        "Invisible:1b,Invulnerable:1b}}".format(n=marker_name)
    )

    # 2. 常加载区（覆盖加载器与近场红石链）
    lines.append("tickingarea add ~ ~ ~ ~ ~ ~ {n}_area".format(n=marker_name))

    # 3. 加载载入器结构（于玩家处放置）
    lines.append(
        "execute as {sel} at @s run structure load redstone_loader ~ ~ ~".format(
            sel=player_selector
        )
    )

    # 4. 加载第一段红石链
    if segments:
        seg0 = segments[0]
        rel0 = _axis_load_relative_coord(axis_, seg0.start_offset)
        lines.append(
            "execute as {m} at {m} run structure load {n} {c}".format(
                m=marker_name, n=seg0.name, c=rel0
            )
        )

    # 5. setblock 红石块于链首触发播放
    lines.append(
        "execute as {m} at {m} run setblock {c} redstone_block".format(
            m=marker_name, c=_trigger_coord(axis_)
        )
    )

    # 6. 初始化计分板计时器
    lines.append("scoreboard objectives add {sb} dummy".format(sb=scoreboard_name))
    lines.append(
        "scoreboard players set {sel} {sb} 0".format(sel=player_selector, sb=scoreboard_name)
    )

    return "\n".join(lines) + "\n"


def _generate_player_position_mcfunction(
    segments: List[RedstoneSegment],
    player_selector: str,
    axis_: str,
    marker_name: str,
    scoreboard_name: str,
) -> str:
    """
    生成 functions/<scoreboard_name>/player_position.mcfunction 内容。

    每刻由加载器顶部循环方块调用一次：
      - 计时器 +1
      - 依据当前时刻落在哪一段的 [t_i, t_{i+1}] 区间，
        将玩家 tp 至该段中心（相对 marker 的轴向偏移）
      - 超过总时长后输出结束提示（不再 tp）

    时间近似：每外延方块约 2 红石刻，故 t_i = start_offset * 2，
    t_{i+1} = (start_offset + length) * 2。
    """

    lines: List[str] = ["# 由 to_redstone_mixed_structure 生成"]

    # 计时器自增
    lines.append(
        "scoreboard players add {sel} {sb} 1".format(
            sel=player_selector, sb=scoreboard_name
        )
    )

    total_end_tick = 0

    # 每段一个条件 tp
    for seg in segments:
        t_i = seg.start_offset * 2
        t_end = (seg.start_offset + seg.length) * 2
        total_end_tick = max(total_end_tick, t_end)
        center = seg.start_offset + seg.length // 2
        center_coord = _axis_tp_delta(axis_, center)
        lines.append(
            "execute if score {sel} {sb} matches {a}..{b} run execute as {m} at {m} "
            "run tp {sel} {c}".format(
                sel=player_selector,
                sb=scoreboard_name,
                a=t_i,
                b=t_end,
                m=marker_name,
                c=center_coord,
            )
        )

    # 结束提示
    if segments:
        lines.append(
            "execute if score {sel} {sb} matches {t}.. run say 音乐播放结束".format(
                sel=player_selector, sb=scoreboard_name, t=total_end_tick
            )
        )

    return "\n".join(lines) + "\n"


def assemble_mcpack(
    music: SingleMusic,
    segments: List[RedstoneSegment],
    loader_structure,
    config,
) -> bytes:
    """
    组装完整 .mcpack 行为包并返回其字节内容。

    产出的包结构：
        manifest.json
        structures/
            redstone_loader.mcstructure
            redstone_part_001.mcstructure
            redstone_part_002.mcstructure
            ...
        functions/
            index.mcfunction
            <scoreboard_name>/
                player_position.mcfunction

    Parameters
    ------------
    music: SingleMusic
        音乐数据（用以取乐曲名作为包名）
    segments: List[RedstoneSegment]
        红石链分段列表
    loader_structure: Structure
        加载器结构（由 build_loader_structure 产出）
    config: RedstoneMixedExportConfig
        导出配置（取 player_selector / axis_ / scoreboard_name 等字段）

    Returns
    ---------
    bytes
        打包好的 mcpack 字节流
    """

    player_selector = config.player_selector
    axis_ = config.axis_
    marker_name = "mscply_origin"
    scoreboard_name = config.scoreboard_name

    temp_dir = tempfile.mkdtemp(prefix="mscply_pack_")
    try:
        # —— manifest.json ——
        pack_name = music.music_name or "RedstoneMusic"
        pack_description = "音·创 红石-混合指令音乐链：{}".format(pack_name)
        manifest = behavior_mcpack_manifest(
            format_version=2,
            pack_description=pack_description,
            pack_version=[0, 0, 1],
            pack_name=pack_name,
            pack_engine_version=[1, 21, 0],
        )
        with open(os.path.join(temp_dir, "manifest.json"), "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

        # —— structures/ ——
        structures_dir = os.path.join(temp_dir, "structures")
        os.makedirs(structures_dir, exist_ok=True)

        # 加载器结构
        with open(
            os.path.join(structures_dir, "redstone_loader.mcstructure"), "wb"
        ) as f:
            loader_structure.dump(f)

        # 各红石段结构
        for seg in segments:
            with open(
                os.path.join(structures_dir, "{}.mcstructure".format(seg.name)), "wb"
            ) as f:
                seg.structure.dump(f)

        # —— functions/ ——
        functions_dir = os.path.join(temp_dir, "functions")
        os.makedirs(functions_dir, exist_ok=True)

        index_content = _generate_index_mcfunction(
            segments, player_selector, axis_, marker_name, scoreboard_name
        )
        with open(os.path.join(functions_dir, "index.mcfunction"), "w", encoding="utf-8") as f:
            f.write(index_content)

        # 函数子目录名与 scoreboard_name 一致，以匹配
        # function <scoreboard_name>/player_position 的调用路径
        sb_func_dir = os.path.join(functions_dir, scoreboard_name)
        os.makedirs(sb_func_dir, exist_ok=True)
        pp_content = _generate_player_position_mcfunction(
            segments, player_selector, axis_, marker_name, scoreboard_name
        )
        with open(
            os.path.join(sb_func_dir, "player_position.mcfunction"), "w", encoding="utf-8"
        ) as f:
            f.write(pp_content)

        # —— 在内存中打包为 zip ——
        buf = BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zipf:
            pre_len = len(temp_dir.rstrip(os.sep)) + 1
            for parent, _dirnames, filenames in os.walk(temp_dir):
                for filename in filenames:
                    pathfile = os.path.join(parent, filename)
                    arc_name = pathfile[pre_len:].replace(os.sep, "/")
                    zipf.write(pathfile, arc_name)

        return buf.getvalue()
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
