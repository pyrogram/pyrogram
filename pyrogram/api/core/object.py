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

from collections import OrderedDict
from datetime import datetime
from io import BytesIO
from json import JSONEncoder, dumps

from ..all import objects


class Object:
    all = {}

    @staticmethod
    def read(b: BytesIO, *args):
        return Object.all[int.from_bytes(b.read(4), "little")].read(b, *args)

    def write(self, *args) -> bytes:
        pass

    def __str__(self) -> str:
        return dumps(self, cls=Encoder, indent=4)

    def __bool__(self) -> bool:
        return True

    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__

    def __len__(self) -> int:
        return len(self.write())

    def __call__(self):
        pass

    def __getitem__(self, item):
        return getattr(self, item)


def remove_none(obj):
    if isinstance(obj, (list, tuple, set)):
        return type(obj)(remove_none(x) for x in obj if x is not None)
    elif isinstance(obj, dict):
        return type(obj)((remove_none(k), remove_none(v)) for k, v in obj.items() if k is not None and v is not None)
    else:
        return obj


class Encoder(JSONEncoder):
    def default(self, o: Object):
        try:
            content = o.__dict__
        except AttributeError:
            if isinstance(o, datetime):
                return o.strftime("%d-%b-%Y %H:%M:%S")
            else:
                return repr(o)

        name = o.__class__.__name__
        o = objects.get(getattr(o, "ID", None), None)

        if o is not None:
            if o.startswith("pyrogram.client"):
                r = remove_none(OrderedDict([("_", "pyrogram:" + name)] + [i for i in content.items()]))
                r.pop("_client", None)

                return r
            else:
                return OrderedDict(
                    [("_", o.replace("pyrogram.api.types.", "telegram:"))]
                    + [i for i in content.items()]
                )
        else:
            return None
