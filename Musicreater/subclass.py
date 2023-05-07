'''
存储许多非主要的相关类
'''


from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T")  # Declare type variable


@dataclass(init=False)
class SingleNote:
    instrument: int
    """乐器编号"""
    note: int
    """音符编号"""
    velocity: int
    """力度/响度"""
    startTime: int
    """开始之时 ms"""
    lastTime: int
    """音符持续时间 ms"""

    def __init__(
        self, instrument: int, pitch: int, velocity: int, startTime: int, lastTime: int
    ):
        """用于存储单个音符的类
        :param instrument 乐器编号
        :param pitch 音符编号
        :param velocity 力度/响度
        :param startTime 开始之时(ms)
            注：此处的时间是用从乐曲开始到当前的毫秒数
        :param lastTime 音符延续时间(ms)"""
        self.instrument: int = instrument
        """乐器编号"""
        self.note: int = pitch
        """音符编号"""
        self.velocity: int = velocity
        """力度/响度"""
        self.startTime: int = startTime
        """开始之时 ms"""
        self.lastTime: int = lastTime
        """音符持续时间 ms"""

    @property
    def inst(self):
        """乐器编号"""
        return self.instrument

    @inst.setter
    def inst(self, inst_):
        self.instrument = inst_

    @property
    def pitch(self):
        """音符编号"""
        return self.note

    def __str__(self):
        return (
            f"Note(inst = {self.inst}, pitch = {self.note}, velocity = {self.velocity}, "
            f"startTime = {self.startTime}, lastTime = {self.lastTime}, )"
        )

    def __tuple__(self):
        return self.inst, self.note, self.velocity, self.startTime, self.lastTime

    def __dict__(self):
        return {
            "inst": self.inst,
            "pitch": self.note,
            "velocity": self.velocity,
            "startTime": self.startTime,
            "lastTime": self.lastTime,
        }


class MethodList(list):
    """函数列表，列表中的所有元素均为函数"""

    def __init__(self, in_=()):
        """函数列表，列表中的所有元素均为函数"""
        super().__init__()
        self._T = [_x for _x in in_]

    def __getitem__(self, item) -> T:
        return self._T[item]

    def __len__(self) -> int:
        return self._T.__len__()
