"""
 @Author: jiran
 @Email: jiran214@qq.com
 @FileName: room.py
 @DateTime: 2023/4/22 21:23
 @SoftWare: PyCharm
"""
import sys
sys.path.append("../..")

from bilibili_api import live, sync
from abc import abstractmethod
from functools import cached_property
from typing import Union
from src.sys_log.log import worker_logger
import time
from src import config
import queue
logger = worker_logger


from bilibili_api import Credential, Danmaku, sync
from bilibili_api.live import LiveDanmaku, LiveRoom

class BilibiliDanmakuBot:
    def __init__(self, room_id, sessdata, bili_jct, buvid3):
        self.room_id = room_id
        self.credential = Credential(sessdata=sessdata, bili_jct=bili_jct, buvid3=buvid3)
        self.monitor = LiveDanmaku(self.room_id, credential=self.credential)
        self.sender = LiveRoom(self.room_id, credential=self.credential)
        self.uid = sync(self.sender.get_room_info())["room_info"]["uid"]

    def run(self):
        @self.monitor.on("DANMU_MSG")
        async def _damu_msg(event):
            """_summary_

            Args:
                event (_type_): _description_
                用户发送的弹幕
            """
            uid = event["data"]["info"][2][0]
            print(event["data"]["info"][1])
            if uid == self.uid:
                return
            msg = event["data"]["info"][1]
            if msg == "你好":
                await self.sender.send_danmaku(Danmaku("你好！"))
                
        @self.monitor.on("INTERACT_WORD")
        async def _ineract_word(event):
            """_summary_

            Args:
                event (_type_): _description_
                用户进入直播间
            """
            print(event["data"])

        sync(self.monitor.connect())

# 用法示例
if __name__ == "__main__":
    room_id = 24917692  # 替换为你的直播间号
    sessdata = "38e62704%2C1713204178%2Cd15d4%2Aa1CjDswtwKiGf1JOMH3zztSxNtyx8WantASXjK2DBwq2f2jDmxDTf-v6eYCCFNlol2-0oSVmFpZnEzaW0ySV95OHJpNHliUW5xVk92QWw1N3BQSFNnUzV6Q3Bkb09vUHdROHJESVZDWUlmUlJ4RjFMWnFiSVc1cUFOZ09nWDZkY0JGdGJJeE5kSXZBIIEC"
    bili_jct = "f5a617f1ef14b2e411a4e9a22fcad0c5"
    buvid3 = "BDE81E1D-D3FD-4490-A517-88F857ED514527558infoc"

    bot = BilibiliDanmakuBot(room_id, sessdata, bili_jct, buvid3)
    bot.run()

