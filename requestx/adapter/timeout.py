# -*- coding: utf-8 -*-
# @Author      : BrotherBe
# @Time        : 2021/1/22 15:59
# @Version     : Python 3.8.5
from .base import IAdapter


class TimeoutAdapter(IAdapter):
    def adjust(self, *args, **kwargs):
        self_, method, url = args
        if kwargs.get('timeout') is None:
            kwargs['timeout'] = self_._timeout

        return kwargs
