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

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md


from dataclasses import dataclass
from typing import Optional

from .constants import PERCUSSION_INSTRUMENT_LIST
from .utils import inst_to_souldID_withX, perc_inst_to_soundID_withX


@dataclass(init=False)
class SingleNote:
    """存储单个音符的类"""

    instrument: int
    """乐器编号"""

    note: int
    """音符编号"""

    velocity: int
    """力度/响度"""

    start_time: int
    """开始之时 ms"""

    duration: int
    """音符持续时间 ms"""

    track_no: int
    """音符所处的音轨"""

    percussive: bool
    """是否为打击乐器"""

    def __init__(
        self,
        instrument: int,
        pitch: int,
        velocity: int,
        startime: int,
        lastime: int,
        track_number: int = 0,
        is_percussion: Optional[bool] = None,
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
        self.start_time: int = startime
        """开始之时 ms"""
        self.duration: int = lastime
        """音符持续时间 ms"""
        self.track_no: int = track_number
        """音符所处的音轨"""
        self.track_no: int = track_number
        """音符所处的音轨"""

        self.percussive = (
            (is_percussion in PERCUSSION_INSTRUMENT_LIST)
            if (is_percussion is None)
            else is_percussion
        )
        """是否为打击乐器"""

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
        return "{}Note(Instrument = {}, {}Velocity = {}, StartTime = {}, Duration = {},)".format(
            "Percussive" if self.percussive else "",
            self.inst,
            "" if self.percussive else "Pitch = {}, ".format(self.pitch),
            self.start_time,
            self.duration,
        )

    def __tuple__(self):
        return (
            (self.percussive, self.inst, self.velocity, self.start_time, self.duration)
            if self.percussive
            else (
                self.percussive,
                self.inst,
                self.note,
                self.velocity,
                self.start_time,
                self.duration,
            )
        )

    def __dict__(self):
        return (
            {
                "Percussive": self.percussive,
                "Instrument": self.inst,
                "Velocity": self.velocity,
                "StartTime": self.start_time,
                "Duration": self.duration,
            }
            if self.percussive
            else {
                "Percussive": self.percussive,
                "Instrument": self.inst,
                "Pitch": self.note,
                "Velocity": self.velocity,
                "StartTime": self.start_time,
                "Duration": self.duration,
            }
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.__str__() == other.__str__()

    def to_command(self, volume_percentage: float = 1) -> str:
        """
        将音符转为播放的指令
        :param volume_percentage:int 音量占比(0,1]

        :return str指令
        """
        self.mc_sound_ID, _X = (
            perc_inst_to_soundID_withX(self.inst)
            if self.percussive
            else inst_to_souldID_withX(self.inst)
        )

        # delaytime_now = round(self.start_time / float(speed) / 50)
        self.mc_pitch = "" if self.percussive else 2 ** ((self.note - 60 - _X) / 12)
        self.mc_distance_volume = 128 / volume_percentage / self.velocity + (
            1 if self.percussive else self.velocity / 32
        )

        return "playsound {} @s ^ ^ ^{} {} {}".format(
            self.mc_sound_ID,
            self.mc_distance_volume,
            self.velocity / 128,
            self.mc_pitch,
        )


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


@dataclass(init=False)
class SingleNoteBox:
    """存储单个音符盒"""

    instrument_block: str
    """乐器方块"""

    note_value: int
    """音符盒音高"""

    annotation_text: str
    """音符注释"""

    is_percussion: bool
    """是否为打击乐器"""

    def __init__(
        self,
        instrument_block_: str,
        note_value_: int,
        percussion: Optional[bool] = None,
        annotation: str = "",
    ):
        """用于存储单个音符盒的类
        :param instrument_block_ 音符盒演奏所使用的乐器方块
        :param note_value_ 音符盒的演奏音高
        :param percussion 此音符盒乐器是否作为打击乐处理
            注：若为空，则自动识别是否为打击乐器
        :param annotation 音符注释"""
        self.instrument_block = instrument_block_
        """乐器方块"""
        self.note_value = note_value_
        """音符盒音高"""
        self.annotation_text = annotation
        """音符注释"""
        if percussion is None:
            self.is_percussion = percussion in PERCUSSION_INSTRUMENT_LIST
        else:
            self.is_percussion = percussion

    @property
    def inst(self) -> str:
        """获取音符盒下的乐器方块"""
        return self.instrument_block

    @inst.setter
    def inst(self, inst_):
        self.instrument_block = inst_

    @property
    def note(self) -> int:
        """获取音符盒音调特殊值"""
        return self.note_value

    @note.setter
    def note(self, note_):
        self.note_value = note_

    @property
    def annotation(self) -> str:
        """获取音符盒的备注"""
        return self.annotation_text

    @annotation.setter
    def annotation(self, annotation_):
        self.annotation_text = annotation_

    def copy(self):
        return SingleNoteBox(
            instrument_block_=self.instrument_block,
            note_value_=self.note_value,
            annotation=self.annotation_text,
        )

    def __str__(self) -> str:
        return f"Note(inst = {self.inst}, note = {self.note}, )"

    def __tuple__(self) -> tuple:
        return self.inst, self.note, self.annotation

    def __dict__(self) -> dict:
        return {
            "inst": self.inst,
            "note": self.note,
            "annotation": self.annotation,
        }

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.__str__() == other.__str__()
