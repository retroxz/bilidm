import yaml
import os


def yml():
    # 获取当前文件路径
    filePath = os.path.dirname(__file__)
    # 获取当前文件的Realpath
    fileNamePath = os.path.split(os.path.realpath(__file__))[0]
    # 获取配置文件的路径
    yamlPath = os.path.join(fileNamePath, 'config.yml')
    # 加上 ,encoding='utf-8'，处理配置文件中含中文出现乱码的情况
    return yaml.load(open(yamlPath, 'r', encoding='utf-8').read(), Loader=yaml.FullLoader)
