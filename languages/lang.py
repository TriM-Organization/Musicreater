# -*- coding:utf-8 -*-
'''对于音·创的语言支持兼语言文件编辑器'''

"""
   Copyright 2022 Team-Ryoun

   Licensed under the Apache License, Version 2.0 (the 'License');
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an 'AS IS' BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

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
    #     "繁体中文 香港",
    #     "Traditional Chinese, the Hong Kong Special Administrative Region",
    #     "繁體中文,香港特別行政區",
    # ),
    # 'zh-MO': (
    #     "繁体中文 澳门",
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


from msctLib.log import log

def __loadLanguage(languageFilename: str):
    with open(languageFilename, 'r', encoding='utf-8') as languageFile:
        _text = {}
        for line in languageFile:
            if line.startswith('#'):
                continue
            line = line.split(' ', 1)
            _text[line[0]] = line[1].replace('\n', '')
    langkeys = _text.keys()
    with open(languageFilename.replace(languageFilename[-10:-5], 'zh-CN'), 'r', encoding='utf-8') as defaultLangFile:
        for line in defaultLangFile:
            if line.startswith('#'):
                continue
            line = line.split(' ', 1)
            if not line[0] in langkeys:
                _text[line[0]] = line[1].replace('\n', '')
                from msctLib.log import log
                log(f'丢失对于 {line[0]} 的本地化文本', 'WARRING')
                langkeys = _text.keys()
    return _text


if not DEFAULTLANGUAGE == 'zh-CN':
    if DEFAULTLANGUAGE in LANGUAGELIST.keys():
        _TEXT = __loadLanguage('./languages/' + DEFAULTLANGUAGE + '.lang')
    else:
        raise KeyError(f'无法打开默认语言{DEFAULTLANGUAGE}')


def wordTranslate(singleWord: str, debug: bool = False):
    import requests
    try:
        return \
            requests.post('https://fanyi.baidu.com/sug', data={'kw': f'{singleWord}'}).json()['data'][0]['v'].split(
                '; ')[0]
    except:
        log(f"无法翻译文本{singleWord}", level='WARRING', isPrinted=debug)
        return None


def _(text: str, debug: bool = False):
    try:
        return _TEXT[text]
    except:
        if debug:
            raise KeyError(f'无法找到翻译文本{text}')
        else:
            log(f'无法找到本地化文本{text}','ERROR')
            return ''


if __name__ == '__main__':
    # 启动语言编辑器
    import tkinter as tk
    from tkinter.filedialog import askopenfilename as askfilen

    LANGNAME = _('LANGLOCALNAME')


    def _changeDefaultLang():
        global _TEXT
        global DEFAULTLANGUAGE

        fileName = askfilen(title='选择所翻译的语言文件', initialdir=r'./',
                            filetypes=[('音·创语言文件', '.lang'), ('所有文件', '*')],
                            defaultextension='.lang',
                            initialfile='.lang')
        _TEXT = __loadLanguage(fileName)
        DEFAULTLANGUAGE = _('LANGKEY')
        LANGNAME = _('LANGLOCALNAME')

        orignText = ''
        transText = ''
        for i, j in _TEXT.items():
            orignText += i + '\n'
            transText += j + '\n'

        Origntextbar.insert('end', orignText)
        Translatetextbar.insert('end', transText)

        global setlangbutton
        setlangbutton['text'] = f'对标语言{LANGNAME}'


    def _autoSave(event=None):
        with open('autosave.tmp.txt', 'w', encoding='utf-8') as f:
            f.write(Translatetextbar.get(1.0, 'end'))
        print(str(event))


    root = tk.Tk()

    root.geometry('600x500')

    root.bind("<Motion>", _autoSave)

    nowText = ''

    Orignrame = tk.Frame(root, bd=2)
    Translaterame = tk.Frame(root, bd=2)

    Orignscrollbar = tk.Scrollbar(Orignrame)
    Origntextbar = tk.Text(Orignrame, width=35, height=40)

    Translatetextbar = tk.Text(Translaterame, width=40, height=37, undo=True)
    Translatescrollbar = tk.Scrollbar(Translaterame)

    def ctrlZ():
        Translatetextbar.edit_undo()
    Translatetextbar.bind("<Control-z>", ctrlZ)

    def ctrlY():
        Translatetextbar.edit_redo()
    Translatetextbar.bind("<Control-y>", ctrlY)

    tk.Button(Translaterame, text='保存', command=_autoSave).pack(side='bottom', fill='x')

    tk.Label(Orignrame, text='中文原文').pack(side='top')
    Origntextbar.pack(side='left', fill='y')
    Orignscrollbar.pack(side='left', fill='y')

    setlangbutton = tk.Button(Translaterame, text=f'对标语言{LANGNAME}', command=_changeDefaultLang)
    setlangbutton.pack(side='top')
    Translatescrollbar.pack(side='right', fill='y')
    Translatetextbar.pack(side='right', fill='y')

    Orignscrollbar.config(command=Origntextbar.yview)
    Origntextbar.config(yscrollcommand=Orignscrollbar.set)

    Translatescrollbar.config(command=Translatetextbar.yview)
    Translatetextbar.config(yscrollcommand=Translatescrollbar.set)

    Orignrame.pack(side='left')
    Translaterame.pack(side='right')

    tk.mainloop()
