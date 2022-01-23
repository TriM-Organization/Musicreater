import os
import brotli

'''感谢由 Charlie_Ping “查理平” 带来的bdx转换代码'''


# 诸葛亮与八卦阵帮忙修改语法 日期：---2022年1月19日
# 统计：致命（三级）错误：0个；警告（二级）错误：0个；语法（一级）错误：7个


class BdxConverter:
    __header = "BD@"
    __bin_header = b"BDX"
    __generator_author = b"&Charlie_Ping"

    keys = {
        # x--, x++, addSmallX(-128~127), addX(-32768~32767), addBigX(-2147483648~2147483647)
        "x": [b"\x0f", b"\x0e", b"\x1c", b"\x14", b"\x15"],
        "y": [b"\x11", b"\x10", b"\x1d", b"\x16", b"\x17"],
        "z": [b"\x13", b"\x12", b"\x1e", b"\x18", b"\x19"],
        "end": b"\x58",
        "isSigned": b"\x5a",
        "placeCommandBlockWithData": b"\x1b",
        "placeBlock": b"\x07"
    }

    def __init__(self, file_path: str, author: str, blocks):
        self.author = author
        self.blocks = blocks
        self.file_path = file_path
        self.direction = [0, 0, 0]
        self.block_type = self.get_block_type
        self.__file = self.create_and_upload_file

    @property
    def get_block_type(self):
        """
        blocks
        [
            {
                "direction": [x: int, y: int, z: int],
                block_name: str,
                particular_value: int,
            }
        ]
        :return: list 给出的所有方块种类名称
        """
        block_type = set()
        for block_ in self.blocks:
            block_type.add(block_["block_name"])
        block_type = list(block_type)
        return block_type

    @property
    def create_and_upload_file(self):
        """
        （瞎用property？ 害怕
        创建一个bdx文件
        要close！
        :return: 一个文件对象
        """
        _dir = os.path.dirname(self.file_path)
        if not os.path.isdir(_dir):
            os.makedirs(_dir)
        _bytes = self.__bin_header
        _bytes += b"\x00"
        _bytes += self.author.encode("utf-8") + self.__generator_author
        for i in self.block_type:
            _bytes += b"\x00\x01"
            _bytes += bytes(i, encoding="utf-8")
        _bytes += b"\x00"
        _bytes += self.upload_blocks()
        _bytes += b"X"
        with open(self.file_path, "w+") as f:
            f.write("BD@")
            f.close()
        with open(self.file_path, "ab+") as f:
            f.write(brotli.compress(_bytes))
            f.close()
        return

    def upload_blocks(self):
        """
        计算差值
        写入移动过程
        写入方块
        更新差值
        :return:
        """
        _types = b""
        for block_ in self.blocks:
            # print(f"当前方块：{block['block_name']}, 位置： {block['direction']}]")
            diff = self.move_pointer(self.direction, block_["direction"])
            _types += diff
            if block_["block_name"] in ["command_block",
                                        "chain_command_block",
                                        "repeating_command_block"]:
                _types += self.obtain_command_block(block_)
            else:
                _types += self.obtain_universal_block(block_)
            self.direction = block_["direction"]
        return _types

    def move_pointer(self, direction: list, new_direction):
        """
        给出 两个[x, y, z]坐标，返回pointer的移动过程
        :param direction: 坐标 1
        :param new_direction: 坐标 2
        :return: bytes
        """
        _bytes = b""
        for i, sign in enumerate(["x", "y", "z"]):
            # print(f"<{sign}> 新-旧={new_direction[i]-direction[i]}")
            distance = new_direction[i] - direction[i]
            if distance == 0:
                # print("距离是0？跳过了")
                continue
            _bytes += self.obtain_pointer_type(distance, sign)
            # print(f"向 {sign} 运动了 {distance} 格子")
        return _bytes

    @classmethod
    def obtain_pointer_type(cls, num: int, coordinate: str):
        """

        用于确定辅助玩家以某一数据类型走指定长度

        -1 -> 0
        1 -> 1
        [128, 127] -> 2
        [-32768, 32767] -> 3
        [-2147483648, 2147483647] -> 4
        :param num:
        :param coordinate: 坐标轴种类，x y 或 z
        :return:
        """
        if num == 0:
            return
        pointer = 0
        condition = (num != -1,  # byte=0, pointer=1
                     num < -1 or num > 1,  # byte=1, pointer=2
                     num < -128 or num > 127,  # byte=2, pointer=3
                     num < -32768 or num > 32767,  # byte=4, pointer=4
                     )
        for i in condition:
            if i:
                pointer += 1
        pointer_type = cls.keys[coordinate][pointer]

        byte_len = 2 ** (pointer - 2)
        if byte_len >= 1:
            num_byte = num.to_bytes(byte_len, byteorder="big", signed=True)
            return pointer_type + num_byte
        return pointer_type

    def obtain_universal_block(self, block1):
        """
        给定一个方块， 返回此方块在这个bdx中的id和方块data
        :param block1: {block_name: str,particular_value: int}
        :return: bytes
        """
        block_id = b"\x07" + self.block_type.index(block1["block_name"]).to_bytes(2, byteorder="big", signed=False)
        particular_value = block1["particular_value"].to_bytes(2, byteorder="big", signed=False)
        block_header = block_id + particular_value
        return block_header

    def obtain_command_block(self, block1):
        """
        给定一个命令方块，返回命令方块各种数据
        :param block1: {
            "direction": [x: int, y: int, z: int]
            "block_name": str,
            "particular_value": int,
            "impluse": int,  # unsigned_int32
            "command": str,
            "customName": str,
            "lastOutput": str,  # 没特殊要求写个\x00就得了
            "tickdelay": int,  # int32
            "executeOnFirstTick": int,  # 1 bytes
            "trackOutput": int,  # 1 bytes
            "conditional": int,  # 1 bytes
            "needRedstone": int  # 1 bytes
        }
        :return: bytes of command_block
        """

        block_id = b"\x1b" + self.block_type.index(block1["block_name"]).to_bytes(2, byteorder="big", signed=False)
        particular_value = block1["particular_value"].to_bytes(2, byteorder="big", signed=False)
        block_header = block_id + particular_value
        for i in [
            block1["impluse"].to_bytes(4, byteorder="big", signed=False),
            bytes(block1["command"], encoding="utf-8") + b"\x00",
            bytes(block1["customName"], encoding="utf-8") + b"\x00",
            bytes(block1["lastOutput"], encoding="utf-8") + b"\x00",
            block1["tickdelay"].to_bytes(4, byteorder="big", signed=True),
            block1["executeOnFirstTick"].to_bytes(1, byteorder="big"),
            block1["trackOutput"].to_bytes(1, byteorder="big"),
            block1["conditional"].to_bytes(1, byteorder="big"),
            block1["needRedstone"].to_bytes(1, byteorder="big")
        ]:
            block_header += i
        return block_header


if __name__ == '__main__':
    block = [{"direction": [-1, -1, -1], "block_name": "concrete", "particular_value": 5},
             {"direction": [1, 5, 1], "block_name": "stained_glass", "particular_value": 7},
             {"direction": [2, 4, 1], "block_name": "command_block", "particular_value": 3,
              "impluse": 0,
              "command": "say A generator test",
              "customName": "test",
              "lastOutput": "",
              "tickdelay": 24,
              "executeOnFirstTick": 0,
              "trackOutput": 0,
              "conditional": 0,
              "needRedstone": 1
              },
             {"direction": [3, 4, 1], "block_name": "concrete", "particular_value": 6},
             {"direction": [-123412133, 4, 1], "block_name": "concrete", "particular_value": 7}]
    bdx = BdxConverter("./test02.bdx", "Charlie_Ping", block)
