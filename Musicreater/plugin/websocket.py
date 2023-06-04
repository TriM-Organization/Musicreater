# -*- coding: utf-8 -*-
"""
存放有关WebSocket服务器操作的内容
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



import fcwslib

# 这个库有问题，正在检修

class Plugin(fcwslib.Plugin):
    async def on_connect(self) -> None:
        print('对象已被连接')
        await self.send_command('list', callback=self.list)
        await self.subscribe('PlayerMessage', callback=self.player_message)

    async def on_disconnect(self) -> None:
        print('对象停止连接')

    async def on_receive(self, response) -> None:
        print('已接收非常规回复 {}'.format(response))

    async def list(self, response) -> None:
        print('已收取指令执行回复 {}'.format(response))

    async def player_message(self, response) -> None:
        print('已收取玩家事件回复 {}'.format(response))

