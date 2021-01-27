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


