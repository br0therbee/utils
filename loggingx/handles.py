# -*- coding: utf-8 -*-
# @Author      : BrotherBe
# @Time        : 2021/1/21 11:33
# @Version     : Python 3.8.5
import logging

from .level import _NameColorMap


class ColorStreamHandler(logging.StreamHandler):
    """
    带颜色的控制台日志输出
    """

    def __init__(self, stream=None):
        """
        Initialize the handler.
        If stream is not specified, sys.stderr is used.
        """
        super().__init__(stream)

    def emit(self, record):
        """
        Emit a record.
        If a formatter is specified, it is used to format the record.
        The record is then written to the stream with a trailing newline.  If
        exception information is present, it is formatted using
        traceback.print_exception and appended to the stream.  If the stream
        has an 'encoding' attribute, it is used to determine how to do the
        output to the stream.
        """
        try:
            msg = self.format(record)
            stream = self.stream
            stream.write(f'\033[{_NameColorMap[record.levelname]}m{msg}\033[0m')
            stream.write(self.terminator)
            self.flush()
        except (OSError, IOError, Exception):
            self.handleError(record)
