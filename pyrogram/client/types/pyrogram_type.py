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
from json import dumps, JSONEncoder


class PyrogramType:
    def __init__(self, client, raw):
        self._client = client
        self._raw = raw

    def __str__(self):
        return dumps(self, cls=Encoder, indent=4)

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
    def default(self, o: PyrogramType):
        content = {i: getattr(o, i) for i in filter(lambda x: not x.startswith("_"), o.__dict__)}
        return remove_none(OrderedDict([("_", "pyrogram:" + o.__class__.__name__)] + [i for i in content.items()]))
