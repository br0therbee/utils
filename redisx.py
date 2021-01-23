# -*- coding: utf-8 -*-
# @Author      : BrotherBe
# @Time        : 2020/7/25 2:00
# @Version     : Python 3.8.5
import redis

from patterns import FlyWeight


class RedisConnection(metaclass=FlyWeight):
    def __init__(self, host, port, db, password):
        self.redis = redis.Redis(
            connection_pool=redis.ConnectionPool(host=host, port=port, db=db, password=password, decode_responses=True)
        )
