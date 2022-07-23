#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
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

import pyrogram
from pyrogram import raw, types
from .inline_query_result import InlineQueryResult


class InlineQueryResultLocation(InlineQueryResult):
    """A location on a map.

    By default, the location will be sent by the user. Alternatively, you can use *input_message_content* to send a
    message with the specified content instead of the location.

    Parameters:
        title (``str``):
            Title for the result.

        latitude (``float``):
            Location latitude in degrees.

        longitude (``float``):
            Location longitude in degrees.

        id (``str``, *optional*):
            Unique identifier for this result, 1-64 bytes.
            Defaults to a randomly generated UUID4.

        horizontal_accuracy (``float``, *optional*)
            The radius of uncertainty for the location, measured in meters; 0-1500.

        live_period (``int``, *optional*):
            Period in seconds for which the location can be updated, should be between 60 and 86400.

        heading (``int``, *optional*):
            For live locations, a direction in which the user is moving, in degrees.
            Must be between 1 and 360 if specified.

        proximity_alert_radius (``int``, *optional*):
            For live locations, a maximum distance for proximity alerts about approaching another chat member,
            in meters. Must be between 1 and 100000 if specified.

        reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
            Inline keyboard attached to the message.

        input_message_content (:obj:`~pyrogram.types.InputMessageContent`):
            Content of the message to be sent instead of the file.

        thumb_url (``str``, *optional*):
            Url of the thumbnail for the result.

        thumb_width (``int``, *optional*):
            Thumbnail width.

        thumb_height (``int``, *optional*):
            Thumbnail height.
    """

    def __init__(
        self,
        title: str,
        latitude: float,
        longitude: float,
        horizontal_accuracy: float = None,
        live_period: int = None,
        heading: int = None,
        proximity_alert_radius: int = None,
        id: str = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        input_message_content: "types.InputMessageContent" = None,
        thumb_url: str = None,
        thumb_width: int = 0,
        thumb_height: int = 0
    ):
        super().__init__("location", id, input_message_content, reply_markup)

        self.title = title
        self.latitude = latitude
        self.longitude = longitude
        self.horizontal_accuracy = horizontal_accuracy
        self.live_period = live_period
        self.heading = heading
        self.proximity_alert_radius = proximity_alert_radius
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height

    async def write(self, client: "pyrogram.Client"):
        return raw.types.InputBotInlineResult(
            id=self.id,
            type=self.type,
            title=self.title,
            send_message=(
                await self.input_message_content.write(client, self.reply_markup)
                if self.input_message_content
                else raw.types.InputBotInlineMessageMediaGeo(
                    geo_point=raw.types.InputGeoPoint(
                        lat=self.latitude,
                        long=self.longitude
                    ),
                    heading=self.heading,
                    period=self.live_period,
                    proximity_notification_radius=self.proximity_alert_radius,
                    reply_markup=await self.reply_markup.write(client) if self.reply_markup else None
                )
            )
        )
