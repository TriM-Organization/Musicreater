# -*- coding:utf-8 -*-

import mido
import os
import json
import uuid
import shutil
import zipfile


def makeZip(sourceDir, outFilename, compression=8, exceptFile=None):
    """使用compression指定的算法打包目录为zip文件\n
    默认算法为DEFLATED(8),可用算法如下：\n
    STORED = 0\n
    DEFLATED = 8\n
    BZIP2 = 12\n
    LZMA = 14\n
    """
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
        """简单的midi转换类，将midi文件转换为我的世界结构或者包"""
        self.midiFile = midiFile
        '''midi文件路径'''
        self.midi = mido.MidiFile(self.midiFile)
        '''MidiFile对象'''
        self.outputPath = outputPath
        '''输出路径'''
        # 将self.midiFile的文件名，不含路径且不含后缀存入self.midiFileName
        self.midFileName = os.path.splitext(os.path.basename(self.midiFile))[0]
        '''文件名，不含路径且不含后缀'''

        self.staticDebug = True

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

    def _toCmdList_m1(self, scoreboardname: str = 'mscplay', volume: float = 1.0, speed: float = 1.0) -> list:
        """使用Dislink Sforza的转换算法，将midi转换为我的世界命令列表
        :param scoreboardname: 我的世界的计分板名称
        :param volume: 音量，注意：这里的音量范围为(0,1]，如果超出将被处理为正确值，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
        :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
        :return: 我的世界命令列表"""
        tracks = []
        if volume > 1:
            volume = 1
        if volume <= 0:
            volume = 0.001

        for i, track in enumerate(self.midi.tracks):

            ticks = 0
            commands = 0
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
                        singleTrack.append('execute @a[scores={' + scoreboardname + '=' +
                                           str(round((ticks * tempo)((self.midi.ticks_per_beat * float(speed)) *
                                                                     50000))) + '}' +
                                           f'] ~~~ playsound {self.__Inst2SoundID(instrumentID)} '
                                           f'@s ~~{1 / volume - 1}~ {msg.velocity * (0.7 if msg.channel == 0 else 0.9)}'
                                           f' {2 ** ((msg.note - 66) / 12)}')
                        commands += 1

            tracks.append(singleTrack)

        return tracks

    def tomcpack(self, method: int = 1, scoreboardname: str = 'mscplay', volume: float = 1.0,
                 speed: float = 1.0) -> tuple:
        """使用method指定的转换算法，将midi转换为我的世界mcpack格式的包
        :param method: 转换算法
        :param scoreboardname: 我的世界的计分板名称
        :param volume: 音量，注意：这里的音量范围为(0,1]，其原理为在距离玩家 (1 / volume -1) 的地方播放音频
        :param speed: 速度，注意：这里的速度指的是播放倍率，其原理为在播放音频的时候，每个音符的播放时间除以 speed
        :return 成功与否，成功返回(True,True)，失败返回(False,str失败原因)"""
        if method == 1:
            cmdlist = self._toCmdList_m1(scoreboardname, volume, speed)
        else:
            return False, f'无法找到算法ID{method}对应的转换算法'

        # 当文件f夹{self.outputPath}/temp/functions存在时清空其下所有项目，若其不存在则创建
        if os.path.exists(f'{self.outputPath}/temp/functions/'):
            shutil.rmtree(f'{self.outputPath}/temp/functions/')
        os.makedirs(f'{self.outputPath}/temp/functions/mscplay')

        # 写入manifest.json
        if not os.path.exists(f'{self.outputPath}/temp/manifest.json'):
            with open(f"{self.outputPath}/temp/manifest.json", "w") as f:
                f.write(
                    "{\n  \"format_version\": 1,\n  \"header\": {\n    \"description\": \"" + self.midFileName +
                    " Pack : behavior pack\",\n    \"version\": [ 0, 0, 1 ],\n    \"name\": \"" + self.midFileName +
                    "Pack\",\n    \"uuid\": \"" + str(
                        uuid.uuid4()) + "\"\n  },\n  \"modules\": [\n    {\n      \"description\": \"" +
                    f"the Player of the Music {self.midFileName}" + "\",\n      \"type\": \"data\",\n      "
                                                                    "\"version\": [ 0, 0, 1 ],\n      \"uuid\": "
                                                                    "\"" + str(
                        uuid.uuid4()) + "\"\n    }\n  ]\n}")
        else:
            with open(f'{self.outputPath}/temp/manifest.json', 'r') as manifest:
                data = json.loads(manifest.read())
                data['header']['description'] = f"the Player of the Music {self.midFileName}"
                data['header']['name'] = self.midFileName
                data['header']['uuid'] = str(uuid.uuid4())
                data['modules'][0]['description'] = 'None'
                data['modules'][0]['uuid'] = str(uuid.uuid4())
                manifest.close()
            open(f'{self.outputPath}/temp/manifest.json', 'w').write(json.dumps(data))

        # 将命令列表写入文件
        indexfile = open(f'{self.outputPath}/temp/functions/index.mcfunction', 'w', encoding='utf-8')
        for track in cmdlist:
            indexfile.write('function mscplay/track' + str(cmdlist.index(track) + 1) + '\n')
            with open(f'{self.outputPath}/temp/functions/mscplay/track{cmdlist.index(track) + 1}.mcfunction', 'w',
                      encoding='utf-8') as f:
                f.write('\n'.join(track))
        indexfile.write('scoreboard players add @a[scores={' + scoreboardname + '=1..}] ' + scoreboardname + ' 1\n')
        indexfile.close()

        makeZip(f'{self.outputPath}/temp/', self.outputPath + f'/{self.midFileName}.mcpack')

        shutil.rmtree(f'{self.outputPath}/temp/')


def importDebug():
    """调试用的函数，可以在这里写一些调试代码"""
    return None
