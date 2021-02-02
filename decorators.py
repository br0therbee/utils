# -*- coding: utf-8 -*-
# @Author      : BrotherBe
# @Time        : 2020/7/25 0:49
# @Version     : Python 3.8.5
import functools
import time
from pathlib import Path
from threading import Thread, RLock

from commons import makekeys, get_funcname, get_qualname
from loggingx.manager import LogManager

logger = LogManager(Path(__file__).stem).logger


def circulate(sleep: int = 1, is_block: bool = True):
    flag = f'<decorators {get_funcname()}>'

    def _circulate(func):
        prefix = f'{flag} <{get_qualname(func)}>'

        @functools.wraps(func)
        def __circulate(*args, **kwargs):
            def ___circulate():
                while True:
                    logger.info(f'{prefix} is going to start!')
                    try:
                        func(*args, **kwargs)
                    except Exception as e:
                        logger.exception(f'{prefix} {e}')
                    logger.info(f'{prefix} finished! Sleep {sleep} seconds!')
                    time.sleep(sleep)

            if is_block:
                return ___circulate()
            else:
                Thread(target=___circulate).start()

        return __circulate

    return _circulate


def run(times: int = 1, sleep_time: int = 1, is_throw_error: bool = True):
    def _run(func):

        @functools.wraps(func)
        def __run(*args, **kwargs):
            for t in range(times):
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    if t == times - 1 and is_throw_error:
                        raise e
                else:
                    return result
                time.sleep(sleep_time)

        return __run

    return _run


def timer(func):
    @functools.wraps(func)
    def _timer(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = f'{end_time - start_time:.3f} s'
        return duration, result

    return _timer


class FunctionResult(object):
    _caches = {}

    @classmethod
    def cache(cls, duration: float):
        def _cache(func):
            @functools.wraps(func)
            def __cache(*args, **kwargs):
                if not hasattr(func, '__result_lock'):
                    func.__result_lock = RLock()
                key = func, makekeys(args, kwargs, func)
                if key not in cls._caches or time.time() - cls._caches[key][1] > duration:
                    with func.__result_lock:
                        result = func(*args, **kwargs)
                        cls._caches[key] = result, time.time()
                return cls._caches[key][0]

            return __cache

        return _cache
