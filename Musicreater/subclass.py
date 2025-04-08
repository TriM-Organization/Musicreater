# -*- coding: utf-8 -*-

"""
存储音·创附属子类
"""

"""
版权所有 © 2024 金羿 & 诸葛亮与八卦阵
Copyright © 2025 Eilles & bgArray

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md


from dataclasses import dataclass
from typing import Optional, Any, List, Tuple, Union

from .constants import MC_PITCHED_INSTRUMENT_LIST


@dataclass(init=False)
class MineNote:
    """存储单个音符的类"""

    sound_name: str
    """乐器ID"""

    note_pitch: int
    """midi音高"""

    velocity: int
    """响度(力度)"""

    start_tick: int
    """开始之时 命令刻"""

    duration: int
    """音符持续时间 命令刻"""

    high_precision_time: int
    """高精度开始时间偏量 1/1250 秒"""

    percussive: bool
    """是否作为打击乐器启用"""

    position_displacement: Tuple[float, float, float]
    """声像位移"""

    extra_info: Any
    """你觉得放什么好？"""

    def __init__(
        self,
        mc_sound_name: str,
        midi_pitch: Optional[int],
        midi_velocity: int,
        start_time: int,
        last_time: int,
        mass_precision_time: int = 0,
        is_percussion: Optional[bool] = None,
        displacement: Optional[Tuple[float, float, float]] = None,
        extra_information: Optional[Any] = None,
    ):
        """用于存储单个音符的类
        :param mc_sound_name:`str` 《我的世界》声音ID
        :param midi_pitch:`int` midi音高
        :param midi_velocity:`int` midi响度(力度)
        :param start_time:`int` 开始之时(命令刻)
            注：此处的时间是用从乐曲开始到当前的毫秒数
        :param last_time:`int` 音符延续时间(命令刻)
        :param mass_precision_time:`int` 高精度的开始时间偏移量(1/1250秒)
        :param is_percussion:`bool` 是否作为打击乐器
        :param displacement:`tuple[int,int,int]` 声像位移
        :param extra_information:`Any` 附加信息"""
        self.sound_name: str = mc_sound_name
        """乐器ID"""
        self.note_pitch: int = 66 if midi_pitch is None else midi_pitch
        """midi音高"""
        self.velocity: int = midi_velocity
        """响度(力度)"""
        self.start_tick: int = start_time
        """开始之时 tick"""
        self.duration: int = last_time
        """音符持续时间 tick"""
        self.high_precision_time: int = mass_precision_time
        """高精度开始时间偏量 0.4 毫秒"""

        self.percussive = (
            (mc_sound_name not in MC_PITCHED_INSTRUMENT_LIST)
            if (is_percussion is None)
            else is_percussion
        )
        """是否为打击乐器"""

        self.position_displacement = (
            (0, 0, 0) if (displacement is None) else displacement
        )
        """声像位移"""

        self.extra_info = extra_information

    @classmethod
    def decode(cls, code_buffer: bytes, is_high_time_precision: bool = True):
        """自字节码析出MineNote类"""
        group_1 = int.from_bytes(code_buffer[:6], "big")
        percussive_ = bool(group_1 & 0b1)
        duration_ = (group_1 := group_1 >> 1) & 0b11111111111111111
        start_tick_ = (group_1 := group_1 >> 17) & 0b11111111111111111
        note_pitch_ = (group_1 := group_1 >> 17) & 0b1111111
        sound_name_length = group_1 >> 7

        if code_buffer[6] & 0b1:
            position_displacement_ = (
                int.from_bytes(
                    (
                        code_buffer[8 + sound_name_length : 10 + sound_name_length]
                        if is_high_time_precision
                        else code_buffer[7 + sound_name_length : 9 + sound_name_length]
                    ),
                    "big",
                )
                / 1000,
                int.from_bytes(
                    (
                        code_buffer[10 + sound_name_length : 12 + sound_name_length]
                        if is_high_time_precision
                        else code_buffer[9 + sound_name_length : 11 + sound_name_length]
                    ),
                    "big",
                )
                / 1000,
                int.from_bytes(
                    (
                        code_buffer[12 + sound_name_length : 14 + sound_name_length]
                        if is_high_time_precision
                        else code_buffer[
                            11 + sound_name_length : 13 + sound_name_length
                        ]
                    ),
                    "big",
                )
                / 1000,
            )
        else:
            position_displacement_ = (0, 0, 0)

        try:
            return cls(
                mc_sound_name=(
                    o := (
                        code_buffer[8 : 8 + sound_name_length]
                        if is_high_time_precision
                        else code_buffer[7 : 7 + sound_name_length]
                    )
                ).decode(encoding="GB18030"),
                midi_pitch=note_pitch_,
                midi_velocity=code_buffer[6] >> 1,
                start_time=start_tick_,
                last_time=duration_,
                mass_precision_time=code_buffer[7] if is_high_time_precision else 0,
                is_percussion=percussive_,
                displacement=position_displacement_,
            )
        except:
            print(code_buffer, "\n", o)
            raise

    def encode(
        self, is_displacement_included: bool = True, is_high_time_precision: bool = True
    ) -> bytes:
        """
        将数据打包为字节码

        :param is_displacement_included:`bool` 是否包含声像偏移数据，默认为**是**

        :return bytes 打包好的字节码
        """

        # 字符串长度 6 位 支持到 63
        # note_pitch 7 位 支持到 127
        # start_tick 17 位 支持到 131071 即 109.22583 分钟 合 1.8204305 小时
        # duration 17 位 支持到 131071 即 109.22583 分钟 合 1.8204305 小时
        # percussive 长度 1 位 支持到 1
        # 共 48 位 合 6 字节
        # +++
        # velocity 长度 7 位 支持到 127
        # is_displacement_included 长度 1 位 支持到 1
        # 共 8 位 合 1 字节
        # +++
        # （在第二版中已舍弃）
        # track_no 长度 8 位 支持到 255 合 1 字节
        # （在第二版中新增）
        # high_time_precision（可选）长度 8 位 支持到 255 合 1 字节 支持 1/1250 秒
        # +++
        # sound_name 长度最多 63 支持到 31 个中文字符 或 63 个西文字符
        # 第一版编码： UTF-8
        # 第二版编码： GB18030
        # +++
        # position_displacement 每个元素长 16 位 合 2 字节
        # 共 48 位 合 6 字节 支持存储三位小数和两位整数，其值必须在 [0, 65.535] 之间

        return (
            (
                (
                    (
                        (
                            (
                                (
                                    (
                                        (
                                            len(
                                                r := self.sound_name.encode(
                                                    encoding="GB18030"
                                                )
                                            )
                                            << 7
                                        )
                                        + self.note_pitch
                                    )
                                    << 17
                                )
                                + self.start_tick
                            )
                            << 17
                        )
                        + self.duration
                    )
                    << 1
                )
                + self.percussive
            ).to_bytes(6, "big")
            + ((self.velocity << 1) + is_displacement_included).to_bytes(1, "big")
            # + self.track_no.to_bytes(1, "big")
            + (
                self.high_precision_time.to_bytes(1, "big")
                if is_high_time_precision
                else b""
            )
            + r
            + (
                (
                    round(self.position_displacement[0] * 1000).to_bytes(2, "big")
                    + round(self.position_displacement[1] * 1000).to_bytes(2, "big")
                    + round(self.position_displacement[2] * 1000).to_bytes(2, "big")
                )
                if is_displacement_included
                else b""
            )
        )

    def set_info(self, sth: Any):
        """设置附加信息"""
        self.extra_info = sth

    def __str__(self, is_displacement: bool = False):
        return "{}Note(Instrument = {}, {}Velocity = {}, StartTick = {}, Duration = {}{}{})".format(
            "Percussive" if self.percussive else "",
            self.sound_name,
            "" if self.percussive else "NotePitch = {}, ".format(self.note_pitch),
            self.velocity,
            self.start_tick,
            self.duration,
            (
                ", PositionDisplacement = {}".format(self.position_displacement)
                if is_displacement
                else ""
            ),
        )

    def tuplize(self, is_displacement: bool = False):
        tuplized = self.__tuple__()
        return tuplized[:-2] + ((tuplized[-1],) if is_displacement else ())

    def __list__(self) -> List:
        return (
            [
                self.percussive,
                self.sound_name,
                self.velocity,
                self.start_tick,
                self.duration,
                self.position_displacement,
            ]
            if self.percussive
            else [
                self.percussive,
                self.sound_name,
                self.note_pitch,
                self.velocity,
                self.start_tick,
                self.duration,
                self.position_displacement,
            ]
        )

    def __tuple__(
        self,
    ) -> Union[
        Tuple[bool, str, int, int, int, int, Tuple[float, float, float]],
        Tuple[bool, str, int, int, int, Tuple[float, float, float]],
    ]:
        return (
            (
                self.percussive,
                self.sound_name,
                self.velocity,
                self.start_tick,
                self.duration,
                self.position_displacement,
            )
            if self.percussive
            else (
                self.percussive,
                self.sound_name,
                self.note_pitch,
                self.velocity,
                self.start_tick,
                self.duration,
                self.position_displacement,
            )
        )

    def __dict__(self):
        return (
            {
                "Percussive": self.percussive,
                "Instrument": self.sound_name,
                "Velocity": self.velocity,
                "StartTick": self.start_tick,
                "Duration": self.duration,
                "PositionDisplacement": self.position_displacement,
            }
            if self.percussive
            else {
                "Percussive": self.percussive,
                "Instrument": self.sound_name,
                "Pitch": self.note_pitch,
                "Velocity": self.velocity,
                "StartTick": self.start_tick,
                "Duration": self.duration,
                "PositionDisplacement": self.position_displacement,
            }
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.tuplize() == other.tuplize()


@dataclass(init=False)
class MineCommand:
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
        return MineCommand(
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
        return "# {cdt}<{delay}> {ant}\n{cmd}".format(
            cdt="[CDT]" if self.conditional else "",
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
            self.is_percussion = percussion not in MC_PITCHED_INSTRUMENT_LIST
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


@dataclass(init=False)
class ProgressBarStyle:
    """进度条样式类"""

    base_style: str
    """基础样式"""

    to_play_style: str
    """未播放之样式"""

    played_style: str
    """已播放之样式"""

    def __init__(
        self,
        base_s: Optional[str] = None,
        to_play_s: Optional[str] = None,
        played_s: Optional[str] = None,
    ):
        """用于存储进度条样式的类

        | 标识符   | 指定的可变量     |
        |---------|----------------|
        | `%%N`   | 乐曲名(即传入的文件名)|
        | `%%s`   | 当前计分板值     |
        | `%^s`   | 计分板最大值     |
        | `%%t`   | 当前播放时间     |
        | `%^t`   | 曲目总时长       |
        | `%%%`   | 当前进度比率     |
        | `_`     | 用以表示进度条占位|

        :param base_s 基础样式，用以定义进度条整体
        :param to_play_s 进度条样式：尚未播放的样子
        :param played_s 已经播放的样子
        """

        self.base_style = (
            base_s if base_s else r"▶ %%N [ %%s/%^s %%% §e__________§r %%t|%^t ]"
        )
        self.to_play_style = to_play_s if to_play_s else r"§7="
        self.played_style = played_s if played_s else r"="

    @classmethod
    def from_tuple(cls, tuplized_style: Optional[Tuple[str, Tuple[str, str]]]):
        """自旧版进度条元组表示法读入数据（已不建议使用）"""

        if tuplized_style is None:
            return cls(
                r"▶ %%N [ %%s/%^s %%% §e__________§r %%t|%^t ]",
                r"§7=",
                r"=",
            )

        if isinstance(tuplized_style, tuple):
            if isinstance(tuplized_style[0], str) and isinstance(
                tuplized_style[1], tuple
            ):
                if isinstance(tuplized_style[1][0], str) and isinstance(
                    tuplized_style[1][1], str
                ):
                    return cls(
                        tuplized_style[0], tuplized_style[1][0], tuplized_style[1][1]
                    )
        raise ValueError(
            "元组表示的进度条样式组 {} 格式错误，已不建议使用此功能，请尽快更换。".format(
                tuplized_style
            )
        )

    def set_base_style(self, value: str):
        """设置基础样式"""
        self.base_style = value

    def set_to_play_style(self, value: str):
        """设置未播放之样式"""
        self.to_play_style = value

    def set_played_style(self, value: str):
        """设置已播放之样式"""
        self.played_style = value

    def copy(self):
        dst = ProgressBarStyle(self.base_style, self.to_play_style, self.played_style)
        return dst

    def play_output(
        self,
        played_delays: int,
        total_delays: int,
        music_name: str = "无题",
    ) -> str:
        """
        直接依照此格式输出一个进度条

        :param played_delays: int 当前播放进度积分值
        :param total_delays: int  乐器总延迟数（积分数）
        :param music_name: str    曲名
        """

        return (
            self.base_style.replace(r"%%N", music_name)
            .replace(r"%%s", str(played_delays))
            .replace(r"%^s", str(total_delays))
            .replace(r"%%t", mctick2timestr(played_delays))
            .replace(r"%^t", mctick2timestr(total_delays))
            .replace(
                r"%%%",
                "{:0>5.2f}%".format(int(10000 * played_delays / total_delays) / 100),
            )
            .replace(
                "_",
                self.played_style,
                (played_delays * self.base_style.count("_") // total_delays) + 1,
            )
            .replace("_", self.to_play_style)
        )


def mctick2timestr(mc_tick: int) -> str:
    """
    将《我的世界》的游戏刻计转为表示时间的字符串
    """
    return "{:0>2d}:{:0>2d}".format(mc_tick // 1200, (mc_tick // 20) % 60)


DEFAULT_PROGRESSBAR_STYLE = ProgressBarStyle(
    r"▶ %%N [ %%s/%^s %%% §e__________§r %%t|%^t ]",
    r"§7=",
    r"=",
)
"""
默认的进度条样式
"""
