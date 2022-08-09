# -*- coding: utf-8 -*-


# 音·创 开发交流群 861684859
# Email EillesWan2006@163.com W-YI_DoctorYI@outlook.com EillesWan@outlook.com
# 版权所有 金羿("Eilles Wan") & 诸葛亮与八卦阵("bgArray") & 鸣凤鸽子("MingFengPigeon")
# 若需转载或借鉴 请依照 Apache 2.0 许可证进行许可


"""
音·创启动器 (Musicreater Launcher)
对音·创的自动安装以及相应版本选择提供支持的工具
Musicreater Launcher (音·创启动器)
A tool that used for installing Musicreater automatically

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



# 下面为正文


from sys import platform


def __mian__():
    if platform == 'win32':
        import wx
        # 主窗口类
        class MainFrame(wx.Frame):
            def __init__(self, parent, title):
                wx.Frame.__init__(self, id=wx.NewId(), parent=parent, title=title, size=(300, 500))
                
                self.buttonMainVer = wx.Button(self, -1, u"音·创主版本", pos=(50, 20), style=1)

                self.button_pkgver = wx.Button(self, -1, u"音·创库版本", pos=(50, 60))

                self.Bind(wx.EVT_BUTTON, self.mainVer, self.buttonMainVer)
                self.buttonMainVer.SetDefault()

                self.Bind(wx.EVT_BUTTON, self.pkgVer, self.button_pkgver)
                self.button_pkgver.SetDefault()
                
            def mainVer(self, event):
                wx.MessageBox("音·创主版本尚在开发过程中，敬请期待！", "提示", wx.OK | wx.ICON_INFORMATION)

            def pkgVer(self, event):
                downloadPkgVer()
                
                
        
        app = wx.App(False)
        frame = MainFrame(None, "音·创 启动器")
        frame.Show()
        app.MainLoop()
    elif platform == 'linux':
        pass


def downloadPkgVer():
    pass

# from git import Repo

# Repo.clone_from('','')


if __name__ == '__main__':
    __mian__()
    
