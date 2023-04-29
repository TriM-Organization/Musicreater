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


# 获取midi列表
midi_path = input(f"请输入MIDI路径：")


# 获取输出地址
out_path = input(f"请输入输出路径：")

conversion = Musicreater.midiConvert()


def isMethodOK(sth: str):
    if int(sth) in range(1, len(conversion.methods) + 1):
        return int(sth)
    else:
        raise ValueError


convert_method = int(input(f"请输入转换算法[1~{len(conversion.methods)}]："))

# 选择输出格式
fileFormat = int(input(f"请输入输出格式[BDX(1) 或 MCPACK(0)]：").lower())
playerFormat = int(input(f"请选择播放方式[计分板(1) 或 延迟(0)]：").lower())


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


debug = False

if os.path.exists("./demo_config.json"):
    import json

    prompts = json.load(open("./demo_config.json", "r", encoding="utf-8"))
    if prompts[-1] == "debug":
        debug = True
    prompts = prompts[:-1]
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
        (
            f"最大结构高度：",
            int,
        )
        if fileFormat == 1
        else (),
    ]:
        if args:
            prompts.append(args[1](input(args[0])))

conversion = Musicreater.midiConvert(debug=debug)


print(f"正在处理 {midi_path} ：")
conversion.convert(midi_path, out_path)
if debug:
    with open("./records.json", "a", encoding="utf-8") as f:
        json.dump(conversion.toDICT(), f)
        f.write(5 * "\n")
conversion_result = (
    conversion.to_mcpack(convert_method, *prompts)
    if fileFormat == 0
    else (
        conversion.to_BDX_file(convert_method, *prompts)
        if playerFormat == 1
        else conversion.to_BDX_file_with_delay(convert_method, *prompts)
    )
)

if conversion_result[0]:
    print(
        f"	指令总长：{conversion_result[1]}，最高延迟：{conversion_result[2]}{f'''，结构大小{conversion_result[3]}，最末坐标{conversion_result[4]}''' if fileFormat == 1 else ''}"
    )
else:
    print(f"失败：{conversion_result}")

exitSth = input("回车退出").lower()
if exitSth == "record":
    import json

    with open("./demo_config.json", "w", encoding="utf-8") as f:
        json.dump(prompts, f)
elif exitSth == "delrec":
    os.remove("./demo_config.json")
