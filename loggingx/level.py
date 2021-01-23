# -*- coding: utf-8 -*-
# @Author      : BrotherBe
# @Time        : 2021/1/22 11:20
# @Version     : Python 3.8.5
import logging

from .font import Magic, ForeColor

Levels_Map = {
    'class': logging.Logger,
    'levels': {}
}
# REMIND: 新增日志等级
# class Test(logging.Logger):
#     def test(self, msg, *args, **kwargs):
#         """
#         Log 'msg % args' with severity 'ERROR'.
#
#         To pass exception information, use the keyword argument exc_info with
#         a true value, e.g.
#
#         logger.error("Houston, we have a %s", "major problem", exc_info=1)
#         """
#         if self.isEnabledFor(80):
#             self._log(80, msg, args, **kwargs)
#
# from loggingx import level
# level.Levels_Map = {
#     'class': Test,
#     'levels': {
#         'TEST': {
#             'level': 80,
#             'class_func': Test.test,
#             'color': f'{Magic.highlight};{Magic.italic};{ForeColor.grey}',
#         }
#     }
# }
_NameColorMap = {
    'DEBUG': f'{Magic.highlight};{Magic.italic};{ForeColor.cyan}',
    'INFO': f'{Magic.highlight};{Magic.italic};{ForeColor.green}',
    'WARNING': f'{Magic.highlight};{Magic.italic};{ForeColor.yellow}',
    'ERROR': f'{Magic.highlight};{Magic.italic};{ForeColor.red}',
    'CRITICAL': f'{Magic.highlight};{Magic.italic};{ForeColor.wine}',
    'SECRET': f'{Magic.highlight};{Magic.italic};{ForeColor.grey}',
}


def _add_level():
    if not hasattr(_add_level, '_run_once'):
        _add_level._run_once = True
        for _name, _level in Levels_Map['levels'].items():
            _class_func = _level['class_func']
            logging.addLevelName(_level['level'], _name)
            setattr(logging.Logger, _class_func.__name__, _class_func)
            _NameColorMap[_name] = _level['color']
