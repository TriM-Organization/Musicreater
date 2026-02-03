import asyncio
import copy
import json
import uuid

import websockets


class Server:
    sent_commands = {}
    subscribed_events = {}
    _plugins = []
    _connections = []

    def __init__(self, server='0.0.0.0', port=8000, debug_mode=False):
        self._server = server
        self._port = port
        self._debug_mode = debug_mode

    def handler(self):
        return copy.deepcopy(self._plugins)

    def add_plugin(self, plugin):
        if self._plugins:
            for connection in self._connections:
                plugin_ = plugin()
                asyncio.create_task(plugin_.on_connect())
                connection.append(plugin_)
        self._plugins.append(plugin)

    def remove_plugin(self, plugin):
        if self._connections:
            for connection in self._connections:
                for plugin_ in connection.plugins:
                    if isinstance(plugin_, plugin):
                        plugin_.remove(plugin_)
                    break
        self._plugins.remove(plugin)

    async def run_forever(self):
        self.running = True
        async with websockets.serve(self._on_connect, self._server, self._port):
            await asyncio.Future()

    async def _on_connect(self, websocket, path):
        plugins = []
        self._connections.append({
            "websocket": websocket,
            "path": path,
            "plugins": plugins,
        })
        for plugin in self._plugins:
            plugins.append(plugin(websocket, path, self, self._debug_mode))
        for plugin in plugins:
            asyncio.create_task(plugin.on_connect())
        while self.running:
            try:
                response = json.loads(await websocket.recv())
            except (websockets.exceptions.ConnectionClosedOK, websockets.exceptions.ConnectionClosedError):
                tasks = []
                for plugin in plugins:
                    tasks.append(plugin.on_disconnect())
                for task in tasks:
                    await task
                break
            else:
                message_purpose = response['header']['messagePurpose']
                if message_purpose == 'commandResponse':
                    request_id = response['header']['requestId']
                    if request_id in self.sent_commands:
                        asyncio.create_task(self.sent_commands[request_id](response))
                        del self.sent_commands[request_id]
                else:
                    try:
                        event_name = response['header']['eventName']
                        asyncio.create_task(self.subscribed_events[event_name](response))
                    except KeyError:
                        print("ERROR EVENT NAME:\n{}".format(response))

    async def disconnect(self, websocket: websockets.WebSocketServerProtocol):
        self.running = False
        await websocket.close_connection()
        for number in range(len(self._connections) - 1):
            connection = self._connections[number]
            if connection['websocket'] == websocket:
                del self._connections[number]


class Plugin:
    def __init__(self, websocket, path, server, debug_mode=False):
        self._websocket = websocket
        self._path = path
        self._server = server
        self._debug_mode = debug_mode

    async def on_connect(self):
        pass

    async def on_disconnect(self):
        pass

    async def on_receive(self, response):
        pass

    async def send_command(self, command, callback=None):
        request = {
            'body': {'commandLine': command},
            'header': build_header('commandRequest')
        }
        if callback:
            self._server.sent_commands[request['header']['requestId']] = callback
        await self._websocket.send(json.dumps(request, **{'indent': 4} if self._debug_mode else {}))

    async def subscribe(self, event_name, callback):
        request = {
            'body': {'eventName': event_name},
            'header': build_header('subscribe')
        }
        self._server.subscribed_events[event_name] = callback
        await self._websocket.send(json.dumps(request, **{'indent': 4} if self._debug_mode else {}))

    async def unsubscribe(self, event_name):
        request = {
            'body': {'eventName': event_name},
            'header': build_header('unsubscribe')
        }
        del self._server.subscribed_events[event_name]
        await self._websocket.send(json.dumps(request, **{'indent': 4} if self._debug_mode else {}))

    async def disconnect(self):
        await self._server.disconnect(self._websocket)


def build_header(message_purpose, request_id=None):
    if not request_id:
        request_id = str(uuid.uuid4())
    return {
        'requestId': request_id,
        'messagePurpose': message_purpose,
        'version': '1',
        'messageType': 'commandRequest',
    }
