# -*- coding: utf-8 -*-

"""
存储 音·创 v3 内部数据使用的参数曲线
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


# WARNING 本文件所含之功能未经完整测试
# 鉴于白谭若佬给出的建议：本功能应是处于低优先级开发的
# 因此暂时用处不大，可以稍微放一会再进行开发
# 目前用人工智能生成了部分代码，只经过简单的测试
# 可以等伶伦工作站开发出来后再进行完整的测试


from math import ceil
from dataclasses import dataclass
from typing import Optional, Any, List, Tuple
from enum import Enum
import bisect

from .types import FittingFunctionType


def _evaluate_bezier_segment(
    t0: float,
    v0: float,
    t1: float,
    v1: float,
    out_tangent: Optional[Tuple[float, float]],
    in_tangent: Optional[Tuple[float, float]],
    u: float,
) -> float:
    """
    计算贝塞尔区间 [t0, t1] 在归一化参数 u ∈ [0,1] 处的 y 值。

    控制点：
      P0 = (t0, v0)
      P1 = (t0 + out_dt, v0 + out_dv)
      P2 = (t1 - in_dt, v1 - in_dv)   ← 注意：in_tangent 是相对于 t1 的偏移
      P3 = (t1, v1)
    """
    # 默认控制点：退化为线性
    p0 = (t0, v0)
    p3 = (t1, v1)

    if out_tangent is not None:
        p1 = (t0 + out_tangent[0], v0 + out_tangent[1])
    else:
        p1 = p0  # 无出手柄 → 与起点重合

    if in_tangent is not None:
        p2 = (t1 - in_tangent[0], v1 - in_tangent[1])
    else:
        p2 = p3  # 无入手柄 → 与终点重合

    # 三次贝塞尔 y(t)
    mt = 1.0 - u
    return mt**3 * p0[1] + 3 * mt**2 * u * p1[1] + 3 * mt * u**2 * p2[1] + u**3 * p3[1]


class InterpolationMethod:
    """
    预定义的标准化插值函数集合。所有函数接受归一化输入 u ∈ [0,1]，返回 v ∈ [0,1]。
    """

    @staticmethod
    def linear(u: float) -> float:
        """
        线性插值。

        Parameters
        ----------
        u : float
            归一化时间，范围 [0, 1]。

        Returns
        -------
        float
            插值权重，范围 [0, 1]。
        """
        return u

    @staticmethod
    def ease_in_quad(u: float) -> float:
        """
        二次缓入（慢进快出）。

        Parameters
        ----------
        u : float
            归一化时间，范围 [0, 1]。

        Returns
        -------
        float
            插值权重。
        """
        return u * u

    @staticmethod
    def ease_out_quad(u: float) -> float:
        """
        二次缓出（快进慢出）。

        Parameters
        ----------
        u : float
            归一化时间，范围 [0, 1]。

        Returns
        -------
        float
            插值权重。
        """
        return 1 - (1 - u) ** 2

    @staticmethod
    def ease_in_out_quad(u: float) -> float:
        """
        二次缓入缓出。

        Parameters
        ----------
        u : float
            归一化时间，范围 [0, 1]。

        Returns
        -------
        float
            插值权重。
        """
        if u < 0.5:
            return 2 * u * u
        else:
            return 1 - pow(-2 * u + 2, 2) / 2

    @staticmethod
    def hold(u: float) -> float:
        """
        阶梯保持模式占位函数。实际插值逻辑在 ParamCurve.value_at 中特殊处理。

        Parameters
        ----------
        u : float
            归一化时间（忽略）。

        Returns
        -------
        float
            无意义，仅作标识。
        """
        return 0.0


@dataclass
class Keyframe:
    """
    参数曲线上的一个关键帧，支持完整的入/出切线控制。

    插值优先级：
    1. 若 use_bezier=True → 使用贝塞尔模式（需 in_tangent / out_tangent）
    2. 否则 → 使用 out_interp 函数（in_interp 被忽略）
    """

    time: float
    value: float

    # 函数插值模式
    out_interp: Optional[FittingFunctionType] = None

    # 贝塞尔模式
    in_tangent: Optional[Tuple[float, float]] = (
        None  # (dt, dv) ← 相对于自身（负 dt 表示左侧）
    )
    out_tangent: Optional[Tuple[float, float]] = (
        None  # (dt, dv) → 相对于自身（正 dt 表示右侧）
    )
    use_bezier: bool = False


class BoundaryBehaviour(str, Enum):
    """
    边界行为枚举。
    """

    CONSTANT = "constant"
    """返回默认基线值"""
    HOLD = "hold"
    """保持首/尾关键帧的值"""


class ParamCurve:
    """
    参数曲线类
    """

    """
    支持动态节点编辑
    用户通过添加/修改关键帧（时间-值对）来定义曲线，类自动在相邻关键帧之间生成插值段。
    支持多种插值模式：线性（'linear'）、平滑缓动（'smooth'）、保持（'hold'）或自定义函数。
    """

    base_line: float = 0.0
    """基线/默认值"""

    base_interpolation_function: FittingFunctionType
    """默认（未指定区间时的）关键帧插值模式"""

    boundary_behaviour: BoundaryBehaviour
    """边界行为，控制参数曲线在已定义的范围外的返回值"""

    _keys: List[Keyframe]
    """关键帧列表"""

    def __init__(
        self,
        base_value: float = 0.0,
        default_interpolation_function: FittingFunctionType = InterpolationMethod.linear,
        boundary_mode: BoundaryBehaviour = BoundaryBehaviour.CONSTANT,
    ):
        """
        初始化参数曲线。

        Parameters
        ----------
        base_value : float
            边界外默认值（当 boundary_mode 为 BoundaryBehaviour.CONSTANT 时使用）。
        default_interpolation_function : FittingFunctionType
            新关键帧的默认 out_interp。
        boundary_mode : BoundaryBehaviour
            范围外行为：
            - BoundaryBehaviour.CONSTANT: 返回 base_value
            - BoundaryBehaviour.HOLD: 保持首/尾关键帧值
        """
        self.base_line = base_value
        self.base_interpolation_function = default_interpolation_function
        self.boundary_behaviour = boundary_mode

        self._keys: List[Keyframe] = []

    def __bool__(self) -> bool:
        return bool(self._keys) or (self.base_line != 0)

    def add_key(
        self,
        time: float,
        value: float,
        out_interp: Optional[FittingFunctionType] = None,
        in_tangent: Optional[Tuple[float, float]] = None,
        out_tangent: Optional[Tuple[float, float]] = None,
        use_bezier: bool = False,
    ):
        """
        添加或更新关键帧。

        Parameters
        ----------
        time : float
            关键帧时间。
        value : float
            参数值。
        out_interp : Optional[Callable]
            出插值函数（若 use_bezier=False）。
        in_tangent : Optional[Tuple[float, float]]
            入切线偏移 (dt, dv)。dt 通常为负（表示左侧），但存储为绝对偏移。
        out_tangent : Optional[Tuple[float, float]]
            出切线偏移 (dt, dv)。dt 通常为正。
        use_bezier : bool
            是否使用贝塞尔插值。

        Returns
        -------
        None

        Notes
        -----
        若时间已存在，更新该关键帧的所有属性。
        """
        interp = (
            out_interp if out_interp is not None else self.base_interpolation_function
        )
        new_key = Keyframe(time, value, interp, in_tangent, out_tangent, use_bezier)

        idx = bisect.bisect_left(self._keys, time, key=lambda k: k.time)
        if idx < len(self._keys) and self._keys[idx].time == time:
            self._keys[idx] = new_key
        else:
            self._keys.insert(idx, new_key)

    def remove_key(self, time: float):
        """
        移除指定时间的关键帧。

        Parameters
        ----------
        time : float
            要移除的关键帧时间。

        Returns
        -------
        None
        """
        idx = bisect.bisect_left(self._keys, time, key=lambda k: k.time)
        if idx < len(self._keys) and self._keys[idx].time == time:
            del self._keys[idx]

    def update_key_value(self, time: float, new_value: float):
        """更新关键帧值，保留其他属性。"""
        idx = bisect.bisect_left(self._keys, time, key=lambda k: k.time)
        if idx < len(self._keys) and self._keys[idx].time == time:
            k = self._keys[idx]
            self._keys[idx] = Keyframe(
                time, new_value, k.out_interp, k.in_tangent, k.out_tangent, k.use_bezier
            )

    def update_key_interp(
        self,
        time: float,
        out_interp: Optional[FittingFunctionType] = None,
        in_tangent: Optional[Tuple[float, float]] = None,
        out_tangent: Optional[Tuple[float, float]] = None,
        use_bezier: bool = False,
    ):
        """更新关键帧的插值属性。"""
        idx = bisect.bisect_left(self._keys, time, key=lambda k: k.time)
        if idx < len(self._keys) and self._keys[idx].time == time:
            k = self._keys[idx]
            new_value = k.value
            interp = out_interp if out_interp is not None else k.out_interp
            self._keys[idx] = Keyframe(
                time, new_value, interp, in_tangent, out_tangent, use_bezier
            )

    def set_key_tangents(
        self,
        time: float,
        in_tangent: Optional[Tuple[float, float]] = None,
        out_tangent: Optional[Tuple[float, float]] = None,
        use_bezier: bool = True,
    ):
        """单独设置关键帧的切线，不改变值。"""
        idx = bisect.bisect_left(self._keys, time, key=lambda k: k.time)
        if idx < len(self._keys) and self._keys[idx].time == time:
            k = self._keys[idx]
            self._keys[idx] = Keyframe(
                time,
                k.value,
                out_interp=k.out_interp,
                in_tangent=in_tangent,
                out_tangent=out_tangent,
                use_bezier=use_bezier,
            )

    def make_key_smooth(self, time: float):
        """
        将关键帧设为“平滑”模式（自动对称切线，并设为贝塞尔模式）。
        切线长度基于相邻关键帧的时间和值差。
        """
        idx = bisect.bisect_left(self._keys, time, key=lambda k: k.time)
        if idx < len(self._keys) and self._keys[idx].time == time:
            k = self._keys[idx]
            prev_k = self._keys[idx - 1] if idx > 0 else None
            next_k = self._keys[idx + 1] if idx + 1 < len(self._keys) else None

            # 默认切线长度：时间差的 1/3，值差按比例
            dt_in = dt_out = 0.1
            dv_in = dv_out = 0.0

            if prev_k and next_k:
                dt_total = next_k.time - prev_k.time
                dv_total = next_k.value - prev_k.value
                dt_in = dt_out = dt_total / 3.0
                dv_in = dv_out = dv_total / 3.0
            elif prev_k:
                dt_out = (k.time - prev_k.time) / 2.0
                dv_out = (k.value - prev_k.value) / 2.0
                dt_in = dt_out
                dv_in = dv_out
            elif next_k:
                dt_in = (next_k.time - k.time) / 2.0
                dv_in = (next_k.value - k.value) / 2.0
                dt_out = dt_in
                dv_out = dv_in

            self.set_key_tangents(
                time,
                in_tangent=(-dt_in, -dv_in),  # in_tangent 存储为偏移，使用时做减法
                out_tangent=(dt_out, dv_out),
                use_bezier=True,
            )

    def _get_boundary_value(self, t: float) -> float:
        """根据 boundary_mode 获取范围外的值。"""
        if not self._keys:
            return self.base_line
        if self.boundary_behaviour == BoundaryBehaviour.CONSTANT:
            return self.base_line
        elif self.boundary_behaviour == BoundaryBehaviour.HOLD:
            if t < self._keys[0].time:
                return self._keys[0].value
            else:
                return self._keys[-1].value
        else:  # 可能会有别的模式吗？
            return self.base_line

    def value_at(self, t: float) -> float:
        """
        计算时间 t 处的曲线值。

        Parameters
        ----------
        t : float
            查询时间。

        Returns
        -------
        float
            插值结果。
        """
        keys = self._keys
        if not keys:
            return self._get_boundary_value(t)

        if t < keys[0].time or t > keys[-1].time:
            return self._get_boundary_value(t)

        times = [k.time for k in keys]
        idx = bisect.bisect_right(times, t) - 1

        if idx < 0:
            return self._get_boundary_value(t)
        if idx >= len(keys) - 1:
            return keys[-1].value

        k0 = keys[idx]
        k1 = keys[idx + 1]

        if k0.time == k1.time:
            return k0.value
        if k0.time == t:
            return k0.value
        if k1.time == t:
            return k1.value

        t0, v0 = k0.time, k0.value
        t1, v1 = k1.time, k1.value
        u = (t - t0) / (t1 - t0)
        u = max(0.0, min(1.0, u))

        # 贝塞尔模式（高优先级）
        if k0.use_bezier or k1.use_bezier:
            return _evaluate_bezier_segment(
                t0,
                v0,
                t1,
                v1,
                out_tangent=k0.out_tangent,
                in_tangent=k1.in_tangent,  # ← 关键：使用下一帧的 in_tangent！
                u=u,
            )

        # 函数插值模式，优先处理阶梯保持模式
        elif k0.out_interp is InterpolationMethod.hold:
            return v0

        interp_func = k0.out_interp or self.base_interpolation_function
        v_norm = interp_func(u)
        return v0 + v_norm * (v1 - v0)

    def __call__(self, t: float) -> float:
        return self.value_at(t)

    def get_all_keys(self) -> List[Tuple[float, float]]:
        """返回 (time, value) 列表。"""
        return [(k.time, k.value) for k in self._keys]

    def set_default_interpolation_function(self, interp_func: FittingFunctionType):
        """设置默认插值函数。"""
        self.base_interpolation_function = interp_func

    def set_boundary_mode(
        self, mode: BoundaryBehaviour, base_value: Optional[float] = None
    ):
        """
        设置边界行为。

        Parameters
        ----------
        mode : BoundaryBehaviour
            边界行为设定
        base_value : Optional[float]
            当 mode=BoundaryBehaviour.CONSTANT 时，指定新的默认值。
        """
        self.boundary_behaviour = mode
        if base_value is not None:
            self.base_line = base_value

    def bake(
        self,
        start: float,
        end: float,
        sample_rate: Optional[float] = None,
        num_samples: Optional[int] = None,
        dtype: Any = None,
    ) -> "np.ndarray":  # type: ignore 这里这样用会报错吗？不知道，但是人工智能这样写了都，大抵是能用的吧
        """
        将参数曲线在指定时间范围内烘焙为 NumPy 数组，用于高性能实时查询或音频渲染。

        Parameters
        ----------
        start : float
            烘焙起始时间（包含）。
        end : float
            烘焙结束时间（不包含）。
        sample_rate : Optional[float]
            采样率（单位：样本/时间单位）。例如，若时间单位为秒，sample_rate=48000 表示每秒 48k 样本。
            必须与 `num_samples` 二选一提供。
        num_samples : Optional[int]
            输出数组的总样本数。若提供，则忽略 `sample_rate`。
        dtype : Any, optional
            输出数组的数据类型（如 np.float32）。默认为 np.float64。

        Returns
        -------
        np.ndarray
            一维 NumPy 数组，长度为 `num_samples`，`arr[i] ≈ curve(start + i / sample_rate)`。

        Exceptions
        ----------
        ValueError
            - 若 `start >= end`
            - 若未提供 `sample_rate` 且未提供 `num_samples`
            - 若 `num_samples <= 0`

        Notes
        -----
        - 内部使用 `np.linspace` 生成时间轴，然后逐点调用 `self.value_at(t)`。
        - 虽然目前是 Python 循环，但对于典型自动化曲线（<1000 关键帧），NumPy 向量化优势主要体现在内存布局和后续处理。
        - 如需极致性能（如 >1M 样本），可未来优化为 C++/Numba 加速，但当前已满足 DAW 自动化需求。
        """
        if start >= end:
            raise ValueError("起始值须小于结束值。")

        if num_samples is not None:
            if num_samples <= 0:
                raise ValueError("烘焙的采样数须为非零自然数。")
            n = num_samples
        elif sample_rate is not None:
            if sample_rate <= 0:
                raise ValueError("烘焙的采样率须为正值。")
            duration = end - start
            n = int(ceil(duration * sample_rate))
            # 别因为小数数值会产生的问题而越界了来着
            if n == 0:
                n = 1
        else:
            raise ValueError("烘焙参数时，须提供采样率或采样数。")

        import numpy as np

        # 生成对应时间的节点：[start, ..., end - dt]
        times = np.linspace(start, end, n, endpoint=False)

        # 计算每个时间节点上的参数值
        # 我们认为在数字音频工作站的环境里，此值可能最多到 ~1e6 的样子，因此这样 for 一下应当可以接受
        # WARNING: 人工智能是这样理解的，如果有问题的话后续可能需要更改
        values = np.empty(n, dtype=dtype or np.float64)
        for i in range(n):
            values[i] = self.value_at(float(times[i]))

        return values
