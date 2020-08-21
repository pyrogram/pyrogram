#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2020 Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import asyncio


class Filter:
    def __call__(self, message):
        raise NotImplementedError

    def __invert__(self):
        return InvertFilter(self)

    def __and__(self, other):
        return AndFilter(self, other)

    def __or__(self, other):
        return OrFilter(self, other)


class InvertFilter(Filter):
    def __init__(self, base):
        self.base = base

    async def __call__(self, message):
        if asyncio.iscoroutinefunction(self.base.__call__):
            x = await self.base(message)
        else:
            x = self.base(message)

        return not x


class AndFilter(Filter):
    def __init__(self, base, other):
        self.base = base
        self.other = other

    async def __call__(self, message):
        if asyncio.iscoroutinefunction(self.base.__call__):
            x = await self.base(message)
        else:
            x = self.base(message)

        if asyncio.iscoroutinefunction(self.other.__call__):
            y = await self.other(message)
        else:
            y = self.other(message)

        return x and y


class OrFilter(Filter):
    def __init__(self, base, other):
        self.base = base
        self.other = other

    async def __call__(self, message):
        if asyncio.iscoroutinefunction(self.base.__call__):
            x = await self.base(message)
        else:
            x = self.base(message)

        if asyncio.iscoroutinefunction(self.other.__call__):
            y = await self.other(message)
        else:
            y = self.other(message)

        return x or y
