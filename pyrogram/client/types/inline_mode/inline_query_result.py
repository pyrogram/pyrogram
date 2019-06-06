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

from ..object import Object

"""- :obj:`InlineQueryResultCachedAudio`
    - :obj:`InlineQueryResultCachedDocument`
    - :obj:`InlineQueryResultCachedGif`
    - :obj:`InlineQueryResultCachedMpeg4Gif`
    - :obj:`InlineQueryResultCachedPhoto`
    - :obj:`InlineQueryResultCachedSticker`
    - :obj:`InlineQueryResultCachedVideo`
    - :obj:`InlineQueryResultCachedVoice`
    - :obj:`InlineQueryResultAudio`
    - :obj:`InlineQueryResultContact`
    - :obj:`InlineQueryResultGame`
    - :obj:`InlineQueryResultDocument`
    - :obj:`InlineQueryResultGif`
    - :obj:`InlineQueryResultLocation`
    - :obj:`InlineQueryResultMpeg4Gif`
    - :obj:`InlineQueryResultPhoto`
    - :obj:`InlineQueryResultVenue`
    - :obj:`InlineQueryResultVideo`
    - :obj:`InlineQueryResultVoice`"""


class InlineQueryResult(Object):
    """One result of an inline query.

    Pyrogram currently supports results of the following types:

    - :obj:`InlineQueryResultArticle`
    """

    __slots__ = ["type", "id"]

    def __init__(self, type: str, id: str):
        super().__init__()

        self.type = type
        self.id = id

    async def write(self):
        pass
