from sqlalchemy import Column, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import *
from config import database

# 创建对象的基类:
Base = declarative_base()


# 方便的将json转化为数据库对象参数
def DB_object(*args, **kwargs):
    string = ""
    for key in args:
        value = kwargs[key]
        if type(value) == str:
            sql_string = "{} = '{}'".format(key, value)
        else:
            sql_string = "{} = {}".format(key, value)
        string = sql_string + "," + string
    return string


# 创建数据库对象
class User(Base):
    # 表的名字:
    __tablename__ = database.tablename

    # 表的结构:
    """好像必须这么一个一个写（真的好麻烦）"""
    id = Column(Integer(), primary_key=True)
    admin = Column(SmallInteger())
    medal_color = Column(String(255))
    medal_level = Column(SmallInteger())
    medal_name = Column(String(255))
    medal_room_id = Column(Integer())
    medal_runame = Column(String(255))
    mobile_verify = Column(SmallInteger())
    msg = Column(String(255))
    msg_type = Column(Integer())
    privilege_type = Column(SmallInteger())
    room_id = Column(Integer())
    runame = Column(String(255))
    svip = Column(SmallInteger())
    timestamp = Column(BIGINT())
    uid = Column(Integer())
    uname = Column(String(255))
    urank = Column(Integer())
    user_level = Column(SmallInteger())
    vip = Column(SmallInteger())


class DB_Instance:
    def __init__(self):
        # 初始化数据库连接:
        self.engine = create_engine('mysql+mysqlconnector://{}:{}@{}:3306/{}'.format(database.username,
                                                                                     database.password,
                                                                                     database.host,
                                                                                     database.db))
        # 创建DBSession类型:
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)

    def Session(self):
        return self.Session()

    # 插入数据
    def Insert_data(self, string):
        new = eval("User({})".format(string))
        session = self.Session()
        session.add(new)
        session.commit()
        # 关闭session:
        session.close()
