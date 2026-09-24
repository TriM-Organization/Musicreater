# -*- coding: utf-8 -*-

"""
音·创 v3 内置的 红石-混合指令音乐链 生成插件 - 载入器结构生成
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


from typing import List, Tuple

from TrimMCStruct import Block, Structure

from Musicreater.builtin_plugins.mcstructure_common.constants import (
    COMPABILITY_VERSION_119,
)
from Musicreater.builtin_plugins.mcstructure_common.blocks import (
    form_command_block_in_NBT_struct,
)

from .segment import RedstoneSegment


def _axis_rel(axis_: str, offset: int) -> str:
    """
    返回沿传播轴偏移 offset 的相对坐标字符串。

    约定：offset 为非负的偏移量（绝对值），正负方向由 axis_ 编码。
    - "z+" : ~ ~ ~{offset}      （正 z 方向）
    - "z-" : ~ ~ ~-{offset}     （负 z 方向）
    - "x+" : ~{offset} ~ ~      （正 x 方向）
    - "x-" : ~-{offset} ~ ~     （负 x 方向）
    - offset == 0 时统一返回 ~ ~ ~
    """
    if offset == 0:
        return "~ ~ ~"
    axis_lower = str(axis_).lower()
    if axis_lower == "z+":
        return "~ ~ ~{}".format(offset)
    elif axis_lower == "z-":
        return "~ ~ ~-{}".format(offset)
    elif axis_lower == "x+":
        return "~{} ~ ~".format(offset)
    elif axis_lower == "x-":
        return "~-{} ~ ~".format(offset)
    else:
        raise ValueError("axis_({}) 参数错误。".format(axis_))


def _axis_load_relative_coord(axis_: str, offset: int) -> str:
    """返回 structure load 的相对坐标字符串（沿传播轴偏移 offset）。"""
    return _axis_rel(axis_, offset)


def _axis_tp_delta(axis_: str, offset: int) -> str:
    """返回 tp 的相对位移字符串（与 _axis_load_relative_coord 同构）。"""
    return _axis_rel(axis_, offset)


def build_loader_structure(
    segments: List[RedstoneSegment],
    player_selector: str = "@a",
    axis_: str = "z+",
    marker_name: str = "mscply_origin",
    scoreboard_name: str = "mscply",
    compability_version_: int = COMPABILITY_VERSION_119,
) -> Tuple[Structure, Tuple[int, int, int]]:
    """
    构建加载器指令方块结构。

    加载器为一列沿 Y 轴自底向上堆叠的指令方块（1×N×1 结构）：
      - 前 N 个为“分段加载”方块：第 0 个为脉冲方块（impluse=0，自启动），
        其余为连锁方块（impluse=2）；均 alwaysRun=True、particularValue=1（朝上）。
        每个方块的指令为：
            execute as <marker> at <marker> run structure load <seg.name> <相对坐标>
        其 tickDelay 取该段近似加载时刻与上一段加载时刻之差
        （load_time_i = seg.start_offset * 2，红石刻近似：每外延方块约 2 刻），
        以实现顺序预加载。
      - 顶部 1 个为循环方块（impluse=1，repeating，alwaysRun=True），
        每刻调用 function <scoreboard_name>/player_position 以驱动玩家位置同步。

    注意：触发播放（setblock 红石块于链首）不在加载器中完成，
    而是由 index.mcfunction 直接执行，以实现关注点分离。

    边界情况：segments 为空时，返回仅含 1 个循环方块的 1×1×1 结构。

    Parameters
    ------------
    segments: List[RedstoneSegment]
        红石链分段列表
    player_selector: str
        玩家选择器（当前加载器指令不直接使用，保留以备扩展）
    axis_: str
        红石链传播方向，取值 "z+","z-","x+","x-"
    marker_name: str
        作为固定原点的标记实体名称（armor_stand 的 CustomName）
    scoreboard_name: str
        玩家位置计时器所用记分板名称
    compability_version_: int
        结构兼容版本号

    Returns
    ---------
    Tuple[Structure, Tuple[int, int, int]]
        (加载器结构, 结构尺寸)
    """

    seg_count = len(segments)

    # —— 计算每段近似加载时刻（红石刻）：每外延方块约 2 刻 ——
    load_times = [seg.start_offset * 2 for seg in segments]

    # 结构高度 = N 个分段加载方块 + 1 个循环方块；空段时高度为 1
    height = seg_count + 1 if seg_count > 0 else 1
    size: Tuple[int, int, int] = (1, height, 1)

    struct = Structure(
        size=size,
        fill=Block("minecraft", "air", compability_version=compability_version_),
        compability_version=compability_version_,
    )

    # —— 放置分段加载方块 ——
    prev_load_time = 0  # load_time_{-1} = 0
    for i, seg in enumerate(segments):
        rel_delay = max(0, load_times[i] - prev_load_time)
        prev_load_time = load_times[i]

        impluse = 0 if i == 0 else 2  # 首段脉冲自启，其余连锁
        coord = (0, i, 0)
        rel_coord = _axis_load_relative_coord(axis_, seg.start_offset)
        command = "execute as {m} at {m} run structure load {n} {c}".format(
            m=marker_name, n=seg.name, c=rel_coord
        )

        struct.set_block(
            coord,
            form_command_block_in_NBT_struct(
                command=command,
                coordinate=coord,
                particularValue=1,  # 朝上，使连锁向上传播
                impluse=impluse,
                condition=False,
                alwaysRun=True,
                tickDelay=rel_delay,
                customName=seg.name,
                executeOnFirstTick=False,
                trackOutput=True,
                compability_version_number=compability_version_,
            ),
        )

    # —— 顶部放置循环方块：每刻调用 player_position 函数 ——
    # 说明：按规格约定 particularValue=1（朝上）、alwaysRun=True。
    # 该循环方块自激每刻执行；其与下方连锁列的相互触发属可接受的近似行为。
    repeat_coord = (0, seg_count, 0) if seg_count > 0 else (0, 0, 0)
    repeat_command = "function {}/player_position".format(scoreboard_name)

    struct.set_block(
        repeat_coord,
        form_command_block_in_NBT_struct(
            command=repeat_command,
            coordinate=repeat_coord,
            particularValue=1,  # 朝上，与下方列保持一致
            impluse=1,  # 循环方块
            condition=False,
            alwaysRun=True,
            tickDelay=0,
            customName="mscply_player_position_loop",
            executeOnFirstTick=True,
            trackOutput=True,
            compability_version_number=compability_version_,
        ),
    )

    return struct, size
