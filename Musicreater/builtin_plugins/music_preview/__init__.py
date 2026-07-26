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

from io import BytesIO
from pathlib import Path
from time import perf_counter_ns
from dataclasses import dataclass
from typing import BinaryIO, Optional, Iterator, Generator, Any, Tuple, Literal


from Musicreater import SingleMusic, SingleTrack, SingleNote, SoundAtmos, MineNote
from Musicreater.plugins import (
    PluginConfig,
    PluginMetaInformation,
    PluginTypes,
    music_output_plugin,
    MusicOutputPluginBase,
    track_output_plugin,
    TrackOutputPluginBase,
)


from .main import MusicPreview


@dataclass
class PcmConversionConfig(PluginConfig):

    assets_path: Path
    """
    生成音频文件所使用的资源文件路径
    """

    synthesis_mode: Literal[0, 1, 2, 3, 4] = 1
    """
    音频合成模式
    - 0 原始长度，不变化时长
    - 1 拉伸至 mc 播放器定义（我的世界效果）
    - 2 根据 midi 音符长度裁剪
    - 3 混音预留
    - 4 匹配 midi 音符长度
    """
    overlay_mode: Literal[1, 2] = 1
    """
    没看懂这个参数的意思
    """
    target_sample_rate: int = 44100
    """
    目标输出的采样率
    """
    value_get_method: Literal[0, 1] = 1
    """
    采样取值方法，没看懂什么意思
    - 0 均值化
    - 1 钳制位
    """

    pitch_accuracy_decimals: int = 0
    """
    音调处理精度，小数点后位数
    """

    global_volume: float = 1.0
    """
    全局音量控制
    """

    global_deviation: float = 0
    """
    全曲音调偏移
    """


@music_output_plugin("music_to_pcm_plugin")
class NoteDataConvert2PcmPlugin(MusicOutputPluginBase):
    metainfo = PluginMetaInformation(
        name="全曲预览播放·PCM",
        author="金羿、鱼旧梦",
        description="从全曲的音符数据转换为可以用于播放的 PCM 编码数据",
        version=(0, 0, 1),
        type=PluginTypes.FUNCTION_MUSIC_EXPORT,
        license="Apache 2.0",
    )


    supported_formats = ("WAV", "WAVE", "PCM")

    def dump(self, data: SingleMusic, file_path: Path, config: PcmConversionConfig):

        pr = perf_counter_ns()
        music_preview = MusicPreview(
            resource_folder=config.assets_path,
            synthesis_mode=config.synthesis_mode,
            overlay_mode=config.overlay_mode,
            target_sample_rate=config.target_sample_rate,
            value_get_method=config.value_get_method,
            pitch_accuracy_decimals=config.pitch_accuracy_decimals,
            music_volume=config.global_volume,
            music_deviation=config.global_deviation,
        )
        music_preview.to_wav_file(data, file_path)
        af = perf_counter_ns()
        print("合成用时", af - pr, "纳秒，即", (af - pr) / 1000_000_000, "秒")

    def stream_dump(
        self, data: SingleMusic, config: PcmConversionConfig
    ) -> Iterator[bytes]:

        pr = perf_counter_ns()
        music_preview = MusicPreview(
            resource_folder=config.assets_path,
            synthesis_mode=config.synthesis_mode,
            overlay_mode=config.overlay_mode,
            target_sample_rate=config.target_sample_rate,
            value_get_method=config.value_get_method,
            pitch_accuracy_decimals=config.pitch_accuracy_decimals,
            music_volume=config.global_volume,
            music_deviation=config.global_deviation,
        )

        b_out = BytesIO()

        music_preview.to_wav_file_byte(data, b_out)
        af = perf_counter_ns()
        print("合成用时", af - pr, "纳秒，即", (af - pr) / 1000_000_000, "秒")

        b_out.seek(0)

        yield from b_out
