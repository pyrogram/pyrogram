# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

try:
    from pyaes import AESModeOfOperationCTR
except ImportError:
    pass


class CTR:
    def __init__(self, key: bytes, iv: bytes):
        self.ctr = AESModeOfOperationCTR(key)
        self.iv = iv

    def decrypt(self, data: bytes, offset: int) -> bytes:
        replace = int.to_bytes(offset // 16, byteorder="big", length=4)
        iv = self.iv[:-4] + replace
        self.ctr._counter._counter = list(iv)

        return self.ctr.decrypt(data)
