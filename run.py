# -*- coding: utf-8 -*-

import asyncio
from BLiveClient import MyBLiveClient
from config import BLive


async def main():
    # 参数1是直播间ID
    # 如果SSL验证失败就把ssl设为False
    # client = MyBLiveClient(221473, ssl=True)
    client = MyBLiveClient(BLive.roomid, ssl=True)
    print(f'当前监听的直播间: {BLive.roomid}')
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