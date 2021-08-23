import blivedm
import logger
import time
from model.Tables import BiliDanmaku
from model.Tables import BiliGift
from model.Tables import BiliGuard
from model.Tables import BiliSc
from config import api
from config import BLive
import httpx


bili_danmaku = BiliDanmaku()
bili_gift = BiliGift()
bili_guard = BiliGuard()
bili_sc = BiliSc()

# 时间戳转字符串
def timestamp_to_str(timestamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))


class MyBLiveClient(blivedm.BLiveClient):
    # 演示如何自定义handler

    _COMMAND_HANDLERS = blivedm.BLiveClient._COMMAND_HANDLERS.copy()

    async def __on_vip_enter(self, command):
        print(command)

    async def __on_room_change(self, command):
        group_list = api.group
        for group in group_list:
            r = httpx.request('POST', api.url, json={
                'key': api.key,
                'message': F"{BLive.runame}的直播间改标题啦：{command['data']['title']}",
                'qid': group,
                'message_type': 'group'
            })

    async def __on_room_real_time_message_update(self, command):
        print(F"[ROOM_REAL_TIME_MESSAGE_UPDATE]{command}")

    async def __on_live_preparing(self, command):
        print(F"[PREPARING]{command}")

    async def __on_live(self, command):
        print(F"[Live]{command}")

    async def __on_welcome_guard(self,command):
        print(F"[舰长入场]{command}")

    _COMMAND_HANDLERS['WELCOME'] = __on_vip_enter  # 老爷入场

    _COMMAND_HANDLERS['ROOM_CHANGE'] = __on_room_change  # 可能是标题改

    _COMMAND_HANDLERS['ROOM_REAL_TIME_MESSAGE_UPDATE'] = __on_room_real_time_message_update  # 可能是直播间状态

    _COMMAND_HANDLERS['PREPARING'] = __on_live_preparing  # 可能是直播间状态

    _COMMAND_HANDLERS['Live'] = __on_live  # 可能是直播间状态

    _COMMAND_HANDLERS['WELCOME_GUARD'] = __on_welcome_guard  # 可能是直播间状态

    async def _on_receive_popularity(self, popularity: int):
        print(f'当前人气值：{popularity}')

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

        bili_guard.create(uid=params['uid'],
                          uname=params['username'],
                          guard_level=params['guard_level'],
                          num=params['num'],
                          price=params['price'],
                          gift_id=params['gift_id'],
                          gift_name=params['gift_name'],
                          start_time=timestamp_to_str(params['start_time']),
                          end_time=timestamp_to_str(params['end_time']),
                          room_id=params['room_id'],
                          runame=params['runame'])

    # SC回调
    async def _on_super_chat(self, message: blivedm.SuperChatMessage):
        logger.get_logger().info(f'[SC]] ¥{message.price} {message.uname}：{message.message}')
        logger.write_json_str(message.__dict__)

        # 写入数据表
        params = message.__dict__
        # 发送弹幕的房间信息
        params['room_id'] = BLive.roomid
        params['runame'] = BLive.runame

        bili_sc.create(price=params['price'],
                       message=params['message'],
                       message_jpn=params['message_jpn'],
                       time=params['time'],
                       start_time=timestamp_to_str(params['start_time']),
                       end_time=timestamp_to_str(params['end_time']),
                       message_id=params['id'],
                       gift_id=params['gift_id'],
                       gift_name=params['gift_name'],
                       uid=params['uid'],
                       uname=params['uname'],
                       face=params['face'],
                       guard_level=params['guard_level'],
                       user_level=params['user_level'],
                       room_id=params['room_id'],
                       runame=params['runame'],
                       background_bottom_color=params['background_bottom_color'],
                       background_color=params['background_color'],
                       background_icon=params['background_icon'],
                       background_image=params['background_image'],
                       background_price_color=params['background_price_color'])
