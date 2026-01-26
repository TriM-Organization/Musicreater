# -*- coding: utf-8 -*-

"""
存储 音·创 v3 的插件接口与管理相关，提供抽象基类以供其他插件使用
"""

"""
版权所有 © 2025 金羿
Copyright © 2025 Eilles

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md

# =====================
# NOTE: [WARNING]
# 这个文件是一坨屎山代码
# 请勿模仿，请多包容
# =====================


import sys

from abc import ABC, abstractmethod, ABCMeta
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import (
    Dict,
    Any,
    Optional,
    List,
    Tuple,
    Union,
    Sequence,
    BinaryIO,
    Generator,
    Iterator,
    Set,
)
from itertools import chain

if sys.version_info >= (3, 11):
    import tomllib
    import tomli_w
else:
    import tomli as tomllib  # 第三方包
    import tomli_w

from .exceptions import (
    PluginConfigDumpError,
    PluginConfigLoadError,
    PluginMetainfoNotFoundError,
    PluginMetainfoTypeError,
    PluginMetainfoValueError,
    PluginAttributeNotFoundError,
    ParameterTypeError,
    PluginInstanceNotFoundError,
)
from .data import SingleMusic, SingleTrack

__all__ = [
    # 枚举类
    "PluginType",
    # 抽象基类/数据类（插件参数定义）
    "PluginConfig",
    "PluginMetaInformation",
    # 抽象基类（插件定义）
    "MusicInputPlugin",
    "TrackInputPlugin",
    "MusicOperatePlugin",
    "TrackOperatePlugin",
    "MusicOutputPlugin",
    "TrackOutputPlugin",
    "ServicePlugin",
    "LibraryPlugin",
    # 插件注册用装饰函数
    "music_input_plugin",
    "track_input_plugin",
    "music_operate_plugin",
    "track_operate_plugin",
    "music_output_plugin",
    "track_output_plugin",
    "service_plugin",
    "library_plugin",
    # 全局插件注册表
    "plugin_registry",
]


@dataclass
class PluginConfig(ABC):
    """插件配置基类"""

    def to_dict(self) -> Dict[str, Any]:
        """字典化配置文件"""
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PluginConfig":
        """从字典创建配置实例"""
        # 只保留类中定义的字段
        field_names = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in field_names}
        return cls(**filtered_data)

    def save_to_file(self, file_path: Path) -> None:
        """保存配置到文件"""
        if file_path.suffix.upper() == ".TOML":
            file_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            raise PluginConfigDumpError(
                "插件配置文件类型不应为`{}`，须为`TOML`格式。".format(file_path.suffix)
            )

        try:
            with file_path.open("wb") as f:
                tomli_w.dump(self.to_dict(), f, multiline_strings=False, indent=4)
        except Exception as e:
            raise PluginConfigDumpError(e)

    @classmethod
    def load_from_file(cls, file_path: Path) -> "PluginConfig":
        """从文件加载配置"""
        try:
            with file_path.open("rb") as f:
                return cls.from_dict(tomllib.load(f))
        except Exception as e:
            raise PluginConfigLoadError(e)


class PluginType(str, Enum):
    """插件类型枚举"""

    FUNCTION_IMPORT = "import_data"
    FUNCTION_EXPORT = "export_data"
    FUNCTION_OPERATE = "data_operate"
    SERVICE = "service"
    LIBRARY = "library"


@dataclass
class PluginMetaInformation(ABC):
    """插件元信息"""

    name: str
    """插件名称，应为惟一之名"""
    author: str
    """插件作者"""
    description: str
    """插件简介"""
    version: Tuple[int, ...]
    """插件版本号"""
    type: PluginType
    """插件类型"""
    license: str = "MIT License"
    """插件发布时采用的许可协议"""
    dependencies: Sequence[str] = []
    """插件是否对其他插件存在依赖"""


class TopBasePlugin(ABC):
    """所有插件的抽象基类"""

    metainfo: PluginMetaInformation
    """插件元信息"""

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        if hasattr(cls, "metainfo"):
            if not isinstance(cls.metainfo, PluginMetaInformation):
                raise PluginMetainfoTypeError(
                    "类`{cls_name}`之属性`metainfo`的类型，必须为`PluginMetaInformation`".format(
                        cls_name=cls.__name__
                    )
                )
        else:
            raise PluginMetainfoNotFoundError(
                "类`{cls_name}`必须定义一个`metainfo`属性。".format(
                    cls_name=cls.__name__
                )
            )


class TopInOutBasePlugin(TopBasePlugin, ABC):
    """导入导出用抽象基类"""

    supported_formats: Tuple[str, ...] = tuple()
    """支持的格式"""

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        if hasattr(cls, "supported_formats"):
            if cls.supported_formats:
                # 强制转换为大写，并使用元组
                cls.supported_formats = tuple(map(str.upper, cls.supported_formats))
            else:
                cls.supported_formats = tuple()
        else:
            raise PluginAttributeNotFoundError(
                "用于导入导出数据的类`{cls_name}`必须定义一个`supported_formats`属性。".format(
                    cls_name=cls.__name__
                )
            )

    def can_handle_file(self, file_path: Path) -> bool:
        """判断是否可处理某个文件"""
        return file_path.suffix.upper().endswith(self.supported_formats)

    def can_handle_format(self, format_name: str) -> bool:
        """判断是否可处理某个格式"""
        return format_name.upper().endswith(self.supported_formats)


class MusicInputPlugin(TopInOutBasePlugin, ABC):
    """导入用插件抽象基类-完整曲目"""

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        if cls.metainfo.type != PluginType.FUNCTION_IMPORT:
            raise PluginMetainfoValueError(
                "插件类`{cls_name}`是从`MusicInputPlugin`继承的，该类的子类应当为一个`PluginType.FUNCTION_IMPORT`类型的插件，而不是`PluginType.{cls_type}`".format(
                    cls_name=cls.__name__,
                    cls_type=cls.metainfo.type.name,
                )
            )

    @abstractmethod
    def loadbytes(
        self, bytes_buffer_in: BinaryIO, config: Optional[PluginConfig]
    ) -> "SingleMusic":
        """从字节流加载数据到完整曲目"""
        pass

    def load(self, file_path: Path, config: Optional[PluginConfig]) -> "SingleMusic":
        """从文件加载数据到完整曲目"""
        with file_path.open("rb") as f:
            return self.loadbytes(f, config)


class TrackInputPlugin(TopInOutBasePlugin, ABC):
    """导入用插件抽象基类-单个音轨"""

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        if cls.metainfo.type != PluginType.FUNCTION_IMPORT:
            raise PluginMetainfoValueError(
                "插件类`{cls_name}`是从`TrackInputPlugin`继承的，该类的子类应当为一个`PluginType.FUNCTION_IMPORT`类型的插件，而不是`PluginType.{cls_type}`".format(
                    cls_name=cls.__name__,
                    cls_type=cls.metainfo.type.name,
                )
            )

    @abstractmethod
    def loadbytes(
        self, bytes_buffer_in: BinaryIO, config: Optional[PluginConfig]
    ) -> "SingleTrack":
        """从字节流加载音符数据到单个音轨"""
        pass

    def load(self, file_path: Path, config: Optional[PluginConfig]) -> "SingleTrack":
        """从文件加载音符数据到单个音轨"""
        with file_path.open("rb") as f:
            return self.loadbytes(f, config)


class MusicOperatePlugin(TopBasePlugin, ABC):
    """音乐处理用插件抽象基类-完整曲目"""

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        if cls.metainfo.type != PluginType.FUNCTION_OPERATE:
            raise PluginMetainfoValueError(
                "插件类`{cls_name}`是从`MusicOperatePlugin`继承的，该类的子类应当为一个`PluginType.FUNCTION_OPERATE`类型的插件，而不是`PluginType.{cls_type}`".format(
                    cls_name=cls.__name__,
                    cls_type=cls.metainfo.type.name,
                )
            )

    @abstractmethod
    def process(
        self, data: "SingleMusic", config: Optional[PluginConfig]
    ) -> "SingleMusic":
        """处理完整曲目的数据"""
        pass


class TrackOperatePlugin(TopBasePlugin, ABC):
    """音乐处理用插件抽象基类-单个音轨"""

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        if cls.metainfo.type != PluginType.FUNCTION_OPERATE:
            raise PluginMetainfoValueError(
                "插件类`{cls_name}`是从`TrackOperatePlugin`继承的，该类的子类应当为一个`PluginType.FUNCTION_OPERATE`类型的插件，而不是`PluginType.{cls_type}`".format(
                    cls_name=cls.__name__,
                    cls_type=cls.metainfo.type.name,
                )
            )

    @abstractmethod
    def process(
        self, data: "SingleTrack", config: Optional[PluginConfig]
    ) -> "SingleTrack":
        """处理单个音轨的音符数据"""
        pass


class MusicOutputPlugin(TopInOutBasePlugin, ABC):
    """导出用插件的抽象基类-完整曲目"""

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        if cls.metainfo.type != PluginType.FUNCTION_EXPORT:
            raise PluginMetainfoValueError(
                "插件类`{cls_name}`是从`MusicOutputPlugin`继承的，该类的子类应当为一个`PluginType.FUNCTION_EXPORT`类型的插件，而不是`PluginType.{cls_type}`".format(
                    cls_name=cls.__name__,
                    cls_type=cls.metainfo.type.name,
                )
            )

    @abstractmethod
    def dumpbytes(
        self, data: "SingleMusic", config: Optional[PluginConfig]
    ) -> BinaryIO:
        """将完整曲目导出为对应格式的字节流"""
        pass

    @abstractmethod
    def dump(
        self, data: "SingleMusic", file_path: Path, config: Optional[PluginConfig]
    ):
        """将完整曲目导出为对应格式的文件"""
        pass


class TrackOutputPlugin(TopInOutBasePlugin, ABC):
    """导出用插件的抽象基类-单个音轨"""

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        if cls.metainfo.type != PluginType.FUNCTION_EXPORT:
            raise PluginMetainfoValueError(
                "插件类`{cls_name}`是从`TrackOutputPlugin`继承的，该类的子类应当为一个`PluginType.FUNCTION_EXPORT`类型的插件，而不是`PluginType.{cls_type}`".format(
                    cls_name=cls.__name__,
                    cls_type=cls.metainfo.type.name,
                )
            )

    @abstractmethod
    def dumpbytes(
        self, data: "SingleTrack", config: Optional[PluginConfig]
    ) -> BinaryIO:
        """将单个音轨导出为对应格式的字节流"""
        pass

    @abstractmethod
    def dump(
        self, data: "SingleTrack", file_path: Path, config: Optional[PluginConfig]
    ):
        """将单个音轨导出为对应格式的文件"""
        pass


class ServicePlugin(TopBasePlugin, ABC):
    """服务插件抽象基类"""

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        if cls.metainfo.type != PluginType.SERVICE:
            raise PluginMetainfoValueError(
                "插件类`{cls_name}`是从`ServicePlugin`继承的，该类的子类应当为一个`PluginType.SERVICE`类型的插件，而不是`PluginType.{cls_type}`".format(
                    cls_name=cls.__name__,
                    cls_type=cls.metainfo.type.name,
                )
            )

    @abstractmethod
    def serve(self, config: Optional[PluginConfig], *args) -> None:
        """服务插件的运行逻辑"""
        pass


class LibraryPlugin(TopBasePlugin, ABC):
    """插件依赖库的抽象基类"""

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        if cls.metainfo.type != PluginType.LIBRARY:
            raise PluginMetainfoValueError(
                "插件类`{cls_name}`是从`LibraryPlugin`继承的，该类的子类应当为一个`PluginType.LIBRARY`类型的插件，而不是`PluginType.{cls_type}`".format(
                    cls_name=cls.__name__,
                    cls_type=cls.metainfo.type.name,
                )
            )

    # 怎么？
    # 插件的彼此依赖就不需要什么调用了吧


class PluginRegistry:
    """插件注册管理器"""

    def __init__(self):
        self._music_input_plugins: List[MusicInputPlugin] = []
        self._track_input_plugins: List[TrackInputPlugin] = []
        self._music_operate_plugins: List[MusicOperatePlugin] = []
        self._track_operate_plugins: List[TrackOperatePlugin] = []
        self._music_output_plugins: List[MusicOutputPlugin] = []
        self._track_output_plugins: List[TrackOutputPlugin] = []
        self._service_plugins: List[ServicePlugin] = []
        self._library_plugins: List[LibraryPlugin] = []

    def register_music_input_plugin(self, plugin_class: type) -> None:
        """注册输入插件-整首曲目"""
        plugin_instance = plugin_class()
        self._music_input_plugins.append(plugin_instance)

    def register_track_input_plugin(self, plugin_class: type) -> None:
        """注册输入插件-单个音轨"""
        plugin_instance = plugin_class()
        self._track_input_plugins.append(plugin_instance)

    def register_music_operate_plugin(self, plugin_class: type) -> None:
        """注册曲目处理插件"""
        plugin_instance = plugin_class()
        self._music_operate_plugins.append(plugin_instance)

    def register_track_operate_plugin(self, plugin_class: type) -> None:
        """注册音轨处理插件"""
        plugin_instance = plugin_class()
        self._track_operate_plugins.append(plugin_instance)

    def register_music_output_plugin(self, plugin_class: type) -> None:
        """注册输出插件-整首曲目"""
        plugin_instance = plugin_class()
        self._music_output_plugins.append(plugin_instance)

    def register_track_output_plugin(self, plugin_class: type) -> None:
        """注册输出插件-单个音轨"""
        plugin_instance = plugin_class()
        self._track_output_plugins.append(plugin_instance)

    def register_service_plugin(self, plugin_class: type) -> None:
        """注册服务插件"""
        plugin_instance = plugin_class()
        self._service_plugins.append(plugin_instance)

    def register_library_plugin(self, plugin_class: type) -> None:
        """注册支持库插件"""
        plugin_instance = plugin_class()
        self._library_plugins.append(plugin_instance)

    def get_music_input_plugin_by_format(
        self, filepath_or_format: Union[Path, str]
    ) -> Generator[MusicInputPlugin, None, None]:
        """通过指定输入的文件或格式，以获取对应的全曲导入用插件"""
        if isinstance(filepath_or_format, str):
            for plugin in self._music_input_plugins:
                if plugin.can_handle_format(filepath_or_format):
                    yield plugin
        elif isinstance(filepath_or_format, Path):
            for plugin in self._music_input_plugins:
                if plugin.can_handle_file(filepath_or_format):
                    yield plugin
        else:
            raise ParameterTypeError(
                "用于指定“导入全曲的数据之类型”的参数，其类型须为`Path`路径或字符串，而非`{}`类型的`{}`值".format(
                    type(filepath_or_format), filepath_or_format
                )
            )

    def get_track_input_plugin_by_format(
        self, filepath_or_format: Union[Path, str]
    ) -> Generator[TrackInputPlugin, None, None]:
        """通过指定输入的文件或格式，以获取对应的单音轨导入用插件"""
        if isinstance(filepath_or_format, str):
            for plugin in self._track_input_plugins:
                if plugin.can_handle_format(filepath_or_format):
                    yield plugin
        elif isinstance(filepath_or_format, Path):
            for plugin in self._track_input_plugins:
                if plugin.can_handle_file(filepath_or_format):
                    yield plugin
        else:
            raise ParameterTypeError(
                "用于指定“导入单个音轨的数据之类型”的参数，其类型须为`Path`路径或字符串，而非`{}`类型的`{}`值".format(
                    type(filepath_or_format), filepath_or_format
                )
            )

    def get_music_output_plugin_by_format(
        self, filepath_or_format: Union[Path, str]
    ) -> Generator[MusicOutputPlugin, None, None]:
        """通过指定输出的文件或格式，以获取对应的导出全曲用插件"""
        if isinstance(filepath_or_format, str):
            for plugin in self._music_output_plugins:
                if plugin.can_handle_format(filepath_or_format):
                    yield plugin
        elif isinstance(filepath_or_format, Path):
            for plugin in self._music_output_plugins:
                if plugin.can_handle_file(filepath_or_format):
                    yield plugin
        else:
            raise ParameterTypeError(
                "用于指定“全曲数据导出的类型”的参数，其类型须为`Path`路径或字符串，而非`{}`类型的`{}`值".format(
                    type(filepath_or_format), filepath_or_format
                )
            )

    def get_track_output_plugin_by_format(
        self, filepath_or_format: Union[Path, str]
    ) -> Generator[TrackOutputPlugin, None, None]:
        """通过指定输出的文件或格式，以获取对应的导出单个音轨用插件"""
        if isinstance(filepath_or_format, str):
            for plugin in self._track_output_plugins:
                if plugin.can_handle_format(filepath_or_format):
                    yield plugin
        elif isinstance(filepath_or_format, Path):
            for plugin in self._track_output_plugins:
                if plugin.can_handle_file(filepath_or_format):
                    yield plugin
        else:
            raise ParameterTypeError(
                "用于指定“单音轨数据导出的类型”的参数，其类型须为`Path`路径或字符串，而非`{}`类型的`{}`值".format(
                    type(filepath_or_format), filepath_or_format
                )
            )

    def get_music_input_plugin(self, plugin_name: str) -> MusicInputPlugin:
        """获取指定名称的全曲导入用插件，当名称重叠时，取版本号最大的"""
        try:
            return max(
                filter(
                    lambda plugin: plugin.metainfo.name == plugin_name,
                    self._music_input_plugins,
                ),
                key=lambda plugin: plugin.metainfo.version,
            )
        except ValueError:
            raise PluginInstanceNotFoundError(
                "未找到“用于导入曲目、名为`{}`”的插件".format(plugin_name)
            )

    def get_track_input_plugin(self, plugin_name: str) -> TrackInputPlugin:
        """获取指定名称的单音轨导入用插件，当名称重叠时，取版本号最大的"""
        try:
            return max(
                filter(
                    lambda plugin: plugin.metainfo.name == plugin_name,
                    self._track_input_plugins,
                ),
                key=lambda plugin: plugin.metainfo.version,
            )
        except ValueError:
            raise PluginInstanceNotFoundError(
                "未找到“用于导入单个音轨、名为`{}`”的插件".format(plugin_name)
            )

    def get_music_operate_plugin(self, plugin_name: str) -> MusicOperatePlugin:
        """获取指定名称的全曲处理用插件，当名称重叠时，取版本号最大的"""
        try:
            return max(
                filter(
                    lambda plugin: plugin.metainfo.name == plugin_name,
                    self._music_operate_plugins,
                ),
                key=lambda plugin: plugin.metainfo.version,
            )
        except ValueError:
            raise PluginInstanceNotFoundError(
                "未找到“用于处理整个曲目、名为`{}`”的插件".format(plugin_name)
            )

    def get_track_operate_plugin(self, plugin_name: str) -> TrackOperatePlugin:
        """获取指定名称的单音轨处理用插件，当名称重叠时，取版本号最大的"""
        try:
            return max(
                filter(
                    lambda plugin: plugin.metainfo.name == plugin_name,
                    self._track_operate_plugins,
                ),
                key=lambda plugin: plugin.metainfo.version,
            )
        except ValueError:
            raise PluginInstanceNotFoundError(
                "未找到“用于处理单个音轨、名为`{}`”的插件".format(plugin_name)
            )

    def get_music_output_plugin(self, plugin_name: str) -> MusicOutputPlugin:
        """获取指定名称的导出全曲用插件，当名称重叠时，取版本号最大的"""
        try:
            return max(
                filter(
                    lambda plugin: plugin.metainfo.name == plugin_name,
                    self._music_output_plugins,
                ),
                key=lambda plugin: plugin.metainfo.version,
            )
        except ValueError:
            raise PluginMetainfoNotFoundError(
                "未找到“用于导出完整曲目、名为`{}`”的插件".format(plugin_name)
            )

    def get_track_output_plugin(self, plugin_name: str) -> TrackOutputPlugin:
        """获取指定名称的导出单音轨用插件，当名称重叠时，取版本号最大的"""
        try:
            return max(
                filter(
                    lambda plugin: plugin.metainfo.name == plugin_name,
                    self._track_output_plugins,
                ),
                key=lambda plugin: plugin.metainfo.version,
            )
        except ValueError:
            raise PluginMetainfoNotFoundError(
                "未找到“用于导出单个音轨、名为`{}`”的插件".format(plugin_name)
            )

    def get_service_plugin(self, plugin_name: str) -> ServicePlugin:
        """获取服务用插件，当名称重叠时，取版本号最大的"""
        try:
            return max(
                filter(
                    lambda plugin: plugin.metainfo.name == plugin_name,
                    self._service_plugins,
                ),
                key=lambda plugin: plugin.metainfo.version,
            )
        except ValueError:
            raise PluginInstanceNotFoundError(
                "未找到名为`{}`的服务用插件".format(plugin_name)
            )

    def get_library_plugin(self, plugin_name: str) -> LibraryPlugin:
        """获取依赖库类插件，当名称重叠时，取版本号最高的"""
        try:
            return max(
                filter(
                    lambda plugin: plugin.metainfo.name == plugin_name,
                    self._library_plugins,
                ),
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


plugin_registry = PluginRegistry()
"""全局插件注册表实例"""


def music_input_plugin(metainfo: PluginMetaInformation):
    """全曲输入用插件装饰器"""

    def decorator(cls):
        global plugin_registry
        cls.metainfo = metainfo
        plugin_registry.register_music_input_plugin(cls)
        return cls

    return decorator


def track_input_plugin(metainfo: PluginMetaInformation):
    """单轨输入用插件装饰器"""

    def decorator(cls):
        global plugin_registry
        cls.metainfo = metainfo
        plugin_registry.register_track_input_plugin(cls)
        return cls

    return decorator


def music_operate_plugin(metainfo: PluginMetaInformation):
    """全曲处理用插件装饰器"""

    def decorator(cls):
        global plugin_registry
        cls.metainfo = metainfo
        plugin_registry.register_music_operate_plugin(cls)
        return cls

    return decorator


def track_operate_plugin(metainfo: PluginMetaInformation):
    """音轨处理插件装饰器"""

    def decorator(cls):
        global plugin_registry
        cls.metainfo = metainfo
        plugin_registry.register_track_operate_plugin(cls)
        return cls

    return decorator


def music_output_plugin(metainfo: PluginMetaInformation):
    """乐曲输出用插件装饰器"""

    def decorator(cls):
        global plugin_registry
        cls.metainfo = metainfo
        plugin_registry.register_music_output_plugin(cls)
        return cls

    return decorator


def track_output_plugin(metainfo: PluginMetaInformation):
    """音轨输出用插件装饰器"""

    def decorator(cls):
        global plugin_registry
        cls.metainfo = metainfo
        plugin_registry.register_track_output_plugin(cls)
        return cls

    return decorator


def service_plugin(metainfo: PluginMetaInformation):
    """服务插件装饰器"""

    def decorator(cls):
        global plugin_registry
        cls.metainfo = metainfo
        plugin_registry.register_service_plugin(cls)
        return cls

    return decorator


def library_plugin(metainfo: PluginMetaInformation):
    """支持库插件装饰器"""

    def decorator(cls):
        global plugin_registry
        cls.metainfo = metainfo
        plugin_registry.register_library_plugin(cls)
        return cls

    return decorator
