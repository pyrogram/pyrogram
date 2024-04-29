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

from pyrogram import raw, types, utils
from ..object import Object


class CheckedGiftCode(Object):
    """Contains checked gift code data.

    Parameters:
        date (:py:obj:`~datetime.datetime`):
            Date when the giveaway was launched.

        months (``int``):
            Number of months of subscription.

        via_giveaway (``bool``, *optional*):
            True if the gift code is received via giveaway.

        from_chat (:obj:`~pyrogram.types.Chat`, *optional*):
            The channel where the gift code was won.

        winner (:obj:`~pyrogram.types.User`, *optional*):
            The user who won the giveaway.

        giveaway_message_id (``int``, *optional*):
            Identifier of the message from chat where the giveaway was launched.

        used_date (:py:obj:`~datetime.datetime`, *optional*):
            Date when the gift code was used.
    """

    def __init__(
        self,
        *,
        date: datetime,
        months: int,
        via_giveaway: bool = None,
        from_chat: "types.Chat" = None,
        winner: "types.User" = None,
        giveaway_message_id: int = None,
        used_date: datetime = None
    ):
        super().__init__()

        self.date = date
        self.months = months
        self.via_giveaway = via_giveaway
        self.from_chat = from_chat
        self.winner = winner
        self.giveaway_message_id = giveaway_message_id
        self.used_date = used_date

    @staticmethod
    def _parse(client, checked_gift_code: "raw.types.payments.CheckedGiftCode", users, chats):
        from_chat = None
        winner = None

        if getattr(checked_gift_code, "from_id", None):
            from_chat = types.Chat._parse_chat(
                client, chats.get(utils.get_raw_peer_id(checked_gift_code.from_id))
            )
        if getattr(checked_gift_code, "to_id", None):
            winner = types.User._parse(client, users.get(checked_gift_code.to_id))

        return CheckedGiftCode(
            date=utils.timestamp_to_datetime(checked_gift_code.date),
            months=checked_gift_code.months,
            via_giveaway=getattr(checked_gift_code, "via_giveaway", None),
            from_chat=from_chat,
            winner=winner,
            giveaway_message_id=getattr(checked_gift_code, "giveaway_msg_id", None),
            used_date=utils.timestamp_to_datetime(checked_gift_code.used_date) if getattr(checked_gift_code, "used_date") else None,
        )
