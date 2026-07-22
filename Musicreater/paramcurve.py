# -*- coding: utf-8 -*-

"""
音·创 v3 内部数据使用的参数曲线
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


from math import ceil, inf
from dataclasses import dataclass
from typing import Optional, Any, List, Tuple, Callable
from enum import Enum
import bisect


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
    out_interp: Optional[Callable[[float], float]] = None

    # 贝塞尔模式
    in_tangent: Optional[Tuple[float, float]] = (
        None  # (dt, dv) ← 相对于自身（负 dt 表示左侧）
    )
    out_tangent: Optional[Tuple[float, float]] = (
        None  # (dt, dv) → 相对于自身（正 dt 表示右侧）
    )
    use_bezier: bool = False

    def copy(self) -> "Keyframe":
        return Keyframe(
            time=self.time,
            value=self.value,
            out_interp=self.out_interp,
            in_tangent=self.in_tangent,
            out_tangent=self.out_tangent,
            use_bezier=self.use_bezier,
        )


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
    支持值域限制：可设定参数值的上限与下限，所有输出及关键帧写入均受约束。
    """

    base_line: float = 0.0
    """基线/默认值"""

    base_interpolation_function: Callable[[float], float]
    """默认（未指定区间时的）关键帧插值模式"""

    boundary_behaviour: BoundaryBehaviour
    """边界行为，控制参数曲线在已定义的范围外的返回值"""

    value_min: Optional[float] = None
    """参数值下限（None 表示不限制）"""

    value_max: Optional[float] = None
    """参数值上限（None 表示不限制）"""

    _keys: List[Keyframe]
    """关键帧列表"""

    def __init__(
        self,
        base_value: float = 0.0,
        default_interpolation_function: Callable[
            [float], float
        ] = InterpolationMethod.linear,
        boundary_mode: BoundaryBehaviour = BoundaryBehaviour.CONSTANT,
        value_min: Optional[float] = None,
        value_max: Optional[float] = None,
    ):
        """
        初始化参数曲线。

        Parameters
        ----------
        base_value : float
            边界外默认值（当 boundary_mode 为 BoundaryBehaviour.CONSTANT 时使用）。
        default_interpolation_function : Callable
            新关键帧的默认 out_interp。
        boundary_mode : BoundaryBehaviour
            范围外行为：
            - BoundaryBehaviour.CONSTANT: 返回 base_value
            - BoundaryBehaviour.HOLD: 保持首/尾关键帧值
        value_min : Optional[float]
            参数值下限。None 表示无下限。
        value_max : Optional[float]
            参数值上限。None 表示无上限。

        Raises
        ------
        ValueError
            若 value_min 和 value_max 均非 None 且 value_min > value_max。
        """
        # 先设定值域，再设定 base_line（以便 base_line 受约束）
        self._set_value_range_internal(value_min, value_max)

        self.base_line = self._clamp_value(base_value)
        self.base_interpolation_function = default_interpolation_function
        self.boundary_behaviour = boundary_mode

        self._keys: List[Keyframe] = []

    # ──────────────────────────────────────────────
    #  值域限制 相关
    # ──────────────────────────────────────────────

    def _set_value_range_internal(
        self,
        value_min: Optional[float],
        value_max: Optional[float],
    ):
        """
        内部方法：设定值域并校验合法性。

        Raises
        ------
        ValueError
            若 value_min > value_max。
        """
        if value_min is not None and value_max is not None and value_min > value_max:
            raise ValueError(f"值域下限 ({value_min}) 不得大于上限 ({value_max})。")
        self.value_min = value_min
        self.value_max = value_max

    def _clamp_value(self, value: float) -> float:
        """
        将给定值限制在 [value_min, value_max] 范围内。
        仅在低频操作（add_key、update_key_value、set_value_range 等）中使用。
        高频路径 value_at() 使用内联版本。

        Parameters
        ----------
        value : float
            待限制的值。

        Returns
        -------
        float
            限制后的值。若对应边界为 None，则该方向不做限制。
        """
        if self.value_min is not None and value < self.value_min:
            return self.value_min
        if self.value_max is not None and value > self.value_max:
            return self.value_max
        return value

    def set_value_range(
        self,
        value_min: Optional[float] = None,
        value_max: Optional[float] = None,
        clamp_existing_keys: bool = True,
    ):
        """
        设置参数曲线的值域（最大/最小值限制）。

        Parameters
        ----------
        value_min : Optional[float]
            参数值下限。传入 None 表示取消下限限制。
        value_max : Optional[float]
            参数值上限。传入 None 表示取消上限限制。
        clamp_existing_keys : bool
            若为 True（默认），则立即将已有关键帧的值及 base_line
            限制到新的值域范围内。若为 False，则仅影响后续输出与新增关键帧。

        Raises
        ------
        ValueError
            若 value_min > value_max。

        Examples
        --------
        >>> curve = ParamCurve(base_value=0.5)
        >>> curve.add_key(0.0, 1.5)
        >>> curve.add_key(1.0, -0.3)
        >>> curve.set_value_range(0.0, 1.0)  # 限制到 [0, 1]
        >>> curve.value_at(0.0)
        1.0
        >>> curve.value_at(1.0)
        0.0
        """
        self._set_value_range_internal(value_min, value_max)

        if clamp_existing_keys:
            # 限制 base_line
            self.base_line = self._clamp_value(self.base_line)
            # 限制所有已有关键帧的值
            for i, key in enumerate(self._keys):
                clamped = self._clamp_value(key.value)
                if clamped != key.value:
                    self._keys[i] = Keyframe(
                        time=key.time,
                        value=clamped,
                        out_interp=key.out_interp,
                        in_tangent=key.in_tangent,
                        out_tangent=key.out_tangent,
                        use_bezier=key.use_bezier,
                    )

    def get_value_range(self) -> Tuple[Optional[float], Optional[float]]:
        """
        获取当前值域设定。

        Returns
        -------
        Tuple[Optional[float], Optional[float]]
            (value_min, value_max)，None 表示该方向无限制。
        """
        return (self.value_min, self.value_max)

    def clear_value_range(self, clamp_existing_keys: bool = False):
        """
        清除值域限制（恢复为无限制状态）。

        Parameters
        ----------
        clamp_existing_keys : bool
            通常为 False（清除限制无需 clamp）。保留此参数仅为接口对称。
        """
        self.value_min = None
        self.value_max = None

    # ──────────────────────────────────────────────
    #  原有功能
    # ──────────────────────────────────────────────

    def __bool__(self) -> bool:
        return bool(self._keys) or (self.base_line != 0)

    def find_key(self, time: float) -> Tuple[int, Optional[Keyframe]]:
        idx = bisect.bisect_left(self._keys, time, key=lambda k: k.time)
        if idx < len(self._keys) and self._keys[idx].time == time:
            return idx, self._keys[idx]
        else:
            # print("[警告] ParamCurve.find_key: 找不到指定时间点所对应之关键帧")
            return idx, None

    def copy(
        self,
        start: float = 0,
        end: float = inf,
        keep_zone_boundary_value: bool = False,
        global_boundary_safe: bool = True,
    ) -> "ParamCurve":
        """
        返回参数曲线在某时间段内的副本

        Parameters
        ----------
        start : float
            起始时间。
        end : float
            结束时间。
        keep_zone_boundary_value : bool
            是否保留边界值（即在副本中的当前选区之边界创建以当前曲线值作为值的关键帧）。
        global_boundary_safe : bool
            当保留边界值启用时，是否忽略本身就处于参数曲线边界外的值，使其不创建关键帧。

        Returns
        -------
        ParamCurve
            参数曲线之副本
        """
        param_curve = ParamCurve(
            self.base_line,
            self.base_interpolation_function,
            self.boundary_behaviour,
            value_min=self.value_min,
            value_max=self.value_max,
        )
        if start >= end:
            return param_curve
        start_index, starter_keyframe = self.find_key(start)
        end_index, ender_keyframe = self.find_key(end)
        if starter_keyframe and ender_keyframe:
            param_curve._keys = [
                key.copy() for key in self._keys[start_index : end_index + 1]
            ]
        elif starter_keyframe:
            if end_index >= len(self._keys) and global_boundary_safe:
                param_curve._keys = [key.copy() for key in self._keys[start_index:]]
            else:
                param_curve._keys = [
                    key.copy() for key in self._keys[start_index:end_index]
                ]
                if keep_zone_boundary_value:
                    param_curve.add_key(end, self.value_at(end))
        elif ender_keyframe:
            if start_index <= 0 and global_boundary_safe:
                param_curve._keys = [key.copy() for key in self._keys[:end_index]]
            else:
                param_curve._keys = [
                    key.copy() for key in self._keys[start_index : end_index + 1]
                ]
                if keep_zone_boundary_value:
                    param_curve.add_key(start, self.value_at(start))
        else:
            if (
                start_index <= 0
                and end_index >= len(self._keys)
                and global_boundary_safe
            ):
                param_curve._keys = [key.copy() for key in self._keys]
            else:
                param_curve._keys = [
                    key.copy() for key in self._keys[start_index:end_index]
                ]
                if keep_zone_boundary_value:
                    param_curve.add_key(start, self.value_at(start))
                    param_curve.add_key(end, self.value_at(end))
        return param_curve

    def delete(self, start: float, end: float):
        """
        删除参数曲线在某时间段内的关键帧
        """
        if start > end:
            return
        start_index, starter_keyframe = self.find_key(start)
        end_index, ender_keyframe = self.find_key(end)
        if ender_keyframe:
            del self._keys[start_index : end_index + 1]
        else:
            del self._keys[start_index:end_index]

    def add_key(
        self,
        time: float,
        value: float,
        out_interp: Optional[Callable[[float], float]] = None,
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
            参数值（将自动受值域限制约束）。
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
        写入的 value 会被自动 clamp 到 [value_min, value_max]。
        """
        interp = (
            out_interp if out_interp is not None else self.base_interpolation_function
        )
        clamped_value = self._clamp_value(value)
        new_key = Keyframe(
            time, clamped_value, interp, in_tangent, out_tangent, use_bezier
        )

        idx, old_key = self.find_key(time)
        if old_key:
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
        idx, key = self.find_key(time)
        if key:
            del self._keys[idx]

    def update_key_value(self, time: float, new_value: float):
        """更新关键帧值，保留其他属性。值受值域限制约束。"""
        idx, key = self.find_key(time)
        if key:
            clamped_value = self._clamp_value(new_value)
            self._keys[idx] = Keyframe(
                time,
                clamped_value,
                key.out_interp,
                key.in_tangent,
                key.out_tangent,
                key.use_bezier,
            )

    def update_key_interp(
        self,
        time: float,
        out_interp: Optional[Callable[[float], float]] = None,
        in_tangent: Optional[Tuple[float, float]] = None,
        out_tangent: Optional[Tuple[float, float]] = None,
        use_bezier: bool = False,
    ):
        """更新关键帧的插值属性。"""
        idx, key = self.find_key(time)
        if key:
            new_value = key.value
            interp = out_interp if out_interp is not None else key.out_interp
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
        idx, key = self.find_key(time)
        if key:
            self._keys[idx] = Keyframe(
                time,
                key.value,
                out_interp=key.out_interp,
                in_tangent=in_tangent,
                out_tangent=out_tangent,
                use_bezier=use_bezier,
            )

    def make_key_smooth(self, time: float):
        """
        将关键帧设为"平滑"模式（自动对称切线，并设为贝塞尔模式）。
        切线长度基于相邻关键帧的时间和值差。
        """
        idx, key = self.find_key(time)
        if key:
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
                dt_out = (key.time - prev_k.time) / 2.0
                dv_out = (key.value - prev_k.value) / 2.0
                dt_in = dt_out
                dv_in = dv_out
            elif next_k:
                dt_in = (next_k.time - key.time) / 2.0
                dv_in = (next_k.value - key.value) / 2.0
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

        返回值始终受 [value_min, value_max] 值域限制约束。
        即使贝塞尔插值产生过冲（overshoot），输出也会被 clamp。

        Parameters
        ----------
        t : float
            查询时间。

        Returns
        -------
        float
            插值结果（已 clamp）。
        """
        keys = self._keys
        if not keys:
            raw = self._get_boundary_value(t)
        else:
            if t < keys[0].time or t > keys[-1].time:
                raw = self._get_boundary_value(t)
            else:
                times = [k.time for k in keys]
                idx = bisect.bisect_right(times, t) - 1

                if idx < 0:
                    raw = self._get_boundary_value(t)
                elif idx >= len(keys) - 1:
                    raw = keys[-1].value
                else:

                    k0 = keys[idx]
                    k1 = keys[idx + 1]

                    if k0.time == k1.time:
                        raw = k0.value
                    elif k0.time == t:
                        raw = k0.value
                    elif k1.time == t:
                        raw = k1.value
                    else:
                        t0, v0 = k0.time, k0.value
                        t1, v1 = k1.time, k1.value
                        u = (t - t0) / (t1 - t0)
                        u = max(0.0, min(1.0, u))

                        # 贝塞尔模式（高优先级）
                        if k0.use_bezier or k1.use_bezier:
                            raw = _evaluate_bezier_segment(
                                t0,
                                v0,
                                t1,
                                v1,
                                out_tangent=k0.out_tangent,
                                in_tangent=k1.in_tangent,
                                u=u,
                            )
                        # 函数插值模式，优先处理阶梯保持模式
                        elif k0.out_interp is InterpolationMethod.hold:
                            raw = v0
                        else:
                            interp_func = (
                                k0.out_interp or self.base_interpolation_function
                            )
                            v_norm = interp_func(u)
                            raw = v0 + v_norm * (v1 - v0)

        return self._clamp_value(raw)

    def __call__(self, t: float) -> float:
        return self.value_at(t)

    def get_all_keys(self) -> List[Tuple[float, float]]:
        """返回 (time, value) 列表。"""
        return [(k.time, k.value) for k in self._keys]

    def set_default_interpolation_function(self, interp_func: Callable[[float], float]):
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
            当 mode=BoundaryBehaviour.CONSTANT 时，指定新的默认值（受值域约束）。
        """
        self.boundary_behaviour = mode
        if base_value is not None:
            self.base_line = self._clamp_value(base_value)

    def bake(
        self,
        start: float,
        end: float,
        sample_rate: Optional[float] = None,
        num_samples: Optional[int] = None,
        dtype: Any = None,
    ) -> "np.ndarray":  # type: ignore
        """
        将参数曲线在指定时间范围内烘焙为 NumPy 数组。

        当值域限制已启用时，使用 np.clip 进行向量化 clamp，
        避免逐样本调用 Python 层的 clamp 逻辑。
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

        # 向量化 clamp —— 比逐点 Python 调用快一个数量级
        vmin, vmax = self.value_min, self.value_max
        if vmin is not None or vmax is not None:
            np.clip(values, vmin, vmax, out=values)

        return values
