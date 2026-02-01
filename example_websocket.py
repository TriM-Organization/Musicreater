import Musicreater.old_init as old_init
import Musicreater.old_plugin
import Musicreater.old_plugin.websocket

import os

dire = input("midi目录：")

print(
    old_init.old_plugin.websocket.to_websocket_server(
        [
            old_init.MidiConvert.from_midi_file(
                os.path.join(dire, names), old_exe_format=False
            )
            for names in os.listdir(
                dire,
            )
            if names.endswith((".mid", ".midi"))
        ],
        input("服务器地址："),
        int(input("服务器端口：")),
        old_init.DEFAULT_PROGRESSBAR_STYLE,
    )
)
