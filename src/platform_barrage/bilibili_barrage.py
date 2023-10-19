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


from bilibili_api import live, sync,Credential



from bilibili_api import Credential, Danmaku, sync
from bilibili_api.live import LiveDanmaku, LiveRoom
from bilibili_api import settings

# settings.geetest_auto_open = False
# settings.proxy = "http://47.88.103.16:14376"

class BLBARRAGE:
    def __init__(self) -> None:
        self.roomId=config.ROOMID
        self.credential = Credential(
            sessdata=config.SESSDATA,
            bili_jct=config.BILI_JCT,
            buvid3=config.BUVID3
        )
        # ac_time_value="1697651267947",
        # dedeuserid="211540c0bf760aa3"
        # if not sync(self.credential.check_refresh()):
        #     print("--")
        #     self.credential_refresh()
        self.monitor = LiveDanmaku(config.ROOMID, credential=self.credential,max_retry=1) # 直播间弹幕监听对象
        self.sender  = LiveRoom(config.ROOMID, credential=self.credential) # 直播间弹幕发送对象
        self.uid  = sync(self.sender.get_room_info())["room_info"]["uid"]
    
    # 更新认证
    def credential_refresh(self):
        sync(self.credential.refresh())
        
    # 发送弹幕
    def send_danmu(self, msg:str):
        self.sender.send_danmaku(msg)
    
    # 开启监听
    def add_event_listeners(self):
        listener_map = {
            'DANMU_MSG': on_danmaku_event_filter,
            'SUPER_CHAT_MESSAGE': on_super_chat_message_event_filter,
            'SEND_GIFT': on_gift_event_filter,
            'INTERACT_WORD': on_interact_word_event_filter,
        }
        for item in listener_map.items():
            self.monitor.add_event_listener(*item)
        
    # 开启监听
    def consumer(self):
        self.monitor.connect()
        


async def on_danmaku_event_filter(event_dict):
    pass
    print(event_dict)
    # # 收到弹幕
    # event = BlDanmuMsgEvent.filter(event_dict)
    # event = BlDanmuMsgEvent(event_dict)
    # user_queue.send(event)


async def on_super_chat_message_event_filter(event_dict):
    # SUPER_CHAT_MESSAGE
    # info = event['data']['data']
    # user_info = info['user_info']
    # print('SUPER_CHAT_MESSAGE',
    #       user_info['uname'],
    #       user_info['face'],
    #
    #       info['message'],
    #       info['price'],
    #       info['start_time'],
    #       )
    # event = BlSuperChatMessageEvent(event_dict)
    # user_queue.send(event)
    pass


async def on_gift_event_filter(event_dict):
    # 收到礼物
    # info = event_dict['data']['data']
    # print('SEND_GIFT',
    #       info['face'],
    #       info['uname'],
    #       info['action'],
    #       info['giftName'],
    #       info['timestamp'],
    #       )
    # event = BlSendGiftEvent(event_dict)
    # user_queue.send(event)
    pass


async def on_interact_word_event_filter(event_dict):
    # INTERACT_WORD
    # info = event_dict['data']['data']
    # fans_medal = info['fans_medal']
    # print('INTERACT_WORD',
    #       fans_medal['medal_name'],
    #       fans_medal['medal_level'],
    #       info['uname'],
    #       info['timestamp']
    #       )
    # if not user_queue.event_queue.full():
    #     event = BlInteractWordEvent(event_dict)
    #     user_queue.send(event)
    pass

if __name__ == "__main__":
    bl = BLBARRAGE()
    bl.credential_refresh()
    sync(bl.add_event_listeners())