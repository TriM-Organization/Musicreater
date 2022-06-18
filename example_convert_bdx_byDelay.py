# THIS PROGRAM IS ONLY A TEST EXAMPLE


from msctPkgver.main import *

convertion = midiConvert()
convertion.convert(input('请输入midi文件路径：'), input('请输入输出路径：'))
for i in convertion.toBDXfile_withDelay(
    1,
    input('请输入作者：'),
    bool(int(input('是否开启进度条(1|0)：'))),
    int(input('请输入指令结构最大生成高度：')),
    float(input('请输入音量(0-1]：')),
    float(input('请输入速度倍率：')),
    input('请输入玩家选择器(例@a[tag=ply])：'),
):
    print(i)
