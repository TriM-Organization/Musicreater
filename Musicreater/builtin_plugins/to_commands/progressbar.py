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

    style_base_string: str
    """基础样式"""

    progress_toplay: str
    """未播放之样式"""

    progress_played: str
    """已播放之样式"""

    is_animate_autoloop: bool
    """所示动画是否循环"""

    animate_circle: Dict[str, Dict[int, str]]
    """定义动画样式"""

    def __init__(
        self,
        base_string: str = "【%%N】%A%▶ %%s/%^s (%%t|%^t) \n"
        "[§e_________________________§r] %%%",
        to_play_style: str = "§7=",
        played_style: str = "=",
        animate_loop: bool = True,
        animate_circle: Dict[str, Dict[int, str]] = {
            "%A%": {5: "-", 10: "\\\\", 15: "|", 20: "/"}
        },
    ):
        """
        用于存储进度条样式的类，标识符替换顺序如下表

        | 标识符   | 指定的可变量     |
        |---------|----------------|
        | `%%N`   | 乐曲名(即传入的文件名)|
        | `%%s`   | 当前计分板值     |
        | `%^s`   | 计分板最大值     |
        | `%%t`   | 当前播放时间     |
        | `%^t`   | 曲目总时长       |
        | `%%%`   | 当前进度比率     |
        | `_`     | 用以表示进度条占位|
        | `%*%`   | 指定*的动画内容   |a

        Parameters
        ------------
        base_string: str
            基础样式，用以定义进度条整体
        to_play_style: str
            进度条样式：尚未播放的样子
        played_style: str
            已经播放的样子

        Returns
        ---------
        ProgressBarStyle 类
        """

        self.style_base_string = base_string
        self.progress_toplay = to_play_style
        self.progress_played = played_style
        self.is_animate_autoloop = animate_loop
        self.animate_circle = animate_circle

    def set_base_style(self, value: str):
        """设置基础样式"""
        self.style_base_string = value

    def set_to_play_style(self, value: str):
        """设置未播放之样式"""
        self.progress_toplay = value

    def set_played_style(self, value: str):
        """设置已播放之样式"""
        self.progress_played = value

    def copy(self):
        return ProgressBarStyle(
            self.style_base_string,
            self.progress_toplay,
            self.progress_played,
            self.is_animate_autoloop,
            self.animate_circle,
        )

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

        alpha_string = (
            self.style_base_string.replace("%%N", music_name)
            .replace("%%s", str(played_ticks))
            .replace("%^s", str(total_ticks))
            .replace("%%t", mctick2timestr(played_ticks))
            .replace("%^t", mctick2timestr(total_ticks))
            .replace(
                "%%%",
                "{:0>5.2f}%".format(int(10000 * played_ticks / total_ticks) / 100),
            )
            .replace(
                "_",
                self.progress_played,
                (played_ticks * self.style_base_string.count("_") // total_ticks) + 1,
            )
            .replace("_", self.progress_toplay)
        )

        for key, animate_dict in self.animate_circle.items():
            max_animate_tick = max(animate_dict.keys())
            if self.is_animate_autoloop:
                animate_time_key = 0
                for time_key in animate_dict.keys():
                    animate_time_key = time_key
                    if time_key > played_ticks % max_animate_tick:
                        break
            else:
                animate_time_key = max_animate_tick
            alpha_string = alpha_string.replace(key, animate_dict[animate_time_key])
        return alpha_string


def mctick2timestr(mc_tick: int) -> str:
    """
    将《我的世界》的游戏刻计转为表示时间的字符串
    """
    return "{:0>2d}:{:0>2d}".format(mc_tick // 1200, (mc_tick // 20) % 60)


DEFAULT_PROGRESSBAR_STYLE = ProgressBarStyle()
"""
默认的进度条样式
"""
