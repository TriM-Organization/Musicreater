# -*- coding: utf-8 -*-

"""
音·创 v3 内置的 音乐合成预览功能
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

from math import inf
from typing import BinaryIO, Optional, Iterator, Generator, Any, Tuple, Literal
from pathlib import Path

import soundfile as sf
import librosa
import numpy as np


from Musicreater import SingleMusic, SingleTrack, SingleNote, SoundAtmos, MineNote
from Musicreater.constants import MM_INSTRUMENT_DEVIATION_TABLE


class MusicPreview:
    """
    原始资源存储规范：
    Dict[str"ID1": Dict[str"SoundID": ndarray[]]]
    转换资源存储规范：
    Dict[str"ID1": Dict[str"SoundID": Dict[int"Pitch": ndarray]]]
    测试阶段，请直接vanilla作为默认传入，不考虑载入
    """

    res_raw_data: dict = {}  # 原始资源存储
    # res_raw_index: list = []  # 资源转换情况，key: [88]  留着优化
    res_data: dict = {}  # 转换后资源存储
    res_data_sr: int  # 转换后采样率，和输出采样率一致

    @staticmethod
    def res_pitch_shift(y: np.ndarray, *, sr: float, n_steps: float, **kwargs: Any):
        return librosa.effects.pitch_shift(y, sr=sr, n_steps=n_steps)

    @staticmethod
    def res_time_stretch(y: np.ndarray, *, rate: float, **kwargs: Any):
        return librosa.effects.time_stretch(y, rate=rate)

    @staticmethod
    def res_resample(
        y: np.ndarray,
        *,
        orig_sr: float,
        target_sr: float,
        fix: bool = True,
        **kwargs: Any,
    ):
        return librosa.resample(y, orig_sr=orig_sr, target_sr=target_sr, fix=fix)

    def __init__(
        self,
        resource_folder: Path,
        synthesis_mode: Literal[0, 1, 2, 3, 4] = 1,
        overlay_mode: Literal[1, 2] = 1,
        sample_rate: int = 44100,
        value_get_method: Literal[0, 1] = 1,
        pitch_accuracy_decimals: int = 0,
        music_deviation: float = 0,
    ):

        self.mode = synthesis_mode
        self.overlay_mode_c = overlay_mode
        self.output_sample_rate = sample_rate
        self.get_value_method = value_get_method
        self.resources_path = resource_folder
        self.pitch_precision_decimals = pitch_accuracy_decimals

        self.pitch_deviation = music_deviation

        for file in self.resources_path.iterdir():
            if file.is_file():
                self.res_raw_data[file.stem] = librosa.load(file, sr=None)

    def res_shift(
        self,
        sound_name: str,
        percussive: bool,
        pitch: int,
        duration: int,
        # rate: int
    ):
        y_orig, sr_orig = self.res_raw_data[sound_name]
        if not percussive:
            if self.mode == 1:
                # 变调， 时域压扩， 重采样 mc方法
                self.res_data[sound_name][pitch] = librosa.resample(
                    librosa.effects.time_stretch(
                        librosa.effects.pitch_shift(y_orig, sr=sr_orig, n_steps=pitch),
                        rate=2 ** (pitch / 12),
                    ),
                    orig_sr=sr_orig,
                    target_sr=self.output_sample_rate,
                    fix=False,
                )
            elif self.mode == 0:
                # 重采样， 变调
                self.res_data[sound_name][pitch] = librosa.resample(
                    librosa.effects.pitch_shift(y_orig, sr=sr_orig, n_steps=pitch),
                    orig_sr=sr_orig,
                    target_sr=self.output_sample_rate,
                    fix=False,
                )
            elif self.mode == 4:

                # 变调， 时域压扩， 重采样 MIDI-FFT
                if self.overlay_mode_c == 2:
                    rate = duration / 20 / (len(y_orig[0]) / sr_orig)
                else:
                    rate = duration / 20 / (len(y_orig) / sr_orig)
                rate = rate if rate != 0 else 1
                self.res_data[sound_name][pitch] = librosa.resample(
                    librosa.effects.time_stretch(
                        librosa.effects.pitch_shift(y_orig, sr=sr_orig, n_steps=pitch),
                        rate=rate,
                    ),
                    orig_sr=sr_orig,
                    target_sr=self.output_sample_rate,
                    fix=False,
                )
            elif self.mode == 2:
                # 变调， 时域压扩， 重采样 MIDI-cut
                if self.overlay_mode_c == 2:
                    deal = librosa.effects.pitch_shift(
                        y_orig, sr=sr_orig, n_steps=pitch
                    )[
                        ...,
                        : (
                            int(duration / 20 * sr_orig)
                            if duration / 20 * sr_orig > len(y_orig[0])
                            else len(y_orig[0])
                        ),
                    ]
                else:
                    deal = librosa.effects.pitch_shift(
                        y_orig, sr=sr_orig, n_steps=pitch
                    )[
                        : (
                            int(duration / 20 * sr_orig)
                            if duration / 20 * sr_orig > len(y_orig)
                            else len(y_orig)
                        )
                    ]
                self.res_data[sound_name][pitch] = librosa.resample(
                    deal, orig_sr=sr_orig, target_sr=self.output_sample_rate, fix=False
                )
        else:
            # if self.mode == 1:
            # 重采样, 不变调
            print(">>", sound_name, pitch)
            self.res_data[sound_name][pitch] = librosa.resample(
                y_orig,
                orig_sr=sr_orig,
                target_sr=self.output_sample_rate,
                fix=False,  # 尽管这样不变调，但是也不应将 pitch 与打击乐器联系在一起
            )
            """elif self.mode == 0:
                # 重采样, 不变调, 衰弱
                self.cache_dict[raw_name] = librosa_resample(
                    y_orig,
                    orig_sr=sr_orig,
                    target_sr=self.out_sr,
                    fix=False
                )"""

    def make_pitch_accurate(self, pitch: float) -> int:
        """
        相信你知道的，小数并不准确
        """
        return int((pitch + self.pitch_deviation) * (10**self.pitch_precision_decimals))

    # 获取资源方法，需要指定采样率，采样率变了即全局重载
    # 资源存储类里面有就取，没就写入并标识已有数据
    def get_res(
        self,
        sound_name: str,
        pitch: float,
        percussive: bool,
        duration: int,
    ):

        print(
            sound_name,
            pitch,
            ">>",
            (pitch := self.make_pitch_accurate(pitch)),
            percussive,
            duration,
        )

        if sound_name in self.res_data:
            if pitch in self.res_data[sound_name]:
                return self.res_data[sound_name][pitch]
            else:
                self.res_shift(
                    sound_name=sound_name,
                    percussive=percussive,
                    pitch=pitch,
                    duration=duration,
                )
                # print(2, self.res_data[packageID][soundID][pitch])
                return self.res_data[sound_name][pitch]
        else:
            self.res_data[sound_name] = {}
            self.res_shift(
                sound_name=sound_name,
                percussive=percussive,
                pitch=pitch,
                duration=duration,
            )
            # print(2, self.res_data[packageID][soundID][pitch])
            return self.res_data[sound_name][pitch]

    def convert(self, music: SingleMusic, start_tick: float = 0, end_tick: float = inf):

        if self.overlay_mode_c == 1:

            def overlay(seg_overlay: np.ndarray, pos_tick: int):
                pos_ = int(out_sr * pos_tick * 0.05)
                wav_model[pos_ : seg_overlay.size + pos_] += seg_overlay

            # print(0)
            wav_model = np.zeros(
                int(
                    max(
                        [
                            (
                                i.start_tick * 0.05 * self.output_sample_rate
                                + len(
                                    self.get_res(
                                        sound_name=i.instrument,
                                        pitch=i.pitch
                                        - 60
                                        - MM_INSTRUMENT_DEVIATION_TABLE.get(
                                            i.instrument, 6
                                        ),
                                        percussive=i.percussive,
                                        duration=i.duration_tick,
                                    )
                                )
                            )
                            for i in music.get_minenotes(
                                start_time=start_tick, end_time=end_tick
                            )
                        ]
                    )
                ),
                dtype=np.float32,
            )

        elif self.overlay_mode_c == 2:

            def overlay(seg_overlay: np.ndarray, pos_tick: int):
                pos_ = int(out_sr * pos_tick * 0.05)
                wav_model[..., pos_ : len(seg_overlay[0]) + pos_] += seg_overlay

            wav_model = np.zeros(
                (
                    2,
                    int(
                        max(
                            [
                                (
                                    i.start_tick * 0.05 * self.output_sample_rate
                                    + len(
                                        self.get_res(
                                            sound_name=i.instrument,
                                            pitch=i.pitch
                                            - 60
                                            - MM_INSTRUMENT_DEVIATION_TABLE.get(
                                                i.instrument, 6
                                            ),
                                            percussive=i.percussive,
                                            duration=i.duration_tick,
                                        )
                                    )
                                )
                                for i in music.get_minenotes(
                                    start_time=start_tick, end_time=end_tick
                                )
                            ]
                        )
                    ),
                ),
                dtype=np.float32,
            )

        else:
            raise ValueError("错误的 overlay_mode 参数")

        out_sr = self.output_sample_rate

        for note in music.get_minenotes(start_time=start_tick, end_time=end_tick):
            accurate_pitch = self.make_pitch_accurate(
                note.pitch
                - 60
                - (
                    0
                    if note.percussive
                    else MM_INSTRUMENT_DEVIATION_TABLE.get(note.instrument, 6)
                )
            )
            print(
                ":",
                note.instrument,
                note.pitch,
                ">>",
                accurate_pitch,
                note.percussive,
                note.duration_tick,
            )
            if not note.percussive:
                overlay(
                    self.res_data[note.instrument][accurate_pitch] * note.volume / 127,
                    note.start_tick,
                )
            else:
                overlay(
                    self.res_data[note.instrument][accurate_pitch] * note.volume / 127,
                    note.start_tick,
                )

        if self.get_value_method == 0:
            # 归一化，抚摸耳朵 (bushi
            max_val = np.max(np.abs(wav_model))
            if not max_val == 0:
                wav_model = wav_model / max_val
        elif self.get_value_method == 1:
            wav_model[wav_model > 1] = 1
            wav_model[wav_model < -1] = -1
        if self.overlay_mode_c == 2:
            return wav_model.T
        else:
            return wav_model[:, np.newaxis]

    def stream(self, music: SingleMusic):
        pass

    # debug
    def to_wav_file(self, single_music: SingleMusic, out_file_path: Path):

        sf.write(
            out_file_path,
            self.convert(single_music),
            samplerate=self.output_sample_rate,
            format="wav",
        )
        return out_file_path

    def to_wav_file_byte(self, single_music: SingleMusic, output_file: BinaryIO):
        sf.write(
            output_file,
            self.convert(single_music),
            samplerate=self.output_sample_rate,
            format="wav",
        )
