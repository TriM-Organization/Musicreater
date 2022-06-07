# -*- coding: utf-8 -*-

from main import *
import os

convertion = midiConvert()

while True:
    midipath = input('请输入midi文件路径：')
    if os.path.exists(midipath):
        break
    else:
        print('文件不存在，请重新输入')

outpath = input('请输入输出路径：')

while True:
    try:
        outFormat = int(input('请输入输出格式(0:mcpack|1:BDX结构)：'))
        if outFormat == 0:
            isAutoReset = input('是否自动重置计分板(1|0)：')
            if isAutoReset != '':
                isAutoReset = bool(int(isAutoReset))
            isProgress = input('是否开启进度条(1|0)：')
            if isProgress != '':
                isProgress = bool(int(isProgress))
            sbname = input('请输入计分板名称：')
            volume = input('请输入音量（0-1）：')
            if volume != '':
                volume = float(volume)
            speed = input('请输入速度倍率：')
            if speed != '':
                speed = float(speed)
        elif outFormat == 1:
            author = input('请输入作者：')
            isProgress = input('是否开启进度条(1|0)：')
            if isProgress != '':
                isProgress = bool(int(isProgress))
            maxHeight = input('请输入指令结构最大生成高度：')
            if maxHeight != '':
                maxHeight = int(maxHeight)
            sbname = input('请输入计分板名称：')
            volume = input('请输入音量（0-1）：')
            if volume != '':
                volume = float(volume)
            speed = input('请输入速度倍率：')
            if speed != '':
                speed = float(speed)
            isAutoReset = input('是否自动重置计分板(1|0)：')
            if isAutoReset != '':
                isAutoReset = bool(int(isAutoReset))
        break
    except:
        print('输入错误，请重新输入')



if os.path.isdir(midipath):
    for i in os.listdir(midipath):
        if i.endswith('.mid'):
            convertion.convert(midipath + '/' + i, outpath + '/' + i[:-4] + '.mcpack')
            if outFormat == 0:
                convertion.tomcpack(
                    1,
                    isAutoReset if isAutoReset != '' else bool(int(input('是否自动重置计分板(1|0)：'))),
                    isProgress if isProgress != '' else bool(int(input('是否开启进度条(1|0)：'))),
                    sbname if sbname != '' else input('请输入计分板名称：'),
                    volume if volume != '' else float(input('请输入音量（0-1）：')),
                    speed if speed != '' else float(input('请输入速度倍率：')),
                )
            elif outFormat == 1:
                convertion.toBDXfile(
                    1,
                    author if author != '' else input('请输入作者：'),
                    isProgress if isProgress != '' else bool(int(input('是否开启进度条(1|0)：'))),
                    maxHeight if maxHeight != '' else int(input('请输入指令结构最大生成高度：')),
                    sbname if sbname != '' else input('请输入计分板名称：'),
                    volume if volume != '' else float(input('请输入音量（0-1）：')),
                    speed if speed != '' else float(input('请输入速度倍率：')),
                    isAutoReset if isAutoReset != '' else bool(int(input('是否自动重置计分板(1|0)：'))),
                )
else:
    convertion.convert(midipath, outpath)
    if outFormat == 0:
        convertion.tomcpack(
            1,
            isAutoReset if isAutoReset != '' else bool(int(input('是否自动重置计分板(1|0)：'))),
            isProgress if isProgress != '' else bool(int(input('是否开启进度条(1|0)：'))),
            sbname if sbname != '' else input('请输入计分板名称：'),
            volume if volume != '' else float(input('请输入音量（0-1）：')),
            speed if speed != '' else float(input('请输入速度倍率：')),
        )
    elif outFormat == 1:
        convertion.toBDXfile(
            1,
            author if author != '' else input('请输入作者：'),
            isProgress if isProgress != '' else bool(int(input('是否开启进度条(1|0)：'))),
            maxHeight if maxHeight != '' else int(input('请输入指令结构最大生成高度：')),
            sbname if sbname != '' else input('请输入计分板名称：'),
            volume if volume != '' else float(input('请输入音量（0-1）：')),
            speed if speed != '' else float(input('请输入速度倍率：')),
            isAutoReset if isAutoReset != '' else bool(int(input('是否自动重置计分板(1|0)：'))),
        )