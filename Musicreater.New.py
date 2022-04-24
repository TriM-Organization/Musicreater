# -*- coding: utf-8 -*-


# W-YI 金羿
# QQ 2647547478
# 音·创 开发交流群 861684859
# Email EillesWan2006@163.com W-YI_DoctorYI@outlook.com EillesWan@outlook.com
# 版权所有 Team-Ryoun 金羿("Eilles Wan") & 诸葛亮与八卦阵("bgArray")
# 若需转载或借鉴 请附作者


"""
音·创 (Musicreater)
一款免费开源的 《我的世界：基岩版》 音乐制作软件
Musicreater (音·创)
A free opensource software which is used for creating all kinds of musics in Minecraft

   Copyright 2022 Team-Ryoun

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

# 代码写的并非十分的漂亮，还请大佬多多包涵；本软件源代码依照Apache软件协议公开


# 下面为正文

# 一定会好起来的


from msctLib.buildIN import version

__ver__ = f'{version.version[1]} {version.version[0]}'
__author__ = '金羿Eilles'

import msctLib.display as disp

from msctLib.function import *

from msctLib.data import uniteIO


hb = r'''                  __  __                                           
                 /\ \/\ \                                          
                 \ \ \_\ \      __     _____    _____    __  __    
                  \ \  _  \   /'__`\  /\ '__`\ /\ '__`\ /\ \/\ \   
                   \ \ \ \ \ /\ \L\.\_\ \ \L\ \\ \ \L\ \\ \ \_\ \  
                    \ \_\ \_\\ \__/.\_\\ \ ,__/ \ \ ,__/ \/`____ \ 
                     \/_/\/_/ \/__/\/_/ \ \ \/   \ \ \/   `/___/> \
                                         \ \_\    \ \_\      /\___/
                                          \/_/     \/_/      \/__/ 
        ____                  __     __           __                         
       /\  _`\    __         /\ \__ /\ \         /\ \                        
       \ \ \L\ \ /\_\   _ __ \ \ ,_\\ \ \___     \_\ \      __     __  __    
        \ \  _ <'\/\ \ /\`'__\\ \ \/ \ \  _ `\   /'_` \   /'__`\  /\ \/\ \   
         \ \ \L\ \\ \ \\ \ \/  \ \ \_ \ \ \ \ \ /\ \L\ \ /\ \L\.\_\ \ \_\ \  
          \ \____/ \ \_\\ \_\   \ \__\ \ \_\ \_\\ \___,_\\ \__/.\_\\/`____ \ 
           \/___/   \/_/ \/_/    \/__/  \/_/\/_/ \/__,_ / \/__/\/_/ `/___/> \
                                                                       /\___/
                                                                       \/__/ '''


def __main__():
    import datetime, time, random, os, sys, zhdate

    if datetime.date.today().month == 4 and datetime.date.today().day == 3:
        if sys.platform == 'win32':
            os.system('color 4e')
            os.system('cls')
        for i in range(len(hb)):
            print(hb[i], end='', flush=True)
            time.sleep(random.random() * 0.001)
        input("金羿 生日快乐！")
    elif '三月初五' in zhdate.ZhDate.today().chinese():
        input('缅怀先祖 祭祀忠勇 勿忘国耻 振兴中华')

    else:

        def test():
            print('!!!', end=' ')

        def test2():
            print('???', end=' ')
        
        disp.__root = disp.tk.Tk()

        disp.initWindow(
            geometry='1200x800',
            menuWidget={
                '文件': {'新建': test, '打开': test},
                '编辑': {'撤销': test, '重做': test},
                '视图': {'缩放': test},
                '帮助': {'关于': disp.authorWindowStarter},
            },
            title_='音·创 0.2 测试中',
            button=[
                {
                    '新建': ('', test2), 
                    '打开': ('', test2)
                }, 
                {
                    '测试': ('', test2)
                }
            ],
            Debug=True,
        )
        
        disp.winstart()


if __name__ == '__main__':
    __main__()
