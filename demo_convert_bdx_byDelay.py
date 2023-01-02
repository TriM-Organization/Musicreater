# -*- coding: utf-8 -*-

# THIS PROGRAM IS ONLY A TEST EXAMPLE

# 音·创 开发交流群 861684859
# Email EillesWan2006@163.com W-YI_DoctorYI@outlook.com EillesWan@outlook.com
# 版权所有 金羿("Eilles Wan") & 诸葛亮与八卦阵("bgArray") & 鸣凤鸽子("MingFengPigeon")
# 若需转载或借鉴 许可声明请查看仓库目录下的 Lisence.md


"""
音·创 库版 MIDI转换展示程序
Musicreater Package Version : Demo for Midi Conversion

Copyright 2023 all the developers of Musicreater

开源相关声明请见 ./Lisence.md
Terms & Conditions: ./Lisence.md
"""

from msctPkgver.main import *

convertion = midiConvert()

while True:
    midipath = input('请输入midi文件路径：')
    if os.path.exists(midipath):
        break
    else:
        print('文件不存在，请重新输入')

outpath = input('请输入输出路径：')

if not os.path.exists(outpath):
    os.makedirs(outpath)

while True:
    try:
        authorname = input('请输入作者：')
        while True:
            isProgress = input('*进度条[本Demo不支持自定义]：')
            if isProgress != '':
                if isProgress in ('1', 'True'):
                    isProgress = True
                elif isProgress in ('0', 'False'):
                    isProgress = False
                else:
                    isProgress = isProgress
            else:
                continue
            break

        volume = input('请输入音量（0-1）：')
        if volume != '':
            volume = float(volume)
        speed = input('请输入速度倍率：')
        if speed != '':
            speed = float(speed)
        player = input('请输入玩家选择器：')
        heightmax = input('请输入指令结构最大生成高度：')
        if heightmax != '':
            heightmax = int(heightmax)
        break

    except BaseException:
        print('输入错误，请重新输入')


def operation(
    i,
):
    print(f'正在操作{i}')
    convertion.convert(midipath + '/' + i, outpath)
    convertion.toBDXfile_withDelay(
        1,
        authorname if authorname != '' else input('请输入作者：'),
        isProgress,
        heightmax if heightmax != '' else int(input('请输入指令结构最大生成高度：')),
        volume if volume != '' else float(input('请输入音量(0-1]：')),
        speed if speed != '' else float(input('请输入速度倍率：')),
        player if player != '' else input('请输入玩家选择器：'),
    )


if os.path.isdir(midipath):
    import threading

    for i in os.listdir(midipath):
        if i.lower().endswith('.mid'):
            threading.Thread(target=operation, args=(i,)).start()
else:
    convertion.convert(midipath, outpath)
    convertion.toBDXfile_withDelay(
        1,
        authorname if authorname != '' else input('请输入作者：'),
        isProgress,
        heightmax if heightmax != '' else int(input('请输入指令结构最大生成高度：')),
        volume if volume != '' else float(input('请输入音量(0-1]：')),
        speed if speed != '' else float(input('请输入速度倍率：')),
        player if player != '' else input('请输入玩家选择器：'),
    )
