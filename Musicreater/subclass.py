# -*- coding: utf-8 -*-

"""
存储许多非主要的相关类
"""

"""
版权所有 © 2023 音·创 开发者
Copyright © 2023 all the developers of Musicreater

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿穆组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md


from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T")  # Declare type variable


@dataclass(init=False)
class SingleNote:
    """存储单个音符的类"""

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


@dataclass(init=False)
class SingleCommand:
    """存储单个指令的类"""

    command_text: str
    """指令文本"""

    conditional: bool
    """执行是否有条件"""

    delay: int
    """执行的延迟"""

    annotation_text: str
    """指令注释"""

    def __init__(
        self,
        command: str,
        condition: bool = False,
        tick_delay: int = 0,
        annotation: str = "",
    ):
        """
        存储单个指令的类

        Parameters
        ----------
        command: str
            指令
        condition: bool
            是否有条件
        tick_delay: int
            执行延时
        annotation: str
            注释
        """
        self.command_text = command
        self.conditional = condition
        self.delay = tick_delay
        self.annotation_text = annotation

    def copy(self):
        return SingleCommand(
            command=self.command_text,
            condition=self.conditional,
            tick_delay=self.delay,
            annotation=self.annotation_text,
        )

    @property
    def cmd(self) -> str:
        """
        我的世界函数字符串（包含注释）
        """
        return self.__str__()

    def __str__(self) -> str:
        """
        转为我的世界函数文件格式（包含注释）
        """
        return "#[{cdt}]<{delay}> {ant}\n{cmd}".format(
            cdt="CDT" if self.conditional else "",
            delay=self.delay,
            ant=self.annotation_text,
            cmd=self.command_text,
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.__str__() == other.__str__()


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
