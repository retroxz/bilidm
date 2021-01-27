import blivedm
import logger
# from model.Danmaku import Danmaku
from model.Tables import BiliDanmaku
from config import BLive

bili_danmaku = BiliDanmaku()

class MyBLiveClient(blivedm.BLiveClient):
    # danmaku_table = Danmaku()
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
        # 写入日志
        logger.get_logger().debug(f'[弹幕] {danmaku.uname}({danmaku.medal_name}[{danmaku.medal_level}]): {danmaku.msg}')
        # 写入json
        logger.write_json_str(danmaku.__dict__)
        # 写入数据表
        params = danmaku.__dict__
        # 添加数据
        params['medal_room_id'] = params['room_id'] # 勋章房间id
        params['medal_runame'] = params['runame'] # 勋章房间主播名
        params['medal_color'] = params['mcolor'] # 勋章颜色

        # 发送弹幕的房间信息
        params['room_id'] = BLive.roomid
        params['runame'] = BLive.runame
        # self.danmaku_table.insert(params)
        bili_danmaku.create(admin=params['admin'],
                            medal_color=params['medal_color'],
                            medal_level=params['medal_level'],
                            medal_name=params['medal_name'],
                            medal_room_id=params['medal_room_id'],
                            medal_runame=params['medal_runame'],
                            mobile_verify=params['mobile_verify'],
                            msg = params['msg'],
                            msg_type = params['msg_type'],
                            privilege_type = params['privilege_type'],
                            room_id = params['room_id'],
                            runame = params['runame'],
                            svip = params['svip'],
                            timestamp = params['timestamp'],
                            uid = params['uid'],
                            uname = params['uname'],
                            urank = params['urank'],
                            user_level = params['user_level'],
                            vip = params['vip'])


    # 礼物回调
    async def _on_receive_gift(self, gift: blivedm.GiftMessage):
        logger.get_logger().warning(
            f'[礼物] {gift.uname} 赠送{gift.gift_name}x{gift.num} （{gift.coin_type}币x{gift.total_coin}）')
        logger.write_json_str(gift.__dict__)

    # 大航海回调
    async def _on_buy_guard(self, message: blivedm.GuardBuyMessage):
        logger.get_logger().warning(f'[舰团] {message.username} 购买{message.gift_name}')
        logger.write_json_str(message.__dict__)

    # SC回调
    async def _on_super_chat(self, message: blivedm.SuperChatMessage):
        logger.get_logger().info(f'[SC]] ¥{message.price} {message.uname}：{message.message}')
        logger.write_json_str(message.__dict__)
