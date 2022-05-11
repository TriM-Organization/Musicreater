# -*- coding: UTF-8 -*-
"""音·创的核心内置组件功能集合"""



class version:
    libraries = (
        'wxPython', 'mido', 'amulet', 'amulet-core', 'amulet-nbt', 'piano_transcription_inference', 'pypinyin',
        'pyinstaller', 'py7zr','websockets', 'zhdate', 'requests',
        )
    """当前所需库"""

    version = ('0.2.0', 'Delta',)
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
            import shutil
            try:
                shutil.rmtree(os.getenv('APPDATA') + '\\Musicreater\\')
            except FileNotFoundError:
                pass
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
