# -*- coding: utf-8 -*-


# 音·创 开发交流群 861684859
# Email EillesWan2006@163.com W-YI_DoctorYI@outlook.com EillesWan@outlook.com
# 版权所有 金羿("Eilles Wan") & 诸葛亮与八卦阵("bgArray") & 鸣凤鸽子("MingFengPigeon")
# 若需转载或借鉴 许可声明请查看仓库目录下的 Lisence.md


"""
音·创 库版 MIDI转换示例程序
Musicreater Package Version : Demo for Midi Conversion

Copyright 2023 all the developers of Musicreater

开源相关声明请见 ./Lisence.md
Terms & Conditions: ./Lisence.md
"""

languages = {
    "ZH_CN": {
        "MSCT": "音·创",
        "ChooseLang": "选择语言",
        "LangChd": "当前语言已经切换为",
        "ZH_CN": "简体中文",
        "ZH_TW": "繁体中文（台湾）",
        "EN_GB": "英语（英国）",
        "EN_US": "英语（美国）",
        ":": "：",
        ",": "，",
        ".": "。",
        "ChooseFileFormat": "请输入输出格式[BDX(1)或MCPACK(0)]",
        "ChoosePlayer": "请选择播放方式[计分板(1) 或 延迟(0)]",
        "ChoosePath": "请输入MIDI路径或所在文件夹",
        "WhetherArgEntering": "是否为文件夹内文件的转换统一参数[是(1) 或 否(0)]",
        "EnterArgs": "请输入转换参数",
        "noteofArgs": "注：文件夹内的全部midi将统一以此参数转换",
        "EnterVolume": "请输入音量大小(0~1)",
        "EnterSpeed": "请输入速度倍率",
        "WhetherPgb": "是否自动生成进度条[是(1) 或 否(0)]",
        "WhetherCstmProgressBar": "是否自定义进度条[是(1) 或 否(0)]",
        "EnterProgressBarStyle": "请输入进度条样式",
        "EnterSbName": "请输入计分板名称",
        "EnterSelecter": "请输入播放者选择器",
        "WhetherSbReset": "是否自动重置计分板[是(1) 或 否(0)]",
        "EnterAuthor": "请输入作者",
        "EnterMaxHeight": "请输入指令结构最大生成高度",
        "ErrEnter": "输入错误",
        "Re-Enter": "请重新输入",
        "Dealing": "正在处理",
        "FileNotFound": "文件(夹)不存在",
        "ChooseOutPath": "请输入结果输出路径",
        "Saying": "言·论",
        "Failed": "失败",
        "CmdLength": "指令数量",
        "MaxDelay": "曲目时间(游戏刻)",
        "PlaceSize": "结构占用大小",
        "LastPos": "最末方块坐标",
        "PressEnterExit": "请按下回车键退出。",
    }
}


import sys

if sys.argv.__len__() > 0:
    currentLang = sys.argv[0]
    if not currentLang in languages.keys():
        currentLang = "ZH_CN"
else:
    currentLang = "ZH_CN"


def _(__):
    '''
    `languages`
    '''
    return languages[currentLang][__]


import os
import random
import datetime

try:
    import msctPkgver
except ModuleNotFoundError as E:
    if input("您需要安装 mido、Brotli 模块才能使用这个样例\n请问是否安装？(y/n)：").lower() in ('y', '1'):
        os.system("pip install -r requirements.txt")
        import msctPkgver
    else:
        raise E

try:
    from msctPkgver.magicBeing import *
    import requests
    # import zhdate
except ModuleNotFoundError as E:
    if input(
        "您需要安装以下模块才能使用这个样例\nrequests==2.28.1\nrich==12.6.0\nzhdate==0.1\n请问是否安装？(y/n)："
    ).lower() in ('y', '1'):
        open("Demo_Requirements.txt", 'w').write(
            "requests==2.28.1\nrich==12.6.0\nzhdate==0.1"
        )
        os.system("pip install -r Demo_Requirements.txt")
        os.remove("./Demo_Requirements.txt")
        from rich.console import Console
        import requests
        import zhdate
    else:
        raise E



MainConsole.print(
    "[#121110 on #F0F2F4]     ",
    style="#121110 on #F0F2F4",
    justify="center",
)


# 显示大标题
MainConsole.rule(title="[bold #AB70FF]欢迎使用音·创独立转换器", characters="=", style="#26E2FF")
MainConsole.rule(
    title="[bold #AB70FF]Welcome to Independent Musicreater Convernter", characters="-"
)

nowYang = datetime.datetime.now()

if nowYang.month == 8 and nowYang.day == 6:
    # 诸葛八卦生日
    MainConsole.print(
        "[#7DB5F0 on #121110]今天可不是催更的日子！\n诸葛亮与八卦阵{}岁生日快乐！".format(nowYang.year - 2009),
        style="#7DB5F0 on #121110",
        justify="center",
    )
elif nowYang.month == 4 and nowYang.day == 3:
    # 金羿生日快乐
    MainConsole.print(
        "[#0089F2 on #F0F2F4]今天就不要催更啦！\n金羿{}岁生日快乐！".format(nowYang.year - 2006),
        style="#0089F2 on #F0F2F4",
        justify="center",
    )
else:
    # 显示箴言部分
    MainConsole.print(
        "[#121110 on #F0F2F4]{}".format(
            random.choice(
                requests.get(
                    'https://gitee.com/EillesWan/Musicreater/raw/master/resources/myWords.txt'
                )
                .text.strip('\r\n')
                .split('\r\n')
            )
        ),
        style="#121110 on #F0F2F4",
        justify="center",
    )

prt(f"{_('LangChd')}{_(':')}{_(currentLang)}")

def formatipt(
    notice: str,
    fun,
    errnote: str = f"{_('ErrEnter')}{_(',')}{_('Re-Enter')}{_('.')}",
    *extraArg,
):
    '''循环输入，以某种格式
    notice: 输入时的提示
    fun: 格式函数
    errnote: 输入不符格式时的提示
    *extraArg: 对于函数的其他参数'''
    while True:
        result = ipt(notice)
        try:
            funresult = fun(result, *extraArg)
            break
        except:
            prt(errnote)
            continue
    return result, funresult
    

# 获取midi列表
while True:
    midipath = ipt(f"{_('ChoosePath')}{_(':')}").lower()
    if os.path.exists(midipath):
        if os.path.isfile(midipath):
            midis = (midipath,)
        elif os.path.isdir(midipath):
            midis = tuple(
                (
                    os.path.join(midipath, i)
                    for i in os.listdir(midipath)
                    if i.lower().endswith('.mid') or i.lower().endswith('.midi')
                )
            )
        else:
            prt(f"{_('ErrEnter')}{_(',')}{_('Re-Enter')}{_('.')}")
            continue
    else:
        prt(f"{_('FileNotFound')}{_(',')}{_('Re-Enter')}{_('.')}")
        continue
    break

# 获取输出地址
outpath = formatipt(
    f"{_('ChooseOutPath')}{_(':')}",
    os.path.exists,
    f"{_('FileNotFound')}{_(',')}{_('Re-Enter')}{_('.')}",
)[0].lower()


# 选择输出格式
while True:
    fileFormat = ipt(f"{_('ChooseFileFormat')}{_(':')}").lower()
    if fileFormat in ('0', 'mcpack'):
        fileFormat = 0
        playerFormat = 1
        break

    elif fileFormat in ('1', 'bdx'):
        fileFormat = 1
        while True:
            playerFormat = ipt(f"{_('ChoosePlayer')}{_(':')}").lower()
            if playerFormat in ('0', '延迟', 'delay'):
                playerFormat = 0
            elif playerFormat in ('1', '计分板', 'scoreboard'):
                playerFormat = 1
            else:
                prt(f"{_('ErrEnter')}{_(',')}{_('Re-Enter')}{_('.')}")
                continue
            break
    else:
        prt(f"{_('ErrEnter')}{_(',')}{_('Re-Enter')}{_('.')}")
        continue
    break

debug = False
# 真假字符串判断
def boolstr(sth: str) -> bool:
    try:
        return bool(int(sth))
    except:
        if str(sth).lower() == 'true':
            return True
        elif str(sth).lower() == 'false':
            return False
        else:
            raise "布尔字符串啊？"

if os.path.exists("./demo_config.json"):
    import json
    prompts = json.load(open("./demo_config.json",'r',encoding="utf-8"))
    if prompts[-1] == "debug":
        debug = True
    prompts = prompts[:-1]
else:
    prompts = []
    # 提示语 检测函数 错误提示语
    for args in [
        (
            f'{_("EnterVolume")}{_(":")}',
            float,
        ),
        (
            f'{_("EnterSpeed")}{_(":")}',
            float,
        ),
        (
            f'{_("WhetherPgb")}{_(":")}',
            boolstr,
        ),
        (
            f'{_("EnterSbName")}{_(":")}',
            str,
        )
        if playerFormat == 1
        else (
            f'{_("EnterSelecter")}{_(":")}',
            str,
        ),
        (
            f'{_("WhetherSbReset")}{_(":")}',
            boolstr,
        )
        if playerFormat == 1
        else (),
        (
            f'{_("EnterAuthor")}{_(":")}',
            str,
        )
        if fileFormat == 1
        else (),
        (
            f'{_("EnterMaxHeight")}{_(":")}',
            int,
        )
        if fileFormat == 1
        else (),
    ]:
        if args:
            prompts.append(formatipt(*args)[1])






conversion = msctPkgver.midiConvert(debug)
for singleMidi in midis:
    prt("\n"f"{_('Dealing')} {singleMidi} {_(':')}")
    conversion.convert(singleMidi, outpath)
    if debug:
        with open("./records.json",'a',encoding="utf-8") as f:
            json.dump(conversion.toDICT(),f)
            f.write(5*"\n")
    conversion_result = (
        conversion.tomcpack(2, *prompts)
        if fileFormat == 0
        else (
            conversion.toBDXfile(2, *prompts)
            if playerFormat == 1
            else conversion.toBDXfile_withDelay(2, *prompts)
        )
    )
    
    if conversion_result[0]:
        prt(
            f"	{_('CmdLength')}{_(':')}{conversion_result[1]}{_(',')}{_('MaxDelay')}{_(':')}{conversion_result[2]}{f'''{_(',')}{_('PlaceSize')}{_(':')}{conversion_result[3]}{_(',')}{_('LastPos')}{_(':')}{conversion_result[4]}''' if fileFormat == 1 else ''}"
        )
    else:
        prt(f"{_('Failed')}")


exitSth = ipt(_("PressEnterExit")).lower()
if exitSth == "record":
    import json
    with open("./demo_config.json",'w',encoding="utf-8") as f:
        json.dump(prompts,f)
elif exitSth == "delrec":
    os.remove("./demo_config.json")
