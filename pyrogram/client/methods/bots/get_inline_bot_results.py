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

from pyrogram.api import functions, types
from pyrogram.api.errors import UnknownError
from pyrogram.client.ext import BaseClient


class GetInlineBotResults(BaseClient):
    def get_inline_bot_results(self,
                               bot: int or str,
                               query: str,
                               offset: str = "",
                               latitude: float = None,
                               longitude: float = None):
        """Use this method to get bot results via inline queries.
        You can then send a result using :obj:`send_inline_bot_result <pyrogram.Client.send_inline_bot_result>`

        Args:
            bot (``int`` | ``str``):
                Unique identifier of the inline bot you want to get results from. You can specify
                a @username (str) or a bot ID (int).

            query (``str``):
                Text of the query (up to 512 characters).

            offset (``str``, *optional*):
                Offset of the results to be returned.

            latitude (``float``, *optional*):
                Latitude of the location.
                Useful for location-based results only.

            longitude (``float``, *optional*):
                Longitude of the location.
                Useful for location-based results only.

        Returns:
            On Success, :obj:`BotResults <pyrogram.api.types.messages.BotResults>` is returned.

        Raises:
            :class:`Error <pyrogram.Error>`
            ``TimeoutError``: If the bot fails to answer within 10 seconds
        """
        # TODO: Don't return the raw type

        try:
            return self.send(
                functions.messages.GetInlineBotResults(
                    bot=self.resolve_peer(bot),
                    peer=types.InputPeerSelf(),
                    query=query,
                    offset=offset,
                    geo_point=types.InputGeoPoint(
                        lat=latitude,
                        long=longitude
                    ) if (latitude is not None and longitude is not None) else None
                )
            )
        except UnknownError as e:
            # TODO: Add this -503 Timeout error into the Error DB
            if e.x.error_code == -503 and e.x.error_message == "Timeout":
                raise TimeoutError("The inline bot didn't answer in time") from None
            else:
                raise e
