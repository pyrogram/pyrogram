# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2019 Dan Tès <https://github.com/delivrance>
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

from collections import OrderedDict
from datetime import datetime
from io import BytesIO
from json import dumps


class Object:
    all = {}

    __slots__ = []

    QUALNAME = "Base"

    @staticmethod
    def read(b: BytesIO, *args):
        return Object.all[int.from_bytes(b.read(4), "little")].read(b, *args)

    def write(self, *args) -> bytes:
        pass

    def __str__(self) -> str:
        return dumps(self, indent=4, default=default, ensure_ascii=False)

    def __len__(self) -> int:
        return len(self.write())

    def __getitem__(self, item):
        return getattr(self, item)


def remove_none(obj):
    if isinstance(obj, (list, tuple, set)):
        return type(obj)(remove_none(x) for x in obj if x is not None)
    elif isinstance(obj, dict):
        return type(obj)((remove_none(k), remove_none(v)) for k, v in obj.items() if k is not None and v is not None)
    else:
        return obj


def default(o: "Object"):
    try:
        content = {i: getattr(o, i) for i in o.__slots__}

        return remove_none(
            OrderedDict(
                [("_", o.QUALNAME)]
                + [i for i in content.items()]
            )
        )
    except AttributeError:
        if isinstance(o, datetime):
            return o.strftime("%d-%b-%Y %H:%M:%S")
        else:
            return repr(o)
