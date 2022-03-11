# -*- coding:utf-8 -*-
'''对于音·创的语言支持兼语言文件编辑器'''

DEFAULTLANGUAGE = 'zh-CN'

LANGUAGELIST = {
    # 第一个是语言的中文名称和地区
    # 第二个是语言的英文名称和地区
    # 第三个是语言的本地名称和地区
    'zh-CN': (
        "简体中文 中国大陆",
        "Simplified Chinese, Chinese Mainland",
        "简体中文 中国大陆",
    ),
    'zh-TW': (
        "繁体中文 台湾省",
        "Traditional Chinese, Taiwan Province",
        "正體中文,台灣省",
    ),
    # 'zh-HK': (
    #     "简体中文 中国大陆",
    #     "Traditional Chinese, the Hong Kong Special Administrative Region",
    #     "繁體中文,香港特別行政區",
    # ),
    # 'zh-MO': (
    #     "简体中文 中国大陆",
    #     "Traditional Chinese, the Macao Special Administrative Region",
    #     "繁體中文,澳門特別行政區",
    # ),
    'en-GB': (
        "英语 英国",
        "British English, the United Kingdom",
        "British English, the United Kingdom",
    ),
}

# 对于旧版本音·创的语言支持
# 重构之后将停止使用
from languages.zhCN import READABLETEXT

if DEFAULTLANGUAGE in LANGUAGELIST.keys():
    with open('./languages/'+DEFAULTLANGUAGE+'.lang','r',encoding='utf-8') as languageFile :
        _text = []
        for line in languageFile:
            _text.append(line)
    _TEXT = _text.copy()
else:
    raise KeyError(f"无法打开默认语言{DEFAULTLANGUAGE}")




if __name__ == '__main__':
    # 启动语言编辑器
    import tkinter as tk

    root = tk.Tk()

    root.geometry('900x600')





