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
try:
    from languages.zhCN import READABLETEXT
except:
    pass

try:
    from msctLib.log import log
except:
    pass


if not DEFAULTLANGUAGE == 'zh-CN':
    if DEFAULTLANGUAGE in LANGUAGELIST.keys():
        with open('./languages/'+DEFAULTLANGUAGE+'.lang','r',encoding='utf-8') as languageFile :
            _text = {}
            for line in languageFile:
                line = line.split(' ')
                _text.append[line[0]] = line[1]
        langkeys = _text.keys()
        with open('./languages/zh-CN.lang','r',encoding='utf-8') as defaultLangFile:
            for line in defaultLangFile:
                line = line.split(' ')
                if not line[0] in langkeys:
                    _text[line[0]] = line[1]
                    log(f'丢失对于 {line[0]} 的本地化文本','WARRING')
                    langkeys = _text.keys()
        _TEXT = _text.copy()
    else:
        raise KeyError(f'无法打开默认语言{DEFAULTLANGUAGE}')



def wordTranslate(singleWord:str,debug: bool = False):
    import requests
    try:
        return requests.post('https://fanyi.baidu.com/sug', data={'kw': f'{singleWord}'}).json()['data'][0]['v'].split('; ')[0]
    except:
        log(f"无法翻译文本{singleWord}",level='WARRING',isPrinted=debug)
        return None







def _(text:str):
    try:
        return _TEXT[text]
    except:
        raise KeyError(f'无法找到翻译文本{text}')





if __name__ == '__main__':
    # 启动语言编辑器
    import tkinter as tk

    root = tk.Tk()

    root.geometry('900x600')

    Orignrame = tk.Frame(root)
    Translaterame = tk.Frame(root)


    Orignscrollbar = tk.Scrollbar(Orignrame)
    Origntextbar = tk.Text(Orignrame)


    Translatetextbar = tk.Text(Translaterame)
    Translatescrollbar = tk.Scrollbar(Translaterame)

    Origntextbar.pack(side='left', fill='y')
    Orignscrollbar.pack(side='left', fill='y')
    
    Translatescrollbar.pack(side='right', fill='y')
    Translatetextbar.pack(side='right', fill='y')

    Orignscrollbar.config(command=Origntextbar.yview)
    Origntextbar.config(yscrollcommand=Orignscrollbar.set)

    
    Translatescrollbar.config(command=Translatetextbar.yview)
    Translatetextbar.config(yscrollcommand=Translatescrollbar.set)



    Origntextbar.insert('end', 'TEST')

    tk.mainloop(  )






