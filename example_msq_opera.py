import Musicreater

msc_seq = Musicreater.MusicSequence.from_mido(
    Musicreater.mido.MidiFile("./resources/测试片段.mid",),
    "TEST-测试片段",
)

with open("test.msq","wb") as f:
    f.write(msq_bytes := msc_seq.encode_dump())

with open("test.msq","rb") as f:
    msc_seq_r = Musicreater.MusicSequence.load_decode(f.read())
    
print(msc_seq_r)