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

import asyncio
import logging
from typing import List

import pyrogram
from pyrogram.api import functions, types
from pyrogram.errors import FloodWait

from ...ext import BaseClient, utils

log = logging.getLogger(__name__)


class GetDialogs(BaseClient):
    async def get_dialogs(
        self,
        offset_date: int = 0,
        limit: int = 100,
        pinned_only: bool = False
    ) -> List["pyrogram.Dialog"]:
        """Get a chunk of the user's dialogs.

        You can get up to 100 dialogs at once.
        For a more convenient way of getting a user's dialogs see :meth:`~Client.iter_dialogs`.

        Parameters:
            offset_date (``int``):
                The offset date in Unix time taken from the top message of a :obj:`Dialog`.
                Defaults to 0. Valid for non-pinned dialogs only.

            limit (``str``, *optional*):
                Limits the number of dialogs to be retrieved.
                Defaults to 100. Valid for non-pinned dialogs only.

            pinned_only (``bool``, *optional*):
                Pass True if you want to get only pinned dialogs.
                Defaults to False.

        Returns:
            List of :obj:`Dialog`: On success, a list of dialogs is returned.

        Example:
            .. code-block:: python

                # Get first 100 dialogs
                app.get_dialogs()

                # Get pinned dialogs
                app.get_dialogs(pinned_only=True)
        """

        while True:
            try:
                if pinned_only:
                    r = await self.send(functions.messages.GetPinnedDialogs(folder_id=0))
                else:
                    r = await self.send(
                        functions.messages.GetDialogs(
                            offset_date=offset_date,
                            offset_id=0,
                            offset_peer=types.InputPeerEmpty(),
                            limit=limit,
                            hash=0,
                            exclude_pinned=True
                        )
                    )
            except FloodWait as e:
                log.warning("Sleeping for {}s".format(e.x))
                await asyncio.sleep(e.x)
            else:
                break

        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}

        messages = {}

        for message in r.messages:
            to_id = message.to_id

            if isinstance(to_id, types.PeerUser):
                if message.out:
                    chat_id = to_id.user_id
                else:
                    chat_id = message.from_id
            else:
                chat_id = utils.get_peer_id(to_id)

            messages[chat_id] = await pyrogram.Message._parse(self, message, users, chats)

        parsed_dialogs = []

        for dialog in r.dialogs:
            if not isinstance(dialog, types.Dialog):
                continue

            parsed_dialogs.append(pyrogram.Dialog._parse(self, dialog, messages, users, chats))

        return pyrogram.List(parsed_dialogs)
