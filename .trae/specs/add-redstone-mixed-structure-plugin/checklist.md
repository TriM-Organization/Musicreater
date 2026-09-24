# Checklist

> change-id: `add-redstone-mixed-structure-plugin`
>
> 逐项核验；通过则在 `[ ]` 中填 `x`。未通过项需在 `tasks.md` 新增修复任务并重验。
>
> 验证方式说明：[静态] = 通过源码静态分析验证；[运行时] = 需执行 `verify_redstone_plugin.py` 确认。

## 共享库与迁移

- [x] [静态] `Musicreater/builtin_plugins/mcstructure_common/` 目录与文件齐备（`__init__.py`/`blocks.py`/`structure.py`/`packaging.py`/`constants.py`）
- [x] [静态] `mcstructure_common_lib` 以 `LIBRARY` 类型注册，`metainfo` 字段完整（name/author/description/version/type/license）
- [x] [静态] 库导出的 `form_command_block_in_NBT_struct`/`form_note_block_in_NBT_struct`/`form_repeater_in_NBT_struct` 行为与原实现一致（同一函数对象，`A is B` 为真）
- [x] [静态] 库导出 `bottem_side_length_of_smallest_square_bottom_box`、`compress_zipfile`、`behavior_mcpack_manifest`、`COMPABILITY_VERSION_*`、`commands_to_structure`、`commands_to_redstone_delay_structure`、轴/方向工具
- [x] [静态] `commands_to_structure` 的 `common.py`/`mcstructure.py`/`addon.py` 已改为从库导入/重导出，原导入路径仍可用
- [x] [静态] 迁移后 `MusicExportToMcstructureWithDelayPlayerPlugin` 生成结构与迁移前等价（同一函数对象，行为字节级等价）
- [x] [静态] 既有相关测试：仓库中不存在相关自动化测试，已记录此情况

## 新插件：注册与配置

- [x] [静态] `to_redstone_mixed_structure` 以 `FUNCTION_MUSIC_EXPORT` 注册，`supported_formats = ("MCPACK",)`
- [x] [静态] `metainfo.dependencies = ("mcstructure_common_lib", "notedata_to_command_plugin")`
- [x] [静态] `RedstoneMixedExportConfig` 含必要配置项（音调偏移、最小音量、玩家选择器、最大结构边长默认 48、轴向、基底方块、旧版指令开关）
- [x] [静态] `dump` 与 `stream_dump` 均已实现

## 核心功能：音符判定与红石链

- [x] [静态] 依据 `MM_INSTRUMENT_RANGE_TABLE` 判定：`note.` 前缀 + 音域内 → 音符盒；域外 → 指令方块；不在表/非 `note.` → 指令方块
- [x] [静态] 音符盒 `note` 值 = `clamp(midi_pitch - low, 0, 24)`；`instrument` 去除 `note.` 前缀
- [x] [静态] 指令方块路径复用 `get_accurate_deviation` 与既有 `playsound` 指令格式
- [x] [静态] 红石中继器 + `tickDelay` 组合实现任意游戏刻延迟（沿用 `commands_to_redstone_delay_structure` 换算）
- [x] [静态] 同时刻音符沿侧向并排堆叠

## 结构分割与加载器

- [x] [静态] 按阈值切分，每片段任一维度 ≤ `max_segment_length`（默认 48，< 64）
- [x] [静态] 片段边界红石路径连续（按延展轴窗口切分，窗口内所有放置一并迁移）
- [x] [静态] 片段按加载顺序命名 `redstone_part_001` …
- [x] [静态] 加载器结构含每段一个 `structure load` 指令方块，命令含 `execute as <marker> at <marker> run structure load <name> <相对坐标>`
- [x] [静态] 加载器通过 `tickDelay` 控制加载时机（`tickDelay = seg.start_offset * 2 - prev_load_time`），实现顺序预加载
- [x] [静态] 加载器含 `tp` 指令移动玩家（由 `player_position.mcfunction` 每刻执行 `tp <sel> <轴向偏移>`）
- [x] [静态] 加载器含启动红石脉冲的指令（`index.mcfunction` 中 `setblock <coord> redstone_block`）与每刻调用 `player_position` 的循环指令方块

## mcpack 打包

- [x] [静态] `.mcpack` 含 `manifest.json`（`behavior_mcpack_manifest` 生成）
- [x] [静态] `.mcpack` 含 `structures/redstone_loader.mcstructure`
- [x] [静态] `.mcpack` 含 `structures/redstone_part_001.mcstructure` … `redstone_part_NNN.mcstructure`
- [x] [静态] `.mcpack` 含 `functions/index.mcfunction`（放置加载器结构并初始化计时器）
- [x] [静态] `.mcpack` 含 `functions/mscply/player_position.mcfunction`（按计时器 `tp` 玩家，播毕停止）
- [x] [静态] `index.mcfunction` 引用的结构名与 `structures/` 下文件名一致
- [ ] [运行时] 依赖插件先于新插件加载，无 `PluginDependencyNotFound` 错误

## 端到端

- [ ] [运行时] 以示例 `SingleMusic` 导出 `.mcpack` 成功，解包文件清单与命名自洽
- [ ] [运行时] 全程无破坏既有插件行为
