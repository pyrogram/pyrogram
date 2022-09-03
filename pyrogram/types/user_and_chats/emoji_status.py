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

from datetime import datetime
from typing import Optional

import pyrogram
from pyrogram import raw
from pyrogram import utils
from ..object import Object


class EmojiStatus(Object):
    """A user emoji status.

    Parameters:
        custom_emoji_id (``int``):
            Custom emoji id.

        until_date (:py:obj:`~datetime.datetime`, *optional*):
            Valid until date.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        custom_emoji_id: int,
        until_date: Optional[datetime] = None
    ):
        super().__init__(client)

        self.custom_emoji_id = custom_emoji_id
        self.until_date = until_date

    @staticmethod
    def _parse(client, emoji_status: "raw.base.EmojiStatus") -> Optional["EmojiStatus"]:
        if isinstance(emoji_status, raw.types.EmojiStatus):
            return EmojiStatus(
                client=client,
                custom_emoji_id=emoji_status.document_id
            )

        if isinstance(emoji_status, raw.types.EmojiStatusUntil):
            return EmojiStatus(
                client=client,
                custom_emoji_id=emoji_status.document_id,
                until_date=utils.timestamp_to_datetime(emoji_status.until)
            )

        return None

    def write(self):
        if self.until_date:
            return raw.types.EmojiStatusUntil(
                document_id=self.custom_emoji_id,
                until=utils.datetime_to_timestamp(self.until_date)
            )

        return raw.types.EmojiStatus(
            document_id=self.custom_emoji_id
        )
