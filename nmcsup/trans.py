"""音创系列的转换功能"""
# 诸葛亮与八卦阵帮忙修改语法 日期：---2022年1月19日
# 统计：致命（三级）错误：0个；警告（二级）错误：2个；语法（一级）错误：192个


from nmcsup.log import log


import amulet
import amulet_nbt
from amulet.api.block import Block
from amulet.api.block_entity import BlockEntity
from amulet.utils.world_utils import block_coords_to_chunk_coords
from amulet_nbt import TAG_String, TAG_Compound, TAG_Byte


# 输入一个列表 [ [str, float ], [], ... ] 音符str 值为持续时间float
def note2list(Notes: list) -> list:
    from nmcsup.const import notes

    def change(base):
        enwo = {
            'a': 'A',
            'b': 'B',
            'c': 'C',
            'd': "D",
            "e": "E",
            'f': 'F',
            'g': "G"
        }
        nuwo = {
            '6': 'A',
            '7': 'B',
            '1': 'C',
            '2': "D",
            "3": "E",
            '4': 'F',
            '5': "G"
        }
        for k, v in enwo.items():
            if k in base:
                base = base.replace(k, v)
        for k, v in nuwo.items():
            if k in base:
                base = base.replace(k, v)
        return base

    res = []
    log("	===	音符列表=>音调列表")
    for i in Notes:
        s2 = change(i[0])
        log('	===	正在操作音符' + i[0] + '->' + s2)
        if s2 in notes.keys():
            log("	===	找到此音符，加入：" + str(notes[s2][0]))
            res.append([notes[s2][0], float(i[1])])
        else:
            log('	===	' + s2 + '不在音符表内，此处自动替换为 休止符0 ')
            res.append(['0', float(i[1])])
    log('	===	最终反回' + str(res))
    return res


def mcnote2freq(Notes):
    from nmcsup.const import notes
    mcnback = {}
    for i, j in notes.items():
        mcnback[j[0]] = i
    res = []
    log("	===	我的世界音调表=>频率列表")
    for i in Notes:
        log('	===	正在操作音符' + i[0] + '->' + mcnback[i[0]])
        res.append([notes[mcnback[i[0]]][1], float(i[1])])
    log('	===	最终反回' + str(res))
    return res


# MP3文件转midi文件
def Mp32Mid(mp3File, midFile):
    from piano_transcription_inference import PianoTranscription, sample_rate, load_audio
    # 加载
    (audio, _) = load_audio(mp3File, sr=sample_rate)  # , mono=True
    # 实例化并转换
    PianoTranscription(device="cpu").transcribe(audio, midFile)





# 传入一个音符列表转为指令列表
def Note2Cmd(Notes: list, ScoreboardName: str, Instrument: str, PlayerSelect: str = '',
             isProsess: bool = False) -> list:
    commands = []
    a = 0.0
    length = len(Notes)
    j = 1
    for i in range(len(Notes)):
        commands.append("execute @a" + PlayerSelect + " ~ ~ ~ execute @s[scores={" + ScoreboardName + "=" + str(
            int((a + 2) * 5 + int(Notes[i][1] * 5))) + "}] ~ ~ ~ playsound " + Instrument + " @s ~ ~ ~ 1000 " + str(
            Notes[i][0]) + " 1000\n")
        a += Notes[i][1]
        if isProsess:
            commands.append("execute @a" + PlayerSelect + " ~ ~ ~ execute @s[scores={" + ScoreboardName + "=" + str(
                int((a + 2) * 5 + int(Notes[i][1] * 5))) + "}] ~ ~ ~ title @s actionbar §e▶  播放中：  §a" + str(
                j) + "/" + str(length) + "  ||  " + str(int(j / length * 1000) / 10) + "\n")
            j += 1
    commands.append("\n\n# 凌云我的世界开发团队 x 凌云软件开发团队  : W-YI（金羿）\n")
    return commands
# def newDataStructureCounterChange():




















# 简单载入方块
# level.set_version_block(posx,posy,posz,"minecraft:overworld",("bedrock", (1, 16, 20)),Block(namespace, name))


# 转入指令列表与位置信息转至世界
def Cmd2World(cmd: list, world: str, dire: list):
    """将指令以命令链的形式载入世界\n
    cmd指令列表位为一个序列，中包含指令字符串\n
    world为地图所在位置，需要指向文件夹，dire为指令方块生成之位置"""
    level = amulet.load_level(world)
    cdl = []
    for i in cmd:
        # e = True
        try:
            if (i[:i.index('#')].replace(' ', '') != '\n') and (i[:i.index('#')].replace(' ', '') != ''):
                cdl.append(i[:i.index('#')])
            # e = False
        except:
            cdl.append(i)
        # finally:
        #     if e is True:
        #         cdl.append(i)
    i = 0
    # 第一个是特殊
    universal_block = Block('universal_minecraft', 'command_block',
                            {'conditional': TAG_String("false"), 'facing': TAG_String('up'),
                             'mode': TAG_String("repeating")})
    cx, cz = block_coords_to_chunk_coords(dire[0], dire[2])
    chunk = level.get_chunk(cx, cz, "minecraft:overworld")
    offset_x, offset_z = dire[0] - 16 * cx, dire[2] - 16 * cz
    universal_block_entity = BlockEntity('universal_minecraft', 'command_block', dire[0], dire[1], dire[2],
                                         amulet_nbt.NBTFile(TAG_Compound({'utags': TAG_Compound(
                                             {'auto': TAG_Byte(0), 'Command': TAG_String(cdl.pop(0))})})))
    chunk.blocks[offset_x, dire[1], offset_z] = level.block_palette.get_add_block(universal_block)
    chunk.block_entities[(dire[0], dire[1], dire[2])] = universal_block_entity
    chunk.changed = True
    # 集体上移
    dire[1] += 1
    # 真正开始
    down = False
    for j in cdl:
        if dire[1] + i >= 255:
            dire[0] += 1
            i = 0
            down = not down
        # 定义此方块
        if dire[1] + i == 254:
            universal_block = Block('universal_minecraft', 'command_block',
                                    {'conditional': TAG_String("false"), 'facing': TAG_String('east'),
                                     'mode': TAG_String("chain")})
        else:
            if down:
                universal_block = Block('universal_minecraft', 'command_block',
                                        {'conditional': TAG_String("false"), 'facing': TAG_String('down'),
                                         'mode': TAG_String("chain")})
            else:
                universal_block = Block('universal_minecraft', 'command_block',
                                        {'conditional': TAG_String("false"), 'facing': TAG_String('up'),
                                         'mode': TAG_String("chain")})
        cx, cz = block_coords_to_chunk_coords(dire[0], dire[2])
        # 获取区块
        chunk = level.get_chunk(cx, cz, "minecraft:overworld")
        offset_x, offset_z = dire[0] - 16 * cx, dire[2] - 16 * cz
        if down:
            # 定义方块实体
            universal_block_entity = BlockEntity('universal_minecraft', 'command_block', dire[0], 254 - i, dire[2],
                                                 amulet_nbt.NBTFile(TAG_Compound({'utags': TAG_Compound(
                                                     {'auto': TAG_Byte(1), 'Command': TAG_String(j)})})))

            # 将方块加入世界
            chunk.blocks[offset_x, 254 - i, offset_z] = level.block_palette.get_add_block(universal_block)
            chunk.block_entities[(dire[0], 254 - i, dire[2])] = universal_block_entity
        else:
            # 定义方块实体
            universal_block_entity = BlockEntity('universal_minecraft', 'command_block', dire[0], dire[1] + i, dire[2],
                                                 amulet_nbt.NBTFile(TAG_Compound({'utags': TAG_Compound(
                                                     {'auto': TAG_Byte(1), 'Command': TAG_String(j)})})))

            # 将方块加入世界
            chunk.blocks[offset_x, dire[1] + i, offset_z] = level.block_palette.get_add_block(universal_block)
            chunk.block_entities[(dire[0], dire[1] + i, dire[2])] = universal_block_entity
        # 设置为已更新区块
        chunk.changed = True
        i += 1
    del i, cdl
    # 保存世界并退出
    level.save()
    level.close()


# 音符转成方块再加载到世界里头
def Blocks2World(world: str, dire: list, Datas: list):
    from nmcsup.const import Blocks
    level = amulet.load_level(world)
    i = 0

    def setblock(block: str, pos: list):
        """pos : list[int,int,int]"""
        cx, cz = block_coords_to_chunk_coords(pos[0], pos[2])
        chunk = level.get_chunk(cx, cz, "minecraft:overworld")
        offset_x, offset_z = pos[0] - 16 * cx, pos[2] - 16 * cz
        chunk.blocks[offset_x, pos[1], offset_z] = level.block_palette.get_add_block(Block("minecraft", block))
        chunk.changed = True

    for j in Datas:
        if dire[1] + 1 >= 255:
            i = 0
            dire[0] += 1
        setblock(Blocks[j[0]], [dire[0], dire[1] + i, dire[2]])
        i = int(i + j[1] + 0.5)  # 四舍五入
    level.save()
    level.close()


# 传入音符列表制作播放器指令
def Notes2Player(Note, dire: list, CmdData: dict):
    """传入音符列表、坐标、指令数据，生成播放器指令"""
    Notes = {}
    for i in Note:
        Notes[i[0]] = ''
    Notes = list(Notes.keys())
    from nmcsup.const import Blocks
    Cmds = []
    for j in Notes:
        Cmds.append('execute @e[x=' + str(dire[0]) + ',y=' + str(dire[1]) + ',z=' + str(dire[2]) + ',dy=' + str(
            255 - dire[1]) + ',name=' + CmdData['Ent'] + '] ~ ~ ~ detect ~ ~ ~ ' + Blocks[j] + ' 0 execute @a ' +
                    CmdData['Pls'] + ' ~ ~ ~ playsound ' + CmdData['Ins'] + ' @s ~ ~ ~ 1000 ' + str(j) + ' 1000\n')
    Cmds += ['#本函数由 金羿 音·创 生成\n', 'execute @e[y=' + str(dire[1]) + ',dy=' + str(255 - dire[1]) + ',name=' + CmdData[
        'Ent'] + '] ~ ~ ~ tp ~ ~1 ~\n',
             'execute @e[y=255,dy=100,name=' + CmdData['Ent'] + '] ~ ~ ~ tp ~1 ' + str(dire[1]) + ' ~\n',
             '#音·创 开发交流群 861684859']
    return Cmds


# 传入音符列表生成方块至世界
def Datas2BlkWorld(NoteData, world: str, dire: list):
    for i in range(len(NoteData)):
        Blocks2World(world, [dire[0], dire[1], dire[2] + i], NoteData[i])


if __name__ == '__main__':
    from nmcreader import midi_conversion
    path = "L:\\0WorldMusicCreater-MFMS new edition\\框架\\v0.3.2\\Musicreater\\测试用\\同道殊途标准.mid"
    b = midi_conversion(path)
    classList_conversion(b, "n")
