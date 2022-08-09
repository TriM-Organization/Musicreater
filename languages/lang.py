# -*- coding:utf-8 -*-
'''对于音·创的语言支持兼语言文件编辑器'''

"""
   Copyright 2022 all the developers of Musicreater

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
        "Simplified Chinese - China Mainland",
        "简体中文 中国大陆",
    ),
    'zh-TW': (
        "繁体中文 中国台湾省",
        "Traditional Chinese - Taiwan Province, China",
        "正體中文,中国台灣省",
    ),
    # 'zh-HK': (
    #     "繁体中文 香港",
    #     "Traditional Chinese - Hong Kong SAR",
    #     "繁體中文,香港特別行政區",
    # ),
    # 'zh-MO': (
    #     "繁体中文 澳门",
    #     "Traditional Chinese - Macau SAR",
    #     "繁體中文,澳門特別行政區",
    # ),
    'en-GB': (
        "英语 英国",
        "British English - the United Kingdom",
        "British English - the United Kingdom",
    ),
    'zh-ME' : (
        "喵喵文 中国大陆",
        "Meow Catsnese - China Mainland"
        "喵喵喵~ 种花家~"
    )
}


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
    # print(_text)
    return _text



if DEFAULTLANGUAGE in LANGUAGELIST.keys():
    _TEXT = __loadLanguage('./languages/' + DEFAULTLANGUAGE + '.lang')
else:
    log(f"无法打开当前本地化文本{DEFAULTLANGUAGE}", level='ERROR')
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
            log(f'无法找到本地化文本{text}','WARRING')
            return ''


