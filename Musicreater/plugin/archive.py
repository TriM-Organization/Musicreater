# -*- coding: utf-8 -*-
"""
存放关于文件打包的内容
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


import os
import uuid
import zipfile
import datetime
from typing import List, Union, Literal


def compress_zipfile(sourceDir, outFilename, compression=8, exceptFile=None):
    """使用compression指定的算法打包目录为zip文件\n
    默认算法为DEFLATED(8),可用算法如下：\n
    STORED = 0\n
    DEFLATED = 8\n
    BZIP2 = 12\n
    LZMA = 14\n
    """

    zipf = zipfile.ZipFile(outFilename, "w", compression)
    pre_len = len(os.path.dirname(sourceDir))
    for parent, dirnames, filenames in os.walk(sourceDir):
        for filename in filenames:
            if filename == exceptFile:
                continue
            pathfile = os.path.join(parent, filename)
            arc_name = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            zipf.write(pathfile, arc_name)
    zipf.close()


def behavior_mcpack_manifest(
    pack_description: str = "",
    pack_version: Union[List[int], Literal[None]] = None,
    pack_name: str = "",
    pack_uuid: Union[str, Literal[None]] = None,
    modules_description: str = "",
    modules_version: List[int] = [0, 0, 1],
    modules_uuid: Union[str, Literal[None]] = None,
):
    """
    生成一个我的世界行为包组件的定义清单文件
    """
    if not pack_version:
        now_date = datetime.datetime.now()
        pack_version = [
            now_date.year,
            now_date.month * 100 + now_date.day,
            now_date.hour * 100 + now_date.minute,
        ]
    return {
        "format_version": 1,
        "header": {
            "description": pack_description,
            "version": pack_version,
            "name": pack_name,
            "uuid": str(uuid.uuid4()) if not pack_uuid else pack_uuid,
        },
        "modules": [
            {
                "description": modules_description,
                "type": "data",
                "version": modules_version,
                "uuid": str(uuid.uuid4()) if not modules_uuid else modules_uuid,
            }
        ],
    }
