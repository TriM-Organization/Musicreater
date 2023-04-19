
from Musicreater import midiConvert

conversion = midiConvert()
conversion.convert(input("midi path:"),input("out path:"))
conversion.to_mcstructure_file_with_delay(3,)