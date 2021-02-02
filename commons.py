# -*- coding: utf-8 -*-
# @Author      : BrotherBe
# @Time        : 2020/8/17 22:06
# @Version     : Python 3.8.5
import copy
import inspect
import json
import math
import multiprocessing
import os
import platform
import random
import re
import sys
import time
import typing
from threading import Thread
from urllib.parse import urlparse, parse_qsl

RE_CHARACTERS = re.compile(r'\w+')


def ciphers(length: int) -> str:
    seed = '0123456789abcdef'
    seed = math.ceil(length / len(seed)) * seed
    return ''.join(random.sample(seed, length))


def current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def first(data, default=''):
    try:
        if isinstance(data, typing.Match):
            return data.group(1)
        else:
            return data[0]
    except (IndexError, Exception):
        return default


def get_frame(filepath):
    filepath = os.path.normcase(filepath)
    frame_num = 1
    f = sys._getframe(frame_num)
    while hasattr(f, "f_code"):
        code = f.f_code
        filename = os.path.normcase(code.co_filename)
        if filename == filepath:
            f = f.f_back
            frame_num += 1
            continue
        break
    else:
        frame_num -= 1
    return code, frame_num


def get_funcname():
    return sys._getframe(1).f_code.co_name


def get_qualname(func):
    if '__self__' in dir(func):
        self_ = func.__self__
        try:
            cls_name = self_.__name__
        except AttributeError:
            cls_name = type(self_).__name__
        func_name = f'{cls_name}.{func.__name__}'
    else:
        func_name = func.__qualname__
    return f'{type(func).__name__} {func_name}'


def get_params(url):
    query = urlparse(url).query
    params = dict(parse_qsl(query))
    return params


def import_module(module_name: str, module_path: str, filter_stems: set = None):
    import importlib
    from pathlib import Path
    if filter_stems is None:
        filter_stems = set()
    # 导入module下所有模块
    for file in Path(module_path).parent.iterdir():
        if file.suffix == '.py' and file.stem not in filter_stems:
            importlib.import_module(f'{module_name}.{file.stem}')


def is_subprocess():
    if sys.version_info >= (3, 8):
        return bool(multiprocessing.process.parent_process())
    else:
        cur_process = multiprocessing.current_process().name
        return cur_process != 'MainProcess'


def is_windows():
    return platform.system().lower() == 'windows'


def makekeys(args: tuple, kwargs: dict, func) -> tuple:
    makekeys.cache = {}
    # 妥协,直接根据名称过滤,实在找不到更好的过滤办法
    makekeys.filter_args = 'self', 'cls'

    def _default_kwargs():
        __args_num = 0
        __default_kwargs = {}
        signatures = inspect.signature(func)
        for _, parameter in signatures.parameters.items():
            name = parameter.name
            value = parameter.default
            if value == inspect._empty:
                if name not in makekeys.filter_args:
                    __args_num += 1
            else:
                __default_kwargs[name] = value
        return __args_num, __default_kwargs

    def _sort_kwargs():
        nonlocal args
        pos_kwargs = args[args_num:]
        args = args[:args_num]
        for (key, value), pos_kwarg in zip(copy.deepcopy(default_kwargs).items(), pos_kwargs):
            default_kwargs[key] = pos_kwarg
        default_kwargs.update(kwargs)

    if func not in makekeys.cache:
        makekeys.cache[func] = _default_kwargs()
    args_num, default_kwargs = copy.deepcopy(makekeys.cache[func])
    _sort_kwargs()
    for item in sorted(default_kwargs.items(), key=lambda x: x[0]):
        args += item
    return args


def pretty_headers(headers: (list, dict), separator: str = ': '):
    header_dict = {}
    if isinstance(headers, dict):
        header_dict = headers
    else:
        for item in headers:
            if item.strip():
                key, value = item.strip(',').split(separator, 1)
                header_dict[key.strip()] = value.strip()
    print(json.dumps(header_dict, ensure_ascii=False, indent=4))


def remove_special_characters(stings: str):
    stings = RE_CHARACTERS.findall(stings)
    return ''.join(stings)


def runfile(filepath: str):
    def _runfile():
        os.system(f'{sys.executable} {filepath}')

    Thread(target=_runfile).start()


class CustomDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class TimerContextManager(object):

    def __init__(self):
        _frame = sys._getframe(1)
        self._line = _frame.f_lineno
        self._filename = _frame.f_code.co_filename
        self._start = time.time()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.time()
        cost = f'{end - self._start:.3f}'
        stdout = f'{self._filename}:{self._line}  \033[0m{time.strftime("%Y-%m-%d %H:%M:%S")}  用时 {cost} 秒\n\033[0m'
        sys.stdout.write(stdout)
