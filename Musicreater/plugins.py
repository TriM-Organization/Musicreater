# -*- coding: utf-8 -*-

"""
音·创 v3 的插件接口与管理相关内容
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
    TypeVar,
    Mapping,
    Callable,
)
from itertools import chain


from ._plugin_abc import (
    # 枚举类
    PluginTypes,
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
    PluginRegisteredError,
    PluginNotFoundError,
)


__all__ = [
    # 枚举类
    "PluginTypes",
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


T_IOPlugin = TypeVar(
    "T_IOPlugin",
    MusicInputPluginBase,
    TrackInputPluginBase,
    MusicOutputPluginBase,
    TrackOutputPluginBase,
)
T_Plugin = TypeVar(
    "T_Plugin",
    MusicInputPluginBase,
    TrackInputPluginBase,
    MusicOperatePluginBase,
    TrackOperatePluginBase,
    MusicOutputPluginBase,
    TrackOutputPluginBase,
    ServicePluginBase,
    LibraryPluginBase,
)


def load_plugin_module(package: Union[Path, str]):
    """自动发现并加载插件包中的插件

    参数:
    =====
    package: Path | str, 可选
        插件包路径或名称，当为 Path 类时为路径，为 str 时为包名，切勿混淆。
    """

    try:
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
    except ModuleNotFoundError as e:
        raise PluginNotFoundError("无法找到名为`{}`的插件包".format(package))


class PluginRegistry:
    """插件注册管理器（注册表）"""

    def __init__(self):
        self._music_input_plugins: Dict[str, MusicInputPluginBase] = {}
        self._track_input_plugins: Dict[str, TrackInputPluginBase] = {}
        self._music_operate_plugins: Dict[str, MusicOperatePluginBase] = {}
        self._track_operate_plugins: Dict[str, TrackOperatePluginBase] = {}
        self._music_output_plugins: Dict[str, MusicOutputPluginBase] = {}
        self._track_output_plugins: Dict[str, TrackOutputPluginBase] = {}
        self._service_plugins: Dict[str, ServicePluginBase] = {}
        self._library_plugins: Dict[str, LibraryPluginBase] = {}

    def __iter__(self) -> Iterator[Tuple[PluginTypes, Mapping[str, TopPluginBase]]]:
        """迭代器，返回所有插件"""
        return iter(
            (
                (PluginTypes.FUNCTION_MUSIC_IMPORT, self._music_input_plugins),
                (PluginTypes.FUNCTION_TRACK_IMPORT, self._track_input_plugins),
                (PluginTypes.FUNCTION_MUSIC_OPERATE, self._music_operate_plugins),
                (PluginTypes.FUNCTION_TRACK_OPERATE, self._track_operate_plugins),
                (PluginTypes.FUNCTION_MUSIC_EXPORT, self._music_output_plugins),
                (PluginTypes.FUNCTION_TRACK_EXPORT, self._track_output_plugins),
                (PluginTypes.SERVICE, self._service_plugins),
                (PluginTypes.LIBRARY, self._library_plugins),
            )
        )

    @staticmethod
    def _register_plugin(cls_dict: dict, plg_class: type, plg_id: str) -> None:
        """注册插件"""
        if plg_id in cls_dict:
            if cls_dict[plg_id].metainfo.version >= plg_class.metainfo.version:
                raise PluginRegisteredError(
                    "插件惟一识别码`{}`所对应的插件已存在更高版本`{}`，请勿重复注册同一插件！".format(
                        plg_id, plg_class.metainfo
                    )
                )
        cls_dict[plg_id] = plg_class()

    def register_music_input_plugin(
        self,
        plugin_class: type,
        plugin_id: str,
    ) -> None:
        """注册输入插件-整首曲目"""
        self._register_plugin(self._music_input_plugins, plugin_class, plugin_id)

    def register_track_input_plugin(self, plugin_class: type, plugin_id: str) -> None:
        """注册输入插件-单个音轨"""
        self._register_plugin(self._track_input_plugins, plugin_class, plugin_id)

    def register_music_operate_plugin(self, plugin_class: type, plugin_id: str) -> None:
        """注册曲目处理插件"""
        self._register_plugin(self._music_operate_plugins, plugin_class, plugin_id)

    def register_track_operate_plugin(self, plugin_class: type, plugin_id: str) -> None:
        """注册音轨处理插件"""
        self._register_plugin(self._track_operate_plugins, plugin_class, plugin_id)

    def register_music_output_plugin(self, plugin_class: type, plugin_id: str) -> None:
        """注册输出插件-整首曲目"""
        self._register_plugin(self._music_output_plugins, plugin_class, plugin_id)

    def register_track_output_plugin(self, plugin_class: type, plugin_id: str) -> None:
        """注册输出插件-单个音轨"""
        self._register_plugin(self._track_output_plugins, plugin_class, plugin_id)

    def register_service_plugin(self, plugin_class: type, plugin_id: str) -> None:
        """注册服务插件"""
        self._register_plugin(self._service_plugins, plugin_class, plugin_id)

    def register_library_plugin(self, plugin_class: type, plugin_id: str) -> None:
        """注册支持库插件"""
        self._register_plugin(self._library_plugins, plugin_class, plugin_id)

    @staticmethod
    def _get_io_plugin_by_format(
        plugin_regdict: Mapping[str, T_IOPlugin], fpath_or_format: Union[Path, str]
    ) -> Generator[T_IOPlugin, None, None]:
        if isinstance(fpath_or_format, str):
            return (
                plugin
                for plugin in plugin_regdict.values()
                if plugin.can_handle_format(fpath_or_format)
            )
        elif isinstance(fpath_or_format, Path):
            return (
                plugin
                for plugin in plugin_regdict.values()
                if plugin.can_handle_file(fpath_or_format)
            )
        else:
            raise ParameterTypeError(
                "用于指定“导入全曲的数据之类型”的参数，其类型须为`Path`路径或字符串，而非`{}`类型的`{}`值".format(
                    type(fpath_or_format), fpath_or_format
                )
            )

    def get_music_input_plugin_by_format(
        self, filepath_or_format: Union[Path, str]
    ) -> Generator[MusicInputPluginBase, None, None]:
        """通过指定输入的文件或格式，以获取对应的全曲导入用插件"""
        return self._get_io_plugin_by_format(
            self._music_input_plugins, filepath_or_format
        )

    def get_track_input_plugin_by_format(
        self, filepath_or_format: Union[Path, str]
    ) -> Generator[TrackInputPluginBase, None, None]:
        """通过指定输入的文件或格式，以获取对应的单音轨导入用插件"""
        return self._get_io_plugin_by_format(
            self._track_input_plugins, filepath_or_format
        )

    def get_music_output_plugin_by_format(
        self, filepath_or_format: Union[Path, str]
    ) -> Generator[MusicOutputPluginBase, None, None]:
        """通过指定输出的文件或格式，以获取对应的导出全曲用插件"""
        return self._get_io_plugin_by_format(
            self._music_output_plugins, filepath_or_format
        )

    def get_track_output_plugin_by_format(
        self, filepath_or_format: Union[Path, str]
    ) -> Generator[TrackOutputPluginBase, None, None]:
        """通过指定输出的文件或格式，以获取对应的导出单个音轨用插件"""
        return self._get_io_plugin_by_format(
            self._track_output_plugins, filepath_or_format
        )

    def _get_plugin_by_name(
        self,
        plugin_regdict: Mapping[str, T_Plugin],
        plugin_name: str,
        plugin_usage: str = "",
    ) -> T_Plugin:
        """通过指定名称，以获取对应的插件，当名称重叠时，取版本号最大的"""
        try:
            return max(
                [
                    plugin
                    for plugin in plugin_regdict.values()
                    if plugin.metainfo.name == plugin_name
                ],
                key=lambda plugin: plugin.metainfo.version,
            )
        except ValueError as e:
            raise PluginInstanceNotFoundError(
                "未找到“用于{}、名为`{}`”的插件".format(plugin_usage, plugin_name)
            ) from e

    def get_music_input_plugin(self, plugin_name: str) -> MusicInputPluginBase:
        """获取指定名称的全曲导入用插件，当名称重叠时，取版本号最大的"""
        return self._get_plugin_by_name(
            self._music_input_plugins, plugin_name, "导入全曲"
        )

    def get_track_input_plugin(self, plugin_name: str) -> TrackInputPluginBase:
        """获取指定名称的单音轨导入用插件，当名称重叠时，取版本号最大的"""
        return self._get_plugin_by_name(
            self._track_input_plugins, plugin_name, "导入单轨"
        )

    def get_music_operate_plugin(self, plugin_name: str) -> MusicOperatePluginBase:
        """获取指定名称的全曲处理用插件，当名称重叠时，取版本号最大的"""
        return self._get_plugin_by_name(
            self._music_operate_plugins, plugin_name, "处理整个曲目"
        )

    def get_track_operate_plugin(self, plugin_name: str) -> TrackOperatePluginBase:
        """获取指定名称的单音轨处理用插件，当名称重叠时，取版本号最大的"""
        return self._get_plugin_by_name(
            self._track_operate_plugins, plugin_name, "处理单个音轨"
        )

    def get_music_output_plugin(self, plugin_name: str) -> MusicOutputPluginBase:
        """获取指定名称的导出全曲用插件，当名称重叠时，取版本号最大的"""
        return self._get_plugin_by_name(
            self._music_output_plugins, plugin_name, "导出完整曲目"
        )

    def get_track_output_plugin(self, plugin_name: str) -> TrackOutputPluginBase:
        """获取指定名称的导出单音轨用插件，当名称重叠时，取版本号最大的"""
        return self._get_plugin_by_name(
            self._track_output_plugins, plugin_name, "导出单个音轨"
        )

    def get_service_plugin(self, plugin_name: str) -> ServicePluginBase:
        """获取服务用插件，当名称重叠时，取版本号最大的"""
        return self._get_plugin_by_name(self._service_plugins, plugin_name, "提供服务")

    def get_library_plugin(self, plugin_name: str) -> LibraryPluginBase:
        """获取依赖库类插件，当名称重叠时，取版本号最高的"""
        return self._get_plugin_by_name(
            self._library_plugins, plugin_name, "作为依赖库"
        )

    def supported_input_formats(self) -> Set[str]:
        """所有支持的导入格式"""
        return set(
            chain.from_iterable(
                plugin.supported_formats
                for plugin in chain(
                    self._music_input_plugins.values(),
                    self._track_input_plugins.values(),
                )
            )
        )

    def supported_output_formats(self) -> Set[str]:
        """所有支持的导出格式"""
        return set(
            chain.from_iterable(
                plugin.supported_formats
                for plugin in chain(
                    self._music_output_plugins.values(),
                    self._track_output_plugins.values(),
                )
            )
        )


_global_plugin_registry = PluginRegistry()
"""全局插件注册表实例"""


def __plugin_regist_decorator(plg_id: str, rgst_func: Callable[[type, str], None]):

    def decorator(cls):
        global _global_plugin_registry
        cls.id = plg_id
        rgst_func(cls, plg_id)
        return cls

    return decorator


def music_input_plugin(plugin_id: str):
    """全曲输入用插件装饰器"""
    return __plugin_regist_decorator(
        plugin_id, _global_plugin_registry.register_music_input_plugin
    )


def track_input_plugin(plugin_id: str):
    """单轨输入用插件装饰器"""
    return __plugin_regist_decorator(
        plugin_id, _global_plugin_registry.register_track_input_plugin
    )


def music_operate_plugin(plugin_id: str):
    """全曲处理用插件装饰器"""
    return __plugin_regist_decorator(
        plugin_id, _global_plugin_registry.register_music_operate_plugin
    )


def track_operate_plugin(plugin_id: str):
    """音轨处理插件装饰器"""
    return __plugin_regist_decorator(
        plugin_id, _global_plugin_registry.register_track_operate_plugin
    )


def music_output_plugin(plugin_id: str):
    """乐曲输出用插件装饰器"""
    return __plugin_regist_decorator(
        plugin_id, _global_plugin_registry.register_music_output_plugin
    )


def track_output_plugin(plugin_id: str):
    """音轨输出用插件装饰器"""
    return __plugin_regist_decorator(
        plugin_id, _global_plugin_registry.register_track_output_plugin
    )


def service_plugin(plugin_id: str):
    """服务插件装饰器"""
    return __plugin_regist_decorator(
        plugin_id, _global_plugin_registry.register_service_plugin
    )


def library_plugin(plugin_id: str):
    """支持库插件装饰器"""

    return __plugin_regist_decorator(
        plugin_id, _global_plugin_registry.register_library_plugin
    )
