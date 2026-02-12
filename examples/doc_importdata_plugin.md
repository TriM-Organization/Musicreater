

# 示例插件：导入音符数据

> 版权所有 © 2026 金羿  
> Copyright © 2026 Eilles  

睿乐组织 开发交流群 [861684859](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=fxNYIX_zKMgaO8X6K7pP7tHtLB7JRvdX&noverify=0&group_code=861684859)  
Email [TriM-Organization@hotmail.com](mailto:TriM-Organization@hotmail.com)  

```license
本示例模块开放授权，同时，本教程文件已开放至公共领域。
请注意：
若是对本文件的直接转载（在形式上没有修改、增删、添加注释，或单纯修改排版、翻译、录屏、截图）
则该使用者需要在转载所及之处，明确在转载的内容开头标注本文之原始著作权人
在当前文件下，该原始著作权人为金羿(Eilles)
如果是对本文进行了一定程度上的修改和补充、或者以不同方式演绎本文件（如制成视频教程等）
则无需标注原作者，允许该使用者自行署名

本声明仅限于包含此声明的本文件，本声明与项目内其他文件无关。
```

## 新建文件夹 · 基础模块知识


首先，一个 **音·创 v3** 的插件应当存储于一个 Python 模块之中，也就是插件存在于可以被 import 语句引入的 module 中。

这就意味着，承载插件的模块本质上可以是多个 Python 的 `.py` 文件组成的，带有 `__init__.py` 的一个文件夹；
或者是一个简单的 `.py` 文件。

我们有这种共识：你已经知道了模块的相关知识，我后面无需赘述插件和模块的区别。

## 开始编写插件 · 插件基础


首先导入插件所需的类。

在这里我们是一个用来导入数据的插件。

所以就需要导入 `MusicInputPluginBase` 类和 `music_input_plugin` 函数。

同时，`PluginMetaInformation` 类和 `PluginTypes` 类也必须导入，这是插件的元信息所需要的。

```python
from Musicreater.plugins import (
    music_input_plugin,
    PluginMetaInformation,
    PluginTypes,
    MusicInputPluginBase,
)
```

如果插件需要配置，那么请再导入 `PluginConfig` 类，并从此继承一个类，且须用 dataclass 装饰器来注册之。
_对于这个类的使用方式，可以阅读 dataclass 的官方文档_

```python
from Musicreater.plugins import PluginConfig
from dataclasses import dataclass
@dataclass
class ExampleImportConfig(PluginConfig):
    example_config_item3: bool
    example_config_item1: str = "example_config_item"
    example_config_item2: int = 0
```

## 编写插件 · 开始

接着我们来制作一个插件。

首先，一个 **音·创 v3** 的插件应当是一个继承自我们已经准备好的插件基类的**类**（缩句：插件是类）；
在 **音·创 v3** 中，任何对音乐的操作，包括导入、导出、处理，都分为对 **整首曲目** 的操作和对 **单个音轨** 的操作。

我们的样例是一个对**整首曲目**进行**导入操作**的插件，因此需要继承 `MusicInputPluginBase` 类。
插件类的类名称不得以 `Base` 结尾，因为咱写的是插件，不是插件基类。

在插件的类的开头，需要用插件注册装饰函数来对插件类装饰。
```python
@music_input_plugin("example_import_plugin")
class xxx:
    ...
```
我们这里对应插件类型的注册器是 `music_input_plugin` 函数。
在注册器函数后的参数，是这个插件的惟一识别码。不应与其他插件混淆。
通常可以是这个插件的功能描述、或者就是插件名。

接着编写这个插件，也即是此类。
每个插件的类必须包含一个用于指定插件元信息的 `metainfo` 属性。
如果插件是导入数据或者导出数据的插件，则必须包含一个 `supported_formats` 属性，用以声明插件所支持的数据格式。

用于导入的插件类必须包含一个 `loadbytes` 方法，用于从字节流中导入数据。可选是否单独实现 `load` 方法，如果不单独实现，则在调用时，会直接通过打开文件后使用 `loadbytes` 的方式实现。

```python
# 注册插件
@music_input_plugin("something_convert_to_music")
# 继承自对应类型的插件基类
class ExampleImportPlugin(MusicInputPluginBase):  
    
    # 插件元信息定义
    metainfo = PluginMetaInformation(
        name="示例导入插件",                # 插件名称
        author="金羿",                    # 插件作者
        description="这是一个示例导入插件",  # 插件描述
        version=(0, 0, 1),               # 插件版本
        type=PluginTypes.FUNCTION_MUSIC_IMPORT, # 插件类型
        license="The Unlicense",         # 插件许可证
        dependencies=("something_convertion_library") # 插件对于其他插件的依赖项
    )

    # 导入导出插件支持的数据格式，大小写皆可
    supported_formats = ("EXP", "example_format")

    # 定义 loadbytes 方法，从字节流中导入数据
    def loadbytes(
        self, bytes_buffer_in: BinaryIO, config: ExampleImportConfig
    ) -> "SingleMusic":
        ...

    # 插件可选地定义 load 方法，从文件导入数据
    def load(
        self, file_path: Path, config: ExampleImportConfig
    ) -> "SingleMusic":
        ...
```

至此，一个插件的编写已经完成。