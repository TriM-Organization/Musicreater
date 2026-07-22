# -*- coding: utf-8 -*-

"""
音·创 v3 的内部数据类
"""

"""
版权所有 © 2026 金羿
Copyright © 2026 Eilles

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md

# “
# 把代码 洒落在这里
# 和音符 留下的沙砾
# 一点一点爬进你类定义的缝隙
# ”     —— 乐曲访问 by resnah

import heapq
from math import sin, cos, asin, radians, degrees, sqrt, atan, inf, ceil
from dataclasses import dataclass
from typing import (
    Optional,
    Any,
    List,
    SupportsIndex,
    Tuple,
    Union,
    Dict,
    Set,
    Sequence,
    Callable,
    Generator,
    Iterable,
    Iterator,
    Literal,
    Hashable,
    TypeVar,
    Mapping,
    overload,
)
from enum import Enum

from ._utils import volume_weight_to_sound_distance
from .exceptions import (
    SingleNoteDecodeError,
    ParameterTypeError,
    ParameterValueError,
    ParameterCacheUnfreshError,
)
from .paramcurve import ParamCurve

T = TypeVar("T")


class SoundAtmos:
    """声源方位类"""

    sound_distance: float
    """声源距离 方块"""

    sound_azimuth: Tuple[float, float]
    """声源方位 角度(rV左右 rH上下)"""

    def __init__(
        self,
        distance: Optional[float] = None,
        azimuth: Optional[Tuple[float, float]] = None,
    ) -> None:
        """
        定义一个发声方位

        Parameters
        ------------
        distance: float
            发声源距离玩家的距离（半径 `r`）
            注：距离越近，音量越高，默认为 0。此参数可以作为音轨的音量使用。
                音量若默认为 +0，则此值当为 8；此值最小为 0.01，最大为 16。
        azimuth: tuple[float, float]
            声源方位
            注：此参数为tuple，包含两个元素，分别表示：
            `rV`  发声源在竖直（上下）轴上，从玩家视角正前方开始，向顺时针旋转的角度
            `rH`  发声源在水平（左右）轴上，从玩家视角正前方开始，向上
                    （到达玩家正上方顶点后变为向下，以此类推的旋转）旋转的角度
        """

        self.sound_azimuth = (azimuth[0] % 360, azimuth[1] % 360) if azimuth else (0, 0)
        """声源方位"""

        # 如果指定为零，那么为零，但如果不指定或者指定为负数，则为 0.01 的距离
        self.sound_distance = (
            (49 if distance > 48 else (distance if distance >= 0 else 0.01))
            if distance is not None
            else 0.01
        )
        """声源距离"""

    def set_azimuth(self, azimuth: Tuple[float, float]) -> None:
        """设置声源方位"""

        self.sound_azimuth = (azimuth[0] % 360, azimuth[1] % 360)

    def set_distance(self, distance: float) -> None:
        """设置声源距离"""

        self.sound_distance = (
            (49 if distance > 48 else (distance if distance >= 0 else 0.01))
            if distance is not None
            else 0.01
        )

    @classmethod
    def from_displacement(
        cls,
        displacement: Optional[Tuple[float, float, float]] = None,
    ) -> "SoundAtmos":

        if displacement is None:
            # displacement = (0, 0, 0)
            return cls()
        else:
            r = sqrt(displacement[0] ** 2 + displacement[1] ** 2 + displacement[2] ** 2)
            if r == 0:
                return cls(distance=0, azimuth=(0, 0))
            else:
                beta_h = round(degrees(asin(displacement[1] / r)), 8)
                if displacement[2] == 0:
                    alpha_v = -90 if displacement[0] > 0 else 90
                else:
                    alpha_v = round(
                        degrees(atan(-displacement[0] / displacement[2])), 8
                    )
        return cls(distance=r, azimuth=(alpha_v, beta_h))

    @property
    def position_displacement(self) -> Tuple[float, float, float]:
        """声像位移，直接可应用于我的世界的相对视角的坐标参考系中（^x ^y ^z）"""
        dk1 = self.sound_distance * round(cos(radians(self.sound_azimuth[1])), 8)
        return (
            -dk1 * round(sin(radians(self.sound_azimuth[0])), 8),
            self.sound_distance * round(sin(radians(self.sound_azimuth[1])), 8),
            dk1 * round(cos(radians(self.sound_azimuth[0])), 8),
        )

    def __repr__(self) -> str:
        return "SoundAtmos(d={}, rV={}, rH={})".format(
            self.sound_distance, *self.sound_azimuth
        )

    def copy(self) -> "SoundAtmos":
        return SoundAtmos(self.sound_distance, self.sound_azimuth)


@dataclass
class Instrument:
    """乐器类"""

    name: str
    """乐器名称"""

    loadness: int
    """乐器响度 单位`百 LUFS`"""

    def copy(self) -> "Instrument":
        return Instrument(self.name, self.loadness)


class DefaultInstrument(Enum):
    BASS = Instrument("note.bass", -1178)
    BASSATTACK = Instrument("note.bassattack", -1188)
    SNARE = Instrument("note.snare", -1173)
    HAT = Instrument("note.hat", -1480)
    BD = Instrument("note.bd", -957)
    BELL = Instrument("note.bell", -2510)
    FLUTE = Instrument("note.flute", -2076)
    CHIME = Instrument("note.chime", -2984)
    GUITAR = Instrument("note.guitar", -2539)
    XYLOPHONE = Instrument("note.xylophone", -2419)
    IRON_XYLOPHONE = Instrument("note.iron_xylophone", -2078)
    COW_BELL = Instrument("note.cow_bell", -1427)
    DIDGERIDOO = Instrument("note.didgeridoo", -2062)
    BIT = Instrument("note.bit", -2677)
    BANJO = Instrument("note.banjo", -2207)
    PLING = Instrument("note.pling", -1528)
    TRUMPET = Instrument("note.trumpet", -1678)
    TRUMPET_EXPOSED = Instrument("note.trumpet_exposed", -1682)
    TRUMPET_OXIDIZED = Instrument("note.trumpet_oxidized", -2225)
    TRUMPET_WEATHERED = Instrument("note.trumpet_weathered", -1875)
    HARP = Instrument("note.harp", -1448)


@dataclass(init=False, eq=False, order=False)
class SingleNote:
    """存储单个音符的类"""

    midi_pitch: int
    """Midi 音高"""

    start_time: int
    """开始之时 命令刻"""

    duration: int
    """音符持续时间 命令刻"""

    high_precision_start_time: int
    """高精度开始时间偏量 1/5000 秒"""

    extra_info: Dict[str, Any]
    """你觉得放什么好？"""

    def __init__(
        self,
        note_pitch: Optional[int],
        start_tick: int,
        keep_tick: int,
        mass_precision_time: int = 0,
        extra_information: Dict[str, Any] = {},
    ):
        """
        用于存储单个音符的类

        Parameters
        ------------
        midi_pitch: int
            Midi 音高
        start_time: int
            开始之时(命令刻)
            注：此处的时间是用从乐曲开始到当前的刻数
        last_time: int
            音符延续时间(命令刻)
        mass_precision_time: int
            高精度的开始时间偏移量(1/5000秒)
        is_percussion: bool
            是否作为打击乐器
        extra_information: Dict[str, Any]
            附加信息，尽量存储为字典，该内容不被任何“复制”方法保存

        Returns
        ---------
        MineNote 类
        """

        self.midi_pitch: int = 66 if note_pitch is None else note_pitch
        """Midi 音高"""
        self.start_time: int = start_tick
        """开始之时 命令刻"""
        self.duration: int = keep_tick
        """音符持续时间 命令刻"""
        self.high_precision_start_time: int = mass_precision_time
        """高精度开始时间偏量 0.4 毫秒"""

        self.extra_info = extra_information if extra_information else {}

    @property
    def precise_start_time(self) -> float:
        """高精度开始时间"""
        return self.start_time + self.high_precision_start_time / 250

    @classmethod
    def decode(cls, code_buffer: bytes, is_high_time_precision: bool = True):
        """自字节码析出 SingleNote 类"""
        duration_ = (
            group_1 := int.from_bytes(code_buffer[:5], "big")
        ) & 0b11111111111111111
        start_tick_ = (group_1 := group_1 >> 17) & 0b111111111111111111
        note_pitch_ = (group_1 := group_1 >> 18) & 0b1111111

        try:
            return cls(
                note_pitch=note_pitch_,
                start_tick=start_tick_,
                keep_tick=duration_,
                mass_precision_time=code_buffer[5] if is_high_time_precision else 0,
            )
        except Exception as e:
            # 我也不知道为什么这里要放一个异常处理
            # 之前用到过吗？
            # —— 2026.01.25 金羿
            print(
                "[Exception] 单音符解析错误，字节码`{}`，{}启用高精度时间偏移\n".format(
                    code_buffer, "已" if is_high_time_precision else "未"
                )
            )
            raise SingleNoteDecodeError(
                "技术信息：\nGROUP1\t`{}`\nCODE_BUFFER\t`{}`".format(
                    group_1, code_buffer
                ),
            ) from e

    def encode(self, is_high_time_precision: bool = True) -> bytes:
        """
        将数据打包为字节码

        Parameters
        ------------
        is_high_time_precision: bool
            是否启用高精度，默认为**是**

        Returns
        ---------
        bytes
            打包好的字节码
        """

        # SingleNote 的字节码

        # note_pitch 7 位 支持到 127
        # start_tick 18 位 支持到 131071 即 109.22583 分钟 合 1.8204305 小时
        # duration 17 位 支持到 131071 即 109.22583 分钟 合 1.8204305 小时
        # 共 40 位 合 5 字节

        # high_time_precision（可选）长度 8 位 支持到 255 合 1 字节 单位为 1/5000 秒]

        return (
            (
                ((((self.midi_pitch) << 18) + self.start_time) << 17) + self.duration
            ).to_bytes(6, "big")
            # + self.track_no.to_bytes(1, "big")
            + (
                self.high_precision_start_time.to_bytes(1, "big")
                if is_high_time_precision
                else b""
            )
        )

    def set_info(self, key: Union[str, Sequence[str]], value: Any):
        """设置附加信息"""
        if isinstance(key, str):
            self.extra_info[key] = value
        elif (
            isinstance(key, Sequence)
            and isinstance(value, Sequence)
            and (k := len(key)) == len(value)
        ):
            for i in range(k):
                self.extra_info[key[i]] = value[i]
        else:
            # 提供简单报错就行了，如果放一堆 if 语句，降低处理速度
            raise ParameterTypeError(
                "参数类型错误；键：`{}` 值：`{}`".format(key, value)
            )

    def get_info(self, key: str, default: Any = None) -> Any:
        """获取附加信息"""
        return self.extra_info.get(key, default)

    def stringize(self, include_extra_data: bool = False) -> str:
        return "Note(Pitch = {}, StartTick = {}, Duration = {}, TimeOffset = {}".format(
            self.midi_pitch,
            self.start_time,
            self.duration,
            self.high_precision_start_time,
        ) + (", ExtraData = {})".format(self.extra_info) if include_extra_data else ")")

    def copy(
        self,
        note_pitch: Optional[int] = None,
        start_tick: Optional[int] = None,
        keep_tick: Optional[int] = None,
        mass_precision_time: Optional[int] = None,
    ) -> "SingleNote":
        return SingleNote(
            note_pitch=note_pitch or self.midi_pitch,
            start_tick=start_tick or self.start_time,
            keep_tick=keep_tick or self.duration,
            mass_precision_time=mass_precision_time or self.high_precision_start_time,
        )

    # def __list__(self) -> List[int]:
    # 我不认为这个类应当被作为列表使用

    def __bool__(self) -> bool:
        return self.duration > 0

    def __tuple__(
        self,
    ) -> Tuple[int, int, int, int]:
        return (
            self.midi_pitch,
            self.start_time,
            self.duration,
            self.high_precision_start_time,
        )

    def __dict__(  # pyright: ignore[reportIncompatibleVariableOverride]
        self,
    ) -> Dict[str, Any]:
        return {
            "Pitch": self.midi_pitch,
            "StartTick": self.start_time,
            "Duration": self.duration,
            "TimeOffset": self.high_precision_start_time,
            "ExtraData": self.extra_info,
        }

    def __eq__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: "SingleNote"
    ) -> bool:
        """比较两个音符是否具有相同的属性，不计附加信息"""
        if not isinstance(other, self.__class__):
            return False
        return self.__tuple__() == other.__tuple__()

    def __lt__(self, other: "SingleNote") -> bool:
        """比较自己是否在开始时间上早于另一个音符"""
        if self.start_time == other.start_time:
            return self.high_precision_start_time < other.high_precision_start_time
        else:
            return self.start_time < other.start_time

    def __gt__(self, other: "SingleNote") -> bool:
        """比较自己是否在开始时间上晚于另一个音符"""
        if self.start_time == other.start_time:
            return self.high_precision_start_time > other.high_precision_start_time
        else:
            return self.start_time > other.start_time


@dataclass
class MineNote:
    """我的世界音符对象（仅提供我的世界相关接口）"""

    pitch: float
    """Midi 音高"""
    instrument: str
    """乐器标识"""
    start_tick: int
    """开始之时 命令刻"""
    duration_tick: int
    """音符持续时间 命令刻"""
    start_time_offset: int
    """高精度开始时间偏量 1/5000 秒"""
    percussive: bool
    """是否作为打击乐器使用"""
    position: SoundAtmos
    """声像方位"""

    @property
    def precise_tick(self) -> float:
        """高精度开始时间"""
        return self.start_tick + self.start_time_offset / 250

    @classmethod
    def from_single_note(
        cls,
        note: SingleNote,
        note_instrument: str,
        note_volume_weight: float,
        is_persiced_time: bool,
        is_percussive_note: bool,
        sound_position: SoundAtmos,
        adjust_note_pitch: float = 0.0,
        multiple_note_volume_weight: float = 0.0,
        adjust_note_sound_distance: float = 0.0,
        adjust_note_leftright_panning_degree: float = 0.0,
        adjust_note_updown_panning_degree: float = 0.0,
    ) -> "MineNote":
        """从SingleNote对象创建MineNote对象"""
        return cls(
            pitch=note.midi_pitch + adjust_note_pitch,
            instrument=note_instrument,
            start_tick=note.start_time,
            duration_tick=note.duration,
            start_time_offset=note.high_precision_start_time if is_persiced_time else 0,
            percussive=is_percussive_note,
            position=(
                SoundAtmos(
                    (
                        (
                            (
                                (
                                    (
                                        sound_position.sound_distance
                                        + adjust_note_sound_distance
                                        - 48
                                    )
                                    * (note_volume_weight * multiple_note_volume_weight)
                                    / note_volume_weight
                                )
                                + 48
                            )
                        )  # 此处调整须保证前提：音量权的增值必须为负
                        if multiple_note_volume_weight
                        else (
                            sound_position.sound_distance + adjust_note_sound_distance
                        )
                    ),
                    (
                        sound_position.sound_azimuth[0]
                        + adjust_note_leftright_panning_degree,
                        sound_position.sound_azimuth[1]
                        + adjust_note_updown_panning_degree,
                    ),
                )
                if (
                    multiple_note_volume_weight
                    or adjust_note_sound_distance
                    or adjust_note_leftright_panning_degree
                    or adjust_note_updown_panning_degree
                )
                else sound_position
            ),
        )


class CurvableParam(str, Enum):
    """可曲线化的参数 枚举类"""

    PITCH = "adjust_note_pitch"
    VOLUME = "multiple_note_volume_weight"
    DISTANCE = "adjust_note_sound_distance"
    LR_PANNING = "adjust_note_leftright_panning_degree"
    UD_PANNING = "adjust_note_updown_panning_degree"


class SingleTrack(List[SingleNote]):
    """存储单个轨道的类"""

    name: str
    """轨道之名称"""

    is_enabled: bool = True
    """该音轨是否启用"""

    instrument: Instrument
    """乐器ID"""

    is_high_time_precision: bool
    """该音轨是否使用高精度时间"""

    is_percussive: bool
    """该音轨是否标记为打击乐器轨道"""

    _volume_weight: float = 10
    """音量权"""

    _sound_distance: float = -1
    """声源距离"""

    sound_position: Tuple[float, float]
    """声像方位 球坐标系角度(rV左右 rH上下)"""

    argument_curves: Dict[CurvableParam, Union[ParamCurve, Literal[None]]]
    """参数曲线"""

    extra_info: Dict[str, Any]
    """你觉得放什么好？"""

    # 构建类

    def __init__(
        self,
        *args: SingleNote,
        track_name: str = "未命名音轨",
        track_instrument: Optional[Instrument] = None,
        precise_time: bool = True,
        percussion: bool = False,
        volume_weight: float = 10.0,
        sound_direction: Tuple[float, float] = (0, 0),
        extra_information: Dict[str, Any] = {},
    ):
        """
        构建音轨

        Parameters
        ==========
        *args: SingleNote
            音符列表
        track_name: str
            音轨名称
        track_instrument: str
            音轨所使用的乐器名称
        precise_time: bool
            该音轨是否使用高精度时间
        percussion: bool
            该音轨的乐器是否为打击乐器（无音高调整）
        volume_weight: float
            音量权，用以表明音轨的音量应当占有的权重大小。值越大，听起来声音越大。
            默认为 10
        sound_direction: Tuple[float, float]
            声源方位
            注：此参数为tuple，包含两个元素，分别表示：
            `rV`  发声源在竖直（上下）轴上，从玩家视角正前方开始，向顺时针旋转的角度
            `rH`  发声源在水平（左右）轴上，从玩家视角正前方开始，向上
                    （到达玩家正上方顶点后变为向下，以此类推的旋转）旋转的角度
        """
        self.name = track_name
        """音轨名称"""

        self.instrument = (
            track_instrument if track_instrument else DefaultInstrument.HARP.value
        )
        """乐器ID"""

        self.is_high_time_precision = precise_time
        """是否使用高精度时间"""

        self.is_percussive = percussion
        """是否为打击乐器"""

        self._volume_weight = volume_weight
        """音量权"""

        self._sound_distance = -1
        """声源距离"""

        self.sound_position = sound_direction
        """声像方位"""

        self.extra_info = extra_information if extra_information else {}

        self.argument_curves = {item: None for item in CurvableParam}

        super().__init__(args)
        super().sort()

    @classmethod
    def from_note_list(
        cls,
        note_list: Iterable[SingleNote],
        track_name: str = "未命名音轨",
        track_instrument: Optional[Instrument] = None,
        precise_time: bool = True,
        percussion: bool = False,
        volume_weight: float = 10.0,
        sound_direction: Tuple[float, float] = (0, 0),
        extra_information: Dict[str, Any] = {},
    ) -> "SingleTrack":
        """从音符列表创建 SingleTrack 对象"""

        single_track = cls(
            track_name=track_name,
            track_instrument=track_instrument,
            precise_time=precise_time,
            percussion=percussion,
            volume_weight=volume_weight,
            sound_direction=sound_direction,
            extra_information=extra_information,
        )
        single_track.update(note_list)
        return single_track

    # 类参数

    @property
    def volume_weight(self) -> float:
        """音量权"""
        return self._volume_weight

    @property
    def sound_distance(self) -> float:
        """声源距离"""
        if self._sound_distance < 0:
            raise ParameterCacheUnfreshError(
                "未设置声源距离（`{}`），操作时不应直接访问 `__volume_weight` 属性".format(
                    self._sound_distance
                )
            )
        return self._sound_distance

    @property
    def note_amount(self) -> int:
        """音符数"""
        return len(self)

    def disable(self) -> None:
        """禁用音轨"""

        self.is_enabled = False

    def enable(self) -> None:
        """启用音轨"""

        self.is_enabled = True

    def toggle_able(self) -> None:
        """切换音轨的启用状态"""

        self.is_enabled = not self.is_enabled

    def set_volume_weight(
        self, max_weight: float, minimal_loadness: int, weight
    ) -> float:
        """设置音量权

        以下关于距离的计算逻辑请见[计算过程](./resources/响度公式/计算过程.jpg)\n
        关于响度的计算方法请见[此脚本](./resources/experiments/exam_loadness.py)\n
        最终公式为：\n
        声源距离 = 48 - (48 * 音量权 * ( 10 ** ((当前乐器的响度 - 响度最小乐器的响度) / 20 ))) / 全曲最大音量权\n
            D_t = 48 - \\frac{48 \\cdot P_t \\cdot 10^{\\frac{V_t - V_x}{20}}}{P_m}
        由于我们存储的响度都是 百-LUFS，所以下面的计算除数为 2000
        """

        self._volume_weight = weight

        self._sound_distance = volume_weight_to_sound_distance(
            max_weight, minimal_loadness, weight, self.instrument.loadness
        )
        # print(
        #     "收到音量权：",
        #     weight,
        #     "，最大权：",
        #     max_weight,
        #     "，设置声源距离为：",
        #     self.__sound_distance,
        # )
        return self._sound_distance

    # 类操作

    def append(self, object: SingleNote) -> None:
        """
        添加一个音符，推荐使用 add 方法
        """

        return self.add(object)

    def add(self, item: SingleNote) -> None:
        """
        在音轨里添加一个音符
        """

        if not isinstance(item, SingleNote):
            raise ParameterTypeError(
                "单音轨类的元素类型须为单音符（`SingleNote`），不可为：`{}`".format(
                    type(item).__name__
                )
            )
        super().append(item)
        super().sort()  # =========================== TODO 需要优化

    def update(self, items: Iterable[SingleNote]):
        """
        拼接两个音轨
        """
        super().extend(items)
        super().sort()  # =========================== TODO 需要优化

    def copy(
        self,
        start_time: float = 0,
        end_time: float = inf,
        with_argument_curve: bool = False,
        keep_zone_boundary_argument_value: bool = False,
        global_boundary_argument_safe: bool = True,
    ) -> "SingleTrack":
        """
        通过时间范围来复制音轨，返回一个音轨
        """
        single_track = SingleTrack.from_note_list(
            (
                [x for x in self if start_time <= x.precise_start_time <= end_time]
                if self.is_high_time_precision
                else [x for x in self if start_time <= x.start_time <= end_time]
            ),
            track_instrument=self.instrument.copy(),
            precise_time=self.is_high_time_precision,
            percussion=self.is_percussive,
            volume_weight=self.volume_weight,
            sound_direction=self.sound_position,
        )
        single_track._sound_distance = self.sound_distance
        if with_argument_curve:
            single_track.argument_curves = {
                item: (
                    None
                    if curve is None
                    else curve.copy(
                        start=start_time,
                        end=end_time,
                        keep_zone_boundary_value=keep_zone_boundary_argument_value,
                        global_boundary_safe=global_boundary_argument_safe,
                    )
                )
                for item, curve in self.argument_curves.items()
            }
        return single_track

    def paste(
        self,
        items: Iterable[SingleNote],
        offset_time: int,
        offset_mass_precision_time: int = 0,
        is_passin_time_precise: bool = True,
    ):
        """
        将一个音轨粘贴到当前音轨的指定时间
        """
        note_iterator = items.__iter__()
        first_note = next(note_iterator)
        original_start_time = first_note.start_time
        super().append(
            first_note.copy(
                start_tick=offset_time,
                mass_precision_time=(
                    offset_mass_precision_time if self.is_high_time_precision else 0
                ),
            )
        )
        if self.is_high_time_precision:
            for note in note_iterator:
                super().append(
                    note.copy(
                        start_tick=note.start_time
                        - original_start_time
                        + offset_time
                        + (
                            (
                                offset_mass_precision_time
                                + note.high_precision_start_time
                            )
                            // 250
                        ),
                        mass_precision_time=(
                            offset_mass_precision_time + note.high_precision_start_time
                        )
                        % 250,
                    )
                )
        else:
            if is_passin_time_precise:
                for note in note_iterator:
                    super().append(
                        note.copy(
                            start_tick=note.start_time
                            - original_start_time
                            + offset_time
                            + (
                                (
                                    offset_mass_precision_time
                                    + note.high_precision_start_time
                                )
                                // 250
                            )
                        )
                    )
            else:
                for note in note_iterator:
                    super().append(
                        note.copy(
                            start_tick=note.start_time
                            - original_start_time
                            + offset_time
                        )
                    )
        self.sort()  # =========================== TODO 需要优化

    def delete(
        self, start_time: float, end_time: float, with_argument_curve: bool = False
    ):
        """
        删除时间范围内的音符
        """
        if with_argument_curve:
            for curve in self.argument_curves.values():
                if curve is not None:
                    curve.delete(start_time, end_time)

        for i, j in enumerate(
            [
                i
                for i, x in enumerate(self)
                if start_time <= x.precise_start_time <= end_time
            ]
        ):
            del self[j - i]

    # 音符操作

    @property
    def notes(self) -> List[SingleNote]:
        """音符列表"""
        return self

    @property
    def minenotes(self) -> Iterator[MineNote]:
        """
        直接返回当前音轨所有音符的我的世界数据形式
        """
        return (
            MineNote.from_single_note(
                note=_note,
                note_instrument=self.instrument.name,
                note_volume_weight=self.volume_weight,
                is_persiced_time=self.is_high_time_precision,
                is_percussive_note=self.is_percussive,
                sound_position=SoundAtmos(self.sound_distance, self.sound_position),
                **{
                    item.value: argcrv.value_at(_note.precise_start_time)
                    for item in CurvableParam
                    if (argcrv := self.argument_curves[item])
                },
            )
            for _note in self
        )

    def get(self, time: int) -> Generator[SingleNote, None, None]:
        """通过确切的开始时间来获取音符"""

        return (x for x in self if x.precise_start_time == time)

    def get_notes(
        self, start_time: float = 0, end_time: float = inf
    ) -> Iterator[SingleNote]:
        """通过开始时间和结束时间来获取音符"""
        if end_time < start_time:
            raise ParameterValueError(
                "获取音符的时间范围有误，终止时间`{}`早于起始时间`{}`".format(
                    end_time, start_time
                )
            )
        elif end_time < 0:
            raise ParameterValueError(
                "获取音符的时间范围有误，终止时间`{}`不可为负数".format(end_time)
            )
        elif start_time <= 0 and end_time >= self[-1].precise_start_time:
            return iter(self)

        return (
            x
            for x in self
            if (x.precise_start_time >= start_time)
            and (x.precise_start_time <= end_time)
        )

    def get_minenotes(
        self, range_start_time: float = 0, range_end_time: float = inf
    ) -> Generator[MineNote, Any, None]:
        """获取能够用以在我的世界播放的音符数据类"""

        for _note in self.get_notes(range_start_time, range_end_time):
            yield MineNote.from_single_note(
                note=_note,
                note_instrument=self.instrument.name,
                note_volume_weight=self.volume_weight,
                is_persiced_time=self.is_high_time_precision,
                is_percussive_note=self.is_percussive,
                sound_position=SoundAtmos(self.sound_distance, self.sound_position),
                **{
                    item.value: argcrv.value_at(_note.precise_start_time)
                    for item in CurvableParam
                    if (argcrv := self.argument_curves[item])
                },
            )

    # 其他

    def set_info(self, key: Union[str, Sequence[str]], value: Any):
        """设置附加信息"""
        if isinstance(key, str):
            self.extra_info[key] = value
        elif (
            isinstance(key, Sequence)
            and isinstance(value, Sequence)
            and (k := len(key)) == len(value)
        ):
            for i in range(k):
                self.extra_info[key[i]] = value[i]
        else:
            # 提供简单报错就行了，如果放一堆 if 语句，降低处理速度
            raise ParameterTypeError(
                "参数类型错误；键：`{}` 值：`{}`".format(key, value)
            )

    def get_info(self, key: str, default: Any = None) -> Any:
        """获取附加信息"""
        return self.extra_info.get(key, default)


class SingleMusic(List[SingleTrack]):
    """存储单个曲子的类"""

    music_name: str
    """乐曲名称"""

    music_creator: str
    """本我的世界曲目的制作者"""

    music_original_author: str
    """曲目的原作者"""

    music_description: str
    """当前曲目的简介"""

    music_credits: str
    """曲目的版权信息"""

    # 感叹一下什么叫冗余设计啊！（叉腰）
    extra_info: Dict[str, Any]
    """这还得放东西？"""

    __max_volume_weight: float = -1
    """全曲最大音量权"""

    __minimal_loadness: int = 1
    """全曲响度最小的乐器采样的响度"""

    # 前置方法

    def _calc_values(self):
        # print("收到音乐参数计算请求，当前最大：",self.__max_volume_weight, end="；")
        for track in self:
            self.__max_volume_weight = max(
                track.volume_weight, self.__max_volume_weight
            )
            self.__minimal_loadness = min(
                track.instrument.loadness, self.__minimal_loadness
            )
        for track in self:
            track.set_volume_weight(
                max_weight=self.__max_volume_weight,
                minimal_loadness=self.__minimal_loadness,
                weight=track.volume_weight,
            )
        # print("计算后最大：",self.__max_volume_weight)

    # 类的构建方法

    def __init__(
        self,
        *args: SingleTrack,
        name: str = "未命名乐曲",
        creator: str = "未命名制作者",
        original_author: str = "未命名原曲作",
        description: str = "无简介",
        credits: str = "保留所有权利。All Rights Reserved.",
        extra_information: Dict[str, Any] = {},
    ):
        self.music_name = name
        """乐曲名称"""

        self.music_creator = creator
        """曲目制作者"""

        self.music_original_author = original_author
        """乐曲原作者"""

        self.music_description = description
        """简介"""

        self.music_credits = credits
        """版权信息"""

        self.extra_info = extra_information if extra_information else {}

        super().__init__(*args)

        self._calc_values()

    @classmethod
    def from_track_list(
        cls,
        track_list: Sequence[SingleTrack],
        name: str = "未命名乐曲",
        creator: str = "未命名制作者",
        original_author: str = "未命名原曲作",
        description: str = "无简介",
        credits: str = "保留所有权利。All Rights Reserved.",
        extra_information: Dict[str, Any] = {},
    ) -> "SingleMusic":
        single_music = cls(
            name=name,
            creator=creator,
            original_author=original_author,
            description=description,
            credits=credits,
            extra_information=extra_information,
        )
        single_music.extend(track_list)
        return single_music

    # 类操作

    def append(self, track: SingleTrack) -> None:
        """
        将一个音轨添加到全曲中，排列在所有音轨之后。

        Append object to the end of the list.
        """
        super().append(track)
        self._calc_values()

    def extend(self, tracks: Iterable[SingleTrack]) -> None:
        """
        将一个音轨列表添加到全曲中，依顺序在所有音轨之后排列。

        Extend list by appending elements from the iterable.
        """
        super().extend(tracks)
        self._calc_values()

    def insert(self, index: SupportsIndex, track: SingleTrack) -> None:
        """
        将一个音轨插入到全曲中，在指定位置。

        Insert object before index.
        """
        super().insert(index, track)
        self._calc_values()

    def remove(self, track: SingleTrack) -> None:
        """
        从全曲中删除一个音轨。

        Remove first occurrence of value.

        当音轨不存在时，会抛出 `ValueError`。
        Raises `ValueError` if the value is not present.
        """
        super().remove(track)
        self._calc_values()

    def clear(self) -> None:
        """
        清空全曲。

        Remove all items from list.
        """
        super().clear()
        self.__max_volume_weight = -1
        self.__minimal_loadness = 1

    def pop(self, index: SupportsIndex = -1) -> SingleTrack:
        """
        从全曲中删除一个音轨。

        Remove and return item at index (default last).

        当音轨不存在时，会抛出 `IndexError`。

        Raises IndexError if list is empty or index is out of range.
        """
        to_pop = super().pop(index)
        self._calc_values()
        return to_pop

    @overload
    def __setitem__(self, key: SupportsIndex, value: SingleTrack) -> None: ...

    @overload
    def __setitem__(self, key: slice, value: Sequence[SingleTrack]) -> None: ...

    def __setitem__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, key, value
    ) -> None:
        """
        设置一个音轨

        Set self[key] to value.
        """
        super().__setitem__(key, value)
        self._calc_values()

    def __delitem__(self, key: SupportsIndex | slice) -> None:
        """
        删除一个音轨

        Delete self[key].
        """
        super().__delitem__(key)
        self._calc_values()

    def copy(self) -> "SingleMusic":

        # 没想到真的会用到全曲复制……
        return self.from_track_list(
            track_list=[
                tr.copy(
                    with_argument_curve=True,
                )
                for tr in self
            ],
            name=self.music_name,
            creator=self.music_creator,
            original_author=self.music_original_author,
            description=self.music_description,
            credits=self.music_credits,
        )

    # 类属性

    @property
    def track_amount(self) -> int:
        """音轨数"""
        return len(self)

    @property
    def music_tracks(self) -> Iterator[SingleTrack]:
        """音轨列表，不包含被禁用的音轨"""
        return (track for track in self if track.is_enabled)

    def set_loadness(self, track: Union[int, SingleTrack], weight: float) -> None:
        if weight > self.__max_volume_weight:
            if isinstance(track, int):
                self[track]._volume_weight = weight

            elif isinstance(track, SingleTrack):
                if track in self:
                    track._volume_weight = weight
                else:
                    raise ParameterValueError(
                        "音轨：`{}`不属于此曲目".format(track.name)
                    )
            self._calc_values()
            return
        else:
            if isinstance(track, int):
                self[track].set_volume_weight(
                    max_weight=self.__max_volume_weight,
                    minimal_loadness=self.__minimal_loadness,
                    weight=weight,
                )
                return
            elif isinstance(track, SingleTrack):
                track.set_volume_weight(
                    max_weight=self.__max_volume_weight,
                    minimal_loadness=self.__minimal_loadness,
                    weight=weight,
                )
                return

        raise ParameterTypeError("音轨不得为`{}`类型".format(type(track)))

    # 音符操作

    @staticmethod
    def yield_from_tracks(
        tracks: Sequence[Iterator[T]],
        sort_key: Callable[[T], Any],
        is_subseq_sorted: bool = True,
    ) -> Iterator[T]:
        """从任意迭代器列表迭代符合顺序的元素
        （惰性多路归并多个迭代器，按 sort_key 排序）

        参数
        ----
        tracks: Sequence[Iterator[T]]
            迭代器列表
        sort_key: Callable[[T], Any]
            接受 T 元素，返回可比较的键
        is_subseq_sorted: bool = True
            子序列是否已排序

        迭代
        ----
            归并后的每个元素，按 sort_key 升序
        """
        if is_subseq_sorted:
            # 必须这样处理，不能 return 这个 merge，测试过了
            yield from heapq.merge(*tracks, key=sort_key)
        else:
            # 初始化堆
            heap_pool: List[Tuple[Any, int, T]] = []
            for _index, _track in enumerate(tracks):
                try:
                    item = next(_track)
                    heapq.heappush(heap_pool, (sort_key(item), _index, item))
                except StopIteration:
                    continue

            # 归并主循环
            while heap_pool:
                _key, _index, item = heapq.heappop(heap_pool)
                yield item
                try:
                    next_item = next(tracks[_index])
                    heapq.heappush(heap_pool, (sort_key(next_item), _index, next_item))
                except StopIteration:
                    pass
        # NEVER REACH:
        # pool: List[Tuple[str, T]] = []
        # remove_track: List[str] = []
        # for _name, _track in tracks.items():
        #     try:
        #         pool.append((_name, next(_track)))
        #     except StopIteration:
        #         remove_track.append(_name)
        # for _x in remove_track:
        #     tracks.pop(_x)
        # del remove_track
        # while tracks and pool:
        #     yield (_x := min(pool, key=sort_key))[1]
        #     try:
        #         pool.append((_x[0], next(tracks[_x[0]])))
        #     except StopIteration:
        #         tracks.pop(_x[0])
        # pool.sort(key=sort_key)
        # for _remain in pool:
        #     yield _remain[1]

    def get_tracked_notes(
        self, start_time: float = 0, end_time: float = inf
    ) -> Generator[Iterator[SingleNote], Any, None]:
        """获取指定时间段的各个音轨的音符数据"""
        return (track.get_notes(start_time, end_time) for track in self.music_tracks)

    def get_tracked_minenotes(
        self, start_time: float = 0, end_time: float = inf
    ) -> Generator[Iterator[MineNote], Any, None]:
        """获取指定时间段的各个音轨的，供我的世界播放的音符数据类"""
        return (
            track.get_minenotes(start_time, end_time) for track in self.music_tracks
        )

    def get_notes(
        self, start_time: float = 0, end_time: float = inf
    ) -> Iterator[SingleNote]:
        """获取指定时间段的所有音符数据，按照时间顺序"""
        if self.track_amount == 0:
            return iter(())
        return self.yield_from_tracks(
            [track.get_notes(start_time, end_time) for track in self.music_tracks],
            sort_key=lambda x: x.precise_start_time,
        )

    def get_minenotes(
        self, start_time: float = 0, end_time: float = inf
    ) -> Iterator[MineNote]:
        """获取指定时间段所有的，供我的世界播放的音符数据类，按照时间顺序"""
        if self.track_amount == 0:
            return iter(())
        return self.yield_from_tracks(
            [track.get_minenotes(start_time, end_time) for track in self.music_tracks],
            sort_key=lambda x: x.start_tick,
        )

    # 其他

    def set_info(self, key: Union[str, Sequence[str]], value: Any):
        """设置附加信息"""
        if isinstance(key, str):
            self.extra_info[key] = value
        elif (
            isinstance(key, Sequence)
            and isinstance(value, Sequence)
            and (k := len(key)) == len(value)
        ):
            for i in range(k):
                self.extra_info[key[i]] = value[i]
        else:
            # 提供简单报错就行了，如果放一堆 if 语句，降低处理速度
            raise ParameterTypeError(
                "参数类型错误；键：`{}` 值：`{}`".format(key, value)
            )

    def get_info(self, key: str, default: Any = None) -> Any:
        """获取附加信息"""
        return self.extra_info.get(key, default)
