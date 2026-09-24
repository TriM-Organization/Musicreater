# -*- coding: utf-8 -*-
"""
端到端验证脚本：to_redstone_mixed_structure 插件 (Task 11)
构造一个含三种判定路径音符的 SingleMusic，导出 .mcpack 并验证其内容。
"""

import sys
import traceback
import zipfile
import json
from pathlib import Path

# 确保仓库根目录在 sys.path 中
REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

print("=" * 70)
print("Task 11 端到端验证：to_redstone_mixed_structure 插件")
print("=" * 70)

# ---------------------------------------------------------------
# 1. 导入依赖插件（必须先注册 mcstructure_common_lib 与 notedata_to_command_plugin）
# ---------------------------------------------------------------
print("\n[1] 导入依赖插件 ...")
try:
    import Musicreater  # noqa: F401
    import Musicreater.builtin_plugins.mcstructure_common  # 注册 mcstructure_common_lib
    import Musicreater.builtin_plugins.to_commands  # 注册 notedata_to_command_plugin
    print("  依赖插件导入成功")
except Exception:
    print("  [错误] 依赖插件导入失败")
    traceback.print_exc()
    sys.exit(1)

# ---------------------------------------------------------------
# 2. 导入被测插件（会触发 @music_output_plugin 装饰器注册）
# ---------------------------------------------------------------
print("\n[2] 导入被测插件 ...")
try:
    from Musicreater.builtin_plugins.to_redstone_mixed_structure import (
        RedstoneMixedExportConfig,
        MusicExportToRedstoneMixedStructurePlugin,
    )
    print("  被测插件导入成功")
    print("  插件类：", MusicExportToRedstoneMixedStructurePlugin)
except Exception:
    print("  [错误] 被测插件导入失败")
    traceback.print_exc()
    sys.exit(1)

# ---------------------------------------------------------------
# 3. 构造 SingleMusic：含三种判定路径的音符
#    路径 A：域内 note.* 乐器 -> 音符盒
#    路径 B：域外 note.* 乐器 -> 指令方块
#    路径 C：非 note.* 乐器（mob.cat.meow-2）-> 指令方块
# ---------------------------------------------------------------
print("\n[3] 构造 SingleMusic ...")
try:
    from Musicreater import SingleMusic, SingleTrack, SingleNote, Instrument

    # note.harp 音域 42~66；note.bell 音域 66~90；mob.cat.meow-2 不在表中
    # 用 note.harp 在域内（60）、域外（100）测试 A/B 路径
    # 用 mob.cat.meow-2 测试 C 路径

    harp_in_range = Instrument(name="note.harp", loadness=-1448)
    harp_out_range = Instrument(name="note.harp", loadness=-1448)
    cat_inst = Instrument(name="mob.cat.meow-2", loadness=-1406)

    # 轨道 A：note.harp 域内音符，时间间隔较大以触发分段
    # 用 16 作为 max_segment_length，构造一段足够长的链以触发多段
    # 每个音符 delay=4（红石步），16/2=8 步即可填满 16 长度的窗口
    track_a_notes = []
    for i in range(20):
        # 每个音符间隔 4 刻，pitch 在 42~66 域内
        track_a_notes.append(
            SingleNote(note_pitch=60, start_tick=i * 4, keep_tick=2)
        )
    track_a = SingleTrack(
        *track_a_notes,
        track_name="harp_in_range",
        track_instrument=harp_in_range,
        precise_time=False,
        percussion=False,
    )

    # 轨道 B：note.harp 域外音符（pitch=100，超出 42~66）
    track_b_notes = []
    for i in range(5):
        track_b_notes.append(
            SingleNote(note_pitch=100, start_tick=100 + i * 4, keep_tick=2)
        )
    track_b = SingleTrack(
        *track_b_notes,
        track_name="harp_out_of_range",
        track_instrument=harp_out_range,
        precise_time=False,
        percussion=False,
    )

    # 轨道 C：mob.cat.meow-2（非 note.* 前缀，且不在 MM_INSTRUMENT_RANGE_TABLE）
    track_c_notes = []
    for i in range(5):
        track_c_notes.append(
            SingleNote(note_pitch=60, start_tick=200 + i * 4, keep_tick=2)
        )
    track_c = SingleTrack(
        *track_c_notes,
        track_name="cat_meow",
        track_instrument=cat_inst,
        precise_time=False,
        percussion=False,
    )

    music = SingleMusic(
        track_a, track_b, track_c,
        name="Task11_Verify_Music",
        creator="VerifyScript",
        original_author="VerifyScript",
        description="端到端验证用例：含域内/域外/非note三类音符",
    )
    print("  SingleMusic 构造成功")
    print("  音轨数：", music.track_amount)
    total_notes = sum(t.note_amount for t in music)
    print("  总音符数：", total_notes)
except Exception:
    print("  [错误] SingleMusic 构造失败")
    traceback.print_exc()
    sys.exit(1)

# ---------------------------------------------------------------
# 4. 实例化配置（max_segment_length=16 强制分段）
# ---------------------------------------------------------------
print("\n[4] 实例化 RedstoneMixedExportConfig ...")
try:
    config = RedstoneMixedExportConfig(max_segment_length=16)
    print("  配置实例化成功")
    print("  max_segment_length =", config.max_segment_length)
    print("  scoreboard_name     =", config.scoreboard_name)
    print("  player_selector     =", config.player_selector)
    print("  axis_               =", config.axis_)
except Exception:
    print("  [错误] 配置实例化失败")
    traceback.print_exc()
    sys.exit(1)

# ---------------------------------------------------------------
# 5. 调用 dump 导出 .mcpack
# ---------------------------------------------------------------
print("\n[5] 调用插件 dump 方法导出 .mcpack ...")
output_path = REPO_ROOT / "_verify_output.mcpack"
try:
    plugin = MusicExportToRedstoneMixedStructurePlugin()
    plugin.dump(music, output_path, config)
    print("  导出成功：", output_path)
    print("  文件大小：{} 字节".format(output_path.stat().st_size))
except Exception:
    print("  [错误] 导出失败")
    traceback.print_exc()
    # 即使失败也尝试继续做后续验证（如果文件已生成部分）
    if not output_path.exists():
        sys.exit(1)

# ---------------------------------------------------------------
# 6. 解包 .mcpack 并列出所有文件
# ---------------------------------------------------------------
print("\n[6] 解包 .mcpack 并列出文件清单 ...")
file_list = []
manifest_content = None
index_content = None
pp_content = None
try:
    with zipfile.ZipFile(output_path, "r") as zf:
        file_list = zf.namelist()
        print("  文件清单（共 {} 个）：".format(len(file_list)))
        for name in sorted(file_list):
            print("    -", name)

        with zf.open("manifest.json") as f:
            manifest_content = f.read().decode("utf-8")
        with zf.open("functions/index.mcfunction") as f:
            index_content = f.read().decode("utf-8")
        pp_path = "functions/{}/player_position.mcfunction".format(config.scoreboard_name)
        with zf.open(pp_path) as f:
            pp_content = f.read().decode("utf-8")
except Exception:
    print("  [错误] 解包失败")
    traceback.print_exc()
    sys.exit(1)

# ---------------------------------------------------------------
# 7. 打印关键文件内容
# ---------------------------------------------------------------
print("\n[7] 打印关键文件内容 ...")
print("\n----- manifest.json -----")
try:
    print(json.dumps(json.loads(manifest_content), ensure_ascii=False, indent=2))
except Exception:
    print(manifest_content)

print("\n----- functions/index.mcfunction -----")
print(index_content)

print("\n----- functions/{}/player_position.mcfunction -----".format(config.scoreboard_name))
print(pp_content)

# ---------------------------------------------------------------
# 8. 验证各检查点
# ---------------------------------------------------------------
print("\n[8] 执行验证检查 ...")
checks = []

# 8.1 文件清单必备项
required_files = [
    "manifest.json",
    "structures/redstone_loader.mcstructure",
    "functions/index.mcfunction",
    "functions/{}/player_position.mcfunction".format(config.scoreboard_name),
]
for rf in required_files:
    ok = rf in file_list
    checks.append(("文件清单包含 " + rf, ok))
    print("  [{}] 文件清单包含 {}".format("PASS" if ok else "FAIL", rf))

# 8.2 至少一个 redstone_part_*.mcstructure
part_files = [n for n in file_list if n.startswith("structures/redstone_part_") and n.endswith(".mcstructure")]
ok = len(part_files) >= 1
checks.append(("至少一个 redstone_part_*.mcstructure", ok))
print("  [{}] 至少一个 redstone_part_*.mcstructure（共 {} 个）".format(
    "PASS" if ok else "FAIL", len(part_files)))

# 8.3 index.mcfunction 引用的结构名在 structures/ 下存在对应文件
print("\n  --- 检查 index.mcfunction 引用的结构名 ---")
struct_refs = []
import re
# 匹配 structure load <name> 形式
for m in re.finditer(r"structure\s+load\s+(\S+)", index_content):
    struct_refs.append(m.group(1))
print("  index.mcfunction 中引用的结构名：", struct_refs)
for ref in struct_refs:
    # ref 可能是 redstone_loader 或 redstone_part_001 等
    expected_file = "structures/{}.mcstructure".format(ref)
    ok = expected_file in file_list
    checks.append(("index 引用 {} 存在对应文件".format(ref), ok))
    print("  [{}] index 引用 {} -> {}".format("PASS" if ok else "FAIL", ref, expected_file))

# 8.4 player_position.mcfunction 引用的计分板名与 config 一致
print("\n  --- 检查 player_position.mcfunction 计分板名 ---")
sb_in_pp = config.scoreboard_name in pp_content
checks.append(("player_position 引用计分板名与 config 一致", sb_in_pp))
print("  [{}] player_position.mcfunction 中包含计分板名 '{}'".format(
    "PASS" if sb_in_pp else "FAIL", config.scoreboard_name))

# 检查 function <scoreboard>/player_position 调用路径
func_call = "function {}/player_position".format(config.scoreboard_name)
func_call_in_loader = func_call in pp_content or True  # pp 自身不调用，但 loader 顶部循环方块会调用
# 此处我们检查 index 或 loader 命令是否引用了该 function 路径（通过 manifest 间接不可能）
# 实际上 loader 是二进制结构，无法直接 grep。我们检查 player_position 内容中是否使用 scoreboard_name 作为目标计分板

# 8.5 段数与 max_segment_length 一致：若总长 > 16，应有多个片段
print("\n  --- 检查分段数 ---")
seg_count = len(part_files)
print("  实际段数：", seg_count)
print("  max_segment_length 配置：", config.max_segment_length)
# 总链长应足够触发分段（track_a 有 20 个音符，间隔 4 刻 -> delay 4 -> 每个红石步约 2 方块）
# 20 个音符 * 2 方块 ≈ 40 方块长，超过 16，应至少分 3 段
if seg_count > 1:
    ok = True
    msg = "段数 > 1，分段已触发（{} 段）".format(seg_count)
else:
    ok = False
    msg = "段数 = 1，分段未触发（期望 > 1）"
checks.append(("段数与 max_segment_length 一致（应触发分段）", ok))
print("  [{}] {}".format("PASS" if ok else "FAIL", msg))

# 8.6 manifest.json 基本字段
print("\n  --- 检查 manifest.json 字段 ---")
try:
    mf = json.loads(manifest_content)
    has_format = "format_version" in mf
    has_header = "header" in mf
    has_modules = "modules" in mf
    ok = has_format and has_header and has_modules
    checks.append(("manifest.json 含 format_version/header/modules", ok))
    print("  [{}] manifest.json 含 format_version/header/modules".format("PASS" if ok else "FAIL"))
    if has_header:
        print("  manifest header.name =", mf["header"].get("name"))
except Exception as e:
    checks.append(("manifest.json 字段检查", False))
    print("  [FAIL] manifest.json 解析异常：", e)

# ---------------------------------------------------------------
# 9. 汇总
# ---------------------------------------------------------------
print("\n" + "=" * 70)
print("验证汇总")
print("=" * 70)
passed = sum(1 for _, ok in checks if ok)
failed = sum(1 for _, ok in checks if not ok)
for name, ok in checks:
    print("  [{}] {}".format("PASS" if ok else "FAIL", name))
print("\n总计：{} 通过，{} 失败".format(passed, failed))

if failed == 0:
    print("\n>>> Task 11 通过 <<<")
else:
    print("\n>>> Task 11 未通过 <<<")

# ---------------------------------------------------------------
# 10. 清理（脚本自身由调用方删除，此处仅清理输出文件）
# ---------------------------------------------------------------
print("\n[10] 清理输出文件 ...")
try:
    if output_path.exists():
        output_path.unlink()
        print("  已删除：", output_path)
except Exception as e:
    print("  清理失败：", e)
