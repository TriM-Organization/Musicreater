"""音·创 的转换工具库"""

# 诸葛亮与八卦阵帮忙修改语法 日期：---2022年1月19日
# 统计：致命（三级）错误：0个；警告（二级）错误：4个--未解决1个；语法（一级）错误：302个


# 可序列化对象，即可迭代对象
from typing import Iterable

import amulet

from amulet.api.block import Block
from amulet.utils.world_utils import block_coords_to_chunk_coords as bc2cc
from amulet_nbt import TAG_String as ts
from msctLib.log import log


def hans2pinyin(hans, style=3):
    """将汉字字符串转化为拼音字符串"""
    from pypinyin import lazy_pinyin
    result = lazy_pinyin(hans=hans, style=style)
    final = ''
    for i in result:
        final += i
    return final


def classList_conversion_SinglePlayer(List: list, ScoreboardName: str, playerSelection: str = '',
                                      isProsess: bool = False) -> list:
    from bgArrayLib.compute import round_up
    from bgArrayLib.pitchStrConstant import pitch
    from bgArrayLib.instrumentConstant import instrument_list
    commands = []
    length = len(List)
    j = 1
    for k in range(len(List)):
        i = List[k][0]
        try:
            commands.append(
                f"execute @a{playerSelection} ~ ~ ~ execute @s[scores={{{ScoreboardName}="
                f"{str(round_up(i.time_position)).replace('.0', '')}}}] ~ ~{127 - i.velocity} "
                f"~ playsound note.{instrument_list.get(str(i.instrument))} @s ~ ~ ~ "
                f"1000 {pitch.get(str(i.pitch))} 1000\n")
            if isProsess:
                commands.append(
                    f"execute @a{playerSelection} ~ ~ ~ execute @s[scores={{{ScoreboardName}="
                    f"{str(round_up(i.time_position)).replace('.0', '')}}}] ~ ~ ~ "
                    f"title @s actionbar §e▶  播放中：  §a{j}/{length}  ||  {int(j / length * 1000) / 10}\n")
                j += 1
        except Exception:
            pass
            # a += List[i][1]
    # commands.append("\n\n# 凌云我的世界开发团队 x 凌云软件开发团队  : W-YI（金羿）\n")
    return commands


def newList_conversion_SinglePlayer(List: list, ScoreboardName: str, playerSelection: str = '',
                                    isProsess: bool = False) -> list:
    from bgArrayLib.compute import round_up
    commands = []
    length = len(List)
    j = 1
    print(List)
    for k in range(len(List)):
        i = List[k][0]
        print(i)
        print(type(i))
        try:
            if i.instrument > 119:
                pass
            else:
                commands.append(
                    f"execute @a{playerSelection} ~ ~ ~ execute @s[scores={{{ScoreboardName}="
                    f"{str(round_up(i.time_position)).replace('.0', '')}}}] ~ ~{127 - i.velocity} "
                    f"~ playsound {i.instrument}{i.CD}.{i.pitch} @s ~ ~ ~ 1000 1.0 1000\n")
                if isProsess:
                    commands.append(
                        f"execute @a{playerSelection} ~ ~ ~ execute @s[scores={{{ScoreboardName}="
                        f"{str(round_up(i.time_position)).replace('.0', '')}}}] ~ ~ ~ "
                        f"title @s actionbar §e▶  播放中：  §a{j}/{length}  ||  {int(j / length * 1000) / 10}\n")
                    j += 1
        except:
            pass
            # a += List[i][1]
    # commands.append("\n\n# 凌云我的世界开发团队 x 凌云软件开发团队  : W-YI（金羿）\n")
    print(commands)
    return commands


def classList_conversion(List: list, ScoreboardName: str, isProsess: bool = False) -> list:
    from bgArrayLib.compute import round_up
    commands = []
    length = len(List)
    j = 1
    print(List)
    for k in range(len(List)):
        i = List[k][0]
        print(i)
        print(type(i))
        try:
            if i.instrument > 119:
                pass
            else:
                commands.append("execute @e[scores={" +
                                ScoreboardName + "=" + str(round_up(i.time_position)).replace(".0", "") + "}] ~ ~" +
                                str(127 - i.velocity) +
                                " ~ playsound " +
                                str(i.instrument) +
                                str(i.CD) + "." +
                                str(i.pitch)
                                + " @a ~ ~ ~ 1000 1.0 1000\n")
                if isProsess:
                    commands.append("execute @a"" ~ ~ ~ execute @s[scores={" + ScoreboardName + "=" +
                                    str(round_up(i.time_position)).replace(".0", "") +
                                    "}] ~ ~ ~ title @s actionbar §e▶  播放中：  §a" +
                                    str(j) + "/" + str(length) + "  ||  " + str(int(j / length * 1000) / 10) + "\n")
                    j += 1
        except AttributeError:
            pass
            # a += List[i][1]
    # commands.append("\n\n# 凌云我的世界开发团队 x 凌云软件开发团队  : W-YI（金羿）\n")
    print(commands)
    return commands


def formCmdBlock(direction: Iterable, command: str, particularValue: int, impluse: int = 0, condition: bool = False,
                 needRedstone: bool = True, tickDelay: int = 0, customName: str = '', lastOutput: str = '',
                 executeOnFirstTick: bool = False, trackOutput: bool = True):
    """
    使用指定项目返回指定的指令方块格式字典
    :param direction: `list[x: int, y: int, z: int]`
        方块位置
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

    :return: 指令方块字典结构，如下
    """
    '''
    :param block: {
        "direction": [x: int, y: int, z: int]  #方块位置
        "block_name": str,  #方块名称（无需指定，默认为command_block）
        "particular_value": int,  #方块特殊值
        "impluse": int,  #方块类型0脉冲 1循环 2连锁 unsigned_int32
        "command": str,  #指令
        "customName": str,  #悬浮字
        "lastOutput": str,  #上次输出
        "tickdelay": int,  #方块延时 int32
        "executeOnFirstTick": int,  #执行第一个选项 1 bytes
        "trackOutput": int,  #是否输出 1 bytes
        "conditional": int,  #是否有条件 1 bytes
        "needRedstone": int  #是否需要红石 1 bytes
    }
    '''
    return {"direction": direction,
            "block_name": "command_block",
            "particular_value": particularValue,
            "impluse": impluse,
            "command": command,
            "customName": customName,
            "lastOutput": lastOutput,
            "tickdelay": tickDelay,
            "executeOnFirstTick": executeOnFirstTick,
            "trackOutput": trackOutput,
            "conditional": condition,
            "needRedstone": needRedstone
            }


def note2bdx(filePath: str, dire: list, Notes: list, ScoreboardName: str, Instrument: str,
             PlayerSelect: str = '', isProsess: bool = False, height: int = 200):
    """使用方法同Note2Cmd
    :param 参数说明：
        filePath: 生成.bdx文件的位置
        dire: 指令方块在地图中生成的起始位置（相对位置）
        Notes: 以 list[ list[ float我的世界playsound指令音调 , float延续时常（单位s） ] ] 格式存储的音符列表
                例如Musicreater.py的(dataset[0]['musics'][NowMusic]['notes'])
        ScoreboardName: 用于执行的计分板名称
        Instrument: 播放的乐器
        PlayerSelect: 执行的玩家选择器
        isProsess: 是否显示进度条（会很卡）
        height: 生成结构的最高高度
    :return 返回一个BdxConverter类，同时在指定位置生成.bdx文件"""

    from nmcsup.trans import Note2Cmd
    from msctspt.bdxOpera_CP import BdxConverter
    cmd = Note2Cmd(Notes, ScoreboardName, Instrument, PlayerSelect, isProsess)
    cdl = []
    
    for i in cmd:
        if '#' in i:
            if (i[:i.index('#')].replace(' ', '') != '\n') and (i[:i.index('#')].replace(' ', '') != ''):
                cdl.append(i[:i.index('#')])
        else:
            cdl.append(i)
    i = 0
    down = False
    blocks = [formCmdBlock(dire, cdl.pop(0), 1, 1)]
    dire[1] += 1
    for j in cdl:
        if dire[1] + i > height:
            dire[0] += 1
            i = 0
            down = not down
        if dire[1] + i == height:
            blocks.append(formCmdBlock([dire[0], dire[1] + i, dire[2]], j, 5, 2, False, False))
        else:
            if down:
                blocks.append(formCmdBlock([dire[0], dire[1] + i, dire[2]], j, 0, 2, False, False))
            else:
                blocks.append(formCmdBlock([dire[0], dire[1] + i, dire[2]], j, 1, 2, False, False))
        i += 1
    del i, cdl, down, cmd
    return BdxConverter(filePath, 'Build by RyounMusicreater', blocks)



def music2cmdBlocks(direction: Iterable, music: dict, isProsess: bool = False, height: int = 200,
              isSquare: bool = False):
    """使用方法同Note2Cmd
    :param 参数说明：
        filePath: 生成.bdx文件的位置
        dire: 指令方块在地图中生成的起始位置（相对位置）
        music: 详见 Musicreater.py - dataset[0]
        isProsess: 是否显示进度条（会很卡）
        height: 生成结构的最高高度
        isSquare: 生成的结构是否需要遵循生成正方形原则
    :return 返回一个列表，其中包含了音乐生成的所有的指令方块数据"""
    from msctspt.threadOpera import NewThread


    allblocks = []
    '''需要放置的方块'''
    baseDire = direction

    direction = list(direction)

    def trackDealing(direction,track):
        blocks = []
        cmdList = classList_conversion_SinglePlayer(track['notes'], track['set']['ScoreboardName'],
                                                    music['mainset']['PlayerSelect'], isProsess)
        if len(cmdList) == 0:
            return []
        elif cmdList is []:
            return []
        dire = direction
        down = False
        '''当前是否为向下的阶段？'''
        # 开头的指令方块
        blocks.append(formCmdBlock(dire,
                                   f"scoreboard players add @a{music['mainset']['PlayerSelect']} "
                                   f"{track['set']['ScoreboardName']} 1",
                                   1, 1))
        dire[1] += 1
        blocks.append(formCmdBlock(dire, cmdList.pop(0), 2, needRedstone=False))
        dire[1] += 1
        # :0	下	无条件
        # :1	上	无条件
        # :2	z轴负方向	无条件
        # :3	z轴正方向	无条件
        # :4	x轴负方向	无条件
        # :5	x轴正方向	无条件
        for cmd in cmdList:
            blocks.append(formCmdBlock(dire, cmd, 5 if (down is False and dire[1] == height + direction[1]) or (
                    down and dire[1] == direction + 1) else 0 if down else 1, 2, needRedstone=False))
            if down:
                if dire[1] > direction[1] + 1:
                    dire[1] -= 1
            else:
                if dire[1] < height + direction[1]:
                    dire[1] += 1

            if (down is False and dire[1] == height + direction[1]) or (down and dire[1] == direction + 1):
                down = not down
                dire[0] += 1
        return blocks

    threads = []
    for track in music['musics']:
        threads.append(NewThread(trackDealing,(direction,track)))
        threads[-1].start()
        direction[2] += 2

    for th in threads:
        allblocks += th.getResult()

    return allblocks











def music2BDX(filePath: str, direction: Iterable, music: dict, isProsess: bool = False, height: int = 200,
              isSquare: bool = False):
    """使用方法同Note2Cmd
    :param 参数说明：
        filePath: 生成.bdx文件的位置
        dire: 指令方块在地图中生成的起始位置（相对位置）
        music: 详见 Musicreater.py - dataset[0]
        isProsess: 是否显示进度条（会很卡）
        height: 生成结构的最高高度
        isSquare: 生成的结构是否需要遵循生成正方形原则
    :return 返回一个BdxConverter类，同时在指定位置生成.bdx文件"""
    from msctspt.bdxOpera_CP import BdxConverter
    return BdxConverter(filePath, 'Build by Ryoun Musicreater', music2cmdBlocks(direction,music,isProsess,height,isSquare)
)


def note2webs(Notes: list, Instrument: str, speed: float = 5.0, PlayerSelect: str = '', isProsess: bool = False):
    """传入音符，在oaclhost:8080上建立websocket服务器以供我的世界connect/wssever指令连接
    :param 参数说明：
        Notes: 以 list[ list[ float我的世界playsound指令音调 , float延续时常（单位s） ] ] 格式存储的音符列表
        例如Musicreater.py的(dataset[0]['musics'][NowMusic]['notes'])
        Instrument: 播放的乐器
        speed: 用于控制播放速度，数值越大，播放速度越快，相当于把一秒变为几拍
        PlayerSelect: 执行的玩家选择器
        isProsess: 是否显示进度条
    :return None"""

    import time
    import fcwslib
    # import asyncio
    from nmcsup.log import log
    from nmcsup.vers import VER

    async def run_server(websocket):  # , path
        log('服务器连接创建')
        await fcwslib.tellraw(websocket, '已连接服务器——音·创' + VER[1] + VER[0] + ' 作者：金羿(W-YI)')
        length = len(Notes)
        j = 1
        for i in range(len(Notes)):
            await fcwslib.send_command(websocket,
                                       f'execute @a{PlayerSelect} ~ ~ ~ playsound {Instrument} @s ~ ~ ~ 1000 '
                                       f'{Notes[i][0]} 1000')
            if isProsess:
                await fcwslib.send_command(websocket,
                                           'execute @a' + PlayerSelect + ' ~ ~ ~ title @s actionbar §e▶  播放中：  §a' +
                                           str(
                                               j) + '/' + str(length) + '  ||  ' + str(int(j / length * 1000) / 10))
                j += 1
            time.sleep(Notes[i][1] / speed)

    fcwslib.run_server(run_server)


def note2RSworld(world: str, startpos: list, notes: list, instrument: str, speed: float = 2.5,
                 posadder: Iterable = (1, 0, 0), baseblock: str = 'stone'):  # -> bool
    """传入音符，生成以音符盒存储的红石音乐
    :param 参数说明：
        world: 地图文件的路径
        startpos: list[int,int,int] 开始生成的坐标
        notes: list[list[float,float]] 以 list[ list[ float我的世界playsound指令音调 , float延续时常（单位s） ] ]
        格式存储的音符列表 例如Musicreater.py的dataset[0]['musics'][NowMusic]['notes']
        instrument: 播放的乐器
        speed: 一拍占多少个中继器延迟(红石刻/rt)
        posadder: list[int,int,int] 坐标增加规律，即红石的延长时按照此增加规律增加坐标
        baseblock: 在中继器下垫着啥方块呢~
    :return 是否生成成功
    """

    from msctspt.values import height2note, instuments

    def formNoteBlock(note: int, instrument1: str = 'note.harp', powered: bool = False):
        """生成音符盒方块
        :param powered:
        :param instrument1:
        :param note: 0~24
        :return Block()"""
        if powered:
            powered = 'true'
        else:
            powered = 'false'
        return Block('universal_minecraft', 'notebooks',
                     {"instrument": ts(instrument1.replace("note.", '')), 'note': ts(str(note)),
                      'powered': ts(powered)})

    def formRepeater(delay: int, facing: str, locked: bool = False, powered: bool = False):
        """生成中继器方块
        :param powered:
        :param locked:
        :param facing:
        :param delay: 1~4
        :return Block()"""
        if powered:
            powered = 'true'
        else:
            powered = 'false'
        if locked:
            locked = 'true'
        else:
            locked = 'false'
        return Block('universal_minecraft', 'repeater',
                     {"delay": ts(str(delay)), 'facing': ts(facing), 'locked': ts(locked), 'powered': ts(powered)})

    level = amulet.load_level(world)

    def setblock(block: Block, pos: list):
        """pos : list[int,int,int]"""
        cx, cz = bc2cc(pos[0], pos[2])
        chunk = level.get_chunk(cx, cz, "minecraft:overworld")
        offset_x, offset_z = pos[0] - 16 * cx, pos[2] - 16 * cz
        chunk.blocks[offset_x, pos[1], offset_z] = level.block_palette.get_add_block(block)
        chunk.changed = True

    # 1拍 x 2.5 rt
    def placeNoteBlock():
        for i in notes:
            error = True
            try:
                setblock(formNoteBlock(height2note[i[0]], instrument), [startpos[0], startpos[1] + 1, startpos[2]])
                setblock(Block("universal_minecraft", instuments[i[0]][1]), startpos)
                error = False
            except ValueError:
                log("无法放置音符：" + str(i) + '于' + str(startpos))
                setblock(Block("universal_minecraft", baseblock), startpos)
                setblock(Block("universal_minecraft", baseblock), [startpos[0], startpos[1] + 1, startpos[2]])
            finally:
                if error is True:
                    log("无法放置音符：" + str(i) + '于' + str(startpos))
                    setblock(Block("universal_minecraft", baseblock), startpos)
                    setblock(Block("universal_minecraft", baseblock), [startpos[0], startpos[1] + 1, startpos[2]])
            delay = int(i[1] * speed + 0.5)
            if delay <= 4:
                startpos[0] += 1
                setblock(formRepeater(delay, 'west'), [startpos[0], startpos[1] + 1, startpos[2]])
                setblock(Block("universal_minecraft", baseblock), startpos)
            else:
                for j in range(int(delay / 4)):
                    startpos[0] += 1
                    setblock(formRepeater(4, 'west'), [startpos[0], startpos[1] + 1, startpos[2]])
                    setblock(Block("universal_minecraft", baseblock), startpos)
                if delay % 4 != 0:
                    startpos[0] += 1
                    setblock(formRepeater(delay % 4, 'west'), [startpos[0], startpos[1] + 1, startpos[2]])
                    setblock(Block("universal_minecraft", baseblock), startpos)
            startpos[0] += posadder[0]
            startpos[1] += posadder[1]
            startpos[2] += posadder[2]

    # e = True
    try:
        placeNoteBlock()
        # e = False
    except:  # ValueError
        log("无法放置方块了，可能是因为区块未加载叭")
    # finally:
    #     if e:
    #         log("无法放置方块了，可能是因为区块未加载叭")
    level.save()
    level.close()


class ryStruct:

    def __init__(self, world: str) -> None:

        self.RyStruct = dict()
        self._world = world
        self._level = amulet.load_level(world)

    def reloadLevel(self):
        # e = True
        try:
            self._level = amulet.load_level(self.world)
            # e = False
        except:  # ValueError
            log("无法重载地图")
        # finally:
        #     if e:
        #         log("无法重载地图")

    def closeLevel(self):
        # e = True
        try:
            self._level.close()
            # e = False
        except:  # ValueError
            log("无法关闭地图")
        # finally:
        #     if e:
        #         log("无法重载地图")

    def world2Rys(self, startp: list, endp: list, includeAir: bool = False):
        """将世界转换为RyStruct字典，注意，此函数运行成功后将关闭地图，若要打开需要运行 reloadLevel
        :param startp: [x,y,z] 转化的起始坐标
        :param endp  : [x,y,z] 转换的终止坐标，注意，终止坐标需要大于起始坐标，且最终结果包含终止坐标
        :param includeAir : bool = False 是否包含空气，即空气是否在生成之时覆盖地图内容
        :return dict RyStruct """

        level = self._level

        for x in range(startp[0], endp[0] + 1):
            for y in range(startp[1], endp[1] + 1):
                for z in range(startp[2], endp[2] + 1):

                    RyStructBlock = dict()

                    cx, cz = bc2cc(x, z)
                    chunk = level.get_chunk(cx, cz, "minecraft:overworld")
                    universal_block = chunk.block_palette[chunk.blocks[x - 16 * cx, y, z - 16 * cz]]
                    if universal_block == Block("universal_minecraft", "air") and includeAir:
                        continue
                    universal_block_entity = chunk.block_entities.get((x, y, z), None)

                    RyStructBlock["block"] = str(universal_block)
                    RyStructBlock["blockEntity"] = str(universal_block_entity)

                    log("载入方块数据" + str(RyStructBlock))

                    self.RyStruct[(x, y, z)] = RyStructBlock

        level.close()

        return self.RyStruct


"""
RyStruct = {
    (0,0,0) = {
        "block": str 完整的方块结构
        "blockEntity": str | 'None'
    }
}
"""
