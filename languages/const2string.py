# -*- coding:utf-8 -*-
'''此功能已废弃'''




# W-YI 金羿
# QQ 2647547478
# 音·创 开发交流群 861684859
# Email EillesWan2006@163.com W-YI_DoctorYI@outlook.com EillesWan@outlook.com
# 版权所有 Team-Ryoun 金羿("Eilles Wan") & 诸葛亮与八卦阵("bgArray")
# 若需转载或借鉴 请附作者


"""
   Copyright 2022 Team-Ryoun 金羿("Eilles Wan") & 诸葛亮与八卦阵("bgArray")

   Licensed under the Apache License, Version 2.0 (the 'License');
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an 'AS IS' BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

#  代码写的并非十分的漂亮，还请大佬多多包涵；本软件源代码依照Apache软件协议公开

# -----------------------------分割线-----------------------------
# 诸葛亮与八卦阵帮忙修改语法 日期：---2022年1月19日
# 统计：致命（三级）错误：0个；警告（二级）错误：0个；语法（一级）错误：12个
# 目前我的Pycharm并没有显示任何错误，有错误可以向：
# bgArray 诸葛亮与八卦阵
# QQ 474037765 或最好加入：音·创 开发交流群 861684859
# ------------------------- split line-----------------------------
# Zhuge Liang and Bagua array help to modify the grammar date: -- January 19, 2022
# Statistics: fatal (Level 3) errors: 0; Warning (Level 2) errors: 15; Syntax (Level 1) error: 597
# At present, my Pycham does not display any errors. If there are errors, you can report them to me
# Bgarray Zhuge Liang and Bagua array
# QQ 474037765 or better join: Musicreater development exchange group 861684859
# ------------------------- split line-----------------------------

# 下面为正文


# 将程序中用双引号""括起来的字符串
# 转为字符串列表 list[str, str, ...]
# 方便进行语言翻译支持。

import sys
startWith = 0


def __main__():
    textList = []
    for fileName in sys.argv[1:]:
        print('读取文件: {}'.format(fileName))
        fileText = []
        for line in open(fileName, 'r', encoding='utf-8'):
            while line.count('"') >= 2:
                # 只有上帝看得懂我在写什么。
                if line[
                   line.index('"'):2 + line[line.index('"') + 1:].index('"') + len(line[:line.index('"')])] in textList:
                    thisText = textList.index(
                        line[line.index('"'):2 + line[line.index('"') + 1:].index('"') + len(line[:line.index('"')])])
                else:
                    thisText = len(textList)
                    textList.append(
                        line[line.index('"'):2 + line[line.index('"') + 1:].index('"') + len(line[:line.index('"')])])
                line = line.replace(
                    line[line.index('"'):2 + line[line.index('"') + 1:].index('"') + len(line[:line.index('"')])],
                    'READABLETEXT[{}]'.format(thisText + startWith)
                )
            fileText.append(line)

        open(fileName + '_C', 'w', encoding='utf-8').writelines(fileText)

    outFile = open('lang__.py', 'w', encoding='utf-8')
    outFile.write('''# -*- coding:utf-8 -*-

# 由金羿翻译工具生成字符串列表
# 请在所需翻译文件前from 此文件 import READABLETEXT



READABLETEXT = {
''')
    for i in range(len(textList)):
        outFile.write("    {}:{},\n".format(i + startWith, textList[i]))
    outFile.write('}')
    outFile.close()


if __name__ == '__main__':
    __main__()
