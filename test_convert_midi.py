# 一个简单的项目实践测试
from pathlib import Path
from Musicreater import load_plugin_from_module, MusiCreater
from Musicreater.plugins import _global_plugin_registry

load_plugin_from_module("Musicreater.builtin_plugins.midi_read")
load_plugin_from_module("Musicreater.builtin_plugins.to_commands")
load_plugin_from_module("Musicreater.builtin_plugins.commands_to_structure")

from Musicreater.builtin_plugins.midi_read import MidiImportConfig
from Musicreater.builtin_plugins.commands_to_structure import McstructureExportConfig

print("当前支持的导入格式：", _global_plugin_registry.supported_input_formats())
print("当前支持的导出格式：", _global_plugin_registry.supported_output_formats())

msct = MusiCreater.import_music(
    Path("./resources/测试片段.mid"), plugin_config=MidiImportConfig()
)


print("全局插件注册表：", _global_plugin_registry)
print("插件缓存字典：", msct._plugin_cache)


print(msct.music.music_name)

print(
    "大小、音乐总长：",
    msct.export_music(
        Path("./output.mcstructure"),
        plugin_id="music_to_mcstructure_in_delay_plugin",
        plugin_config=McstructureExportConfig(),
    ),
)
