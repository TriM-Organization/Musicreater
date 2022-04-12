# THIS PROGRAM IS ONLY A TEST EXAMPLE

if __name__ == '__main__':
    from main import *
    one = 1
    midiConvert(input('请输入midi文件路径：'), input('请输入输出路径：')).tomcpack(one, input('请输入计分板名称：'), float(input('请输入音量（0-1）：')),
                                                                   float(input('请输入速度倍率：')))
