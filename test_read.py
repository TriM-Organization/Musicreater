# 一个简单的项目实践测试
from pathlib import Path
from Musicreater import load_plugin_module, MusiCreater
from Musicreater.plugins import _global_plugin_registry

load_plugin_module("Musicreater.builtin_plugins.midi_read")

from Musicreater.builtin_plugins.midi_read import MidiImportConfig

print("当前支持的导入格式：", _global_plugin_registry.supported_input_formats())
print("当前支持的导出格式：", _global_plugin_registry.supported_output_formats())

print(msct := MusiCreater.import_music(Path("./resources/测试片段.mid")))

print(msct.music)

# 如果要直接访问插件里面的函数：
# 为了确保类型安全，以下方法不建议使用，因为这本质上是越过了 MusiCreater 类而直接执行插件的函数
print(t := msct.midi_2_music_plugin.load(Path("./resources/测试片段.mid"), None))  # type: ignore
# 我们建议用这种方式来代替
t = _global_plugin_registry._music_input_plugins["midi_2_music_plugin"].load(
    Path("./resources/测试片段.mid"),
    MidiImportConfig(
        speed_multiplier=1.0,
    ),
)
# 或者
from Musicreater.plugins import MusicInputPluginBase

if isinstance((p := msct.midi_2_music_plugin), MusicInputPluginBase):
    t = p.load(Path("./resources/测试片段.mid"), None)

# 但是说实话，既然已经在 MusiCreater 类中提供了
# import_music、export_music、perform_operation_on_music 等方法，
# 那么我们不建议使用上面展示的调取插件的方式来执行插件内的函数。
msct.perform_operation_on_music

print(_global_plugin_registry)
print(msct._plugin_cache)
