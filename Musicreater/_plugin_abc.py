# -*- coding: utf-8 -*-

"""
存储 音·创 v3 的插件基类，提供抽象接口以供实际插件使用
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

# =====================
# NOTE: [WARNING]
# 这个文件是一坨屎山代码
# 请勿模仿，请多包容
# =====================


import sys

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
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

# 已经全部由 plugins.py 提供接口
# 请用户从 plugins.py 导入
# 不要在这里导，会坏掉的

# __all__ = [
#     # 枚举类
#     "PluginType",
#     # 抽象基类/数据类（插件参数定义）
#     "PluginConfig",
#     "PluginMetaInformation",
#     # 抽象基类（插件定义）
#     "MusicInputPlugin",
#     "TrackInputPlugin",
#     "MusicOperatePlugin",
#     "TrackOperatePlugin",
#     "MusicOutputPlugin",
#     "TrackOutputPlugin",
#     "ServicePlugin",
#     "LibraryPlugin",
#     # 插件注册用装饰函数
#     "music_input_plugin",
#     "track_input_plugin",
#     "music_operate_plugin",
#     "track_operate_plugin",
#     "music_output_plugin",
#     "track_output_plugin",
#     "service_plugin",
#     "library_plugin",
# ]


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

    FUNCTION_MUSIC_IMPORT = "import_music_data"
    FUNCTION_TRACK_IMPORT = "import_track_data"
    FUNCTION_MUSIC_OPERATE = "music_data_operating"
    FUNCTION_TRACK_OPERATE = "track_data_operating"
    FUNCTION_MUSIC_EXPORT = "export_music_data"
    FUNCTION_TRACK_EXPORT = "export_track_data"
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
    dependencies: Sequence[str] = tuple()
    """插件是否对其他插件存在依赖"""


class TopPluginBase(ABC):
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
            if not cls.__name__.endswith("PluginBase"):
                raise PluginMetainfoNotFoundError(
                    "类`{cls_name}`必须定义一个`metainfo`属性。".format(
                        cls_name=cls.__name__
                    )
                )


class TopInOutPluginBase(TopPluginBase, ABC):
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


class MusicInputPluginBase(TopInOutPluginBase, ABC):
    """导入用插件抽象基类-完整曲目"""

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        if cls.metainfo.type != PluginType.FUNCTION_MUSIC_IMPORT:
            raise PluginMetainfoValueError(
                "插件类`{cls_name}`是从`MusicInputPlugin`继承的，该类的子类应当为一个`PluginType.FUNCTION_MUSIC_IMPORT`类型的插件，而不是`PluginType.{cls_type}`".format(
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


class TrackInputPluginBase(TopInOutPluginBase, ABC):
    """导入用插件抽象基类-单个音轨"""

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        if cls.metainfo.type != PluginType.FUNCTION_TRACK_IMPORT:
            raise PluginMetainfoValueError(
                "插件类`{cls_name}`是从`TrackInputPlugin`继承的，该类的子类应当为一个`PluginType.FUNCTION_TRACK_IMPORT`类型的插件，而不是`PluginType.{cls_type}`".format(
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


class MusicOperatePluginBase(TopPluginBase, ABC):
    """音乐处理用插件抽象基类-完整曲目"""

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        if cls.metainfo.type != PluginType.FUNCTION_MUSIC_OPERATE:
            raise PluginMetainfoValueError(
                "插件类`{cls_name}`是从`MusicOperatePlugin`继承的，该类的子类应当为一个`PluginType.FUNCTION_MUSIC_OPERATE`类型的插件，而不是`PluginType.{cls_type}`".format(
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


class TrackOperatePluginBase(TopPluginBase, ABC):
    """音乐处理用插件抽象基类-单个音轨"""

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        if cls.metainfo.type != PluginType.FUNCTION_TRACK_OPERATE:
            raise PluginMetainfoValueError(
                "插件类`{cls_name}`是从`TrackOperatePlugin`继承的，该类的子类应当为一个`PluginType.FUNCTION_TRACK_OPERATE`类型的插件，而不是`PluginType.{cls_type}`".format(
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


class MusicOutputPluginBase(TopInOutPluginBase, ABC):
    """导出用插件的抽象基类-完整曲目"""

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        if cls.metainfo.type != PluginType.FUNCTION_MUSIC_EXPORT:
            raise PluginMetainfoValueError(
                "插件类`{cls_name}`是从`MusicOutputPlugin`继承的，该类的子类应当为一个`PluginType.FUNCTION_MUSIC_EXPORT`类型的插件，而不是`PluginType.{cls_type}`".format(
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


class TrackOutputPluginBase(TopInOutPluginBase, ABC):
    """导出用插件的抽象基类-单个音轨"""

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        if cls.metainfo.type != PluginType.FUNCTION_TRACK_EXPORT:
            raise PluginMetainfoValueError(
                "插件类`{cls_name}`是从`TrackOutputPlugin`继承的，该类的子类应当为一个`PluginType.FUNCTION_TRACK_EXPORT`类型的插件，而不是`PluginType.{cls_type}`".format(
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


class ServicePluginBase(TopPluginBase, ABC):
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


class LibraryPluginBase(TopPluginBase, ABC):
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
