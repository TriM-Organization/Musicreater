# -*- coding: utf-8 -*-

"""
音·创 v3 用到的一些报错类型
"""

"""
版权所有 © 2026 金羿 & 玉衡Alioth
Copyright © 2026 Eilles & YuhengAlioth

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md

# “
# There are planty of "exception"s in this library
# for I know I will always go with my heart.
# ”     —— Cyberdevil by resnah


class MusicreaterBaseException(Exception):
    """音·创 v3 的所有错误均继承于此"""

    def __init__(self, *args):
        """音·创 的所有错误均继承于此"""
        super().__init__("[音·创] - ", *args)

    def meow(self):
        for i in self.args:
            print(i + "喵~", end="：")

    def crash_it(self):
        raise self

    def __str__(self) -> str:
        return "".join(self.args)


# =====================================
# NOTE
# 面对用户时候爆出去的我们认为这就是“外部错误”
# 如果是在程序内部数据传输等情况下出现的就是“内部错误”
# 例如，无法读取文件，这就是一个外部错误
# 某个参数的数据类型错误，这就是内部错误
# =====================================


class MusicreaterInnerlyError(MusicreaterBaseException):
    """内部错误"""

    def __init__(self, *args):
        """内部错误（面向开发者的报错信息）"""
        super().__init__("内部错误 - ", *args)


class MusicreaterOuterlyError(MusicreaterBaseException):
    """外部错误"""

    def __init__(self, *args):
        """外部错误（面向用户的报错信息）"""
        super().__init__("外部错误 - ", *args)


class InnerlyParameterError(MusicreaterInnerlyError):
    """内部传参错误"""

    def __init__(self, *args):
        """参数错误"""
        super().__init__("传参错误 - ", *args)


class ParameterTypeError(InnerlyParameterError, TypeError):
    """参数类型错误"""

    def __init__(self, *args):
        """参数类型错误"""
        super().__init__("参数类型错误：", *args)


class ParameterValueError(InnerlyParameterError, ValueError):
    """参数值存在错误"""

    def __init__(self, *args):
        """参数其值存在错误"""
        super().__init__("参数数值错误：", *args)


class PluginNotSpecifiedError(InnerlyParameterError, LookupError):
    """未指定插件"""

    def __init__(self, *args):
        """未指定插件"""
        super().__init__("未指定插件：", *args)


class OuterlyParameterError(MusicreaterOuterlyError):
    """外部参数错误"""

    def __init__(self, *args):
        """参数错误"""
        super().__init__("参数错误 - ", *args)


class ZeroSpeedError(OuterlyParameterError, ZeroDivisionError):
    """以 0 作为播放速度的错误"""

    def __init__(self, *args):
        """以 0 作为播放速度的错误"""
        super().__init__("播放速度为零：", *args)


class IllegalMinimumVolumeError(OuterlyParameterError, ValueError):
    """最小播放音量有误的错误"""

    def __init__(self, *args):
        """最小播放音量错误"""
        super().__init__("最小播放音量超出范围：", *args)


class FileFormatNotSupportedError(MusicreaterOuterlyError):
    """不支持的文件格式"""

    def __init__(self, *args):
        """文件格式不受支持"""
        super().__init__("不支持的文件格式：", *args)


class NoteBinaryDecodeError(MusicreaterOuterlyError):
    """音乐存储二进制数据解码错误"""

    def __init__(self, *args):
        """音乐存储二进制数据无法正确解码"""
        super().__init__("解码音乐存储二进制数据时出现问题 - ", *args)


class SingleNoteDecodeError(NoteBinaryDecodeError):
    """单个音符的二进制数据解码错误"""

    def __init__(self, *args):
        """单个音符的二进制数据无法正确解码"""
        super().__init__("音符解码出错：", *args)


class NoteBinaryFileTypeError(NoteBinaryDecodeError):
    """音乐存储二进制数据的文件类型错误"""

    def __init__(self, *args):
        """无法识别音乐存储文件的类型"""
        super().__init__("无法识别音乐存储文件对应的类型：", *args)


class NoteBinaryFileVerificationFailed(NoteBinaryDecodeError):
    """音乐存储二进制数据校验失败"""

    def __init__(self, *args):
        """音乐存储文件与其校验值不一致"""
        super().__init__("音乐存储文件校验失败：", *args)


class PluginDefineError(MusicreaterInnerlyError):
    """插件定义错误（内部相关）"""

    def __init__(self, *args):
        """插件本身存在错误"""
        super().__init__("插件内部错误 - ", *args)


class PluginInstanceNotFoundError(PluginDefineError, LookupError):
    """插件实例未找到"""

    def __init__(self, *args):
        """插件实例未找到"""
        super().__init__("插件实例未找到：", *args)


class PluginAttributeNotFoundError(PluginDefineError, AttributeError):
    """插件属性定义错误"""

    def __init__(self, *args):
        """插件属性定义错误"""
        super().__init__("插件类的必要属性不存在：", *args)


class PluginMetainfoError(PluginDefineError):
    """插件元信息定义错误"""

    def __init__(self, *args):
        """插件元信息定义错误"""
        super().__init__("插件元信息定义错误 - ", *args)


class PluginMetainfoTypeError(PluginMetainfoError, TypeError):
    """插件元信息定义类型错误"""

    def __init__(self, *args):
        """插件元信息定义类型错误"""
        super().__init__("插件元信息类型错误：", *args)


class PluginMetainfoValueError(PluginMetainfoError, ValueError):
    """插件元信息定义值错误"""

    def __init__(self, *args):
        """插件元信息定义值错误"""
        super().__init__("插件元信息数值错误：", *args)


class PluginMetainfoNotFoundError(PluginMetainfoError, PluginAttributeNotFoundError):
    """插件元信息定义缺少错误"""

    def __init__(self, *args):
        """插件元信息定义缺少错误"""
        super().__init__("插件元信息未定义：", *args)


class PluginLoadError(MusicreaterOuterlyError):
    """插件加载错误（外部相关）"""

    def __init__(self, *args):
        """插件加载错误"""
        super().__init__("插件加载错误 - ", *args)


class PluginDependencyNotFound(PluginLoadError):
    """插件依赖未找到"""

    def __init__(self, *args):
        super().__init__("未找到所需的插件依赖：", *args)


class PluginNotFoundError(PluginLoadError):
    """插件未找到"""

    def __init__(self, *args):
        """插件未找到"""
        super().__init__("无法找到插件：", *args)


class PluginRegisteredError(PluginLoadError):
    """插件重复注册"""

    def __init__(self, *args):
        """插件已被注册注册"""
        super().__init__("插件重复注册：", *args)


class PluginConfigRelatedError(MusicreaterOuterlyError):
    """插件配置相关错误"""

    def __init__(self, *args):
        """插件配置相关错误"""
        super().__init__("插件配置相关错误 - ", *args)


class PluginConfigLoadError(PluginLoadError, PluginConfigRelatedError):
    """插件配置加载错误"""

    def __init__(self, *args):
        """配置文件无法加载"""
        super().__init__("插件配置文件加载错误：", *args)


class PluginConfigDumpError(PluginConfigRelatedError):
    """插件配置保存错误"""

    def __init__(self, *args):
        """配置文件无法保存"""
        super().__init__("插件配置文件保存错误：", *args)
