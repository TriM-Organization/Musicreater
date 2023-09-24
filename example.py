# -*- coding: utf-8 -*-

# 伶伦 开发交流群 861684859


"""
音·创 (Musicreater) 演示程序
是一款免费开源的针对《我的世界》的midi音乐转换库
Musicreater (音·创)
A free open source library used for convert midi file into formats that is suitable for **Minecraft**.

版权所有 © 2023 音·创 开发者
Copyright © 2023 all the developers of Musicreater

开源相关声明请见 ./License.md
Terms & Conditions: ./License.md
"""

import os

import Musicreater
from Musicreater.plugin import ConvertConfig
from Musicreater.plugin.bdxfile import to_BDX_file_in_delay, to_BDX_file_in_score
from Musicreater.plugin.addonpack import (
    to_addon_pack_in_delay,
    to_addon_pack_in_repeater,
    to_addon_pack_in_score,
)

# 获取midi列表
midi_path = input(f"请输入MIDI路径：")


# 获取输出地址
out_path = input(f"请输入输出路径：")


# 选择输出格式
fileFormat = int(input(f"请输入输出格式[BDX(1) 或 MCPACK(0)]：").lower())
playerFormat = int(input(f"请选择播放方式[红石(2) 或 计分板(1) 或 延迟(0)]：").lower())


# 真假字符串判断
def bool_str(sth: str) -> bool:
    try:
        return bool(float(sth))
    except ValueError:
        if str(sth).lower() == "true":
            return True
        elif str(sth).lower() == "false":
            return False
        else:
            raise ValueError("布尔字符串啊？")


if os.path.exists("./demo_config.json"):
    import json

    prompts = json.load(open("./demo_config.json", "r", encoding="utf-8"))
else:
    prompts = []
    # 提示语 检测函数 错误提示语
    for args in [
        (
            f"输入音量：",
            float,
        ),
        (
            f"输入播放速度：",
            float,
        ),
        (
            f"是否启用进度条：",
            bool_str,
        ),
        (
            f"计分板名称：",
            str,
        )
        if playerFormat == 1
        else (
            f"玩家选择器：",
            str,
        ),
        (
            f"是否自动重置计分板：",
            bool_str,
        )
        if playerFormat == 1
        else (),
        (
            f"作者名称：",
            str,
        )
        if fileFormat == 1
        else (),
        ()
        if playerFormat == 1
        else (
            f"最大结构高度：",
            int,
        ),
    ]:
        if args:
            prompts.append(args[1](input(args[0])))


print(f"正在处理 {midi_path} ：")
cvt_mid = Musicreater.MidiConvert.from_midi_file(midi_path, old_exe_format=False)
cvt_cfg = ConvertConfig(out_path, *prompts[:3])

if playerFormat == 1:
    cvt_method = to_addon_pack_in_score
elif playerFormat == 0:
    cvt_method = to_addon_pack_in_delay
elif playerFormat == 2:
    cvt_method = to_addon_pack_in_repeater


print(
    "	指令总长：{}，最高延迟：{}".format(
        *(cvt_method(cvt_mid, cvt_cfg, *prompts[3:]))  # type: ignore
    )
    if fileFormat == 0
    else "	指令总长：{}，最高延迟：{}，结构大小{}，终点坐标{}".format(
        *(
            to_BDX_file_in_score(cvt_mid, cvt_cfg, *prompts[3:])
            if playerFormat == 1
            else to_BDX_file_in_delay(cvt_mid, cvt_cfg, *prompts[3:])
        )
    )
)


exitSth = input("回车退出").lower()
if exitSth == "record":
    import json

    with open("./demo_config.json", "w", encoding="utf-8") as f:
        json.dump(prompts, f)
elif exitSth == "delrec":
    os.remove("./demo_config.json")
