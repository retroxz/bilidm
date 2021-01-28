import blivedm
import logger
import time
from model.Tables import BiliDanmaku
from model.Tables import BiliGift
from model.Tables import BiliGuard
from model.Tables import BiliSc
from config import BLive

bili_danmaku = BiliDanmaku()
bili_gift = BiliGift()
bili_guard = BiliGuard()
bili_sc = BiliSc()


# 时间戳转字符串
def timestamp_to_str(timestamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

class MyBLiveClient(blivedm.BLiveClient):

    # 弹幕回调
    async def _on_receive_danmaku(self, danmaku: blivedm.DanmakuMessage):
        # 写入日志
        logger.get_logger().debug(f'[弹幕] {danmaku.uname}({danmaku.medal_name}[{danmaku.medal_level}]): {danmaku.msg}')
        # 写入json
        logger.write_json_str(danmaku.__dict__)
        # 写入数据表
        params = danmaku.__dict__
        # 添加数据
        params['medal_room_id'] = params['room_id']  # 勋章房间id
        params['medal_runame'] = params['runame']  # 勋章房间主播名
        params['medal_color'] = params['mcolor']  # 勋章颜色

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
                            msg=params['msg'],
                            msg_type=params['msg_type'],
                            privilege_type=params['privilege_type'],
                            room_id=params['room_id'],
                            runame=params['runame'],
                            svip=params['svip'],
                            timestamp=params['timestamp'],
                            uid=params['uid'],
                            uname=params['uname'],
                            urank=params['urank'],
                            user_level=params['user_level'],
                            vip=params['vip'])

    # 礼物回调
    async def _on_receive_gift(self, gift: blivedm.GiftMessage):
        logger.get_logger().warning(
            f'[礼物] {gift.uname} 赠送{gift.gift_name}x{gift.num} （{gift.coin_type}币x{gift.total_coin}）')
        logger.write_json_str(gift.__dict__)

        # 写入数据表
        params = gift.__dict__
        # 发送弹幕的房间信息
        params['room_id'] = BLive.roomid
        params['runame'] = BLive.runame

        bili_gift.create(gift_name=params['gift_name'],
                         gift_id=params['gift_id'],
                         gift_type=params['gift_type'],
                         num=params['num'],
                         price=params['price'],
                         action=params['action'],
                         coin_type=params['coin_type'],
                         total_coin=params['total_coin'],
                         uid=params['uid'],
                         uname=params['uname'],
                         face=params['face'],
                         guard_level=params['guard_level'],
                         timestamp=timestamp_to_str(params['timestamp']),
                         room_id=params['room_id'],
                         runame=params['runame'])

    # 大航海回调
    async def _on_buy_guard(self, message: blivedm.GuardBuyMessage):
        logger.get_logger().warning(f'[舰团] {message.username} 购买{message.gift_name}')
        logger.write_json_str(message.__dict__)

        # 写入数据表
        params = message.__dict__
        # 发送弹幕的房间信息
        params['room_id'] = BLive.roomid
        params['runame'] = BLive.runame

        bili_guard.create(uid = params['uid'],
        guard_level = params['guard_level'],
        num = params['num'],
        price = params['price'],
        gift_id = params['gift_id'],
        gift_name = params['gift_name'],
        start_time = timestamp_to_str(params['start_time']),
        end_time = timestamp_to_str(params['end_time']),
        room_id = params['room_id'],
        runame = params['runame'])

    # SC回调
    async def _on_super_chat(self, message: blivedm.SuperChatMessage):
        logger.get_logger().info(f'[SC]] ¥{message.price} {message.uname}：{message.message}')
        logger.write_json_str(message.__dict__)

        # 写入数据表
        params = message.__dict__
        # 发送弹幕的房间信息
        params['room_id'] = BLive.roomid
        params['runame'] = BLive.runame


        bili_sc.create(price = params['price'],
        message = params['message'],
        message_jpn = params['message_jpn'],
        time = params['time'],
        start_time = timestamp_to_str(params['start_time']),
        end_time = timestamp_to_str(params['end_time']),
        message_id = params['id'],
        gift_id = params['gift_id'],
        gift_name = params['gift_name'],
        uid = params['uid'],
        uname = params['uname'],
        face = params['face'],
        guard_level = params['guard_level'],
        user_level = params['user_level'],
        room_id = params['room_id'],
        runame = params['runame'],
        background_bottom_color = params['background_bottom_color'],
        background_color = params['background_color'],
        background_icon = params['background_icon'],
        background_image = params['background_image'],
        background_price_color = params['background_price_color'])


