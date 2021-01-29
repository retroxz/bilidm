#coding=utf-8  

"""
@File: Tables.py
@Author: retroxz
@Email: zzxee666@gmail.com
@Date: 2021/01/27
"""

from peewee import *
from config import database

db = MySQLDatabase(database.db, host=database.host, port=database.port, user=database.username, passwd=database.password)
db.connect()


class BaseModel(Model):

    class Meta:
        database = db


class BiliDanmaku(BaseModel):
    class Meta:
        table_name = 'bili_danmaku'

    admin = IntegerField(null=True)
    medal_color = CharField(null=True)
    medal_level = IntegerField(null=True)
    medal_name = CharField(null=True)
    medal_room_id = IntegerField(null=True)
    medal_runame = CharField(null=True)
    mobile_verify = IntegerField(null=True)
    msg = CharField(null=True)
    msg_type = IntegerField(null=True)
    privilege_type = IntegerField(null=True)
    room_id = IntegerField(null=True)
    runame = CharField(null=True)
    svip = IntegerField(null=True)
    timestamp = BigIntegerField(null=True)
    uid = IntegerField(null=True)
    uname = CharField(null=True)
    urank = IntegerField(null=True)
    user_level = IntegerField(null=True)
    vip = IntegerField(null=True)

class BiliGift(BaseModel):
    action = CharField(null=True)
    coin_type = CharField(null=True)
    face = CharField(null=True)
    gift_id = IntegerField(null=True)
    gift_name = CharField(null=True)
    gift_type = IntegerField(null=True)
    guard_level = IntegerField(null=True)
    num = IntegerField(null=True)
    price = IntegerField(null=True)
    room_id = IntegerField(null=True)
    runame = CharField(null=True)
    timestamp = DateTimeField(null=True)
    total_coin = IntegerField(null=True)
    uid = IntegerField(null=True)
    uname = CharField(null=True)

    class Meta:
        table_name = 'bili_gift'

class BiliGuard(BaseModel):
    end_time = DateTimeField(null=True)
    gift_id = IntegerField(null=True)
    gift_name = CharField(null=True)
    guard_level = IntegerField(null=True)
    num = IntegerField(null=True)
    price = IntegerField(null=True)
    room_id = IntegerField(null=True)
    runame = CharField(null=True)
    start_time = DateTimeField(null=True)
    uid = IntegerField(null=True)
    uname = CharField(null=True)

    class Meta:
        table_name = 'bili_guard'

class BiliSc(BaseModel):
    background_bottom_color = CharField(null=True)
    background_color = CharField(null=True)
    background_icon = CharField(null=True)
    background_image = CharField(null=True)
    background_price_color = CharField(null=True)
    end_time = DateTimeField(null=True)
    face = CharField(null=True)
    gift_id = IntegerField(null=True)
    gift_name = CharField(null=True)
    guard_level = IntegerField(null=True)
    message = CharField(null=True)
    message_id = IntegerField(null=True)
    message_jpn = CharField(null=True)
    price = DecimalField(null=True)
    room_id = IntegerField(null=True)
    runame = CharField(null=True)
    start_time = DateTimeField(null=True)
    time = IntegerField(null=True)
    uid = IntegerField()
    uname = CharField(null=True)
    user_level = IntegerField(null=True)

    class Meta:
        table_name = 'bili_sc'


