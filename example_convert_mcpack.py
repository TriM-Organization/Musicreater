# THIS PROGRAM IS ONLY A TEST EXAMPLE


from main import *

midiConvert(input('请输入midi文件路径：'), input('请输入输出路径：')).tomcpack(1, input('请输入计分板名称：'), float(input('请输入音量（0-1）：')),
                                                                float(input('请输入速度倍率：')))
