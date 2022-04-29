# -*- coding:utf-8 -*-

'''
   Copyright © 2022 Team-Ryoun 金羿("Eilles Wan") & 诸葛亮与八卦阵("bgArray")

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

import os

def makeZip(sourceDir, outFilename, compression=8, exceptFile=None):
    """使用compression指定的算法打包目录为zip文件\n
    默认算法为DEFLATED(8),可用算法如下：\n
    STORED = 0\n
    DEFLATED = 8\n
    BZIP2 = 12\n
    LZMA = 14\n
    """
    import zipfile

    zipf = zipfile.ZipFile(outFilename, 'w', compression)
    pre_len = len(os.path.dirname(sourceDir))
    for parent, dirnames, filenames in os.walk(sourceDir):
        for filename in filenames:
            if filename == exceptFile:
                continue
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            zipf.write(pathfile, arcname)
    zipf.close()


class midiConvert:
    def __init__(self, midiFile: str, outputPath: str):
        '''简单的midi转换类，将midi文件转换为我的世界结构或者包'''

        import mido

        self.midiFile = midiFile
        '''midi文件路径'''
        self.midi = mido.MidiFile(self.midiFile)
        '''MidiFile对象'''
        self.outputPath = outputPath
        '''输出路径'''
        # 将self.midiFile的文件名，不含路径且不含后缀存入self.midiFileName
        self.midFileName = os.path.splitext(os.path.basename(self.midiFile))[0]
        '''文件名，不含路径且不含后缀'''

    def __Inst2SoundID(self, instrumentID, default='note.harp'):
        """返回midi的乐器ID对应的我的世界乐器名
        :param instrumentID: midi的乐器ID
        :param default: 如果instrumentID不在范围内，返回的默认我的世界乐器名称
        :return: 我的世界乐器名 str"""
        if self.staticDebug:
            pass

        if instrumentID == 105:
            return 'note.banjo'
        if instrumentID in range(32, 40):
            return 'note.bass'
        if instrumentID in range(115, 119):
            return 'note.basedrum'
        if instrumentID == 9 or instrumentID == 14:
            return 'note.bell'
        if instrumentID == 80 or instrumentID == 81:
            return 'note.bit'
        if instrumentID == 112:
            return 'note.cow_bell'
        if instrumentID == -1:
            return 'note.didgeridoo'  # 这是什么？我看不懂，但我大受震撼
        if instrumentID in range(72, 80):
            return 'note.flute'
        if instrumentID in range(24, 32):
            return 'note.guitar'
        if instrumentID == -2:
            return 'note.hat'
        if instrumentID == 14:
            return 'note.chime'
        if instrumentID == 8 or instrumentID == 11:
            return 'iron_xylophone'
        if instrumentID == 2:
            return 'note.pling'
        if instrumentID == 114:
            return 'note.snare'
        if instrumentID == 13:
            return 'note.xylophone'
        return default

    def _toCmdList_m1(
        self, scoreboardname: str = 'mscplay', volume: float = 1.0, speed: float = 1.0
    ) -> list:
        """
        使用Dislink Sforza的转换算法，将midi转换为我的世界命令列表
        :param scoreboardname: 我的世界的计分板名称
        :param volume: 音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
        :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
        :return: 我的世界命令列表
        """
        tracks = []
        if volume > 1:
            volume = 1
        if volume <= 0:
            volume = 0.001

        commands = 0

        for i, track in enumerate(self.midi.tracks):

            ticks = 0
            instrumentID = 0
            singleTrack = []

            for msg in track:
                if msg.is_meta:
                    if msg.type == 'set_tempo':
                        tempo = msg.tempo
                    if msg.type == 'program_change':
                        instrumentID = msg.program
                else:
                    ticks += msg.time
                    if msg.type == 'note_on' and msg.velocity != 0:
                        singleTrack.append(
                            'execute @a[scores={'
                            + scoreboardname
                            + '='
                            + str(
                                round(
                                    (ticks * tempo)
                                    / (
                                        (self.midi.ticks_per_beat * float(speed))
                                        * 50000
                                    )
                                )
                            )
                            + '}'
                            + f'] ~~~ playsound {self.__Inst2SoundID(instrumentID)} @s ~~{1/volume-1}~ {msg.velocity*(0.7 if msg.channel == 0 else 0.9)} {2**((msg.note-66)/12)}'
                        )
                        commands += 1

            tracks.append(singleTrack)

        return tracks, commands

    def tomcpack(
        self,
        method: int = 1,
        scoreboardname: str = 'mscplay',
        volume: float = 1.0,
        speed: float = 1.0,
    ) -> bool:
        """
        使用method指定的转换算法，将midi转换为我的世界mcpack格式的包
        :param method: 转换算法
        :param scoreboardname: 我的世界的计分板名称
        :param volume: 音量，注意：这里的音量范围为(0,1]，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
        :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
        :return 成功与否，成功返回(True,True)，失败返回(False,str失败原因)
        """
        if method == 1:
            cmdlist, _a = self._toCmdList_m1(scoreboardname, volume, speed)
        else:
            return (False, f'无法找到算法ID{method}对应的转换算法')
        del _a

        import json
        import uuid
        import shutil

        # 当文件f夹{self.outputPath}/temp/functions存在时清空其下所有项目，若其不存在则创建
        if os.path.exists(f'{self.outputPath}/temp/functions/'):
            shutil.rmtree(f'{self.outputPath}/temp/functions/')
        os.makedirs(f'{self.outputPath}/temp/functions/mscplay')

        # 写入manifest.json
        if not os.path.exists(f'{self.outputPath}/temp/manifest.json'):
            with open(f"{self.outputPath}/temp/manifest.json", "w") as f:
                f.write(
                    "{\n  \"format_version\": 1,\n  \"header\": {\n    \"description\": \""
                    + self.midFileName
                    + " Pack : behavior pack\",\n    \"version\": [ 0, 0, 1 ],\n    \"name\": \""
                    + self.midFileName
                    + "Pack\",\n    \"uuid\": \""
                    + str(uuid.uuid4())
                    + "\"\n  },\n  \"modules\": [\n    {\n      \"description\": \""
                    + f"the Player of the Music {self.midFileName}"
                    + "\",\n      \"type\": \"data\",\n      \"version\": [ 0, 0, 1 ],\n      \"uuid\": \""
                    + str(uuid.uuid4())
                    + "\"\n    }\n  ]\n}"
                )
        else:
            with open(f'{self.outputPath}/temp/manifest.json', 'r') as manifest:
                data = json.loads(manifest.read())
                data['header'][
                    'description'
                ] = f"the Player of the Music {self.midFileName}"
                data['header']['name'] = self.midFileName
                data['header']['uuid'] = str(uuid.uuid4())
                data['modules'][0]['description'] = 'None'
                data['modules'][0]['uuid'] = str(uuid.uuid4())
                manifest.close()
            open(f'{self.outputPath}/temp/manifest.json', 'w').write(json.dumps(data))

        # 将命令列表写入文件
        indexfile = open(
            f'{self.outputPath}/temp/functions/index.mcfunction', 'w', encoding='utf-8'
        )
        for track in cmdlist:
            indexfile.write(
                'function mscplay/track' + str(cmdlist.index(track) + 1) + '\n'
            )
            with open(
                f'{self.outputPath}/temp/functions/mscplay/track{cmdlist.index(track)+1}.mcfunction',
                'w',
                encoding='utf-8',
            ) as f:
                f.write('\n'.join(track))
        indexfile.write(
            'scoreboard players add @a[scores={'
            + scoreboardname
            + '=1..}] '
            + scoreboardname
            + ' 1\n'
        )
        indexfile.close()

        makeZip(
            f'{self.outputPath}/temp/', self.outputPath + f'/{self.midFileName}.mcpack'
        )

        shutil.rmtree(f'{self.outputPath}/temp/')

    def toBDXfile(
        self,
        method: int,
        author: str,
        maxheight: int,
        scoreboardname: str = 'mscplay',
        volume: float = 1.0,
        speed: float = 1.0,
    ) -> bool:
        """
        使用method指定的转换算法，将midi转换为BDX结构文件
        :param method: 转换算法
        :param scoreboardname: 我的世界的计分板名称
        :param volume: 音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
        :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
        :return 成功与否，成功返回(True,未经过压缩的源)，失败返回(False,str失败原因)
        """

        import brotli

        if method == 1:
            cmdlist, totalcount = self._toCmdList_m1(scoreboardname, volume, speed)
        else:
            return (False, f'无法找到算法ID{method}对应的转换算法')

        if not os.path.exists(self.outputPath):
            os.makedirs(self.outputPath)

        with open(f"{self.outputPath}/{self.midFileName}.bdx", "w+") as f:
            f.write("BD@")

        _bytes = (
            b"BDX\x00"
            + author.encode("utf-8")
            + b" & Musicreater\x00\x01command_block\x00"
        )

        key = {
            "x": (b"\x0f", b"\x0e"),
            "y": (b"\x11", b"\x10"),
            "z": (b"\x13", b"\x12"),
        }
        '''key存储了方块移动指令的数据，其中可以用key[x|y|z][0|1]来表示xyz的减或增'''
        x = 'x'
        y = 'y'
        z = 'z'

        def __formCMDblk(
            command: str,
            particularValue: int,
            impluse: int = 0,
            condition: bool = False,
            needRedstone: bool = True,
            tickDelay: int = 0,
            customName: str = '',
            executeOnFirstTick: bool = False,
            trackOutput: bool = True,
        ):
            """
            使用指定项目返回指定的指令方块放置指令项
            :param command: `str`
                指令
            :param particularValue:
                方块特殊值，即朝向
                    :0	下	无条件
                    :1	上	无条件
                    :2	z轴负方向	无条件
                    :3	z轴正方向	无条件
                    :4	x轴负方向	无条件
                    :5	x轴正方向	无条件
                    :6	下	无条件
                    :7	下	无条件

                    :8	下	有条件
                    :9	上	有条件
                    :10	z轴负方向	有条件
                    :11	z轴正方向	有条件
                    :12	x轴负方向	有条件
                    :13	x轴正方向	有条件
                    :14	下	有条件
                    :14	下	有条件
                注意！此处特殊值中的条件会被下面condition参数覆写
            :param impluse: `int 0|1|2`
                方块类型
                    0脉冲 1循环 2连锁
            :param condition: `bool`
                是否有条件
            :param needRedstone: `bool`
                是否需要红石
            :param tickDelay: `int`
                执行延时
            :param customName: `str`
                悬浮字
            :param lastOutput: `str`
                上次输出字符串，注意此处需要留空
            :param executeOnFirstTick: `bool`
                执行第一个已选项(循环指令方块是否激活后立即执行，若为False，则从激活时起延迟后第一次执行)
            :param trackOutput: `bool`
                是否输出

            :return:str
            """
            block = b"\x24" + particularValue.to_bytes(2, byteorder="big", signed=False)

            for i in [
                impluse.to_bytes(4, byteorder="big", signed=False),
                bytes(command, encoding="utf-8") + b"\x00",
                bytes(customName, encoding="utf-8") + b"\x00",
                bytes('', encoding="utf-8") + b"\x00",
                tickDelay.to_bytes(4, byteorder="big", signed=True),
                executeOnFirstTick.to_bytes(1, byteorder="big"),
                trackOutput.to_bytes(1, byteorder="big"),
                condition.to_bytes(1, byteorder="big"),
                needRedstone.to_bytes(1, byteorder="big"),
            ]:
                block += i
            return block

        def __fillSquareSideLength(self, total: int, maxHeight: int):
            '''给定总方块数量和最大高度，返回所构成的图形外切正方形的边长
            :param total: 总方块数量
            :param maxHeight: 最大高度
            :return: 外切正方形的边长 int'''
            import math

            math.ceil(math.sqrt(total / maxHeight))

        _sideLength = __fillSquareSideLength(totalcount, maxheight)

        yforward = True
        zforward = True

        nowy = 0
        nowz = 0

        for track in cmdlist:
            for cmd in track:
                _bytes += __formCMDblk(
                    cmd,
                    (1 if yforward else 0)
                    if (nowy != 0) and (nowy != maxheight)
                    else (3 if zforward else 2),
                    impluse=2,
                    condition=False,
                    needRedstone=False,
                    tickDelay=0,
                    customName='',
                    executeOnFirstTick=False,
                    trackOutput=True,
                )
                nowy += 1 if yforward else -1
                _bytes += key[y][int(yforward)]
                if ((nowy > maxheight) and (yforward)) or (
                    (nowy < 0) and (not yforward)
                ):
                    yforward = not yforward
                    nowz += 1 if zforward else -1
                    _bytes += key[z][int(zforward)]
                    if ((nowz > _sideLength) and (zforward)) or (
                        (nowz < 0) and (not zforward)
                    ):
                        zforward = not zforward
                        _bytes += key[x][1]

        with open(f"{self.outputPath}/{self.midFileName}.bdx", "ab+") as f:
            f.write(brotli.compress(_bytes + b'XE'))

        return (True, _bytes)
