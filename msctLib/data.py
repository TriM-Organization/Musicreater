# -*- coding:utf-8 -*-


import pickle
import json
from typing import Any, Iterable




class pickleIO:

    def __init__(self,fileName:str,data: Any = None) -> None:
        '''简单的pickle操作功能'''
        self.file = fileName
        if data:
            self._data = data
        else:
            with open (self.file, 'rb') as f: 
                self._data = pickle.load(f)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.data

    def write(self):
        '''将数据写入pickle'''
        with open (self.file, 'wb') as f: 
            pickle.dump(self._data, f) 


    def load(self) -> Any:
        '''从文件读取数据'''
        with open (self.file, 'rb') as f: 
            self._data = pickle.load(f)
        return self.data

    @property
    def data(self):
        '''返回数据值'''
        if self._data is None:
            raise ValueError('无可用值载入或值为None')
        else:
            return self._data



class jsonIO:

    def __init__(self,fileName:str,data: Any = None) -> None:
        '''简单的json操作功能'''
        self.file = fileName
        if data:
            self._data = data
        else:
            with open (self.file, 'r', encoding='utf-8') as f: 
                self._data = json.load(f)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.data

    def write(self):
        '''将数据写入json'''
        with open (self.file, 'w', encoding='utf-8') as f: 
            json.dump(self._data, f) 


    def load(self) -> Any:
        '''从文件读取数据'''
        with open (self.file, 'r', encoding='utf-8') as f: 
            self._data = json.load(f)
        return self.data

    @property
    def data(self):
        '''返回数据值'''
        return self._data


class uniteIO:

    def __init__(self,fileName:str,fileType = None,data: Any = None) -> None:
        '''简单的文件数据IO操作功能'''
        self.filename = fileName
        if not fileType is None:
            self._type = fileType
        else:
            try:
                with open (self.filename, 'r', encoding='utf-8') as f: 
                    self._type = json
            except:
                with open (self.file, 'rb') as f: 
                    self._type = pickle



        if not data is None:
            self._data = data
        else:
            self._data = self.load()
    

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.data

    def write(self):
        '''将数据写入文件'''
        if self._type == json:
            self._wfile = open(self.filename, 'w', encoding='utf-8')
        elif self._type == pickle:
            self._wfile = open(self.file, 'wb')
        self._type.dump(self._data, self._wfile) 


    def load(self) -> Any:
        '''从文件读取数据'''
        if self._type == json:
            self._rfile = open(self.filename, 'r', encoding='utf-8')
        elif self._type == pickle:
            self._rfile = open(self.file, 'rb')
        self._data = self._type.load(self._rfile)
        return self.data

    @property
    def data(self):
        '''返回数据值'''
        return self._data


if __name__ == '__main__':
    from sys import argv

    if argv[1]:
        input(uniteIO(argv[1]).data)