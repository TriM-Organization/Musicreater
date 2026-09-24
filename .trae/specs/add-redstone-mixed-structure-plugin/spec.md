# 红石-混合指令音乐链生成插件 Spec

> change-id: `add-redstone-mixed-structure-plugin`

## Why

当前 `commands_to_structure` 插件仅能生成「纯指令方块延迟结构」或「计分板指令结构」，缺少以红石中继器为时序骨架、并将音符盒与指令方块混合使用的传统红石音乐播放方式。`MM_INSTRUMENT_RANGE_TABLE`（[constants.py:567-593](../../../Musicreater/constants.py#L567-L593)）以及 `form_note_block_in_NBT_struct`、`form_repeater_in_NBT_struct`、`commands_to_redstone_delay_structure` 等函数在 v3 代码中已定义但均未被实际调用（仅 `old-things/` 遗留代码引用），属于可复用但未被激活的资产。本变更在不破坏既有功能的前提下，激活并泛化这些资产，新增一个生成「红石-混合指令音乐链」的导出插件，并产出可一键导入的 `.mcpack` 包。

## What Changes

- **新增 Library 类型插件 `mcstructure_common_lib`**（模块 `Musicreater/builtin_plugins/mcstructure_common/`）：将 `commands_to_structure` 中可复用的方块生成、结构组装、打包辅助函数提取为共享依赖。
- **迁移既有 `commands_to_structure` 插件**：将其 `common.py` / `mcstructure.py` / `addon.py` 中已迁移至库的实现改为从库导入（局部模块退化为薄重导出层，**严格保持既有公开 API 与行为不变**）。
- **新增导出插件 `to_redstone_mixed_structure`**（模块 `Musicreater/builtin_plugins/to_redstone_mixed_structure/`）：
  - 基于红石中继器构建音乐播放时序骨架；
  - 依据 `MM_INSTRUMENT_RANGE_TABLE` 自动判定：音域内的 `note.*` 乐器用音符盒播放，音域外或非音符盒乐器用指令方块（`playsound`）播放；
  - 按体积/边长阈值自动将红石链切分为多个 `.mcstructure` 片段；
  - 生成「加载器」指令方块结构，通过 `structure` 指令、命令延迟、`execute` 与 `tp` 组合，在玩家加载区域内顺序加载片段；
  - 组装完整 `.mcpack`，含 `index.mcfunction` 与控制玩家位置的辅助 `mcfunction`。
- 依赖关系：新插件 `metainfo.dependencies = ("mcstructure_common_lib", "notedata_to_command_plugin")`。

## Impact

- **Affected specs**: 无既有 spec 受影响（本仓库 `.trae/specs` 此前为空）。
- **Affected code**:
  - 新增：`Musicreater/builtin_plugins/mcstructure_common/`（Library 插件）
  - 新增：`Musicreater/builtin_plugins/to_redstone_mixed_structure/`（导出插件）
  - 修改：`Musicreater/builtin_plugins/commands_to_structure/{common,mcstructure,addon,main}.py`（改为从库导入，保持行为）
  - 复用（只读）：`Musicreater/constants.py`（`MM_INSTRUMENT_RANGE_TABLE`、`MM_INSTRUMENT_DEVIATION_TABLE`）、`Musicreater/builtin_plugins/to_commands/`（`MineCommand`、`get_accurate_deviation`、playsound 指令格式）、`Musicreater/data.py`（`MineNote`）、`TrimMCStruct`（`Structure`/`Block`）

## ADDED Requirements

### Requirement: 共享结构原语库（Library 插件）

系统 SHALL 提供一个 `LIBRARY` 类型插件 `mcstructure_common_lib`，作为结构生成类插件共享的依赖模块，集中提供方块生成、结构组装与打包辅助函数。

#### Scenario: 库提供可复用的方块生成函数
- **GIVEN** 任意需要生成 MCSTRUCTURE 方块的插件依赖了 `mcstructure_common_lib`
- **WHEN** 调用库中的 `form_command_block_in_NBT_struct` / `form_note_block_in_NBT_struct` / `form_repeater_in_NBT_struct`
- **THEN** 返回与原 `commands_to_structure/mcstructure.py` 中行为完全一致的 `TrimMCStruct.Block` 对象

#### Scenario: 库提供打包与尺寸辅助函数
- **GIVEN** 依赖了 `mcstructure_common_lib` 的插件
- **WHEN** 调用 `bottem_side_length_of_smallest_square_bottom_box`、`compress_zipfile`、`behavior_mcpack_manifest`、兼容版本常量
- **THEN** 返回结果与原实现一致，且不依赖 `commands_to_structure` 内部模块

### Requirement: 既有插件迁移至共享库且行为不变

系统 SHALL 将 `commands_to_structure` 插件中已迁入 `mcstructure_common_lib` 的函数改为从库导入，并保持该插件对外的类、函数签名与生成结果完全不变。

#### Scenario: 既有延迟播放器导出结果不变
- **GIVEN** 同一首 `SingleMusic` 与相同的 `McstructureExportConfig`
- **WHEN** 调用迁移后的 `MusicExportToMcstructureWithDelayPlayerPlugin.dump`
- **THEN** 生成的 `.mcstructure` 字节流与迁移前逐字节等价（或结构等价：方块种类、NBT、坐标一致）

### Requirement: 音符盒/指令方块自动判定

新插件 SHALL 依据 `MM_INSTRUMENT_RANGE_TABLE` 对每个音符判定播放方式：
1. 乐器存在于表中、且乐器名以 `note.` 为前缀（即为合法音符盒乐器）、且 `midi_pitch` 落在该乐器音域 `[low, high]` 内 → 使用**音符盒**播放；
2. 乐器存在于表中但 `midi_pitch` 超出音域 → 使用**指令方块**（`playsound`）播放；
3. 乐器不存在于表中，或不以 `note.` 为前缀 → 强制使用**指令方块**（`playsound`）播放。

> 说明：表中 `mob.zombie.wood`、`firework.*`、`fire.*` 等非 `note.` 条目虽在表中且音域为 `(-1, 128)`，但因 Minecraft 音符盒不支持这些乐器，按规则 3 落入指令方块路径。表中 `note.snare`/`note.hat`/`note.bd`/`note.basedrum` 等打击乐器（音域 `(-1, 128)`）视为始终在域内，使用音符盒（note 值取 `clamp(midi_pitch - low, 0, 24)`，打击乐 note 值不影响音色）。

#### Scenario: 域内音符使用音符盒
- **GIVEN** 一个 `MineNote`，乐器 `note.harp`（音域 `(42, 66)`），`midi_pitch = 54`
- **WHEN** 进行音符判定
- **THEN** 生成一个 `noteblock` 方块，`instrument="harp"`，`note = 54 - 42 = 12`

#### Scenario: 域外音符回退指令方块
- **GIVEN** 一个 `MineNote`，乐器 `note.harp`，`midi_pitch = 70`（超出 66）
- **WHEN** 进行音符判定
- **THEN** 生成一个含 `playsound note.harp ...` 的指令方块（复用既有 playsound 指令构造方式）

#### Scenario: 未列入表的乐器强制指令方块
- **GIVEN** 一个 `MineNote`，乐器为 `mob.cat.meow-2`（不在表中）
- **WHEN** 进行音符判定
- **THEN** 生成一个含 `playsound mob.cat.meow-2 ...` 的指令方块

### Requirement: 红石中继器时序骨架

新插件 SHALL 以红石中继器构建时序骨架：相邻音符间的时间差（游戏刻）转换为中继器延迟（1 红石刻 = 2 游戏刻）与指令方块 `tickDelay`（用于消化 1 刻余数）的组合，使信号沿单一轴向传播并依次激活途中的音符盒/指令方块。

#### Scenario: 延迟转换为中继器
- **GIVEN** 两音符间延迟为 5 游戏刻
- **WHEN** 构建红石骨架
- **THEN** 放置 2 个满延迟中继器（各 4 刻，共 4 红石刻=8 刻的满延迟组合中取所需）与 1 个 `tickDelay=1` 的指令方块，总延迟等价于 5 游戏刻（沿用 `commands_to_redstone_delay_structure` 的延迟换算逻辑）

### Requirement: 同时刻音符（和弦）并排放置

新插件 SHALL 将同一游戏刻触发的多个音符沿与传播方向垂直的侧向并排堆叠，使它们被同一红石信号同时激活。

#### Scenario: 和弦并排
- **GIVEN** 同一时刻 3 个音符
- **WHEN** 构建结构
- **THEN** 3 个方块沿侧向相邻排列，共享同一传播轴坐标

### Requirement: 基于体积的结构自动分割

新插件 SHALL 将整条红石音乐链按分割阈值切分为多个 `.mcstructure` 片段，使每个片段的任一维度 ≤ 配置的最大边长（默认 48，确保低于 MC 结构文件 64 上限），且片段在传播轴上首尾相接、红石信号可跨片段连续传递。

#### Scenario: 长链自动切分
- **GIVEN** 一首总延时换算后轴向长度为 200 的红石链，`max_segment_length = 48`
- **WHEN** 执行切分
- **THEN** 产出 `ceil(200/48) = 5` 个片段，命名依加载顺序如 `redstone_part_001.mcstructure` … `redstone_part_005.mcstructure`，片段边界处的红石路径连续

### Requirement: 加载器结构与顺序加载

新插件 SHALL 生成一个「加载器」指令方块结构，内含若干指令方块，每个指令方块通过 `execute as <选择器> at @s run structure load <片段名> <相对坐标>` 在玩家加载区域内放置对应片段；加载器通过命令 `tickDelay` 控制各片段加载时机，并配合 `tp` 指令移动玩家，确保当前播放片段始终处于玩家加载范围内、且下一片段在当前片段信号到达边界前已完成预加载。

#### Scenario: 加载器在玩家处放置片段
- **GIVEN** 已生成 5 个红石片段与一个加载器结构
- **WHEN** 玩家执行 `function index`
- **THEN** 加载器结构被放置于玩家处，其指令方块依次（带延迟）以玩家为参照执行 `structure load` 放置各片段，玩家被 `tp` 沿传播轴前移，整条红石链在玩家加载区内连续成形并开始播放

### Requirement: mcpack 打包规范

新插件 SHALL 生成一个完整 `.mcpack` 行为包，包含以下组件：
- `manifest.json`：行为包清单（复用 `behavior_mcpack_manifest`）；
- `structures/redstone_loader.mcstructure`：加载器指令方块结构；
- `structures/redstone_part_001.mcstructure` … `redstone_part_NNN.mcstructure`：红石音乐片段，按加载顺序命名；
- `functions/index.mcfunction`：初始化指令，放置加载器结构并启动播放；
- `functions/mscply/player_position.mcfunction`：辅助功能，播放期间控制玩家位置（基于计分板计时器 `tp` 玩家沿传播轴跟随播放进度）。

#### Scenario: mcpack 内容完整
- **GIVEN** 一次成功的导出
- **WHEN** 解包生成的 `.mcpack`
- **THEN** 上述所有文件存在，`manifest.json` 合法，`index.mcfunction` 引用的结构名与 `structures/` 下文件名一致

### Requirement: 导出插件注册与配置

新插件 SHALL 以 `FUNCTION_MUSIC_EXPORT` 类型注册，`supported_formats = ("MCPACK",)`，提供 `dump` 与 `stream_dump`，并接受配置项：音调偏移、最小音量、玩家选择器、最大结构边长、传播轴向、旧版指令格式开关等。

#### Scenario: 插件可被发现并调用
- **GIVEN** 已加载新插件与其依赖
- **WHEN** 以 `MCPACK` 格式导出一首 `SingleMusic`
- **THEN** 返回一个可写入的 `.mcpack` 字节流（`stream_dump`）或写入磁盘的 `.mcpack` 文件（`dump`）

## MODIFIED Requirements

### Requirement: commands_to_structure 共享结构原语

`commands_to_structure` 插件 SHALL 不再自身持有方块生成/打包原语的实现，而是从 `mcstructure_common_lib` 导入；其局部 `common.py` / `mcstructure.py` / `addon.py` 保留为薄重导出层以维持向后兼容的导入路径。功能行为与迁移前完全一致。

## REMOVED Requirements

无。
