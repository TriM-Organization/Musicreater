# -*- coding: utf-8 -*-

"""
存储音·创新数据存储类
"""

# WARNING 本文件中使用之功能尚未启用

"""
版权所有 © 2025 金羿
Copyright © 2025 Eilles

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md


from math import sin, cos, asin, radians, degrees, sqrt, atan, inf
from dataclasses import dataclass
from typing import Optional, Any, List, Tuple, Union, Dict, Sequence, Callable
import bisect

from .types import FittingFunctionType
from .constants import MC_PITCHED_INSTRUMENT_LIST


class ArgumentCurve:

    base_line: float = 0
    """基线/默认值"""

    default_curve: Callable[[float], float]
    """默认曲线"""

    defined_curves: Dict[float, "ArgumentCurve"] = {}
    """调整后的曲线集合"""

    left_border: float = 0
    """定义域左边界"""

    right_border: float = inf
    """定义域右边界"""

    def __init__(self, baseline: float = 0, default_function: Callable[[float], float] = lambda x: 0, function_set: Dict = {}) -> None:
        pass

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass



class SoundAtmos:

    sound_distance: float
    """声源距离 方块"""

    sound_azimuth: Tuple[float, float]
    """声源方位 角度"""

    def __init__(
        self,
        distance: Optional[float] = None,
        azimuth: Optional[Tuple[float, float]] = None,
    ) -> None:

        self.sound_azimuth = (azimuth[0] % 360, azimuth[1] % 360) if azimuth else (0, 0)
        """声源方位"""

        # 如果指定为零，那么为零，但如果不指定或者指定为负数，则为 0.01 的距离
        self.sound_distance = (
            (16 if distance > 16 else (distance if distance >= 0 else 0.01))
            if distance is not None
            else 0.01
        )
        """声源距离"""

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
        """声像位移"""
        dk1 = self.sound_distance * round(cos(radians(self.sound_azimuth[1])), 8)
        return (
            -dk1 * round(sin(radians(self.sound_azimuth[0])), 8),
            self.sound_distance * round(sin(radians(self.sound_azimuth[1])), 8),
            dk1 * round(cos(radians(self.sound_azimuth[0])), 8),
        )


@dataclass(init=False)
class SingleNote:
    """存储单个音符的类"""

    note_pitch: int
    """midi音高"""

    velocity: int
    """力度"""

    start_tick: int
    """开始之时 命令刻"""

    duration: int
    """音符持续时间 命令刻"""

    high_precision_time: int
    """高精度开始时间偏量 1/1250 秒"""

    extra_info: Dict[str, Any]
    """你觉得放什么好？"""

    def __init__(
        self,
        midi_pitch: Optional[int],
        midi_velocity: int,
        start_time: int,
        last_time: int,
        mass_precision_time: int = 0,
        extra_information: Dict[str, Any] = {},
    ):
        """
        用于存储单个音符的类

        Parameters
        ------------
        midi_pitch: int
            midi音高
        midi_velocity: int
            midi响度(力度)
        start_time: int
            开始之时(命令刻)
            注：此处的时间是用从乐曲开始到当前的刻数
        last_time: int
            音符延续时间(命令刻)
        mass_precision_time: int
            高精度的开始时间偏移量(1/1250秒)
        is_percussion: bool
            是否作为打击乐器
        distance: float
            发声源距离玩家的距离（半径 `r`）
            注：距离越近，音量越高，默认为 0。此参数可以与音量成某种函数关系。
        azimuth: tuple[float, float]
            声源方位
            注：此参数为tuple，包含两个元素，分别表示：
            `rV`  发声源在竖直（上下）轴上，从玩家视角正前方开始，向顺时针旋转的角度
            `rH`  发声源在水平（左右）轴上，从玩家视角正前方开始，向上（到达玩家正上方顶点后变为向下，以此类推的旋转）旋转的角度
        extra_information: Dict[str, Any]
            附加信息，尽量存储为字典

        Returns
        ---------
        MineNote 类
        """

        self.note_pitch: int = 66 if midi_pitch is None else midi_pitch
        """midi音高"""
        self.velocity: int = midi_velocity
        """响度(力度)"""
        self.start_tick: int = start_time
        """开始之时 命令刻"""
        self.duration: int = last_time
        """音符持续时间 命令刻"""
        self.high_precision_time: int = mass_precision_time
        """高精度开始时间偏量 0.4 毫秒"""

        self.extra_info = extra_information if extra_information else {}

    @classmethod
    def decode(cls, code_buffer: bytes, is_high_time_precision: bool = True):
        """自字节码析出 SingleNote 类"""
        duration_ = (
            group_1 := int.from_bytes(code_buffer[:6], "big")
        ) & 0b11111111111111111
        start_tick_ = (group_1 := group_1 >> 17) & 0b11111111111111111
        note_velocity_ = (group_1 := group_1 >> 17) & 0b1111111
        note_pitch_ = (group_1 := group_1 >> 7) & 0b1111111

        try:
            return cls(
                midi_pitch=note_pitch_,
                midi_velocity=note_velocity_,
                start_time=start_tick_,
                last_time=duration_,
                mass_precision_time=code_buffer[6] if is_high_time_precision else 0,
            )
        except:
            print(
                "[Error] 单音符解析错误，字节码`{}`，{}启用高精度时间偏移\n".format(
                    code_buffer, "已" if is_high_time_precision else "未"
                )
            )
            raise

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
        # velocity 长度 7 位 支持到 127
        # start_tick 17 位 支持到 131071 即 109.22583 分钟 合 1.8204305 小时
        # duration 17 位 支持到 131071 即 109.22583 分钟 合 1.8204305 小时
        # 共 48 位 合 6 字节

        # high_time_precision（可选）长度 8 位 支持到 255 合 1 字节 支持 1/1250 秒]

        return (
            (
                (
                    ((((self.note_pitch << 7) + self.velocity) << 17) + self.start_tick)
                    << 17
                )
                + self.duration
            ).to_bytes(6, "big")
            # + self.track_no.to_bytes(1, "big")
            + (
                self.high_precision_time.to_bytes(1, "big")
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
            raise TypeError("参数类型错误；键：`{}` 值：`{}`".format(key, value))

    def get_info(self, key: str, default: Any = None) -> Any:
        """获取附加信息"""
        return self.extra_info.get(key, default)

    def stringize(self, include_extra_data: bool = False) -> str:
        return "TrackedNote(Pitch = {}, Velocity = {}, StartTick = {}, Duration = {}, TimeOffset = {}".format(
            self.note_pitch,
            self.velocity,
            self.start_tick,
            self.duration,
            self.high_precision_time,
        ) + (
            ", ExtraData = {})".format(self.extra_info) if include_extra_data else ")"
        )

    # def __list__(self) -> List[int]:
    # 我不认为这个类应当被作为列表使用

    def __tuple__(
        self,
    ) -> Tuple[int, int, int, int, int]:
        return (
            self.note_pitch,
            self.velocity,
            self.start_tick,
            self.duration,
            self.high_precision_time,
        )

    def __dict__(self):
        return {
            "Pitch": self.note_pitch,
            "Velocity": self.velocity,
            "StartTick": self.start_tick,
            "Duration": self.duration,
            "TimeOffset": self.high_precision_time,
            "ExtraData": self.extra_info,
        }

    def __eq__(self, other) -> bool:
        """比较两个音符是否具有相同的属性，不计附加信息"""
        if not isinstance(other, self.__class__):
            return False
        return self.__tuple__() == other.__tuple__()

    def __lt__(self, other) -> bool:
        """比较自己是否在开始时间上早于另一个音符"""
        if self.start_tick == other.start_tick:
            return self.high_precision_time < other.high_precision_time
        else:
            return self.start_tick < other.start_tick

    def __gt__(self, other) -> bool:
        """比较自己是否在开始时间上晚于另一个音符"""
        if self.start_tick == other.start_tick:
            return self.high_precision_time > other.high_precision_time
        else:
            return self.start_tick > other.start_tick


class SingleTrack(list):
    """存储单个轨道的类"""

    track_name: str
    """轨道之名称"""

    track_instrument: str
    """乐器ID"""

    track_volume: float
    """该音轨的音量"""

    is_high_time_precision: bool
    """该音轨是否使用高精度时间"""

    is_percussive: bool
    """该音轨是否标记为打击乐器轨道"""

    sound_position: SoundAtmos
    """声像方位"""

    argument_curves: Dict[str, FittingFunctionType]
    """参数曲线"""

    extra_info: Dict[str, Any]
    """你觉得放什么好？"""

    def __init__(
        self,
        name: str = "未命名音轨",
        instrument: str = "",
        volume: float = 0,
        precise_time: bool = True,
        percussion: bool = False,
        sound_direction: SoundAtmos = SoundAtmos(),
        extra_information: Dict[str, Any] = {},
        *args: SingleNote,
    ):
        self.track_name = name
        """音轨名称"""

        self.track_instrument = instrument
        """乐器ID"""

        self.track_volume = volume
        """音量"""

        self.is_high_time_precision = precise_time
        """是否使用高精度时间"""

        self.is_percussive = percussion
        """是否为打击乐器"""

        self.sound_position = sound_direction
        """声像方位"""

        self.extra_info = extra_information if extra_information else {}

        super().__init__(*args)

    @property
    def note_amount(self) -> int:
        """音符数"""
        return len(self)

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
            raise TypeError("参数类型错误；键：`{}` 值：`{}`".format(key, value))

    def get_info(self, key: str, default: Any = None) -> Any:
        """获取附加信息"""
        return self.extra_info.get(key, default)


class SingleMusic:
    pass
