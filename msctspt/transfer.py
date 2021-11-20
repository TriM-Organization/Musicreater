"""音·创 的转换工具库"""








def hans2pinyin(hans,style=3):
    """将汉字字符串转化为拼音字符串"""
    from pypinyin import lazy_pinyin
    result = lazy_pinyin(hans=hans,style=style)
    final = ''
    for i in result:
        final += i;
    return final




def formCmdBlock(direction:list,command:str,particularValue:int,impluse:int,condition:bool=False,needRedstone:bool=True,tickDelay:int=0,customName:str='',lastOutput:str='',executeOnFirstTick:bool=False,trackOutput:bool=True):
    """
    使用指定项目返回指定的指令方块格式字典
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
    :return: 指令方块字典结构
    """
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




def note2bdx(filePath:str,dire:list,Notes : list,ScoreboardName:str,Instrument:str, PlayerSelect:str='',isProsess:bool=False) :
    '''使用方法同Note2Cmd
    :param 参数说明：
        filePath: 生成.bdx文件的位置
        dire: 指令方块在地图中生成的起始位置（相对位置）
        Notes: 以 list[ list[ float我的世界playsound指令音调 , float延续时常（单位s） ] ] 格式存储的音符列表 例如Musicreater.py的(dataset[0]['musics'][NowMusic]['notes'])
        ScoreboardName: 用于执行的计分板名称
        Instrument: 播放的乐器
        PlayerSelect: 执行的玩家选择器
        isProsess: 是否显示进度条（会很卡）
    :return 返回一个BdxConverter类（实际上没研究过），同时在指定位置生成.bdx文件'''


    from msctspt.transfer import formCmdBlock
    from nmcsup.trans import Note2Cmd
    from msctspt.bdxOpera_CP import BdxConverter
    cmd = Note2Cmd(Notes,ScoreboardName,Instrument, PlayerSelect,isProsess)
    cdl = []
    for i in cmd:
        try:
            if (i[:i.index('#')].replace(' ','') != '\n') and(i[:i.index('#')].replace(' ','') != ''):
                cdl.append(i[:i.index('#')])
        except:
            cdl.append(i)
    i = 0
    down = False
    blocks = [formCmdBlock(dire,cdl.pop(0),1,1)]
    dire[1]+=1;
    for j in cdl:
        if dire[1]+i > 200:
            dire[0]+=1
            i=0
            down = not down
        if dire[1]+i == 200 :
            blocks.append(formCmdBlock([dire[0],dire[1]+i,dire[2]],j,5,2,False,False))
        else:
            if down:
                blocks.append(formCmdBlock([dire[0],dire[1]+i,dire[2]],j,0,2,False,False))
            else:
                blocks.append(formCmdBlock([dire[0],dire[1]+i,dire[2]],j,1,2,False,False))
        i+=1
    del i, cdl, down, cmd
    return BdxConverter(filePath,'RyounMusicreater',blocks)




def note2webs(Notes : list,Instrument:str, speed:float = 5.0, PlayerSelect:str='',isProsess:bool=False) :
    '''传入音符，在oaclhost:8080上建立websocket服务器以供我的世界connect/wssever指令连接
    :param 参数说明：
        Notes: 以 list[ list[ float我的世界playsound指令音调 , float延续时常（单位s） ] ] 格式存储的音符列表 例如Musicreater.py的(dataset[0]['musics'][NowMusic]['notes'])
        Instrument: 播放的乐器
        speed: 用于控制播放速度，数值越大，播放速度越快，相当于把一秒变为几拍
        PlayerSelect: 执行的玩家选择器
        isProsess: 是否显示进度条
    :return None'''
    
    import time
    import fcwslib
    import asyncio
    from nmcsup.log import log
    from nmcsup.vers import VER

    async def run_server(websocket, path):
        log('服务器连接创建')
        await fcwslib.tellraw(websocket, '已连接服务器——音·创'+VER[1]+VER[0]+' 作者：金羿(W-YI)')
        if isProsess:
            length = len(Notes)
            j = 1;
        for i in range(len(Notes)):
            await fcwslib.send_command(websocket,'execute @a'+PlayerSelect+' ~ ~ ~ playsound '+Instrument+' @s ~ ~ ~ 1000 '+str(Notes[i][0])+' 1000')
            if isProsess:
                fcwslib.send_command(websocket,'execute @a'+PlayerSelect+' ~ ~ ~ title @s actionbar §e▶  播放中：  §a'+str(j)+'/'+str(length)+'  ||  '+str(int(j/length*1000)/10))
                j+=1;
            time.sleep(Notes[i][1]/speed)

    fcwslib.run_server(run_server)








def note2RSworld(world:str,startpos:list,notes:list,instrument:str,speed:float = 2.5,posadder:list = [1,0,0],baseblock:str = 'stone') -> bool:
    '''传入音符，生成以音符盒存储的红石音乐
    :param 参数说明：
        world: 地图文件的路径
        startpos: list[int,int,int] 开始生成的坐标
        notes: list[list[float,float]] 以 list[ list[ float我的世界playsound指令音调 , float延续时常（单位s） ] ] 格式存储的音符列表 例如Musicreater.py的dataset[0]['musics'][NowMusic]['notes']
        instrument: 播放的乐器
        speed: 一拍占多少个中继器延迟(红石刻/rt)
        posadder: list[int,int,int] 坐标增加规律，即红石的延长时按照此增加规律增加坐标
        baseblock: 在中继器下垫着啥方块呢~
    :return 是否生成成功
    '''
    import amulet
    from amulet.api.block import Block
    from amulet.utils.world_utils import block_coords_to_chunk_coords as bc2cc
    from amulet_nbt import TAG_String as ts

    from msctspt.values import height2note,instuments
    from nmcsup.log import log

    def formNoteBlock(note:int,instrument:str='note.harp',powered:bool = False):
        '''生成音符盒方块
        :param note: 0~24
        :return Block()'''
        if powered:
            powered = 'true';
        else:
            powered = 'false';
        return Block('universal_minecraft','noteblock',{"instrument":ts(instrument.replace("note.",'')),'note':ts(str(note)),'powered':ts(powered)})
    
    def formRepeater(delay:int,facing:str,locked:bool=False,powered:bool=False):
        '''生成中继器方块
        :param delay: 1~4
        :return Block()'''
        if powered:powered = 'true';
        else:powered = 'false';
        if locked:locked = 'true';
        else:locked = 'false';
        return Block('universal_minecraft','repeater',{"delay":ts(str(delay)),'facing':ts(facing),'locked':ts(locked),'powered':ts(powered)})
        
    
    level = amulet.load_level(world)

    def setblock(block:Block,pos:list):
        '''pos : list[int,int,int]'''
        cx, cz = bc2cc(pos[0], pos[2])
        chunk = level.get_chunk(cx, cz, "minecraft:overworld")
        offset_x, offset_z = pos[0] - 16 * cx, pos[2] - 16 * cz
        chunk.blocks[offset_x, pos[1], offset_z] = level.block_palette.get_add_block(block)
        chunk.changed = True

    # 1拍 x 2.5 rt
    def placeNoteBlock():
        for i in notes:
            try :
                setblock(formNoteBlock(height2note[i[0]],instrument),[startpos[0],startpos[1]+1,startpos[2]])
                setblock(Block("universal_minecraft",instuments[i[0]][1]),startpos)
            except :
                log("无法放置音符："+str(i)+'于'+str(startpos))
                setblock(Block("universal_minecraft",baseblock),startpos)
                setblock(Block("universal_minecraft",baseblock),[startpos[0],startpos[1]+1,startpos[2]])
            delay = int(i[1]*speed+0.5)
            if delay <= 4:
                startpos[0]+=1
                setblock(formRepeater(delay,'west'),[startpos[0],startpos[1]+1,startpos[2]])
                setblock(Block("universal_minecraft",baseblock),startpos)
            else:
                for i in range(int(delay/4)):
                    startpos[0]+=1
                    setblock(formRepeater(4,'west'),[startpos[0],startpos[1]+1,startpos[2]])
                    setblock(Block("universal_minecraft",baseblock),startpos)
                if delay % 4 != 0:
                    startpos[0]+=1
                    setblock(formRepeater(delay%4,'west'),[startpos[0],startpos[1]+1,startpos[2]])
                    setblock(Block("universal_minecraft",baseblock),startpos)
            startpos[0]+=posadder[0]
            startpos[1]+=posadder[1]
            startpos[2]+=posadder[2]
    try:
        placeNoteBlock()
    except:
        log("无法放置方块了，可能是因为区块未加载叭")
    level.save()
    level.close()
    