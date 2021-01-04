# -*- coding: utf-8 -*-

import logging
import os

import colorlog
import json
import time

# 日志颜色设置
log_colors_config = {
    'DEBUG': 'white',  # cyan white
    'INFO': 'blue',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}


def get_logger():
    # 目录
    log_path = f"{os.getcwd()}{os.sep}log{os.sep}{time.strftime('%Y%m', time.localtime(time.time()))}{os.sep}"
    # 文件名
    log_file_name = f"{time.strftime('%d', time.localtime(time.time()))}.log"

    logger = logging.getLogger('bili_logger')
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    # 定义控制台输出流
    console_stream = logging.StreamHandler()
    console_stream.setLevel(logging.DEBUG)
    console_stream.setFormatter(colorlog.ColoredFormatter(
        fmt='%(log_color)s[%(asctime)s.%(msecs)03d]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors=log_colors_config
    ))

    # 定义文件输出流
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    file_stream = logging.FileHandler(filename=f"{log_path}{log_file_name}", mode='a', encoding='utf-8')
    file_stream.setLevel(logging.DEBUG)
    file_stream.setFormatter(
        logging.Formatter('[%(asctime)s] %(message)s'))

    # 添加Handler
    logger.addHandler(console_stream)
    logger.addHandler(file_stream)

    return logger


def write_json_str(d):
    # 目录
    json_path = f"{os.getcwd()}{os.sep}json{os.sep}{time.strftime('%Y%m', time.localtime(time.time()))}{os.sep}"
    # 文件名
    json_file_name = f"{time.strftime('%d', time.localtime(time.time()))}.txt"
    if not os.path.exists(json_path):
        os.makedirs(json_path)
    f = open(f"{json_path}{json_file_name}", 'a', encoding='utf-8')
    f.write(json.dumps(d, ensure_ascii=False))
    f.write('\n')
    f.close()
