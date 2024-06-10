import Musicreater
import Musicreater.plugin
import Musicreater.plugin.websocket

import os

dire = input("midi目录：")

print(
    Musicreater.plugin.websocket.to_websocket_server(
        [
            Musicreater.MidiConvert.from_midi_file(
                os.path.join(dire, names), old_exe_format=False
            )
            for names in os.listdir(
                dire,
            )
            if names.endswith((".mid", ".midi"))
        ],
        input("服务器地址："),
        int(input("服务器端口：")),
        Musicreater.DEFAULT_PROGRESSBAR_STYLE,
    )
)
