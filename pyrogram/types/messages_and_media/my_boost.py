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

import pyrogram
from pyrogram import raw, types, utils
from ..object import Object


class MyBoost(Object):
    """Contains information about boost.

    Parameters:
        slot (``int``):
            Boost slot.

        date (:py:obj:`~datetime.datetime`):
            Date the boost was sent.

        expire_date (:py:obj:`~datetime.datetime`):
            Point in time when the boost will expire.

        chat (:obj:`~pyrogram.types.Chat`):
            Conversation the boost belongs to.

        cooldown_until_date (:py:obj:`~datetime.datetime`):
            Point in time when you'll be able to boost again.

    """

    def __init__(
        self,
        *,
        slot: int,
        chat: "types.Chat",
        date: datetime,
        expire_date: datetime,
        cooldown_until_date: datetime
    ):
        super().__init__()

        self.slot = slot
        self.chat = chat
        self.date = date
        self.expire_date = expire_date
        self.cooldown_until_date = cooldown_until_date

    @staticmethod
    def _parse(client: "pyrogram.Client", my_boost: "raw.types.MyBoost", users, chats) -> "MyBoost":
        peer_id = utils.get_raw_peer_id(my_boost.peer)

        if isinstance(my_boost.peer, raw.types.PeerChannel):
            chat = types.Chat._parse_channel_chat(client, chats.get(peer_id, None))
        else:
            chat = types.Chat._parse_user_chat(client, users.get(peer_id, None))

        return MyBoost(
            slot=my_boost.slot,
            chat=chat,
            date=utils.timestamp_to_datetime(my_boost.date),
            expire_date=utils.timestamp_to_datetime(my_boost.expire_date),
            cooldown_until_date=utils.timestamp_to_datetime(my_boost.cooldown_until_date),
        )
