# -*- coding: utf-8 -*-
"""
版权所有 © 2024 音·创 开发者
Copyright © 2024 all the developers of Musicreater

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md


import fcwslib
import asyncio
import uuid
import time

from ...main import MidiConvert
from ...subclass import ProgressBarStyle
from ...types import Optional, Literal, Tuple, List

from ...subclass import MineCommand


def to_websocket_server(
    midi_cvt_lst: List[MidiConvert],
    server_dist: str,
    server_port: int,
    progressbar_style: Optional[ProgressBarStyle],
) -> None:
    """
    将midi以延迟播放器形式转换为mcstructure结构文件后打包成附加包，并在附加包中生成相应地导入函数

    Parameters
    ----------
    midi_cvt: List[MidiConvert]
        一组用于转换的MidiConvert对象
    server_dist: str
        WebSocket播放服务器开启地址
    server_port: str
        WebSocket播放服务器开启端口
    progressbar_style: ProgressBarStyle 对象
        进度条对象

    Returns
    -------
    None
    """

    replacement = str(uuid.uuid4())

    musics = dict(
        [
            (k.music_name, k.to_command_list_in_delay(replacement)[:2])
            for k in midi_cvt_lst
        ]
    )

    class Plugin(fcwslib.Plugin):
        async def on_connect(self) -> None:
            print("已成功获连接")
            await self.send_command("list", callback=self.cmd_feedback)
            await self.subscribe("PlayerMessage", callback=self.player_message)

        async def on_disconnect(self) -> None:
            print("连接已然终止")
            await self.disconnect()

        async def on_receive(self, response) -> None:
            print("已收取非已知列回复 {}".format(response))

        async def cmd_feedback(self, response) -> None:
            print("已收取指令执行回复 {}".format(response))

        async def player_message(self, response) -> None:
            print("已收取玩家事件回复 {}".format(response))
            if response["body"]["message"].startswith(("。播放", ".play")):
                whom_to_play: str = response["body"]["sender"]
                music_to_play: str = (
                    response["body"]["message"]
                    .replace("。播放", "")
                    .replace(".play", "")
                    .strip()
                )
                if music_to_play in musics.keys():
                    self.check_play = True
                    delay_of_now = 0
                    for cmd in musics[music_to_play][0]:
                        if not self.check_play:
                            break
                        _time = time.time()
                        if progressbar_style:
                            await self.send_command(
                                "title {} actionbar {}".format(
                                    whom_to_play,
                                    progressbar_style.play_output(
                                        played_delays=delay_of_now,
                                        total_delays=musics[music_to_play][1],
                                        music_name=music_to_play,
                                    ),
                                ),
                                callback=self.cmd_feedback,
                            )
                        await self.send_command(
                            cmd.command_text.replace(replacement, whom_to_play),
                            callback=self.cmd_feedback,
                        )
                        delay_of_now += cmd.delay
                        await asyncio.sleep((time.time() - _time) + cmd.delay / 20)

                else:
                    await self.send_command(
                        "tellraw {} {}{}{}".format(
                            whom_to_play,
                            r'{"rawtext":[{"text":"§c§l所选歌曲',
                            music_to_play,
                            '无法播放：播放列表不存在之"}]}',
                        ),
                        callback=self.cmd_feedback,
                    )
            elif response["body"]["message"].startswith(
                ("。停止播放", ".stopplay", ".stoplay")
            ):
                self.check_play = False

    server = fcwslib.Server(server=server_dist, port=server_port, debug_mode=True)
    server.add_plugin(Plugin)
    asyncio.run(server.run_forever())
