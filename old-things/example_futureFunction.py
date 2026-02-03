import Musicreater.experiment
import Musicreater.old_plugin
import Musicreater.old_plugin.mcstructfile

print(
    Musicreater.old_plugin.mcstructfile.to_mcstructure_file_in_delay(
        Musicreater.experiment.FutureMidiConvertM4.from_midi_file(
            input("midi路径:"), old_exe_format=False
        ),
        input("输出路径:"),
        # Musicreater.plugin.ConvertConfig(input("输出路径:"),),
        max_height=32,
    )
)
