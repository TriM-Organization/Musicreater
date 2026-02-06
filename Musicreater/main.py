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

import re


from difflib import get_close_matches
from typing import Dict, Generator, List, Optional, Tuple, Union, Mapping, Callable
from pathlib import Path


from .data import SingleMusic, SingleTrack
from .exceptions import (
    FileFormatNotSupportedError,
    PluginNotSpecifiedError,
    PluginNotFoundError,
)
from ._plugin_abc import TopPluginBase
from .plugins import (
    _global_plugin_registry,
    PluginRegistry,
    PluginConfig,
    PluginTypes,
    load_plugin_module,
    T_IOPlugin,
    T_Plugin,
)


class MusiCreater:
    """
    音·创 v3 主要控制类
    另：“创建者”一词的英文应该是“Creator”
    """

    __plugin_registry: PluginRegistry
    """插件注册表实例"""
    _plugin_cache: Dict[str, TopPluginBase]
    """插件缓存字典，插件id为键、插件实例为值"""
    music: SingleMusic
    """当前曲目实例"""

    def __init__(self, whole_music: SingleMusic) -> None:
        global _global_plugin_registry

        self.__plugin_registry = _global_plugin_registry

        self._plugin_cache = {}
        self._cache_all_plugins()

        self.music = whole_music

    @staticmethod
    def _get_plugin_within_iousage(
        get_func: Callable[[Union[Path, str]], Generator[T_IOPlugin, None, None]],
        fpath: Path,
        plg_regdict: Dict[str, T_IOPlugin],
        plg_id: Optional[str],
    ) -> T_IOPlugin:

        __plugin: Optional[T_IOPlugin] = None
        if plg_id:
            __plugin = plg_regdict.get(plg_id)

        else:
            for __plg in get_func(fpath):
                if __plugin:
                    raise PluginNotSpecifiedError(
                        "文件类型`{}`可被多个插件处理，请在调用函数的参数中指定插件名称".format(
                            fpath.suffix.upper()
                        )
                    )
                __plugin = __plg
        if __plugin:
            return __plugin
        else:
            raise FileFormatNotSupportedError(
                "无法找到处理`{}`类型文件的插件".format(fpath.suffix.upper())
            )

    @classmethod
    def import_music(
        cls,
        file_path: Path,
        plugin_id: Optional[str] = None,
        plugin_config: Optional[PluginConfig] = None,
    ) -> "MusiCreater":
        return cls(
            whole_music=cls._get_plugin_within_iousage(
                _global_plugin_registry.get_music_input_plugin_by_format,
                file_path,
                _global_plugin_registry._music_input_plugins,
                plugin_id,
            ).load(file_path, plugin_config)
        )

    def import_track(
        self,
        file_path: Path,
        plugin_id: Optional[str] = None,
        plugin_config: Optional[PluginConfig] = None,
    ) -> SingleTrack:
        self.music.append(
            self._get_plugin_within_iousage(
                self.__plugin_registry.get_track_input_plugin_by_format,
                file_path,
                self.__plugin_registry._track_input_plugins,
                plugin_id,
            ).load(file_path, plugin_config)
        )
        return self.music[-1]

    def export_music(
        self,
        file_path: Path,
        plugin_id: Optional[str] = None,
        plugin_config: Optional[PluginConfig] = None,
    ) -> None:
        self._get_plugin_within_iousage(
            self.__plugin_registry.get_music_output_plugin_by_format,
            file_path,
            self.__plugin_registry._music_output_plugins,
            plugin_id,
        ).dump(self.music, file_path, plugin_config)

    def export_track(
        self,
        track_index: int,
        file_path: Path,
        plugin_id: Optional[str] = None,
        plugin_config: Optional[PluginConfig] = None,
    ) -> None:
        self._get_plugin_within_iousage(
            self.__plugin_registry.get_track_output_plugin_by_format,
            file_path,
            self.__plugin_registry._track_output_plugins,
            plugin_id,
        ).dump(self.music[track_index], file_path, plugin_config)

    def perform_operation_on_music(
        self, plugin_id: str, plugin_config: Optional[PluginConfig] = None
    ):
        if __plugin := self.__plugin_registry._music_operate_plugins.get(plugin_id):
            # 这样做是为了兼容以后的*撤回/重做*功能
            self.music = __plugin.process(self.music, plugin_config)
        else:
            raise PluginNotFoundError(
                "无法找到惟一识别码为`{}`的插件".format(plugin_id)
            )

    def perform_operation_on_track(
        self,
        track_index: int,
        plugin_id: str,
        plugin_config: Optional[PluginConfig] = None,
    ):
        if __plugin := self.__plugin_registry._track_operate_plugins.get(plugin_id):
            # 这样做是为了兼容以后的*撤回/重做*功能
            self.music[track_index] = __plugin.process(
                self.music[track_index], plugin_config
            )
        else:
            raise PluginNotFoundError(
                "无法找到惟一识别码为`{}`的插件".format(plugin_id)
            )

    @staticmethod
    def _camel_to_snake(name: str) -> str:
        """
        将驼峰命名转换为蛇形命名
        CyberAngel -> cyber_angel
        """
        return re.sub(
            "([a-z0-9])([A-Z])", r"\1_\2", re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        ).lower()

    def _parse_plugin_id(self, attr_name: str) -> Optional[str]:
        """解析属性名称为插件惟一识别码"""

        # 尝试去除 _plugin 后缀
        if attr_name.endswith("_plugin"):
            candidate_name = attr_name[:-7]  # 去除 "_plugin"
            if candidate_name in self._plugin_cache:
                return candidate_name

        # 尝试转换为 snake_case（如果插件名是驼峰式）
        snake_case_name = self._camel_to_snake(attr_name)

        if snake_case_name != attr_name:  # 避免重复转换
            if snake_case_name in self._plugin_cache:  # 尝试转换后的插件名
                return snake_case_name
            else:
                return self._parse_plugin_id(snake_case_name)

        return None

    def _get_closest_plugin_id(self, requested_id: str) -> Optional[str]:
        """找到最接近的插件识别码（用于更好的错误提示）"""

        matches = get_close_matches(
            requested_id, self._plugin_cache.keys(), n=1, cutoff=0.6
        )
        return matches[0] if matches else None

    def get_plugin_by_id(self, plg_id: str):
        """获取插件实例，并缓存起来，提高性能"""
        if plg_id.startswith("_"):
            raise AttributeError("属性`{}`不存在，不应访问类的私有属性".format(plg_id))

        if plg_id in self._plugin_cache:
            return self._plugin_cache[plg_id]
        else:
            plugin_name = self._parse_plugin_id(plg_id)
            if plugin_name:
                self._plugin_cache[plg_id] = self._plugin_cache[plugin_name]
                return self._plugin_cache[plg_id]

        closest = self._get_closest_plugin_id(plg_id)

        raise AttributeError(
            "插件`{}`不存在，请检查插件的惟一识别码是否正确".format(plg_id)
            + (
                "；或者阁下可能想要使用的是`{}`插件？".format(closest)
                if closest
                else ""
            )
        )

    def __getattr__(self, plugin_id: str):
        """动态属性访问，允许直接 实例.插件名 来访问插件"""
        return self.get_plugin_by_id(plugin_id)

    def _cache_all_plugins(self):
        """获取所有已注册插件的名称"""
        for __plugin_type, __plugins_map in self.__plugin_registry:
            for __plugin_id, __plugin in __plugins_map.items():
                if __plugin_id in self._plugin_cache:  # 避免重复缓存
                    if (
                        __plugin.metainfo.version
                        <= self._plugin_cache[__plugin_id].metainfo.version
                    ):  # 优先使用版本号最大的插件
                        continue
                self._plugin_cache[__plugin_id] = __plugin
