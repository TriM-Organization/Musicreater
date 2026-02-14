# -*- coding: utf-8 -*-

"""
音·创 v3 内置的 指令生成插件的进度条相关内容
"""

"""
版权所有 © 2026 金羿、玉衡Alioth
Copyright © 2026 Eilles, YuhengAlioth

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md


from dataclasses import dataclass
from typing import BinaryIO, Optional, Dict, List, Callable, Tuple, Mapping


# 这个类也有很大的优化空间a
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
        """
        用于存储进度条样式的类

        | 标识符   | 指定的可变量     |
        |---------|----------------|
        | `%%N`   | 乐曲名(即传入的文件名)|
        | `%%s`   | 当前计分板值     |
        | `%^s`   | 计分板最大值     |
        | `%%t`   | 当前播放时间     |
        | `%^t`   | 曲目总时长       |
        | `%%%`   | 当前进度比率     |
        | `_`     | 用以表示进度条占位|

        Parameters
        ------------
        base_s: str
            基础样式，用以定义进度条整体
        to_play_s: str
            进度条样式：尚未播放的样子
        played_s: str
            已经播放的样子

        Returns
        ---------
        ProgressBarStyle 类
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
        played_ticks: int,
        total_ticks: int,
        music_name: str = "无题",
    ) -> str:
        """
        直接依照此格式输出一个进度条

        Parameters
        ------------
        played_delays: int
            当前播放进度积分值
        total_delays: int
            乐器总延迟数（计分板值）
        music_name: str
            曲名

        Returns
        ---------
        str
            进度条字符串
        """

        return (
            self.base_style.replace(r"%%N", music_name)
            .replace(r"%%s", str(played_ticks))
            .replace(r"%^s", str(total_ticks))
            .replace(r"%%t", mctick2timestr(played_ticks))
            .replace(r"%^t", mctick2timestr(total_ticks))
            .replace(
                r"%%%",
                "{:0>5.2f}%".format(int(10000 * played_ticks / total_ticks) / 100),
            )
            .replace(
                "_",
                self.played_style,
                (played_ticks * self.base_style.count("_") // total_ticks) + 1,
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
