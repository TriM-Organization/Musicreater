# -*- coding:utf-8 -*-


DEFAULTLANGUAGE = 'en-GB'


LANGUAGELIST = {
    'zh-CN':(
        "简体中文 中国大陆",
        "Simplified Chinese, China Mainland",
    ),
    'en-GB':(
        "英式英语 大不列颠",
        "British English, Great Britain",
    ),
}

if DEFAULTLANGUAGE == 'zh-CN':
    from languages.zhCN import READABLETEXT
elif DEFAULTLANGUAGE == 'en-GB':
    from languages.enGB import READABLETEXT


