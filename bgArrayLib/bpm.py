import mido
import numpy


def mt2gt(mt, tpb_a, bpm_a):
    return round(mt / tpb_a / bpm_a * 60)


def get(mid:mido.MidiFile):
    # mid = mido.MidiFile(mf)
    long = mid.length
    tpb = mid.ticks_per_beat
    bpm = 20
    gotV = 0

    for track in mid.tracks:
        global_time = 0
        for msg in track:
            global_time += msg.time
            if msg.type == "note_on" and msg.velocity > 0:
                gotV = mt2gt(global_time, tpb, bpm)
    errorV = numpy.fabs(gotV - long)
    last_dic = {bpm: errorV}
    if last_dic.get(bpm) > errorV:
        last_dic = {bpm: errorV}
    bpm += 2

    while True:
        for track in mid.tracks:
            global_time = 0
            for msg in track:
                global_time += msg.time
                if msg.type == "note_on" and msg.velocity > 0:
                    gotV = mt2gt(global_time, tpb, bpm)
        errorV = numpy.fabs(gotV - long)
        try:
            if last_dic.get(bpm - 2) > errorV:
                last_dic = {bpm: errorV}
        except TypeError:
            pass
        bpm += 2
        if bpm >= 252:
            break
    print(list(last_dic.keys())[0])
    return list(last_dic.keys())[0]


def compute(mid:mido.MidiFile):
    answer = 60000000/mid.ticks_per_beat
    print(answer)
    return answer


if __name__ == '__main__':
    mid = mido.MidiFile(r"C:\Users\lc\Documents\MuseScore3\乐谱\乐谱\Bad style - Time back.mid")
    get(mid)
    compute(mid)
