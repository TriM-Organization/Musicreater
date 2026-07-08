# 一个简单的项目实践测试

from pathlib import Path

from rich import print

from Musicreater import load_plugin_from_module, MusiCreater
from Musicreater.plugins import _global_plugin_registry
from Musicreater._utils import incremental_save_path

load_plugin_from_module("Musicreater.builtin_plugins.midi_read")
load_plugin_from_module("Musicreater.builtin_plugins.music_preview")

from Musicreater.builtin_plugins.midi_read import MidiImportConfig
from Musicreater.builtin_plugins.music_preview import PcmConversionConfig

print("当前支持的导入格式：", _global_plugin_registry.supported_input_formats())
print("当前支持的导出格式：", _global_plugin_registry.supported_output_formats())

msct = MusiCreater.import_music(
    Path(input("文件路径：")).resolve(),
    plugin_config=MidiImportConfig(),
)

print("全局插件注册表：", _global_plugin_registry)
print("插件缓存字典：", msct._plugin_cache)

print(
    msct.export_music(
        (fn := incremental_save_path("output", suffix=".wav")),
        plugin_id="music_to_pcm_plugin",
        plugin_config=PcmConversionConfig(
            assets_path=Path("./vanilla_assets/wav/").resolve(),
            synthesis_mode=2,
            pitch_accuracy_decimals=0,
        ),
    ),
    "\n文件路径：",
    fn,
)
