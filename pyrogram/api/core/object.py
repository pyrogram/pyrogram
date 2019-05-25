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
    def read(b: BytesIO, *args):  # TODO: Rename b -> data
        return Object.all[int.from_bytes(b.read(4), "little")].read(b, *args)

    def write(self, *args) -> bytes:
        pass

    def __eq__(self, other: "Object") -> bool:
        for attr in self.__slots__:
            try:
                if getattr(self, attr) != getattr(other, attr):
                    return False
            except AttributeError:
                return False

        return True

    def __str__(self) -> str:
        def default(obj: Object):
            try:
                return OrderedDict(
                    [("_", obj.QUALNAME)]
                    + [(attr, getattr(obj, attr))
                       for attr in obj.__slots__
                       if getattr(obj, attr) is not None]
                )
            except AttributeError:
                if isinstance(obj, datetime):
                    return obj.strftime("%d-%b-%Y %H:%M:%S")
                else:
                    return repr(obj)

        return dumps(self, indent=4, default=default, ensure_ascii=False)

    def __repr__(self) -> str:
        return "pyrogram.api.{}({})".format(
            self.QUALNAME,
            ", ".join(
                "{}={}".format(attr, repr(getattr(self, attr)))
                for attr in self.__slots__
                if getattr(self, attr) is not None
            )
        )

    def __len__(self) -> int:
        return len(self.write())

    def __getitem__(self, item):
        return getattr(self, item)
