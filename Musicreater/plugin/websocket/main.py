# -*- coding: utf-8 -*-
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

from ...main import MidiConvert

from ..main import ConvertConfig
from ...subclass import SingleCommand


def open_websocket_server(
    midi_cvt: MidiConvert,
    data_cfg: ConvertConfig,
    player: str = "@a",
    server_dist: str = "localhost",
    server_port: int = 8000,
):
    wssever = fcwslib.Server(server=server_dist,port=server_port,debug_mode=False)