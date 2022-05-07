# THIS PROGRAM IS ONLY A TEST EXAMPLE


from main import *

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
