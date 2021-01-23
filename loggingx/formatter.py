# -*- coding: utf-8 -*-
# @Author      : BrotherBe
# @Time        : 2021/1/20 19:30
# @Version     : Python 3.8.5
import logging


class Formatter(object):
    stream = logging.Formatter(
        fmt='%(pathname)s:%(lineno)d - %(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
        datefmt="%H:%M:%S"
    )
    file = logging.Formatter(
        fmt='%(pathname)s:%(lineno)d - %(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S"
    )
