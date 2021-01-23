# -*- coding: utf-8 -*-
# @Author      : BrotherBe
# @Time        : 2021/1/20 19:30
# @Version     : Python 3.8.5
import os


class Magic(object):
    close = 0  # 关闭所有属性
    highlight = 1  # 设置高亮度
    italic = 3  # 斜体
    underline = 4  # 下划线
    flash = 5  # 闪烁
    reverse = 7  # 反显
    blank = 8  # 隐藏
    strikethrough = 9  # 删除线


class ForeColor(object):
    black = 30
    red = 31
    green = 32
    yellow = 33
    dark_blue = 34
    wine = 35
    cyan = 36
    grey = 37
    white = 38


class BackColor(object):
    black = 40
    red = 41
    green = 42
    yellow = 43
    dark_blue = 44
    wine = 45
    cyan = 46
    grey = 47
    white = 38


if os.name == 'nt':
    ForeColor.blue = 94
    ForeColor.yellow = 93
