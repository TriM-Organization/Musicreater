# -*- coding: utf-8 -*-

"""
存储 音·创 v3 的插件接口与管理相关内容
"""

"""
版权所有 © 2026 金羿
Copyright © 2026 Eilles

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md


import importlib
from pathlib import Path
from typing import (
    Dict,
    Any,
    Optional,
    List,
    Tuple,
    Union,
    Generator,
    Set,
    Iterable,
    Iterator,
)
from itertools import chain


from ._plugin_abc import (
    # 枚举类
    PluginType,
    # 抽象基类/数据类（插件参数定义）
    PluginConfig,
    PluginMetaInformation,
    # 抽象基类（插件定义）
    MusicInputPluginBase,
    TrackInputPluginBase,
    MusicOperatePluginBase,
    TrackOperatePluginBase,
    MusicOutputPluginBase,
    TrackOutputPluginBase,
    ServicePluginBase,
    LibraryPluginBase,
    # 顶层插件定义
    TopPluginBase,
)
from .exceptions import (
    PluginMetainfoNotFoundError,
    ParameterTypeError,
    PluginInstanceNotFoundError,
)


__all__ = [
    # 枚举类
    "PluginType",
    # 抽象基类/数据类（插件参数定义）
    "PluginConfig",
    "PluginMetaInformation",
    # 抽象基类（插件定义）
    "MusicInputPluginBase",
    "TrackInputPluginBase",
    "MusicOperatePluginBase",
    "TrackOperatePluginBase",
    "MusicOutputPluginBase",
    "TrackOutputPluginBase",
    "ServicePluginBase",
    "LibraryPluginBase",
    # 插件注册用装饰函数
    "music_input_plugin",
    "track_input_plugin",
    "music_operate_plugin",
    "track_operate_plugin",
    "music_output_plugin",
    "track_output_plugin",
    "service_plugin",
    "library_plugin",
]


def load_plugin_module(package: Union[Path, str]):
    """自动发现并加载插件包中的插件

    参数:
    =====
    package: Path | str, 可选
        插件包路径或名称，当为 Path 类时为路径，为 str 时为包名，切勿混淆。
    """

    if isinstance(package, Path):
        relative_path = package.resolve().relative_to(Path.cwd().resolve())
        if relative_path.stem == "__init__":
            return importlib.import_module(".".join(relative_path.parts[:-1]))
        else:
            return importlib.import_module(
                ".".join(relative_path.parts[:-1] + (relative_path.stem,))
            )
    else:
        return importlib.import_module(package)


class PluginRegistry:
    """插件注册管理器（注册表）"""

    def __init__(self):
        # 实际上在纵容那些有着同样名称的插件……
        # （不用 Dict[str`plugin name`, PluginClass`] 的形式）
        # 啊，我真的很高尚
        # 你真的不会把插件注册两遍吧……对吧？

        # EMERGENCY TODO ================================================ CRITICAL 紧急更改
        # 改成 Dict[str`plugin id`, PluginClass`]] 的形式吧
        # 刚刚才想起来，这个 name 是显示名称啊！草
        # 现在测试情况下就将错就错吧，先把 name 当成 id 来写吧
        self._music_input_plugins: Set[MusicInputPluginBase] = set()
        self._track_input_plugins: Set[TrackInputPluginBase] = set()
        self._music_operate_plugins: Set[MusicOperatePluginBase] = set()
        self._track_operate_plugins: Set[TrackOperatePluginBase] = set()
        self._music_output_plugins: Set[MusicOutputPluginBase] = set()
        self._track_output_plugins: Set[TrackOutputPluginBase] = set()
        self._service_plugins: Set[ServicePluginBase] = set()
        self._library_plugins: Set[LibraryPluginBase] = set()

    def __iter__(self) -> Iterator[Tuple[PluginType, Set[TopPluginBase]]]:
        """迭代器，返回所有插件"""
        return iter(
            (
                (PluginType.FUNCTION_MUSIC_IMPORT, self._music_input_plugins),
                (PluginType.FUNCTION_TRACK_IMPORT, self._track_input_plugins),
                (PluginType.FUNCTION_MUSIC_OPERATE, self._music_operate_plugins),
                (PluginType.FUNCTION_TRACK_OPERATE, self._track_operate_plugins),
                (PluginType.FUNCTION_MUSIC_EXPORT, self._music_output_plugins),
                (PluginType.FUNCTION_TRACK_EXPORT, self._track_output_plugins),
                (PluginType.SERVICE, self._service_plugins),
                (PluginType.LIBRARY, self._library_plugins),
            )
        )  # pyright: ignore[reportReturnType]

    def register_music_input_plugin(self, plugin_class: type) -> None:
        """注册输入插件-整首曲目"""
        self._music_input_plugins.add(plugin_class())

    def register_track_input_plugin(self, plugin_class: type) -> None:
        """注册输入插件-单个音轨"""
        self._track_input_plugins.add(plugin_class())

    def register_music_operate_plugin(self, plugin_class: type) -> None:
        """注册曲目处理插件"""
        self._music_operate_plugins.add(plugin_class())

    def register_track_operate_plugin(self, plugin_class: type) -> None:
        """注册音轨处理插件"""
        self._track_operate_plugins.add(plugin_class())

    def register_music_output_plugin(self, plugin_class: type) -> None:
        """注册输出插件-整首曲目"""
        self._music_output_plugins.add(plugin_class())

    def register_track_output_plugin(self, plugin_class: type) -> None:
        """注册输出插件-单个音轨"""
        self._track_output_plugins.add(plugin_class())

    def register_service_plugin(self, plugin_class: type) -> None:
        """注册服务插件"""
        self._service_plugins.add(plugin_class())

    def register_library_plugin(self, plugin_class: type) -> None:
        """注册支持库插件"""
        self._library_plugins.add(plugin_class())

    def get_music_input_plugin_by_format(
        self, filepath_or_format: Union[Path, str]
    ) -> Generator[MusicInputPluginBase, None, None]:
        """通过指定输入的文件或格式，以获取对应的全曲导入用插件"""
        if isinstance(filepath_or_format, str):
            return (
                plugin
                for plugin in self._music_input_plugins
                if plugin.can_handle_format(filepath_or_format)
            )
        elif isinstance(filepath_or_format, Path):
            return (
                plugin
                for plugin in self._music_input_plugins
                if plugin.can_handle_file(filepath_or_format)
            )
        else:
            raise ParameterTypeError(
                "用于指定“导入全曲的数据之类型”的参数，其类型须为`Path`路径或字符串，而非`{}`类型的`{}`值".format(
                    type(filepath_or_format), filepath_or_format
                )
            )

    def get_track_input_plugin_by_format(
        self, filepath_or_format: Union[Path, str]
    ) -> Generator[TrackInputPluginBase, None, None]:
        """通过指定输入的文件或格式，以获取对应的单音轨导入用插件"""
        if isinstance(filepath_or_format, str):
            return (
                plugin
                for plugin in self._track_input_plugins
                if plugin.can_handle_format(filepath_or_format)
            )
        elif isinstance(filepath_or_format, Path):
            return (
                plugin
                for plugin in self._track_input_plugins
                if plugin.can_handle_file(filepath_or_format)
            )
        else:
            raise ParameterTypeError(
                "用于指定“导入单个音轨的数据之类型”的参数，其类型须为`Path`路径或字符串，而非`{}`类型的`{}`值".format(
                    type(filepath_or_format), filepath_or_format
                )
            )

    def get_music_output_plugin_by_format(
        self, filepath_or_format: Union[Path, str]
    ) -> Generator[MusicOutputPluginBase, None, None]:
        """通过指定输出的文件或格式，以获取对应的导出全曲用插件"""
        if isinstance(filepath_or_format, str):
            return (
                plugin
                for plugin in self._music_output_plugins
                if plugin.can_handle_format(filepath_or_format)
            )
        elif isinstance(filepath_or_format, Path):
            return (
                plugin
                for plugin in self._music_output_plugins
                if plugin.can_handle_file(filepath_or_format)
            )
        else:
            raise ParameterTypeError(
                "用于指定“全曲数据导出的类型”的参数，其类型须为`Path`路径或字符串，而非`{}`类型的`{}`值".format(
                    type(filepath_or_format), filepath_or_format
                )
            )

    def get_track_output_plugin_by_format(
        self, filepath_or_format: Union[Path, str]
    ) -> Generator[TrackOutputPluginBase, None, None]:
        """通过指定输出的文件或格式，以获取对应的导出单个音轨用插件"""
        if isinstance(filepath_or_format, str):
            return (
                plugin
                for plugin in self._track_output_plugins
                if plugin.can_handle_format(filepath_or_format)
            )
        elif isinstance(filepath_or_format, Path):
            return (
                plugin
                for plugin in self._track_output_plugins
                if plugin.can_handle_file(filepath_or_format)
            )
        else:
            raise ParameterTypeError(
                "用于指定“单音轨数据导出的类型”的参数，其类型须为`Path`路径或字符串，而非`{}`类型的`{}`值".format(
                    type(filepath_or_format), filepath_or_format
                )
            )

    def get_music_input_plugin(self, plugin_name: str) -> MusicInputPluginBase:
        """获取指定名称的全曲导入用插件，当名称重叠时，取版本号最大的"""
        try:
            return max(
                [
                    plugin
                    for plugin in self._music_input_plugins
                    if plugin.metainfo.name == plugin_name
                ],
                key=lambda plugin: plugin.metainfo.version,
            )
        except ValueError:
            raise PluginInstanceNotFoundError(
                "未找到“用于导入曲目、名为`{}`”的插件".format(plugin_name)
            )

    def get_track_input_plugin(self, plugin_name: str) -> TrackInputPluginBase:
        """获取指定名称的单音轨导入用插件，当名称重叠时，取版本号最大的"""
        try:
            return max(
                [
                    plugin
                    for plugin in self._track_input_plugins
                    if plugin.metainfo.name == plugin_name
                ],
                key=lambda plugin: plugin.metainfo.version,
            )
        except ValueError:
            raise PluginInstanceNotFoundError(
                "未找到“用于导入单个音轨、名为`{}`”的插件".format(plugin_name)
            )

    def get_music_operate_plugin(self, plugin_name: str) -> MusicOperatePluginBase:
        """获取指定名称的全曲处理用插件，当名称重叠时，取版本号最大的"""
        try:
            return max(
                [
                    plugin
                    for plugin in self._music_operate_plugins
                    if plugin.metainfo.name == plugin_name
                ],
                key=lambda plugin: plugin.metainfo.version,
            )
        except ValueError:
            raise PluginInstanceNotFoundError(
                "未找到“用于处理整个曲目、名为`{}`”的插件".format(plugin_name)
            )

    def get_track_operate_plugin(self, plugin_name: str) -> TrackOperatePluginBase:
        """获取指定名称的单音轨处理用插件，当名称重叠时，取版本号最大的"""
        try:
            return max(
                [
                    plugin
                    for plugin in self._track_operate_plugins
                    if plugin.metainfo.name == plugin_name
                ],
                key=lambda plugin: plugin.metainfo.version,
            )
        except ValueError:
            raise PluginInstanceNotFoundError(
                "未找到“用于处理单个音轨、名为`{}`”的插件".format(plugin_name)
            )

    def get_music_output_plugin(self, plugin_name: str) -> MusicOutputPluginBase:
        """获取指定名称的导出全曲用插件，当名称重叠时，取版本号最大的"""
        try:
            return max(
                [
                    plugin
                    for plugin in self._music_output_plugins
                    if plugin.metainfo.name == plugin_name
                ],
                key=lambda plugin: plugin.metainfo.version,
            )
        except ValueError:
            raise PluginMetainfoNotFoundError(
                "未找到“用于导出完整曲目、名为`{}`”的插件".format(plugin_name)
            )

    def get_track_output_plugin(self, plugin_name: str) -> TrackOutputPluginBase:
        """获取指定名称的导出单音轨用插件，当名称重叠时，取版本号最大的"""
        try:
            return max(
                [
                    plugin
                    for plugin in self._track_output_plugins
                    if plugin.metainfo.name == plugin_name
                ],
                key=lambda plugin: plugin.metainfo.version,
            )
        except ValueError:
            raise PluginMetainfoNotFoundError(
                "未找到“用于导出单个音轨、名为`{}`”的插件".format(plugin_name)
            )

    def get_service_plugin(self, plugin_name: str) -> ServicePluginBase:
        """获取服务用插件，当名称重叠时，取版本号最大的"""
        try:
            return max(
                [
                    plugin
                    for plugin in self._service_plugins
                    if plugin.metainfo.name == plugin_name
                ],
                key=lambda plugin: plugin.metainfo.version,
            )
        except ValueError:
            raise PluginInstanceNotFoundError(
                "未找到名为`{}`的服务用插件".format(plugin_name)
            )

    def get_library_plugin(self, plugin_name: str) -> LibraryPluginBase:
        """获取依赖库类插件，当名称重叠时，取版本号最高的"""
        try:
            return max(
                [
                    plugin
                    for plugin in self._library_plugins
                    if plugin.metainfo.name == plugin_name
                ],
                key=lambda plugin: plugin.metainfo.version,
            )
        except ValueError:
            raise PluginInstanceNotFoundError(
                "未找到名为`{}`的依赖库插件".format(plugin_name)
            )

    def supported_input_formats(self) -> Set[str]:
        """所有支持的导入格式"""
        return set(
            chain.from_iterable(
                plugin.supported_formats
                for plugin in chain(
                    self._music_input_plugins, self._track_input_plugins
                )
            )
        )

    def supported_output_formats(self) -> Set[str]:
        """所有支持的导出格式"""
        return set(
            chain.from_iterable(
                plugin.supported_formats
                for plugin in chain(
                    self._music_output_plugins, self._track_output_plugins
                )
            )
        )


_global_plugin_registry = PluginRegistry()
"""全局插件注册表实例"""


def music_input_plugin(plugin_id: str):
    """全曲输入用插件装饰器"""

    def decorator(cls):
        global _global_plugin_registry
        cls.id = plugin_id
        _global_plugin_registry.register_music_input_plugin(cls)
        return cls

    return decorator


def track_input_plugin(plugin_id: str):
    """单轨输入用插件装饰器"""

    def decorator(cls):
        global _global_plugin_registry
        cls.id = plugin_id
        _global_plugin_registry.register_track_input_plugin(cls)
        return cls

    return decorator


def music_operate_plugin(plugin_id: str):
    """全曲处理用插件装饰器"""

    def decorator(cls):
        global _global_plugin_registry
        cls.id = plugin_id
        _global_plugin_registry.register_music_operate_plugin(cls)
        return cls

    return decorator


def track_operate_plugin(plugin_id: str):
    """音轨处理插件装饰器"""

    def decorator(cls):
        global _global_plugin_registry
        cls.id = plugin_id
        _global_plugin_registry.register_track_operate_plugin(cls)
        return cls

    return decorator


def music_output_plugin(plugin_id: str):
    """乐曲输出用插件装饰器"""

    def decorator(cls):
        global _global_plugin_registry
        cls.id = plugin_id
        _global_plugin_registry.register_music_output_plugin(cls)
        return cls

    return decorator


def track_output_plugin(plugin_id: str):
    """音轨输出用插件装饰器"""

    def decorator(cls):
        global _global_plugin_registry
        cls.id = plugin_id
        _global_plugin_registry.register_track_output_plugin(cls)
        return cls

    return decorator


def service_plugin(plugin_id: str):
    """服务插件装饰器"""

    def decorator(cls):
        global _global_plugin_registry
        cls.id = plugin_id
        _global_plugin_registry.register_service_plugin(cls)
        return cls

    return decorator


def library_plugin(plugin_id: str):
    """支持库插件装饰器"""

    def decorator(cls):
        global _global_plugin_registry
        cls.id = plugin_id
        _global_plugin_registry.register_library_plugin(cls)
        return cls

    return decorator
