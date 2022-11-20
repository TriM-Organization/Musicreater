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

from rich.console import Console


MainConsole = Console()

import requests
import random


# 欸嘿！
while True:

    MainConsole.print(
        "[#121110 on #F0F2F4]     ",
        style="#121110 on #F0F2F4",
        justify="center",
    )


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

    MainConsole.print()
