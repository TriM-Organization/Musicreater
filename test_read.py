
# 一个简单的项目实践测试
from pathlib import Path
from Musicreater import load_plugin_module, MusiCreater
from Musicreater.plugins import _global_plugin_registry

load_plugin_module("Musicreater.builtin_plugins.midi_read")

print("当前支持的导入格式：", _global_plugin_registry.supported_input_formats())
print("当前支持的导出格式：", _global_plugin_registry.supported_output_formats())

print(msct:=MusiCreater.import_music(Path("./resources/测试片段.mid")))

print(msct.music)



print(msct.midi_2_music_plugin.load(Path("./resources/测试片段.mid"), None))