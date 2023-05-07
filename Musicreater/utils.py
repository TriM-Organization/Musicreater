'''
存放主程序所必须的功能性内容
'''


def mctick2timestr(mc_tick: int):
    """
    将《我的世界》的游戏刻计转为表示时间的字符串
    """
    return str(int(int(mc_tick / 20) / 60)) + ":" + str(int(int(mc_tick / 20) % 60))


def empty_midi_channels(channel_count: int = 17) -> dict:
    """
    空MIDI通道字典
    """
    return dict((i, {}) for i in range(channel_count))
