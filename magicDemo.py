# -*- coding: utf-8 -*-


# 音·创 开发交流群 861684859
# Email EillesWan2006@163.com W-YI_DoctorYI@outlook.com EillesWan@outlook.com
# 版权所有 金羿("Eilles Wan") & 诸葛亮与八卦阵("bgArray") & 鸣凤鸽子("MingFengPigeon")
# 若需转载或借鉴 请依照 Apache 2.0 许可证进行许可


"""
音·创 库版 MIDI转换示例程序
Musicreater Package Version : Demo for Midi Conversion

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

languages = {
    "ZH_CN": {
        "MSCT": "音·创",
        "ChooseLang": "选择语言",
        "LangChd": "当前语言已经切换为",
        "ZH_CN": "简体中文",
        "ZH_TW": "繁体中文（台湾）",
        "EN_GB": "英语（英国）",
        "EN_US": "英语（美国）",
        ":": "：",
        ",": "，",
        ".": "。",
        "ChooseFileFormat": "请输入输出格式[BDX(1)或MCPACK(0)]",
        "ChoosePlayer": "请选择播放方式[计分板(1) 或 延迟(0)]",
        "ChoosePath": "请输入MIDI路径或所在文件夹",
        "WhetherArgEntering": "是否为文件夹内文件的转换统一参数[是(1) 或 否(0)]",
        "ChooseSbReset": "是否自动重置计分板[是(1) 或 否(0)]",
        "WhetherCstmProgressBar": "是否自定义进度条[是(1) 或 否(0)]",
        "EnterProgressBarStyle": "请输入进度条样式",
        "EnterSbName": "请输入计分板名称",
        "EnterVolume": "请输入音量大小(0~1)",
        "EnterSpeed": "请输入速度倍率",
        "EnterAuthor": "请输入作者",
        "EnterMaxHeight": "请输入指令结构最大生成高度",
        "ErrEnter": "输入错误",
        "Re-Enter": "请重新输入",
        "Dealing": "正在处理",
        "FileNotFound": "文件(夹)不存在",
        "ChooseOutPath": "请输入输出路径",
        "EnterSelecter": "请输入播放者选择器",
        "Saying": "言·论",
    }
}


import sys


if sys.argv.__len__() > 0:
    currentLang = sys.argv[0]
    if not currentLang in languages.keys():
        currentLang = "ZH_CN"
else:
    currentLang = "ZH_CN"


def _(__):
    '''
    :ChooseFileFormat 请输入输出格式[bdx(1)或mcpack(0)]
    :ChoosePlayer 请选择播放方式[计分板(1) 或 延迟(0)]
    :ChoosePath 请输入midi路径或所在文件夹
    :WhetherArgEntering 是否为文件夹内文件的转换统一参数[是1 或 否0]
    :ChooseSbReset 是否自动重置计分板[1或0]：
    :WhetherCstmProgressBar 是否自定义进度条
    :EnterProgressBarStyle 请输入进度条样式
    :EnterSbName 请输入计分板名称
    :EnterVolume 请输入音量大小(0~1)
    :EnterSpeed 请输入速度倍率
    :EnterAuthor 请输入作者
    :EnterMaxHeight 请输入指令结构最大生成高度
    :ErrEnter 输入错误
    :Re-Enter 请重新输入
    :Dealing 正在处理
    :FileNotFound 文件不存在
    :ChooseOutPath 请输入输出路径
    :EnterSelecter 请输入播放者选择器
    :Saying 箴言
    '''
    return languages[currentLang][__]


from msctPkgver.main import *

from rich.console import Console


MainConsole = Console()


import requests
import random


MainConsole.rule(title="[bold #AB70FF]欢迎使用音·创独立转换器", characters="=", style="#26E2FF")
MainConsole.rule(
    title="[bold #AB70FF]Welcome to Independent Musicreater Convernter", characters="-"
)

MainConsole.print(
    "[#121110 on #F0F2F4]"
    + random.choice(
        requests.get(
            "https://gitee.com/EillesWan/Musicreater/raw/master/resources/myWords.txt"
        )
        .text.strip("\r\n")
        .split("\r\n")
    ),
    style="#121110 on #F0F2F4",
    justify="center",
)


from typing import Any, Optional, TextIO, Literal

JustifyMethod = Literal["default", "left", "center", "right", "full"]
OverflowMethod = Literal["fold", "crop", "ellipsis", "ignore"]


def prt(
    *objects: Any,
    sep: str = " ",
    end: str = "\n",
    justify: Optional[JustifyMethod] = None,
    overflow: Optional[OverflowMethod] = None,
    no_wrap: Optional[bool] = None,
    emoji: Optional[bool] = None,
    markup: Optional[bool] = None,
    highlight: Optional[bool] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    crop: bool = True,
    soft_wrap: Optional[bool] = None,
    new_line_start: bool = False,
) -> None:
    """打印到控制台。

    Args:
        objects (位置性的args): 要记录到终端的对象。
        sep (str, 可选): 要在打印数据之间写入的字符串。默认为""。
        end (str, optio可选nal): 在打印数据结束时写入的字符串。默认值为"\\\\n"。
        style (Union[str, Style], 可选): 应用于输出的样式。默认为`None`。
        justify (str, 可选): 校正位置，可为"default", "left", "right", "center" 或 "full". 默认为`None`。
        overflow (str, 可选): 控制溢出："ignore"忽略, "crop"裁剪, "fold"折叠, "ellipsis"省略号。默认为`None`。
        no_wrap (Optional[bool], 可选): 禁用文字包装。默认为`None`。
        emoji (Optional[bool], 可选): 启用表情符号代码，或使用控制台默认的`None`。默认为`None`。
        markup (Optional[bool], 可选): 启用标记，或`None`使用控制台默认值。默认为`None`。
        highlight (Optional[bool], 可选): 启用自动高亮，或`None`使用控制台默认值。默认为`None`。
        width (Optional[int], 可选): 输出的宽度，或`None`自动检测。默认为`None`。
        crop (Optional[bool], 可选): 裁剪输出到终端的宽度。默认为`True`。
        soft_wrap (bool, 可选): 启用软包装模式，禁止文字包装和裁剪，或`None``用于 控制台默认值。默认为`None`。
        new_line_start (bool, False): 如果输出包含多行，在开始时插入一个新行。默认值为`False`。
    """
    MainConsole.print(
        *objects,
        sep=sep,
        end=end,
        style="#F0F2F4 on #121110",
        justify=justify,
        overflow=overflow,
        no_wrap=no_wrap,
        emoji=emoji,
        markup=markup,
        highlight=highlight,
        width=width,
        height=height,
        crop=crop,
        soft_wrap=soft_wrap,
        new_line_start=new_line_start,
    )


prt(f"{_('LangChd')}{_(':')}{_(currentLang)}")


def ipt(
    *objects: Any,
    sep: str = " ",
    justify: Optional[JustifyMethod] = None,
    overflow: Optional[OverflowMethod] = None,
    no_wrap: Optional[bool] = None,
    emoji: Optional[bool] = None,
    markup: Optional[bool] = None,
    highlight: Optional[bool] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    crop: bool = True,
    soft_wrap: Optional[bool] = None,
    new_line_start: bool = False,
    password: bool = False,
    stream: Optional[TextIO] = None,
) -> str:
    """显示一个提示并等待用户的输入。

    它的工作方式与Python内建的 :func:`input` 函数相同，如果Python内建的 :mod:`readline` 模块先前已经加载，则提供详细的行编辑和历史功能。

    Args:
        objects (位置性的args): 要记录到终端的对象。
        sep (str, 可选): 要在打印数据之间写入的字符串。默认为""。
        end (str, optio可选nal): 在打印数据结束时写入的字符串。默认值为"\\\\n"。
        style (Union[str, Style], 可选): 应用于输出的样式。默认为`None`。
        justify (str, 可选): 校正位置，可为"default", "left", "right", "center" 或 "full". 默认为`None`。
        overflow (str, 可选): 控制溢出："ignore"忽略, "crop"裁剪, "fold"折叠, "ellipsis"省略号。默认为`None`。
        no_wrap (Optional[bool], 可选): 禁用文字包装。默认为`None`。
        emoji (Optional[bool], 可选): 启用表情符号代码，或使用控制台默认的`None`。默认为`None`。
        markup (Optional[bool], 可选): 启用标记，或`None`使用控制台默认值。默认为`None`。
        highlight (Optional[bool], 可选): 启用自动高亮，或`None`使用控制台默认值。默认为`None`。
        width (Optional[int], 可选): 输出的宽度，或`None`自动检测。默认为`None`。
        crop (Optional[bool], 可选): 裁剪输出到终端的宽度。默认为`True`。
        soft_wrap (bool, 可选): 启用软包装模式，禁止文字包装和裁剪，或`None``用于 控制台默认值。默认为`None`。
        new_line_start (bool, False): 如果输出包含多行，在开始时插入一个新行。默认值为`False`。
        password (bool, 可选): 隐藏已经输入的文案，默认值为`False`。
        stream (TextIO, 可选): 可选从文件中读取（而非控制台），默认为 `None`。

    Returns:
        str: 从stdin读取的字符串
    """
    MainConsole.print(
        *objects,
        sep=sep,
        end="",
        style="#F0F2F4 on #121110",
        justify=justify,
        overflow=overflow,
        no_wrap=no_wrap,
        emoji=emoji,
        markup=markup,
        highlight=highlight,
        width=width,
        height=height,
        crop=crop,
        soft_wrap=soft_wrap,
        new_line_start=new_line_start,
    )

    return MainConsole.input("", password=password, stream=stream)

import os

while True:
    midipath = ipt(f"{_('ChoosePath')}{_(':')}").lower()
    if os.path.exists(midipath):
        if os.path.isfile(midipath):
            midis = (midipath,)
        elif os.path.isdir(midipath):
            midis = (os.path.join(midipath,i) for i in os.listdir(midipath) if i.lower().endswith('.mid') or i.lower().endswith('.midi'))
        else:
            prt(f"{_('ErrEnter')}{_(',')}{_('Re-Enter')}{_('.')}")
            continue
    else:
        prt(f"{_('FileNotFound')}{_(',')}{_('Re-Enter')}{_('.')}")
        continue
    break



while True:
    fileFormat = ipt(f"{_('ChooseFileFormat')}{_(':')}").lower()
    if fileFormat in ('0','mcpack'):
        fileFormat = 0
        if len(midis) > 1:
            while True:
                isFirstArgs = ipt(f"{_('WhetherArgEntering')}{_(':')}").lower()
                if isFirstArgs in ('0','否'):
                    isFirstArgs = 0
                elif isFirstArgs in ('1','是'):
                    isFirstArgs = 1
                else:
                    prt(f"{_('ErrEnter')}{_(',')}{_('Re-Enter')}{_('.')}")
                    continue
                break
    elif fileFormat in ('1','bdx'):
        fileFormat = 1
        while True:
            playerFormat = ipt(f"{_('ChoosePlayer')}{_(':')}").lower()
            if playerFormat in ('0','延迟'):
                playerFormat = 0
            elif playerFormat in ('1','计分板'):
                playerFormat = 1
            else:
                prt(f"{_('ErrEnter')}{_(',')}{_('Re-Enter')}{_('.')}")
                continue
            break
    else:
        prt(f"{_('ErrEnter')}{_(',')}{_('Re-Enter')}{_('.')}")
        continue
    break


if fileFormat == 0:
    pass




MainConsole.input()
