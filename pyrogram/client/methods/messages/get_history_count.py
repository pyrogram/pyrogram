# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2019 Dan Tès <https://github.com/delivrance>
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

import logging
import time
from typing import Union

from pyrogram.api import types, functions
from pyrogram.client.ext import BaseClient
from pyrogram.errors import FloodWait

log = logging.getLogger(__name__)


class GetHistoryCount(BaseClient):
    def get_history_count(
        self,
        chat_id: Union[int, str]
    ) -> int:
        """Use this method to get the total count of messages in a chat.

        .. note::

            Due to Telegram latest internal changes, the server can't reliably find anymore the total count of messages
            a **private** or a **basic group** chat has with a single method call. To overcome this limitation, Pyrogram
            has to iterate over all the messages. Channels and supergroups are not affected by this limitation.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

        Returns:
            ``int``: On success, an integer is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        peer = self.resolve_peer(chat_id)

        if not isinstance(peer, types.InputPeerChannel):
            offset = 0
            limit = 100

            while True:
                try:
                    r = self.send(
                        functions.messages.GetHistory(
                            peer=peer,
                            offset_id=1,
                            offset_date=0,
                            add_offset=-offset - limit,
                            limit=limit,
                            max_id=0,
                            min_id=0,
                            hash=0
                        )
                    )
                except FloodWait as e:
                    log.warning("Sleeping for {}s".format(e.x))
                    time.sleep(e.x)
                    continue

                if not r.messages:
                    return offset

                offset += len(r.messages)

        return self.get_history(chat_id=chat_id, limit=1).total_count
