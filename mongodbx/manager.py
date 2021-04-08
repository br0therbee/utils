# -*- coding: utf-8 -*-
# @Author      : BrotherBe
# @Time        : 2020/9/19 18:37
# @Version     : Python 3.8.5
from patterns import FlyWeight
from .client import MongoClient


class MongoDB(metaclass=FlyWeight):
    def __init__(self, mongodb_url: str):
        self.mongodb = MongoClient(mongodb_url, connect=False)
