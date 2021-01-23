# -*- coding: utf-8 -*-
# @Author      : BrotherBe
# @Time        : 2021/1/22 16:01
# @Version     : Python 3.8.5
from .base import IAdapter


class HeadersAdapter(IAdapter):
    def adjust(self, *args, **kwargs):
        _headers = kwargs.get('headers')
        stream = kwargs.get('stream')
        self_, method, url = args
        if not _headers:
            _headers = dict()
        _headers = {k.lower(): v for k, v in _headers.items()}
        cookies = _headers.pop('cookie', None)
        if cookies:
            self_.add_cookies(cookies)
        if 'user-agent' not in _headers:
            _headers['user-agent'] = self_._user_agent
        # if 'host' not in _headers:
        #     _headers['host'] = urlparse(url).hostname
        if stream and 'range' not in _headers:
            _headers['range'] = "bytes=0-"
        kwargs['headers'] = _headers
        return kwargs
