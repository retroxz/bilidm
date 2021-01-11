import blivedm
import logger
from SQLAlchemy import *
from config import database

db = DB_Instance()


class MyBLiveClient(blivedm.BLiveClient):
    # 演示如何自定义handler
    # _COMMAND_HANDLERS = blivedm.BLiveClient._COMMAND_HANDLERS.copy()

    """async def __on_vip_enter(self, command):
        print(command)

    # 老爷入场
    _COMMAND_HANDLERS['WELCOME'] = __on_vip_enter

    async def _on_receive_popularity(self, popularity: int):
        print(f'当前人气值：{popularity}')"""

    # 弹幕回调
    async def _on_receive_danmaku(self, danmaku: blivedm.DanmakuMessage):
        # print(danmaku.__dict__)
        logger.get_logger().debug(f'[弹幕] {danmaku.uname}({danmaku.medal_name}[{danmaku.medal_level}]): {danmaku.msg}')
        logger.write_json_str(danmaku.__dict__)
        string = DB_object(*database.column, **danmaku.__dict__)
        db.Insert_data(string)

    # 礼物回调
    async def _on_receive_gift(self, gift: blivedm.GiftMessage):
        # print(gift.__dict__)
        logger.get_logger().warning(
            f'[礼物] {gift.uname} 赠送{gift.gift_name}x{gift.num} （{gift.coin_type}币x{gift.total_coin}）')
        logger.write_json_str(gift.__dict__)

    # 大航海回调
    async def _on_buy_guard(self, message: blivedm.GuardBuyMessage):
        # print(message.__dict__)
        logger.get_logger().warning(f'[舰团] {message.username} 购买{message.gift_name}')
        logger.write_json_str(message.__dict__)

    # SC回调
    async def _on_super_chat(self, message: blivedm.SuperChatMessage):
        # print(message.__dict__)
        logger.get_logger().info(f'[SC]] ¥{message.price} {message.uname}：{message.message}')
        logger.write_json_str(message.__dict__)
