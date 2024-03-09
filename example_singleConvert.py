import Musicreater
import Musicreater.plugin
import Musicreater.plugin.addonpack

print(
    Musicreater.plugin.addonpack.to_addon_pack_in_repeater_divided_by_instrument(
        Musicreater.MidiConvert.from_midi_file(
            input("midi路径:"), old_exe_format=False
        ),
        input("输出路径:"),
        # Musicreater.plugin.ConvertConfig(input("输出路径:"),),
        # max_height=32,
    )
)
