import Musicreater.experiment


print(
    Musicreater.experiment.FutureMidiConvertRSNB.from_midi_file(
        input("midi路径:"), old_exe_format=False
    ).to_note_list_in_delay()
)
