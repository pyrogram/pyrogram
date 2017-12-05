# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017 Dan Tès <https://github.com/delivrance>
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
from importlib import import_module
from io import BytesIO
from json import JSONEncoder, dumps

from ..all import objects


class Object:
    @staticmethod
    def read(b: BytesIO, *args):
        id = int.from_bytes(b.read(4), "little")
        name = objects.get(id)
        path, name = name.rsplit(".", 1)

        return getattr(
            import_module("pyrogram.api." + path),
            name
        ).read(b, *args)

    def write(self, *args) -> bytes:
        pass

    def __str__(self) -> str:
        return dumps(self, cls=Encoder, indent=4)

    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__

    def __len__(self) -> int:
        return len(self.write())

    def __call__(self):
        pass


class Encoder(JSONEncoder):
    def default(self, o: Object):
        try:
            content = o.__dict__
        except AttributeError:
            if isinstance(o, datetime):
                return o.strftime("%d-%b-%Y %H:%M:%S")
            else:
                return repr(o)

        return OrderedDict(
            [("_", objects.get(getattr(o, "ID", None), None))]
            + [i for i in content.items()]
        )
