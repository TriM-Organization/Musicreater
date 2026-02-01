# -*- coding: utf-8 -*-


"""
音·创
是一款免费开源的《我的世界》数字音频支持库。

Musicreater (音·创)
A free and open-source library for handling with **Minecraft** digital music.

版权所有 © 2026 睿乐组织
Copyright © 2026 TriM-Organization

音·创（“本项目”）的协议颁发者为 金羿、玉衡Alioth
The Licensor of Musicreater("this project") is Eilles, YuhengAlioth

本项目根据 第一版 汉钰律许可协议（“本协议”）授权。
任何人皆可从以下地址获得本协议副本：
https://gitee.com/TriM-Organization/Musicreater/blob/master/LICENSE.md。
若非因法律要求或经过了特殊准许，此作品在根据本协议“原样”提供的基础上，
不予提供任何形式的担保、任何明示、任何暗示或类似承诺。
也就是说，用户将自行承担因此作品的质量或性能问题而产生的全部风险。
详细的准许和限制条款请见原协议文本。
"""

# 音·创 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库根目录下的 License.md


# BUG退散！BUG退散！
# 异常与错误作乱之时
# 二六字组！万国码合！二六字组！万国码合！
# 赶快呼叫 程序员！Let's Go！

# BUG退散！BUG退散！
# 異常、誤りが、困った時は
# パラメータ メソッド！パラメータ メソッド！
# 助けてもらおう、開発者！レッツゴー！

# Bug retreat! Bug retreat!
# Exceptions and errors are causing chaos
# Words combine! Codes unite!
# Hurry to call the programmer! Let's Go!


from typing import Dict, Generator, List, Optional, Tuple, Union
from pathlib import Path

from .data import SingleMusic, SingleTrack
from ._plugin_abc import TopBasePlugin
from .plugins import __global_plugin_registry, PluginRegistry


class MusiCreater:
    """
    音·创 v3 主要控制类
    另：“创建者”一词的英文应该是“Creator”
    """

    __plugin_registry: PluginRegistry
    """插件注册表实例"""
    _plugin_cache: Dict[str, TopBasePlugin]
    """插件缓存字典，插件名为键、插件实例为值"""
    music: SingleMusic
    """当前曲目实例"""

    def __init__(self, whole_music: SingleMusic) -> None:
        global __global_plugin_registry

        self.__plugin_registry = __global_plugin_registry

        self._plugin_cache = {}

        self.music = whole_music
    
    
    

    def import_music(self, file_path: Path, plugin_name: Optional[str] = None) -> SingleMusic: