import Musicreater.experiment
import Musicreater.plugin
import Musicreater.plugin.mcstructpack

print(
    Musicreater.plugin.mcstructpack.to_mcstructure_addon_in_delay(
        Musicreater.experiment.FutureMidiConvertM4.from_midi_file(input("midi路径:"), old_exe_format=False),
        Musicreater.plugin.ConvertConfig(
            input("输出路径:"),
            volume=1
        ),
    )
)
