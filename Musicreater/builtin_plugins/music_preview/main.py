# -*- coding: utf-8 -*-

"""
音·创 v3 内置的 音乐预览插件
"""

"""
版权所有 © 2026 金羿、鱼旧梦
Copyright © 2026 Eilles, ElapsingDreams

继承自：

版权所有 © 2026 鱼旧梦
Copyright © 2026 ElapsingDreams

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 本插件依照 Apache 2.0 协议开放源代码，若需转载或借鉴
# 许可声明请查看 http://www.apache.org/licenses/LICENSE-2.0


import os
import pathlib
from typing import Any, Union

import soundfile as sf
import librosa
import numpy as np


from Musicreater import SingleMusic, SingleTrack, SingleNote, SoundAtmos, MineNote
from Musicreater.plugins import (
    library_plugin,
    PluginConfig,
    PluginMetaInformation,
    PluginTypes,
    LibraryPluginBase,
)
from Musicreater.exceptions import ZeroSpeedError, IllegalMinimumVolumeError
from Musicreater._utils import enumerated_stuffcopy_dictionary







@library_plugin("notedata_to_pcm_plugin")
class NoteDataConvert2PcmPlugin(LibraryPluginBase):
    metainfo = PluginMetaInformation(
        name="音符数据预览播放支持插件·PCM",
        author="金羿、鱼旧梦",
        description="从音符数据转换为可以用于播放的 PCM 编码数据",
        version=(0, 0, 1),
        type=PluginTypes.LIBRARY,
        license="Apache 2.0",
    )


