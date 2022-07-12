# THIS PROGRAM IS ONLY A TEST EXAMPLE


from msctPkgver.main import *

convertion = midiConvert()
convertion.convert(input('请输入midi文件路径：'), input('请输入输出路径：'))
convertion.tomcpack(
    1,
    bool(int(input('是否自动重置计分板(1|0)：'))),
    bool(int(input('是否开启进度条(1|0)：'))),
    input('请输入计分板名称：'),
    float(input('请输入音量（0-1）：')),
    float(input('请输入速度倍率：')),
)

# for the test
# if __name__ == '__main__':
#     convertion = midiConvert()
#     convertion.convert(r"C:\Users\lc\Documents\MuseScore3\乐谱\乐谱\victory.mid", ".")
#     convertion.tomcpack(
#         1, True, True, "scb", 1, 1)
