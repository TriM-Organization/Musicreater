from rich.pretty import pprint

import Musicreater
from Musicreater.utils import (
    load_decode_msq_flush_release,
    load_decode_musicsequence_metainfo,
)

msc_seq = Musicreater.MusicSequence.from_mido(
    Musicreater.mido.MidiFile(
        "./resources/测试片段.mid",
    ),
    "TEST-测试片段",
)

pprint("音乐源取入成功：")
pprint(msc_seq)

with open("test.msq", "wb") as f:
    f.write(msq_bytes := msc_seq.encode_dump())

with open("test.msq", "rb") as f:
    msc_seq_r = Musicreater.MusicSequence.load_decode(f.read())

pprint("常规 MSQ 读取成功：")
pprint(msc_seq_r)


with open("test.msq", "rb") as f:
    pprint("流式 MSQ 元数据：")
    pprint(metas := load_decode_musicsequence_metainfo(f))
    pprint("流式 MSQ 音符序列：")
    for i in load_decode_msq_flush_release(f, metas[-2], metas[-3], metas[-1]):
        pprint(i)
