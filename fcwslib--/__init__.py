#!/usr/bin/python
# -*- coding: utf-8 -*-

__version__ = '0.0.1'
__all__ = ['run_server', 'subscribe', 'unsubscribe', 'send_command', 'tellraw']
__author__ = 'Fuckcraft <https://gitee.com/fuckcraft>'

import os
import json
import uuid
import logging
import asyncio
import time
import websockets

# 写这段代码的时候，只有我和上帝知道这段代码是干什么的。
# 现在只有上帝知道。

# 此函数用于向 Minecraft 订阅请求
async def subscribe(websocket, event_name):
    '''
    参数:
    : websocket  : websocket 对象 :
    : event_name : 需要订阅的请求 :

    返回:
    None
    '''

    response = {
            'body': {
                'eventName': str(event_name)  # 示例：PlayerMessage
            },
            'header': {
                'requestId': str(uuid.uuid4()),
                'messagePurpose': 'subscribe',
                'version': 1,
                'messageType': 'commandRequest'
            }
        }

    # 增加 json 的可读性
    # response = json.dumps(response, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False)
    response = json.dumps(response)
    
    await websocket.send(response)

# 此函数用于向 Minecraft 消除订阅请求
async def unsubscribe(webscket):
    '''
    参数:
    : websocket  : websocket 对象     :
    : event_name : 需要消除订阅的请求 :

    返回:
    None
    '''

    response = {
            "body": {
                "eventName": str(event_name)  # PlayerMessage
            },
            "header": {
                "requestId": str(uuid.uuid4()),
                "messagePurpose": "unsubscribe",
                "version": 1,
                "messageType": "commandRequest"
            }
        }
    
    # 增加 json 的可读性
    # response = json.dumps(response, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False)
    response = json.dumps(response)

    await websocket.send(response)

# 此函数用于向 Minecraft 执行命令
async def send_command(websocket, command):
    '''
    参数:
    : websocket : websocket 对象 :
    : command   : 执行的命令     :

    返回:
    None
    '''

    response = {
            'body': {
                'origin': {
                    'type': 'player'
                },
                'commandLine': str(command),
                'version': 1
            },
            'header': {
                'requestId': str(uuid.uuid4()),
                'messagePurpose': 'commandRequest',
                'version': 1,
                'messageType': 'commandRequest'
            }
        }

    # 增加 json 的可读性
    # response = json.dumps(response, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False)
    response = json.dumps(response)

    await websocket.send(response)

# 此函数用于向 Minecraft 发送消息
async def tellraw(websocket, message):
    '''
    参数:
    : websocket : websocket 对象 :
    : message   : 发送的消息     :

    返回:
    None
    '''

    command = {
            'rawtext':[
                {
                    'text':'[{}] {}'.format(time.asctime(), message)
                }
            ]
        }

    # 增加 json 可读性
    # command = json.dumps(command, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False)
    command = json.dumps(command)
    command = 'tellraw @a {}'.format(command)

    await send_command(websocket, command)

def run_server(function):
    # 修改 ip 地址和端口
    start_server = websockets.serve(function, 'localhost', 8080)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

