import Musicreater
import Musicreater.plugin
import Musicreater.plugin.mcstructfile

print(
    Musicreater.plugin.mcstructfile.to_mcstructure_file_in_delay(
        Musicreater.MidiConvert.from_midi_file(input("midi路径:"), old_exe_format=False),
        Musicreater.plugin.ConvertConfig(
            input("输出路径:"),
        ),
    )
)
