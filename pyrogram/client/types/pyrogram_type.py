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
from json import dumps

import pyrogram


class PyrogramType:
    __slots__ = ["_client"]

    def __init__(self, client: "pyrogram.BaseClient" = None):
        self._client = client

        if self._client is None:
            del self._client

    def __eq__(self, other: "PyrogramType") -> bool:
        for attr in self.__slots__:
            try:
                if getattr(self, attr) != getattr(other, attr):
                    return False
            except AttributeError:
                return False

        return True

    def __str__(self) -> str:
        def default(obj: PyrogramType):
            try:
                return OrderedDict(
                    [("_", "pyrogram." + obj.__class__.__name__)]
                    + [(attr, getattr(obj, attr))
                       for attr in obj.__slots__
                       if getattr(obj, attr) is not None]
                )
            except AttributeError:
                return repr(obj)

        return dumps(self, indent=4, default=default, ensure_ascii=False)

    def __repr__(self) -> str:
        return "pyrogram.{}({})".format(
            self.__class__.__name__,
            ", ".join(
                "{}={}".format(attr, repr(getattr(self, attr)))
                for attr in self.__slots__
                if getattr(self, attr) is not None
            )
        )

    def __getitem__(self, item):
        return getattr(self, item)
