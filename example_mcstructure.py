from Musicreater import midiConvert

conversion = midiConvert(enable_old_exe_format=False)
conversion.convert(input("midi路径:"), input("输出路径:"))

conversion.to_mcstructure_file_with_delay(
    3,
)
