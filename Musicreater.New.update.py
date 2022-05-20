# -*- coding: utf-8 -*-


# 金羿 Eilles
# QQ 2647547478
# 音·创 开发交流群 861684859
# Email EillesWan2006@163.com W-YI_DoctorYI@outlook.com EillesWan@outlook.com
# 版权所有 金羿("Eilles Wan") & 诸葛亮与八卦阵("bgArray") & 鸣凤鸽子("MingFengPigeon")
# 若需转载或借鉴 请依照 Apache 2.0 许可证进行许可


"""
音·创 (Musicreater)
一款免费开源的 《我的世界：基岩版》 音乐制作软件
Musicreater (音·创)
A free opensource software which is used for creating all kinds of musics in Minecraft

   Copyright 2022 all the developers of Musicreater

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

# 代码写的并非十分的漂亮，还请大佬多多包涵；本软件源代码依照 Apache 2.0 软件协议公开


# 下面为正文

# 一定会好起来的


from msctLib.buildIN import version
from languages.lang import _

__ver__ = f'{version.version[1]} {version.version[0]}'
__author__ = '金羿Eilles'



def __main__():
    import wx                           # 引入wxPython库
    app = wx.App(False) 
    frame = wx.Frame(None, id=wx.ID_ANY, title=f"{_('F音创')} {__ver__}", size=(1600, 900))
    # 创建图标
    icon_obj = wx.Icon(name="./resources/msctIcon.png")
    frame.SetIcon(icon_obj)            # 设定图标
    frame.Show(True)                 # 显示该窗口
    app.MainLoop()                   # 应用程序消息处理
        


if __name__ == '__main__':
    __main__()
