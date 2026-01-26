import Musicreater.experiment
import Musicreater.old_plugin
import Musicreater.old_plugin.mcstructfile

msct = Musicreater.experiment.FutureMidiConvertLyricSupport.from_midi_file(
    input("midi路径:"), old_exe_format=False
)

opt = input("输出路径:")

# print(
#     "乐器使用情况",
# )

# for name in sorted(
#     set(
#         [
#             n.split(".")[0].replace("c", "").replace("d", "")
#             for n in msct.note_count_per_instrument.keys()
#         ]
#     )
# ):
#     print("\t", name, flush=True)

print(
    "\n输出：",
    Musicreater.old_plugin.mcstructfile.to_mcstructure_file_in_delay(
        msct,
        opt,
        # Musicreater.plugin.ConvertConfig(input("输出路径:"),),
        max_height=32,
    ),
)
