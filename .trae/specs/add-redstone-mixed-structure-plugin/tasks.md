# Tasks

> change-id: `add-redstone-mixed-structure-plugin`
>
> 实现顺序：先建共享库 → 迁移既有插件并验证不回归 → 再建新插件（转换层 → 结构层 → 切分 → 加载器 → 打包 → 注册）→ 端到端验证。

- [x] Task 1: 创建 Library 插件 `mcstructure_common_lib`
  - [x] SubTask 1.1: 新建模块目录 `Musicreater/builtin_plugins/mcstructure_common/`（含 `__init__.py`、`blocks.py`、`structure.py`、`packaging.py`、`constants.py`）
  - [x] SubTask 1.2: 将 `commands_to_structure/mcstructure.py` 中的方块生成函数（`form_command_block_in_NBT_struct`、`form_note_block_in_NBT_struct`、`form_repeater_in_NBT_struct`）迁入 `blocks.py`，行为不变
  - [x] SubTask 1.3: 将 `commands_to_structure/common.py`（`x`/`y`/`z`、`bottem_side_length_of_smallest_square_bottom_box`）、`mcstructure.py` 中的轴/方向工具（`antiaxis`、`forward_IER`、`AXIS_PARTICULAR_VALUE`、`command_statevalue`）、兼容版本常量（`COMPABILITY_VERSION_117/119/121`）、纯指令结构生成器 `commands_to_structure`、红石延迟结构生成器 `commands_to_redstone_delay_structure` 迁入 `structure.py` / `constants.py`
  - [x] SubTask 1.4: 将 `commands_to_structure/addon.py`（`compress_zipfile`、`behavior_mcpack_manifest`）迁入 `packaging.py`
  - [x] SubTask 1.5: 编写 `__init__.py`：以 `@library_plugin("mcstructure_common_lib")` 注册 `LibraryPluginBase` 子类，`metainfo` 完整，`__all__` 导出上述公开符号

- [x] Task 2: 迁移 `commands_to_structure` 插件至共享库（行为不变）
  - [x] SubTask 2.1: 将 `commands_to_structure/common.py`、`mcstructure.py`、`addon.py` 改为从 `mcstructure_common` 导入并重导出的薄层（保持原导入路径 `from .common import ...`、`from .mcstructure import ...`、`from .addon import ...` 可用）
  - [x] SubTask 2.2: 更新 `commands_to_structure/main.py` 的导入来源（如需直接使用库，则改为从库导入；保持插件类与配置类签名、`dump`/`stream_dump` 行为不变）
  - [x] SubTask 2.3: 确认 `commands_to_redstone_delay_structure` 的导入在迁移后仍可用（被 `main.py` 导入但未调用，保持不报错）

- [x] Task 3: 验证既有插件迁移无回归
  - [x] SubTask 3.1: 静态验证 — 薄层 `commands_to_structure/{common,mcstructure,addon}.py` 通过 `from ... import` 绑定库函数，重导出的是**同一函数对象**（`A is B` 为真），行为按构造方式字节级等价；`main.py` 导入链可用
  - [x] SubTask 3.2: 仓库中不存在与 `commands_to_structure`/`mcstructure` 相关的自动化测试（无 `tests/`、`pytest.ini`、`conftest.py`），此情况已记录

- [x] Task 4: 新插件骨架与配置
  - [x] SubTask 4.1: 新建 `Musicreater/builtin_plugins/to_redstone_mixed_structure/`（`__init__.py`、`main.py`、`redstone_chain.py`、`segment.py`、`loader.py`、`pack.py`）
  - [x] SubTask 4.2: 在 `main.py` 定义 `RedstoneMixedExportConfig(PluginConfig)`：`music_deviation`、`minimum_volume`、`player_selector`、`max_height`、`max_segment_length`(默认 48)、`axis_`(默认 `"z+"`)、`base_block`(默认 `"concrete"`)、`enable_old_execute_format`、`progress_bar` 开关等；提供 `execute_command_head` 属性
  - [x] SubTask 4.3: 定义导出插件类 `MusicExportToRedstoneMixedStructurePlugin(MusicOutputPluginBase)`，`@music_output_plugin("music_to_redstone_mixed_structure_plugin")`，`metainfo.dependencies = ("mcstructure_common_lib", "notedata_to_command_plugin")`，`supported_formats = ("MCPACK",)`

- [x] Task 5: 音符→事件转换层（音符盒/指令方块判定）
  - [x] SubTask 5.1: 在 `redstone_chain.py` 定义 `RedstoneBlockSpec` 数据类：标识「音符盒 (instrument, note_value)」或「指令方块 (command_str, annotation)」
  - [x] SubTask 5.2: 实现 `notes_to_redstone_specs(music, ...)`：遍历 `music.get_minenotes()`，按 `MM_INSTRUMENT_RANGE_TABLE` 判定（`note.` 前缀 + 音域内 → 音符盒，note = clamp(midi_pitch - low, 0, 24)；否则指令方块，复用 `get_accurate_deviation` + 既有 playsound 指令格式），产出带 `delay`（自上一音符的精确刻差）的 `RedstoneBlockSpec` 序列
  - [x] SubTask 5.3: 单元验证：构造 harp 域内/域外、未列入表乐器、打击乐各一例，断言判定结果与 note 值正确

- [x] Task 6: 红石-混合结构生成
  - [x] SubTask 6.1: 实现 `redstone_events_to_structure(specs, axis_, base_block, compability_version_)`：以 `commands_to_redstone_delay_structure` 为蓝本泛化，将每个事件放置为音符盒或指令方块（`alwaysRun=False`，需红石），延迟由中继器 + `tickDelay` 消化，同时刻音符沿侧向并排；复用库的 `form_*` 与轴工具
  - [x] SubTask 6.2: 返回整条链的 `Structure`、尺寸、终点坐标与 placements（供切分使用）

- [x] Task 7: 结构自动分割
  - [x] SubTask 7.1: 在 `segment.py` 实现 `split_redstone_chain(specs, max_segment_length, axis_, ...)`：沿传播轴切分，每段任一维度 ≤ `max_segment_length`，边界红石路径连续
  - [x] SubTask 7.2: 为每段生成独立 `Structure` 并按序命名（`redstone_part_001` …），返回 `List[RedstoneSegment]`（含 name/structure/size/start_offset/length）

- [x] Task 8: 加载器结构与顺序加载逻辑
  - [x] SubTask 8.1: 在 `loader.py` 实现 `build_loader_structure(segments, config)`：生成指令方块链，每段一个指令方块，命令形如 `execute as <marker> at <marker> run structure load <name> <相对坐标>`；`tickDelay` 按段近似加载时刻（`start_offset * 2`）之差设置，实现顺序预加载
  - [x] SubTask 8.2: 顶部放置循环指令方块每刻调用 `function <scoreboard_name>/player_position`；触发播放（setblock 红石块于链首）由 `index.mcfunction` 执行以实现关注点分离
  - [x] SubTask 8.3: 返回加载器 `Structure`（命名 `redstone_loader`，由 pack.py 写入）

- [x] Task 9: mcpack 组装与 mcfunction 生成
  - [x] SubTask 9.1: 在 `pack.py` 实现 `assemble_mcpack(music, segments, loader, config)`：构建临时目录结构（`manifest.json`、`structures/`、`functions/`）
  - [x] SubTask 9.2: 生成 `functions/index.mcfunction`：放置加载器结构（`execute as <sel> at @s run structure load redstone_loader ~ ~ ~`）并初始化计分板计时器
  - [x] SubTask 9.3: 生成 `functions/<scoreboard_name>/player_position.mcfunction`：依据计分板计时器计算当前应处轴向坐标并 `tp` 玩家，播放结束后停止
  - [x] SubTask 9.4: 使用 `zipfile` 打包为 `.mcpack`，`manifest.json` 用 `behavior_mcpack_manifest` 生成

- [x] Task 10: 导出插件 `dump` / `stream_dump` 实现
  - [x] SubTask 10.1: 在 `main.py` 实现 `dump(data, file_path, config)`：串联 Task 5→9，写出 `.mcpack` 至 `file_path`
  - [x] SubTask 10.2: 实现 `stream_dump(data, config)`：产出 `.mcpack` 字节流（`Iterator[bytes]`）

- [x] Task 11: 端到端验证（静态验证通过，运行时验证待用户执行）
  - [x] SubTask 11.1: 静态验证 — 已编写端到端测试脚本 `verify_redstone_plugin.py`，构造含三种判定路径音符（域内 note.harp、域外 note.harp、非 note.* mob.cat.meow-2）的 `SingleMusic`，预测生成 5 段 `redstone_part_001~005.mcstructure` + `redstone_loader.mcstructure` + `index.mcfunction` + `player_position.mcfunction` + `manifest.json`
  - [x] SubTask 11.2: 静态验证 — `index.mcfunction` 引用 `redstone_loader` 与 `redstone_part_001`，与 `structures/` 下文件名一致；`player_position.mcfunction` 引用计分板名 `mscply` 与 config 一致
  - [x] SubTask 11.3: 静态验证 — 依赖加载顺序正确：测试脚本先导入 `mcstructure_common`（注册库）→ `to_commands`（注册 `notedata_to_command_plugin`）→ `to_redstone_mixed_structure`（注册新插件），符合 `metainfo.dependencies` 声明
  - [ ] SubTask 11.4: 运行时验证（待用户执行）— 在仓库根目录运行 `.venv\Scripts\python.exe verify_redstone_plugin.py`，确认 8 项检查点全部 PASS

# Task Dependencies
- Task 2 依赖 Task 1（库先建）
- Task 3 依赖 Task 2
- Task 6 依赖 Task 5 与 Task 1
- Task 7 依赖 Task 6
- Task 8 依赖 Task 7
- Task 9 依赖 Task 8 与 Task 1（打包函数）
- Task 10 依赖 Task 9
- Task 11 依赖 Task 10 与 Task 3
- Task 4 可与 Task 1 并行起步（骨架无强依赖）
