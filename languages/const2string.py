# -*- coding:utf-8 -*-


# W-YI 金羿
# QQ 2647547478
# 音·创 开发交流群 861684859
# Email EillesWan2006@163.com W-YI_DoctorYI@outlook.com EillesWan@outlook.com
# 版权所有 Team-Ryoun 金羿
# 若需转载或借鉴 请附作者


'''
   Copyright 2022 Eilles Wan (金羿)

   Licensed under the Apache License, Version 2.0 (the 'License')
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an 'AS IS' BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''


#  代码写的并非十分的漂亮，还请大佬多多包涵；本软件源代码依照Apache软件协议公开

'''
将程序中用双引号""括起来的字符串
转为字符串列表 list[str, str, ...]
方便进行语言翻译支持。
'''

startWith = 0


import sys


def __main__():
    textList = []
    for fileName in sys.argv[1:]:
        print('读取文件: {}'.format(fileName))
        fileText = []
        for line in open(fileName, 'r', encoding='utf-8'):
            while line.count('"') >=2:
                # 只有上帝看得懂我在写什么。
                if line[line.index('"'):2+line[line.index('"')+1:].index('"')+len(line[:line.index('"')])] in textList:
                    thisText = textList.index(line[line.index('"'):2+line[line.index('"')+1:].index('"')+len(line[:line.index('"')])])
                else:
                    thisText = len(textList)
                    textList.append(line[line.index('"'):2+line[line.index('"')+1:].index('"')+len(line[:line.index('"')])])
                line = line.replace(
                    line[line.index('"'):2+line[line.index('"') + 1:].index('"')+len(line[:line.index('"')])],
                    'READABLETEXT[{}]'.format(thisText+startWith)
                )
            fileText.append(line)
            
        open(fileName+'_C','w',encoding='utf-8').writelines(fileText)
        
    
    outFile = open('lang__.py','w',encoding='utf-8')
    outFile.write('''# -*- coding:utf-8 -*-

# 由金羿翻译工具生成字符串列表
# 请在所需翻译文件前from 此文件 import READABLETEXT



READABLETEXT = {
''')
    for i in range(len(textList)):
        outFile.write("    {}:{},\n".format(i+startWith,textList[i]))
    outFile.write('}')
    outFile.close()


if __name__ == '__main__':
    __main__()
