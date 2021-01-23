# -*- coding: utf-8 -*-
# @Author      : BrotherBe
# @Time        : 2021/1/22 16:00
# @Version     : Python 3.8.5
from .base import IAdapter


class CookiesAdapter(IAdapter):
    def adjust(self, *args, **kwargs):
        self_, method, url = args
        _cookies = kwargs.get('cookies')
        if _cookies:
            self_.add_cookies(_cookies)
            kwargs['cookies'] = None
        return kwargs
