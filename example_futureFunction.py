import Musicreater.experiment
import Musicreater.plugin
import Musicreater.plugin.mcstructfile

print(
    Musicreater.plugin.mcstructfile.to_mcstructure_file_in_delay(
        Musicreater.experiment.FutureMidiConvertM4.from_midi_file(
            input("midi路径:"), old_exe_format=False
        ),
        input("输出路径:"),
        # Musicreater.plugin.ConvertConfig(input("输出路径:"),),
        max_height=32,
    )
)
