import sys
sys.path.append("../..")
import pyvts
import json
from src import config
import asyncio



class  VTUBE:
    def __init__(self, plugin_info):
        self.plugin_info = plugin_info
         
    async def initialize_action(self):
        # websocket连接 获取token到本地
        vts = pyvts.vts(plugin_info=plugin_info)
        await vts.connect()
        print('请在live2D VTS弹窗中点击确认！')
        await vts.request_authenticate_token()  # get token
        await vts.write_token()
        await vts.request_authenticate()  # use token

        response_data = await vts.request(vts.vts_request.requestHotKeyList())
        hotkey_list = []
        for hotkey in response_data['data']['availableHotkeys']:
            hotkey_list.append(hotkey['name'])
        print('读取到所有模型动作:', hotkey_list)
        for i in range(len(hotkey_list)):
            action_index=i
            send_hotkey_request = vts.vts_request.requestTriggerHotKey(hotkey_list[action_index])
            await vts.request(send_hotkey_request)
        await vts.close()
            
    async def play_action_vt(self,action_index, live2D_actions):
        vts = pyvts.vts(plugin_info=self.plugin_info)
        await vts.connect()
        await vts.read_token()
        await vts.request_authenticate()
        if action_index > len(live2D_actions) - 1:
            raise ValueError('动作不存在')
        send_hotkey_request = vts.vts_request.requestTriggerHotKey(live2D_actions[action_index])
        await vts.request(send_hotkey_request)
        await vts.close()

            
if __name__ == "__main__":
    # 使用示例
    plugin_info = config.PLUGININFO  # 传入插件信息
    live2D_actions = ['Heart Eyes', 'Eyes Cry', 'Angry Sign', 'Shock Sign', 'Remove Expressions', 'Anim Shake', '']  # 传入动作列表

    action_player = VTUBE(plugin_info)
    
    
    asyncio.run(action_player.play_action_vt(0,live2D_actions))
    asyncio.run(action_player.play_action_vt(1,live2D_actions))
    asyncio.run(action_player.play_action_vt(2,live2D_actions))
    asyncio.run(action_player.play_action_vt(3,live2D_actions))
    asyncio.run(action_player.play_action_vt(4,live2D_actions))
    asyncio.run(action_player.play_action_vt(5,live2D_actions))
    # asyncio.run(action_player.initialize_action())
    
   