# -*- coding: utf-8 -*-
# @Author      : BrotherBe
# @Time        : 2021/1/20 18:58
# @Version     : Python 3.8.5
import logging

from patterns import FlyWeight
from .level import _add_level, Levels_Map

_add_level()
SECRET = 100

logging.addLevelName(SECRET, 'SECRET')


class AESCBC(metaclass=FlyWeight):
    def __init__(self, key: bytes = None, iv: bytes = None):
        from Crypto.Cipher import AES
        self.key = key or b'THISISAESCBCMODE'
        self.iv = iv or b'THISISAESCBCMODE'
        self.cbc = AES.new(self.key, AES.MODE_CBC, self.iv)

    def encrypt(self, msg: str):
        from binascii import b2a_hex
        length = len(msg)
        add = 16 - (length % 16)
        msg += '\0' * add
        return b2a_hex(self.cbc.encrypt(msg.encode('utf-8'))).decode('utf-8')

    def decrypt(self, msg: str):
        from binascii import a2b_hex
        return self.cbc.decrypt(a2b_hex(msg)).decode('utf-8').rstrip('\0')


class DefaultLogger(Levels_Map['class']):

    def secret(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'ERROR'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.error("Houston, we have a %s", "major problem", exc_info=1)
        """
        if self.isEnabledFor(SECRET):
            msg = AESCBC().encrypt(msg)
            self._log(SECRET, msg, args, **kwargs)


logging.Logger.secret = DefaultLogger.secret
del DefaultLogger
DefaultLogger = logging.Logger
