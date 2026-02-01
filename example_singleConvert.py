import Musicreater.old_init as old_init
import Musicreater.old_plugin
import Musicreater.old_plugin.mcstructfile

print(
    old_init.old_plugin.mcstructfile.to_mcstructure_file_in_delay(
        old_init.MidiConvert.from_midi_file(
            input("midi路径:"),
            old_exe_format=False,
            # note_table_replacement={"note.harp": "note.flute"},
        ),
        input("输出路径:"),
        # Musicreater.plugin.ConvertConfig(input("输出路径:"),),
        # max_height=32,
    )
)
