# -*- coding: utf-8 -*-

"""
音·创 v3 内置的 红石-混合指令音乐链 生成插件 - 红石链分段与结构化
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
from typing import List, Tuple, Literal

from TrimMCStruct import Block, Structure

from Musicreater.builtin_plugins.mcstructure_common.constants import (
    x,
    y,
    z,
    COMPABILITY_VERSION_119,
)
from Musicreater.builtin_plugins.mcstructure_common.structure import forward_IER

from .redstone_chain import RedstoneBlockSpec, redstone_events_to_structure


@dataclass
class RedstoneSegment:
    """红石链切分后的一段结构。"""

    name: str
    """段名，如 'redstone_part_001'"""

    structure: Structure
    """该段的结构对象"""

    size: Tuple[int, int, int]
    """该段的结构尺寸"""

    start_offset: int
    """该段在世界中沿传播轴放置的起始偏移（相对于链起点）"""

    length: int
    """该段沿传播轴的长度"""


def split_redstone_chain(
    specs: List[RedstoneBlockSpec],
    max_segment_length: int = 48,
    axis_: str = "z+",
    base_block: str = "concrete",
    compability_version_: int = COMPABILITY_VERSION_119,
) -> Tuple[List[RedstoneSegment], Structure, Tuple[int, int, int]]:
    """
    生成完整红石-混合结构并按 max_segment_length 沿传播轴切分为多段。

    Parameters
    ------------
    specs: List[RedstoneBlockSpec]
        红石链放置规格列表
    max_segment_length: int
        单段沿传播轴的最大长度阈值
    axis_: str
        红石链延展方向，取值 "z+","z-","x+","x-"
    base_block: str
        结构基底方块
    compability_version_: int
        结构兼容版本号

    Returns
    ---------
    Tuple[List[RedstoneSegment], Structure, Tuple[int,int,int]]
        (段列表, 完整结构, 完整结构尺寸)
    """

    full_struct, full_size, _end_pos, placements = redstone_events_to_structure(
        specs,
        axis_=axis_,
        base_block=base_block,
        compability_version_=compability_version_,
    )

    # 空规格特判
    if not placements:
        return [], full_struct, full_size

    # 由 axis_ 推导延展轴 / 侧轴（与构建器一致）
    if axis_ in ["z+", "Z+", "z-", "Z-"]:
        extensioon_direction = z
        aside_direction = x
        ext_idx = 2  # z 在 (x,y,z) 中的索引
        aside_idx = 0  # x
    elif axis_ in ["x+", "X+", "x-", "X-"]:
        extensioon_direction = x
        aside_direction = z
        ext_idx = 0  # x
        aside_idx = 2  # z
    else:
        raise ValueError(f"axis_({axis_}) 参数错误。")

    # 沿延展轴的坐标范围
    ext_coords = [c[ext_idx] for c, _ in placements]
    ext_min = min(ext_coords)
    ext_max = max(ext_coords)
    total_length = ext_max - ext_min + 1

    # 单段即可容纳
    if total_length <= max_segment_length:
        return (
            [
                RedstoneSegment(
                    name="redstone_part_001",
                    structure=full_struct,
                    size=full_size,
                    start_offset=0,
                    length=total_length,
                )
            ],
            full_struct,
            full_size,
        )

    # 多段切分：沿延展轴按窗口切分
    segments: List[RedstoneSegment] = []
    seg_index = 0
    window_start = ext_min
    while window_start <= ext_max:
        window_end = min(window_start + max_segment_length - 1, ext_max)
        window_length = window_end - window_start + 1

        # 收集落在该窗口内的放置
        window_placements = [
            (c, b) for c, b in placements if window_start <= c[ext_idx] <= window_end
        ]

        if window_placements:
            # 侧轴范围（主链始终位于 aside=0，故 aside_min 通常为 0）
            aside_coords = [c[aside_idx] for c, _ in window_placements]
            aside_min = min(aside_coords)
            aside_max = max(aside_coords)
            aside_extent = aside_max - aside_min + 1

            y_extent = 3  # y 始终为 0..2

            if extensioon_direction == z:
                seg_size = (aside_extent, y_extent, window_length)
            else:  # x
                seg_size = (window_length, y_extent, aside_extent)

            seg_struct = Structure(
                size=seg_size,
                fill=Block(
                    "minecraft", "air", compability_version=compability_version_
                ),
                compability_version=compability_version_,
            )

            for coord, block in window_placements:
                # 延展轴平移至 0；侧轴平移至 0（aside_min 通常为 0，平移为 no-op）；y 不变
                new_coord = list(coord)
                new_coord[ext_idx] = coord[ext_idx] - window_start
                new_coord[aside_idx] = coord[aside_idx] - aside_min
                seg_struct.set_block(tuple(new_coord), block)

            segments.append(
                RedstoneSegment(
                    name=f"redstone_part_{seg_index + 1:03d}",
                    structure=seg_struct,
                    size=seg_size,
                    start_offset=window_start - ext_min,
                    length=window_length,
                )
            )

        window_start = window_end + 1
        seg_index += 1

    return segments, full_struct, full_size
