# -*- coding: utf-8 -*-
"""
音·创 v3 的功能性内容合辑
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
    file_name: str, suffix: str = ".file", appendix_connector: str = "-"
) -> Path:
    ss_path = Path(file_name).with_suffix(suffix)
    if ss_path.exists():
        now_appendix = 2
        while (
            ss_path := Path(file_name + appendix_connector + str(now_appendix) + suffix)
        ).exists():
            now_appendix += 1
    return ss_path
