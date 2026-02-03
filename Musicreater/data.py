# -*- coding: utf-8 -*-

"""
存储 音·创 v3 的内部数据类
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
)
from enum import Enum

from .exceptions import SingleNoteDecodeError, ParameterTypeError, ParameterValueError
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
            注：距离越近，音量越高，默认为 0。此参数可以与音量成某种函数关系。
        azimuth: tuple[float, float]
            声源方位
            注：此参数为tuple，包含两个元素，分别表示：
            `rV`  发声源在竖直（上下）轴上，从玩家视角正前方开始，向顺时针旋转的角度
            `rH`  发声源在水平（左右）轴上，从玩家视角正前方开始，向上（到达玩家正上方顶点后变为向下，以此类推的旋转）旋转的角度
        """

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
        """声像位移，直接可应用于我的世界的相对视角的坐标参考系中（^x ^y ^z）"""
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

    start_time: int
    """开始之时 命令刻"""

    duration: int
    """音符持续时间 命令刻"""

    high_precision_start_time: int
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
        self.start_time: int = start_time
        """开始之时 命令刻"""
        self.duration: int = last_time
        """音符持续时间 命令刻"""
        self.high_precision_start_time: int = mass_precision_time
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
                e,
                "技术信息：\nGROUP1\t`{}`\nCODE_BUFFER\t`{}`".format(
                    group_1, code_buffer
                ),
            )

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
                    ((((self.note_pitch << 7) + self.velocity) << 17) + self.start_time)
                    << 17
                )
                + self.duration
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
        return "TrackedNote(Pitch = {}, Velocity = {}, StartTick = {}, Duration = {}, TimeOffset = {}".format(
            self.note_pitch,
            self.velocity,
            self.start_time,
            self.duration,
            self.high_precision_start_time,
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
            self.start_time,
            self.duration,
            self.high_precision_start_time,
        )

    def __dict__(self):
        return {
            "Pitch": self.note_pitch,
            "Velocity": self.velocity,
            "StartTick": self.start_time,
            "Duration": self.duration,
            "TimeOffset": self.high_precision_start_time,
            "ExtraData": self.extra_info,
        }

    def __eq__(self, other) -> bool:
        """比较两个音符是否具有相同的属性，不计附加信息"""
        if not isinstance(other, self.__class__):
            return False
        return self.__tuple__() == other.__tuple__()

    def __lt__(self, other) -> bool:
        """比较自己是否在开始时间上早于另一个音符"""
        if self.start_time == other.start_tick:
            return self.high_precision_start_time < other.high_precision_time
        else:
            return self.start_time < other.start_tick

    def __gt__(self, other) -> bool:
        """比较自己是否在开始时间上晚于另一个音符"""
        if self.start_time == other.start_tick:
            return self.high_precision_start_time > other.high_precision_time
        else:
            return self.start_time > other.start_tick


class CurvableParam(str, Enum):
    """可曲线化的参数枚举类"""

    PITCH = "adjust_note_pitch"
    VELOCITY = "adjust_note_velocity"
    VOLUME = "adjust_note_volume"
    DISTANCE = "adjust_note_sound_distance"
    LR_PANNING = "adjust_note_leftright_panning_degree"
    UD_PANNING = "adjust_note_updown_panning_degree"


@dataclass
class MineNote:
    """我的世界音符对象（仅提供我的世界相关接口）"""

    pitch: float
    """midi音高"""
    instrument: str
    """乐器ID"""
    velocity: float
    """力度"""
    volume: float
    """音量"""
    start_tick: int
    """开始之时 命令刻"""
    duration_tick: int
    """音符持续时间 命令刻"""
    persiced_time: int
    """高精度开始时间偏量 1/1250 秒"""
    percussive: bool
    """是否作为打击乐器启用"""
    position: SoundAtmos
    """声像方位"""

    @classmethod
    def from_single_note(
        cls,
        note: SingleNote,
        note_instrument: str,
        sound_volume: float,
        is_persiced_time: bool,
        is_percussive_note: bool,
        sound_position: SoundAtmos,
        adjust_note_pitch: float = 0.0,
        adjust_note_velocity: float = 0.0,
        adjust_note_volume: float = 0.0,
        adjust_note_sound_distance: float = 0.0,
        adjust_note_leftright_panning_degree: float = 0.0,
        adjust_note_updown_panning_degree: float = 0.0,
    ) -> "MineNote":
        """从SingleNote对象创建MineNote对象"""
        sound_position.sound_distance += adjust_note_sound_distance
        sound_position.sound_azimuth = (
            sound_position.sound_azimuth[0] + adjust_note_leftright_panning_degree,
            sound_position.sound_azimuth[1] + adjust_note_updown_panning_degree,
        )
        return cls(
            pitch=note.note_pitch + adjust_note_pitch,
            instrument=note_instrument,
            velocity=note.velocity + adjust_note_velocity,
            volume=sound_volume + adjust_note_volume,
            start_tick=note.start_time,
            duration_tick=note.duration,
            persiced_time=note.high_precision_start_time if is_persiced_time else 0,
            percussive=is_percussive_note,
            position=sound_position,
        )


class SingleTrack(List[SingleNote]):
    """存储单个轨道的类"""

    track_name: str
    """轨道之名称"""

    is_enabled: bool = True
    """该音轨是否启用"""

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

    argument_curves: Dict[CurvableParam, Union[ParamCurve, Literal[None]]]
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

        self.argument_curves = {
            CurvableParam.PITCH: None,
            CurvableParam.VELOCITY: None,
            CurvableParam.VOLUME: None,
            CurvableParam.DISTANCE: None,
            CurvableParam.LR_PANNING: None,
            CurvableParam.UD_PANNING: None,
        }

        super().__init__(*args)
        super().sort()

    def disable(self) -> None:
        """禁用音轨"""

        self.is_enabled = False

    def enable(self) -> None:
        """启用音轨"""

        self.is_enabled = True

    def toggle_able(self) -> None:
        """切换音轨的启用状态"""

        self.is_enabled = not self.is_enabled

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

    def get(self, time: int) -> Generator[SingleNote, None, None]:
        """通过开始时间来获取音符"""

        return (x for x in self if x.start_time == time)

    def get_notes(
        self, start_time: float, end_time: float = inf
    ) -> Generator[SingleNote, None, None]:
        """通过开始时间和结束时间来获取音符"""
        if end_time < start_time:
            raise ParameterValueError(
                "获取音符的时间范围有误，终止时间`{}`早于起始时间`{}`".format(
                    end_time, start_time
                )
            )
        elif start_time < 0 or end_time < 0:
            raise ParameterValueError(
                "获取音符的时间范围有误，终止时间`{}`和起始时间`{}`皆不可为负数".format(
                    end_time, start_time
                )
            )
        return (
            x
            for x in self
            if (x.start_time >= start_time) and (x.start_time <= end_time)
        )

    def get_minenotes(
        self, range_start_time: float = 0, range_end_time: float = inf
    ) -> Generator[MineNote, Any, None]:
        """获取能够用以在我的世界播放的音符数据类"""

        for _note in self.get_notes(range_start_time, range_end_time):
            yield MineNote.from_single_note(
                note=_note,
                note_instrument=self.track_instrument,
                sound_volume=self.track_volume,
                is_persiced_time=self.is_high_time_precision,
                is_percussive_note=self.is_percussive,
                sound_position=self.sound_position,
                **{
                    item.value: self.argument_curves[item].value_at(_note.start_time)  # type: ignore
                    for item in CurvableParam
                    if self.argument_curves[item]
                },
            )

    @property
    def note_amount(self) -> int:
        """音符数"""
        return len(self)

    @property
    def track_notes(self) -> List[SingleNote]:
        """音符列表"""
        return self

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

    # 感叹一下什么交冗余设计啊！（叉腰）
    extra_info: Dict[str, Any]
    """这还得放东西？"""

    def __init__(
        self,
        name: str = "未命名乐曲",
        creator: str = "未命名制作者",
        original_author: str = "未命名原作者",
        description: str = "未命名简介",
        credits: str = "未命名版权信息",
        *args: SingleTrack,
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

    @property
    def track_amount(self) -> int:
        """音轨数"""
        return len(self)

    @property
    def music_tracks(self) -> Iterator[SingleTrack]:
        """音轨列表，不包含被禁用的音轨"""
        return (track for track in self if track.is_enabled)

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
            return heapq.merge(*tracks, key=sort_key)
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
        self, start_time: float, end_time: float = inf
    ) -> Generator[Iterator[SingleNote], Any, None]:
        """获取指定时间段的各个音轨的音符数据"""
        return (track.get_notes(start_time, end_time) for track in self.music_tracks)

    def get_tracked_minenotes(
        self, start_time: float, end_time: float = inf
    ) -> Generator[Iterator[MineNote], Any, None]:
        """获取指定时间段的各个音轨的，供我的世界播放的音符数据类"""
        return (
            track.get_minenotes(start_time, end_time) for track in self.music_tracks
        )

    def get_notes(
        self, start_time: float, end_time: float = inf
    ) -> Iterator[SingleNote]:
        """获取指定时间段的所有音符数据，按照时间顺序"""
        if self.track_amount == 0:
            return iter(())
        return self.yield_from_tracks(
            [track.get_notes(start_time, end_time) for track in self.music_tracks],
            sort_key=lambda x: x.start_time,
        )

    def get_minenotes(
        self, start_time: float, end_time: float = inf
    ) -> Generator[MineNote, Any, None]:
        """获取指定时间段所有的，供我的世界播放的音符数据类，按照时间顺序"""
        if self.track_amount == 0:
            return
        yield from self.yield_from_tracks(
            [track.get_minenotes(start_time, end_time) for track in self.music_tracks],
            sort_key=lambda x: x.start_tick,
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
