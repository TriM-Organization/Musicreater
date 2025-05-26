from rich.pretty import pprint

import Musicreater
from Musicreater.utils import (
    load_decode_fsq_flush_release,
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

with open("test.fsq", "wb") as f:
    f.write(fsq_bytes := msc_seq.encode_dump(flowing_codec_support=True))

with open("test.fsq", "rb") as f:
    msc_seq_r = Musicreater.MusicSequence.load_decode(f.read(), verify=True)

pprint("FSQ 传入类成功：")
pprint(msc_seq_r)


with open("test.fsq", "rb") as f:
    pprint("流式 FSQ 元数据：")
    pprint(metas := load_decode_musicsequence_metainfo(f))
    pprint("流式 FSQ 音符序列：")
    cnt = 0
    for i in load_decode_fsq_flush_release(f, metas[-1], metas[-2]):
        pprint(
            i,
        )
        cnt += 1
    pprint(f"共 {cnt} 个音符")
