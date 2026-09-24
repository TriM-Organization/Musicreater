# -*- coding: utf-8 -*-

"""
音·创 v3 内置的 红石-混合指令音乐链 生成插件 - 音符到红石链规格转换
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
from typing import List, Literal, Tuple

from Musicreater import SingleMusic, MineNote
from Musicreater.constants import MM_INSTRUMENT_RANGE_TABLE
from Musicreater.builtin_plugins.to_commands.utils import get_accurate_deviation
from Musicreater.builtin_plugins.to_commands.progressbar import mctick2timestr

from TrimMCStruct import Block, Structure

from Musicreater.builtin_plugins.mcstructure_common.constants import (
    x,
    y,
    z,
    COMPABILITY_VERSION_117,
    COMPABILITY_VERSION_119,
)
from Musicreater.builtin_plugins.mcstructure_common.blocks import (
    form_command_block_in_NBT_struct,
    form_note_block_in_NBT_struct,
    form_repeater_in_NBT_struct,
)
from Musicreater.builtin_plugins.mcstructure_common.structure import (
    forward_IER,
    command_statevalue,
)


@dataclass
class RedstoneBlockSpec:
    """红石链中单个音符的放置规格（与 MineCommand 同构，增加音符盒信息）"""

    delay: int
    """自上一个方块起的延迟（游戏刻），与 MineCommand.delay 语义一致"""

    kind: Literal["note_block", "command_block"]
    """该方块种类：音符盒 或 指令方块"""

    # note_block 专用
    instrument: str = ""
    """音符盒乐器名（已去除 note. 前缀）"""

    note_value: int = 0
    """音符盒音高 0~24"""

    # command_block 专用
    command: str = ""
    """指令方块中的指令文本"""

    annotation: str = ""
    """指令注释"""


def _is_note_block_eligible(
    instrument: str, midi_pitch: float
) -> Tuple[bool, int]:
    """
    依据 MM_INSTRUMENT_RANGE_TABLE 判定是否可用音符盒。

    返回
    ----
    (eligible: bool, note_value: int)
        eligible 为 False 时 note_value 无意义（恒为 0）。

    规则
    ----
    - 乐器必须在 MM_INSTRUMENT_RANGE_TABLE 中 且 以 "note." 为前缀
      （表中存在的 mob.zombie.wood / firework.blast / fire.ignite 等
        虽在表中但不以 "note." 为前缀，故不可用音符盒）
    - midi_pitch 必须在 [low, high] 内（对 (-1, 128) 的范围始终为真）
    - 满足则 note_value = clamp(midi_pitch - low, 0, 24)，
      其中 clamp 使用 int(round(midi_pitch - low)) 以处理浮点 midi_pitch
    """
    entry = MM_INSTRUMENT_RANGE_TABLE.get(instrument)
    if entry is None:
        # 乐器不在表中
        return False, 0

    (low, high), _default = entry

    if not instrument.startswith("note."):
        # 在表中但不是 note.* 前缀（如 mob.zombie.wood / firework.* / fire.*）
        return False, 0

    if not (low <= midi_pitch <= high):
        # 音域外
        return False, 0

    note_value = max(0, min(24, int(round(midi_pitch - low))))
    return True, note_value


def notes_to_redstone_specs(
    music: SingleMusic,
    music_deviation: float = 0,
    minimum_volume: float = 0.01,
    player_selector: str = "@a",
    execute_command_head: str = "execute as {} at @s positioned ~ ~ ~ run ",
) -> List[RedstoneBlockSpec]:
    """
    遍历 music.get_minenotes(start_time=0)，为每个音符生成 RedstoneBlockSpec。

    转换规则
    --------
    - 域内 note.* 乐器 -> note_block
      （instrument 去除 "note." 前缀，note_value=clamp(midi_pitch-low,0,24)）
    - 否则 -> command_block，command 为 playsound 指令
      （复用 to_command_list_in_delay 的指令与注释格式）
    - delay = int(note.precise_tick - previous_precise_tick)，
      首音符 delay = int(note.precise_tick)（与 to_command_list_in_delay 一致，
      delaytime_previous 初值为 0）

    返回
    ----
    List[RedstoneBlockSpec]
        与 MineCommand 列表同构的 RedstoneBlockSpec 列表
    """
    spec_list: List[RedstoneBlockSpec] = []
    delaytime_previous = 0

    for note in music.get_minenotes(start_time=0):
        tickdelay = int(note.precise_tick - delaytime_previous)

        eligible, note_value = _is_note_block_eligible(
            note.instrument, note.midi_pitch
        )

        if eligible:
            spec_list.append(
                RedstoneBlockSpec(
                    delay=tickdelay,
                    kind="note_block",
                    instrument=note.instrument.replace("note.", ""),
                    note_value=note_value,
                )
            )
        else:
            mc_pitch = note.minecraft_pitch(
                get_accurate_deviation(note.instrument, music_deviation)
            )
            command = (
                execute_command_head.format(player_selector)
                + "playsound {} @s ^{:.4f} ^{:.4f} ^{:.4f} 3.0 {:.6f} {}".format(
                    note.instrument,
                    *note.position.position_displacement,
                    mc_pitch,
                    minimum_volume,
                )
            )
            annotation = (
                "[{}] 打击乐音符{}".format(
                    mctick2timestr(note.start_tick), note.instrument
                )
                if note.percussive
                else "[{}] 音符{}:{:.2f}".format(
                    mctick2timestr(note.start_tick), note.instrument, mc_pitch
                )
            )
            spec_list.append(
                RedstoneBlockSpec(
                    delay=tickdelay,
                    kind="command_block",
                    command=command,
                    annotation=annotation,
                )
            )

        delaytime_previous = note.precise_tick

    return spec_list


def redstone_events_to_structure(
    specs: List[RedstoneBlockSpec],
    axis_: str = "z+",
    base_block: str = "concrete",
    compability_version_: int = COMPABILITY_VERSION_119,
) -> Tuple[
    Structure,
    Tuple[int, int, int],
    Tuple[int, int, int],
    List[Tuple[Tuple[int, int, int], Block]],
]:
    """
    由 RedstoneBlockSpec 列表生成红石-混合结构（音符盒 + 指令方块 + 中继器）。

    本函数对 commands_to_redstone_delay_structure 的逻辑进行泛化：
    每个 spec 既可放置音符盒，也可放置指令方块。

    Parameters
    ------------
    specs: List[RedstoneBlockSpec]
        红石链放置规格列表
    axis_: str
        红石链延展方向，取值 "z+","z-","x+","x-"
    base_block: str
        结构基底方块（如 "concrete"）
    compability_version_: int
        结构兼容版本号

    Returns
    ---------
    Tuple[Structure, Tuple[int,int,int], Tuple[int,int,int], List[Tuple[Tuple[int,int,int], Block]]]
        (结构类, 结构占用大小, 终点坐标, placements)
        placements: List[(coordinate, Block)] 记录所有已放置方块，供切分使用。
    """

    # —— 轴向设定（与 commands_to_redstone_delay_structure 一致）——
    if axis_ in ["z+", "Z+"]:
        extensioon_direction = z
        aside_direction = x
        repeater_facing = 2
        forward = True
    elif axis_ in ["z-", "Z-"]:
        extensioon_direction = z
        aside_direction = x
        repeater_facing = 0
        forward = False
    elif axis_ in ["x+", "X+"]:
        extensioon_direction = x
        aside_direction = z
        repeater_facing = 3
        forward = True
    elif axis_ in ["x-", "X-"]:
        extensioon_direction = x
        aside_direction = z
        repeater_facing = 1
        forward = False
    else:
        raise ValueError(f"axis_({axis_}) 参数错误。")

    goahead = forward_IER(forward)

    # —— 起点设定 ——
    # 正向时与原函数一致：延展轴从 1 开始、侧轴从 0 开始（原函数的怪癖，保留以保持一致）。
    # 负向时从 0 开始向负方向延展，构建完成后统一平移至非负坐标。
    if forward:
        pos_now = {
            x: 1 if extensioon_direction == x else 0,
            y: 0,
            z: 1 if extensioon_direction == z else 0,
        }
    else:
        pos_now = {x: 0, y: 0, z: 0}

    chain_list = 0
    placements: List[Tuple[Tuple[int, int, int], Block]] = []

    def _payload_block(
        spec: RedstoneBlockSpec, coord: Tuple[int, int, int]
    ) -> Block:
        """根据 spec.kind 生成音符盒或指令方块（指令方块吸收奇数刻余量）。"""
        if spec.kind == "note_block":
            # 音符盒无 tickDelay 参数，奇数刻余量无法吸收（音符盒固有 2 刻粒度）
            return form_note_block_in_NBT_struct(
                note=spec.note_value,
                coordinate=coord,
                instrument=spec.instrument,
                powered=False,
                compability_version_number=compability_version_,
            )
        # command_block
        return form_command_block_in_NBT_struct(
            command=spec.command,
            coordinate=coord,
            particularValue=command_statevalue(extensioon_direction, forward),
            impluse=0,
            condition=False,
            alwaysRun=False,
            tickDelay=spec.delay % 2,
            customName=spec.annotation,
            compability_version_number=compability_version_,
        )

    for spec in specs:
        if spec.delay > 1:
            # —— 新的红石步（中继器延时，照搬原函数逻辑）——
            single_repeater_value = int(spec.delay / 2) % 4 - 1
            additional_repeater = int(spec.delay / 2 // 4)
            for _ in range(additional_repeater):
                placements.append(
                    (
                        (pos_now[x], 0, pos_now[z]),
                        Block(
                            "minecraft",
                            base_block,
                            compability_version=compability_version_,
                        ),
                    )
                )
                placements.append(
                    (
                        (pos_now[x], 1, pos_now[z]),
                        form_repeater_in_NBT_struct(
                            delay=3,
                            facing=repeater_facing,
                            compability_version_number=compability_version_,
                        ),
                    )
                )
                pos_now[extensioon_direction] += goahead
            if single_repeater_value >= 0:
                placements.append(
                    (
                        (pos_now[x], 0, pos_now[z]),
                        Block(
                            "minecraft",
                            base_block,
                            compability_version=compability_version_,
                        ),
                    )
                )
                placements.append(
                    (
                        (pos_now[x], 1, pos_now[z]),
                        form_repeater_in_NBT_struct(
                            delay=single_repeater_value,
                            facing=repeater_facing,
                            compability_version_number=compability_version_,
                        ),
                    )
                )
                pos_now[extensioon_direction] += goahead
            # 放置音符盒 / 指令方块
            payload_coord = (pos_now[x], 1, pos_now[z])
            placements.append((payload_coord, _payload_block(spec, payload_coord)))
            # 上方红石粉
            placements.append(
                (
                    (pos_now[x], 2, pos_now[z]),
                    Block(
                        "minecraft",
                        "redstone_wire",
                        compability_version=compability_version_,
                    ),
                )
            )
            pos_now[extensioon_direction] += goahead
            chain_list = 1
        else:
            # —— 侧和弦（照搬原函数 else 分支）——
            now_pos_copy = pos_now.copy()
            now_pos_copy[extensioon_direction] -= goahead
            now_pos_copy[aside_direction] += chain_list
            payload_coord = (now_pos_copy[x], 1, now_pos_copy[z])
            placements.append((payload_coord, _payload_block(spec, payload_coord)))
            placements.append(
                (
                    (now_pos_copy[x], 2, now_pos_copy[z]),
                    Block(
                        "minecraft",
                        "redstone_wire",
                        compability_version=compability_version_,
                    ),
                )
            )
            chain_list += 1

    # —— 空规格特判 ——
    if not placements:
        empty_struct = Structure(
            size=(1, 1, 1),
            fill=Block("minecraft", "air", compability_version=compability_version_),
            compability_version=compability_version_,
        )
        return empty_struct, (1, 1, 1), (0, 0, 0), []

    # —— 负方向平移：确保所有坐标非负（size = max+1 公式要求）——
    min_x = min(c[0] for c, _ in placements)
    min_y = min(c[1] for c, _ in placements)
    min_z = min(c[2] for c, _ in placements)
    shift = (
        0 if min_x >= 0 else -min_x,
        0 if min_y >= 0 else -min_y,
        0 if min_z >= 0 else -min_z,
    )
    if any(shift):
        placements = [
            ((c[0] + shift[0], c[1] + shift[1], c[2] + shift[2]), b)
            for c, b in placements
        ]
        pos_now[x] += shift[0]
        pos_now[y] += shift[1]
        pos_now[z] += shift[2]

    # —— 由实际放置计算尺寸 ——
    max_x = max(c[0] for c, _ in placements)
    max_y = max(c[1] for c, _ in placements)
    max_z = max(c[2] for c, _ in placements)
    size = (max_x + 1, max_y + 1, max_z + 1)

    # —— 创建结构并写入方块 ——
    struct = Structure(
        size=size,
        fill=Block("minecraft", "air", compability_version=compability_version_),
        compability_version=compability_version_,
    )
    for coord, block in placements:
        struct.set_block(coord, block)

    end_pos = (pos_now[x], pos_now[y], pos_now[z])
    return struct, size, end_pos, placements
