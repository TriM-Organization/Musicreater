# -*- coding: utf-8 -*-

"""
存储 音·创 v3 的插件管理和上层设计内容
"""

"""
版权所有 © 2025 金羿
Copyright © 2025 Eilles

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

# 睿乐组织 开发交流群 861684859
# Email TriM-Organization@hotmail.com
# 若需转载或借鉴 许可声明请查看仓库目录下的 License.md

from typing import List, Optional, Dict, Generator, Any
from pathlib import Path

from .plugin import MusicInputPlugin, MusicOperatePlugin, MusicOutputPlugin, TrackInputPlugin, TrackOperatePlugin, TrackOutputPlugin, ServicePlugin, LibraryPlugin
