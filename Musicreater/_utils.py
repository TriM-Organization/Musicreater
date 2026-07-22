# -*- coding: utf-8 -*-
"""
音·创 v3 的功能性内容合辑
此处存放无需本体类的内容
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


from copy import deepcopy, copy
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Tuple, Union, TypeVar

T = TypeVar("T")


def enumerated_stuffcopy_dictionary(
    enumeration_times: int = 17, staff: T = {}
) -> Dict[int, T]:
    """
    生成一个字典，其中键从 `0` 到 `enumeration_times-1`，值是 `staff` 的拷贝
    """
    # 这告诉我们，你不能忽略任何一个复制的序列，因为它真的，我哭死，折磨我一整天，全在这个bug上了
    # 上面的这指的是 copy.deepcopy  —— 金羿 来自 20260210
    return {i: deepcopy(staff) for i in range(enumeration_times)}


def incremental_save_path(
    file_name: str,
    suffix: str = ".file",
    appendix_connector: str = "-",
    parent_path: Union[Path, str] = Path.cwd(),
) -> Path:
    """
    生成一个文件路径，该文件地址指向的文件名应为 `file_name` 添加一个后缀 `suffix`。\n
    如果 `file_name` 已经存在，则添加一个后缀 `appendix_connector` 和一个数字。
    此数字由 2 开始，每存在此文件，则递增 1。直到找到最后那个惟一的未被占用的文件路径。\n
    例如：
    -   file_name = "test", suffix = ".txt", appendix_connector = "-", parent_path = "/tmp/" \n
        若在 `/tmp` 中：
            1.  `test.txt` 不存在，则返回 Path("/tmp/test.txt")
            2.  上述文件存在，且 `test-1.txt` 不存在，则返回 Path("/tmp/test-1.txt")
            3.  上述文件皆存在，但 `test-2.txt` 不存在，则返回 Path("/tmp/test-2.txt")
            ...
    """
    ss_path = parent_path / Path(file_name).with_suffix(suffix)
    if ss_path.exists():
        now_appendix = 2
        while (
            ss_path := parent_path
            / Path(file_name + appendix_connector + str(now_appendix) + suffix)
        ).exists():
            now_appendix += 1
    return ss_path


def volume_weight_to_sound_distance(
    max_weight: float, minimal_loadness: int, weight: float, loadness: int
) -> float:
    """
    通过音量权计算声源距离

    Parameters
    ==========
    max_weight: float
        全曲最大音量权
    minimal_loadness: int
        曲目中响度最小乐器的响度
    weight: float
        当前乐器的音量权
    loadness: int
        当前乐器的响度

    Returns
    =======
    float
        声源距离

    Notes
    =====

    以下关于距离的计算逻辑请见[计算过程](./resources/响度公式/计算过程.jpg)\n
    关于响度的计算方法请见[此脚本](./resources/experiments/exam_loadness.py)\n
    最终公式为：\n
    声源距离 = 48 - (48 * 音量权 * ( 10 ** ((当前乐器的响度 - 响度最小乐器的响度) / 20 ))) / 全曲最大音量权\n
        D_t = 48 - \\frac{48 \\cdot P_t \\cdot 10^{\\frac{V_t - V_x}{20}}}{P_m}
    由于我们存储的响度都是 百-LUFS，所以下面的计算除数为 2000
    """

    if weight == 0:
        return 48
    elif weight == max_weight:
        # print("音量权最大，差比：", ((loadness - minimal_loadness) / 2000), "，率：", (1 - pow(10, (minimal_loadness - loadness)/2000)))
        return 48 * (1 - pow(10, (minimal_loadness - loadness) / 2000))
    else:
        return 48 * (
            1 - pow(10, (minimal_loadness - loadness) / 2000) * weight / max_weight
        )
