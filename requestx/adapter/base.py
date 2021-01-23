# -*- coding: utf-8 -*-
# @Author      : BrotherBe
# @Time        : 2021/1/22 15:59
# @Version     : Python 3.8.5
import abc


class IAdapter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def adjust(self, *args, **kwargs):
        """调整"""
