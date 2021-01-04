# -*- coding: utf-8 -*-

import asyncio
import blivedm
import logger
import config


class MyBLiveClient(blivedm.BLiveClient):
    # 演示如何自定义handler
    _COMMAND_HANDLERS = blivedm.BLiveClient._COMMAND_HANDLERS.copy()

    async def __on_vip_enter(self, command):
        print(command)

    _COMMAND_HANDLERS['WELCOME'] = __on_vip_enter  # 老爷入场

    # async def _on_receive_popularity(self, popularity: int):
    #     print(f'当前人气值：{popularity}')

    # 弹幕回调
    async def _on_receive_danmaku(self, danmaku: blivedm.DanmakuMessage):
        logger.get_logger().debug(f'[弹幕] {danmaku.uname}({danmaku.medal_name}[{danmaku.medal_level}]): {danmaku.msg}')
        logger.write_json_str(danmaku.__dict__)

    # 礼物回调
    async def _on_receive_gift(self, gift: blivedm.GiftMessage):
        logger.get_logger().warning(f'[礼物] {gift.uname} 赠送{gift.gift_name}x{gift.num} （{gift.coin_type}币x{gift.total_coin}）')
        logger.write_json_str(gift.__dict__)

    # 大航海回调
    async def _on_buy_guard(self, message: blivedm.GuardBuyMessage):
        logger.get_logger().warning(f'[舰团] {message.username} 购买{message.gift_name}')
        logger.write_json_str(message.__dict__)

    # SC回调
    async def _on_super_chat(self, message: blivedm.SuperChatMessage):
        logger.get_logger().info(f'[SC]] ¥{message.price} {message.uname}：{message.message}')
        logger.write_json_str(message.__dict__)


async def main():
    # 参数1是直播间ID
    # 如果SSL验证失败就把ssl设为False
    # client = MyBLiveClient(221473, ssl=True)
    print(f'当前监听的直播间: {config.yml()["listen"]}')
    client = MyBLiveClient(config.yml()['listen'], ssl=True)
    future = client.start()
    try:
        # 5秒后停止，测试用
        # await asyncio.sleep(5)
        # future = client.stop()
        # 或者
        # future.cancel()

        await future
    finally:
        await client.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())