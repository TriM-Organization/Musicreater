# -*- coding: utf-8 -*-
"""
存放主程序所必须的功能性内容
"""

"""
版权所有 © 2023 音·创 开发者
Copyright © 2023 all the developers of Musicreater

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿穆组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md

from typing import Any, Dict


def mctick2timestr(mc_tick: int) -> str:
    """
    将《我的世界》的游戏刻计转为表示时间的字符串
    """
    return str(int(int(mc_tick / 20) / 60)) + ":" + str(int(int(mc_tick / 20) % 60))


def empty_midi_channels(channel_count: int = 17, staff: Any = {}) -> Dict[int, Any]:
    """
    空MIDI通道字典
    """

    return dict(
        (
            i,
            (staff.copy() if isinstance(staff, (dict, list)) else staff),
        )  # 这告诉我们，你不能忽略任何一个复制的序列，因为它真的，我哭死，折磨我一整天，全在这个bug上了
        for i in range(channel_count)
    )
