from model.BaseModel import BaseModel

'''
    创建数据表对象
    类名规则为去除数据表前缀之后 将数据表的下划线写法转换为驼峰写法
    例如表 bili_danmaku
    数据表对象的类名是 Danmaku
    表前缀为bili_(在config中配置表前缀)
    也可以用类变量TABLE定义数据表名
    TABLE = 'bili_danmaku' 自定义数据表名
'''
class Danmaku(BaseModel):
    """
        insert函数
            传入一个字典对象 为数据表字段名和字段值的键值对 如果传入不存在的字段 将不会写入
    """