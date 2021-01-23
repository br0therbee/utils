# -*- coding: utf-8 -*-
# @Author      : BrotherBe
# @Time        : 2021/1/21 11:36
# @Version     : Python 3.8.5
import logging
import os
from logging.handlers import TimedRotatingFileHandler, BaseRotatingHandler
from pathlib import Path
from threading import RLock

from commons import is_subprocess
from patterns import FlyWeight
from .default_level import DefaultLogger
from .formatter import Formatter
from .handles import ColorStreamHandler

LevelToName = logging._levelToName
NameToLevel = logging._nameToLevel


class LogManager(metaclass=FlyWeight):
    _lock = RLock()
    _names = {}

    def __init__(self,
                 name: str = 'temp', level: int = NameToLevel['DEBUG'],
                 *,
                 add_stream: bool = True, stream_level: int = None,
                 add_file: bool = True, file_level: int = None,
                 filename: str = None, folder_path: str = None, backup_count: int = 50):
        """
        日志管理器
        多进程下文件名必须添加进程ID, 否则文件会切片错误
        """
        if is_subprocess():
            name = f"{name}_{os.getppid()}_{os.getpid()}"
        self._keys = {}

        # 添加日志
        self._name = self._get_name(name)
        self._level = level
        self.logger: DefaultLogger = logging.getLogger(self._name)
        self.logger.setLevel(self._level)

        # 添加控制台句柄
        self._add_stream = add_stream
        if self._add_stream:
            self._stream_level = stream_level or self._level
            self._stream()

        # 添加文件句柄
        self._add_file = add_file
        if self._add_file:
            self._file_level = file_level or self._level
            self._backup_count = backup_count
            self._path = self._get_path(filename or name, folder_path)
            self._file()
        # self.logger.critical(self._names)

    def _get_name(self, name):
        # REMIND: 同一日志名称但是不同日志等级, 会产生两个日志名称, 以防止相同日志名引发重复打印问题
        if name in self._names:
            name_ = self._names[name][-1].rsplit('_', 1)
            if len(name_) == 2:
                stem, suffix = name_
                try:
                    suffix = int(suffix)
                except ValueError:
                    stem = name
                    suffix = 0
            else:
                stem = name
                suffix = 0
            self._names[name].append(f'{stem}_{suffix + 1}')
        else:
            self._names[name] = [name]
        return self._names[name][-1]

    def _get_path(self, filename, folder_path):
        if not filename.endswith('log'):
            filename = f'{filename}.log'
        self._filename = filename
        self._folder_path = Path(folder_path or Path(Path(__file__).absolute().root) / 'pythonlogs')
        self._folder_path.mkdir(parents=True, exist_ok=True)
        return self._folder_path / self._filename

    def _stream(self):
        """
        添加控制台日志
        Returns:
        """
        self.__add_a_handler(ColorStreamHandler, level=self._stream_level, formatter=Formatter.stream)

    def _file(self):
        """
        添加文件日志
        Returns:
        """
        self.__add_a_handler(TimedRotatingFileHandler, level=self._file_level, path=self._path,
                             formatter=Formatter.file, backup_count=self._backup_count)

    def __add_a_handler(self, handler_type: type, level: int = NameToLevel['DEBUG'],
                        formatter: logging.Formatter = None, path: str = None, backup_count: int = 50):
        with self._lock:
            key = handler_type
            if key not in self._keys:
                if issubclass(handler_type, ColorStreamHandler):
                    handler = ColorStreamHandler()
                elif issubclass(handler_type, BaseRotatingHandler):
                    handler = TimedRotatingFileHandler(path, when='D', backupCount=backup_count, encoding="utf-8")
                handler.setLevel(level)
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)
                self._keys[key] = handler
