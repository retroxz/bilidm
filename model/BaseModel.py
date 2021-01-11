from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

from config import database

class BaseModel:
    # 数据库连接字符串
    DB_CONNECT_STRING = f'mysql+mysqlconnector://{database.username}:{database.password}@{database.host}:{database.port}/{database.db}'
    # 表名
    TABLE = ''
    # 创建引擎
    engine = create_engine(DB_CONNECT_STRING, echo=False)
    # 自动映射
    Base = automap_base()
    Base.prepare(engine, reflect=True)


    def __init__(self):
        # 自动获取表名
        if not self.TABLE:
            self.TABLE = self.get_lower_case_name(self.__class__.__name__)
        # 为数据表添加前缀
        if database.prefix:
            self.TABLE = database.prefix + self.TABLE
        # 创建session
        self.session = sessionmaker()
        self.session.configure(bind=self.engine)
        self.session = self.session()

    # 驼峰转为下划线
    @staticmethod
    def get_lower_case_name(text):
        name_list = []
        for index, char in enumerate(text):
            if char.isupper() and index != 0:
                name_list.append('_')
            name_list.append(char)
        return ''.join(name_list).lower()

    # 插入一条数据
    def inset(self,params:dict):
        table_obj = eval(f'self.Base.classes.{self.TABLE}')()
        for key,value in params.items():
            if hasattr(table_obj,key):
                exec(f"table_obj.{key}='{value}'")
        # 将字典内容赋值给对象之后 写入数据库
        self.session.add(table_obj)
        self.session.commit()
        self.session.close()