# -*- coding: utf-8 -*-
# @Author      : BrotherBe
# @Time        : 2020/8/21 11:52
# @Version     : Python 3.8.5
import json as json_
import random

import requests
from requests.cookies import cookiejar_from_dict
from requests.utils import dict_from_cookiejar

from commons import get_frame
from decorators import timer, run
from loggingx.manager import LogManager
from .adapter.base import IAdapter
from .exceptions import NetworkRequestException
from .response import Response

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/84.0.4147.125 Safari/537.36'
]


def request(method: str,
            url: str,
            *,
            params=None,
            data=None,
            headers=None,
            cookies=None,
            files=None,
            auth=None,
            timeout=None,
            allow_redirects=True,
            proxies=None,
            hooks=None,
            stream=None,
            verify=None,
            cert=None,
            json=None,
            # REMIND: extra fields
            retry_times: int = 3,
            show_response: bool = True,
            show_headers: bool = False,
            log_level: int = 20):
    with RequestManager(times=retry_times,
                        show_response=show_response,
                        show_headers=show_headers,
                        log_level=log_level) as manager:
        return manager.request(method, url,
                               params=params, data=data, headers=headers, cookies=cookies, files=files,
                               auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies,
                               hooks=hooks, stream=stream, verify=verify, cert=cert, json=json)


def retrace(method: str,
            url: str,
            *,
            params=None,
            data=None,
            headers=None,
            cookies=None,
            files=None,
            auth=None,
            timeout=None,
            allow_redirects=True,
            proxies=None,
            hooks=None,
            stream=None,
            verify=None,
            cert=None,
            json=None,
            # REMIND: extra fields
            retry_times: int = 3,
            show_response: bool = True,
            show_headers: bool = False):
    return request(method, url,
                   params=params, data=data, headers=headers, cookies=cookies, files=files,
                   auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies,
                   hooks=hooks, stream=stream, verify=verify, cert=cert, json=json,
                   retry_times=retry_times, show_response=show_response, show_headers=show_headers, log_level=10)


class RequestManager(object):
    def __init__(self, timeout: float = 30, times: int = 3, show_response: bool = True, show_headers: bool = False,
                 log_level: int = 10):
        self._timeout = timeout
        self._times = times
        self._show_response = show_response
        self._show_headers = show_headers
        self._session = requests.session()
        self._user_agent = random.choice(USER_AGENTS)
        self.logger = LogManager(level=log_level, add_file=False, add_stream=True).logger

    def request(self, method: str, url: str, *,
                params=None, data=None, headers=None, cookies=None, files=None,
                auth=None, timeout=None, allow_redirects=True, proxies=None,
                hooks=None, stream=None, verify=None, cert=None, json=None):
        return self._request(method, url,
                             params=params, data=data, headers=headers, cookies=cookies, files=files,
                             auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies,
                             hooks=hooks, stream=stream, verify=verify, cert=cert, json=json)

    def _request(self, *args, **kwargs) -> requests.Response:
        try:
            _, frame_num = get_frame(__file__)
            # 调整请求参数
            for subclass in IAdapter.__subclasses__():
                kwargs = subclass().adjust(self, *args, **kwargs)
            if self._show_headers:
                self.logger.debug(f'\nheaders = {json_.dumps(kwargs.get("headers"), indent=4)}', stacklevel=frame_num)
            durations, resp = timer(run(self._times)(self._session.request))(*args, **kwargs)
            if self._show_response:
                self.logger.debug(Response(resp, durations).show(), stacklevel=frame_num)
        except Exception as e:
            raise NetworkRequestException(e)
        return resp

    @staticmethod
    def _transcode(non_ascii: str):
        # 非ASCII码内容转码为unicode-escape编码
        return non_ascii.encode('unicode-escape').decode('utf-8')

    def add_cookies(self, cookies):
        if isinstance(cookies, str):
            cookie_dict = {}
            for cookie_pair in cookies.split('; '):
                k, v = cookie_pair.split('=', 1)
                cookie_dict[k] = v
            cookies = cookie_dict
        if isinstance(cookies, dict):
            cookies = {k: self._transcode(v) for k, v in cookies.items()}
            cookies = cookiejar_from_dict(cookies)
        self._session.cookies.update(cookies)

    @property
    def cookiejar(self):
        """返回cookiejar"""
        return self._session.cookies

    @property
    def cookiedict(self):
        """返回cookie字典"""
        return dict_from_cookiejar(self.cookiejar)

    @property
    def cookiestr(self):
        """返回cookie字符串"""
        cookies = []
        for cookie in self.cookiejar:
            cookies.append(f"{cookie.name}={cookie.value}; ")
        return "".join(cookies).strip('; ')

    def close(self):
        self._session.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __enter__(self):
        return self
