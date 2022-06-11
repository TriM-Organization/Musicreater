# -*- coding: UTF-8 -*-
"""音·创的核心内置组件功能集合"""

def author_reader(path:str = './resources/msctDevAuthors.txt'):
    '''读入作者数据，格式需要按照署名文件中的指定格式，详见/resources/msctDevAuthors.txt
    :param path: 作者署名文件所在路径
    :return 指定的作者格式
    {
        '作者常用名':{
            '语言码' : '对应语言的名字',
        },
    }'''
    allAuthors = open(path,'r',encoding='utf-8').readlines()
    result = {}
    indexName = ''
    for line in allAuthors:
        line = line.replace('\n', '')
        if (not line.startswith('#')) and line:
            if line.startswith('启'):
                if indexName:
                    result[indexName] = authorList
                indexName = line[line.index('启')+1:]
                authorList = {}
                continue
            line_c = ''
            for char in line:
                if not char == '#':
                    line_c += char
                else:
                    break
            authorList[line_c.split(' ', 1)[0]] = line_c.split(' ', 1)[1]
    result[indexName] = authorList
    return result



class version:
    libraries = (
        'wxPython', 'mido', 'amulet', 'amulet-core', 'amulet-nbt', 'piano_transcription_inference', 'pypinyin',
        'pyinstaller', 'py7zr','websockets', 'zhdate', 'requests',
        )
    """当前所需库"""

    version = ('0.3.0', '丁',)
    """当前版本"""

    def __init__(self) -> None:

        self.libraries = version.libraries
        """当前所需库"""

        self.version = version.version
        """当前版本"""
        

    def installLibraries(self,index:str = 'https://pypi.tuna.tsinghua.edu.cn/simple'):
        """安装全部开发用库"""
        from sys import platform
        import os
        if platform == 'win32':
            for i in self.libraries:
                print("安装库：" + i)
                os.system(f"python -m pip install {i} -i {index}")
        elif platform == 'linux':
            os.system("sudo apt-get install python3-pip")
            os.system("sudo apt-get install python3-tk")
            os.system("sudo apt-get install python3-tkinter")
            for i in self.libraries:
                print("安装库：" + i)
                os.system(f"sudo python3 -m pip install {i} -i {index}")
    

    def __call__(self):
        '''直接安装库，顺便返回一下当前版本'''
        self.installLibraries()
        return self.version
