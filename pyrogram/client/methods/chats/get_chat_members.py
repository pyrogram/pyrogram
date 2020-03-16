# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2020 Dan <https://github.com/delivrance>
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
from typing import Union, List

import pyrogram
from pyrogram.api import functions, types
from pyrogram.errors import FloodWait
from ...ext import BaseClient

log = logging.getLogger(__name__)


class Filters:
    ALL = "all"
    KICKED = "kicked"
    RESTRICTED = "restricted"
    BOTS = "bots"
    RECENT = "recent"
    ADMINISTRATORS = "administrators"


class GetChatMembers(BaseClient):
    def get_chat_members(
        self,
        chat_id: Union[int, str],
        offset: int = 0,
        limit: int = 200,
        query: str = "",
        filter: str = Filters.ALL
    ) -> List["pyrogram.ChatMember"]:
        """Get a chunk of the members list of a chat.

        You can get up to 200 chat members at once.
        A chat can be either a basic group, a supergroup or a channel.
        You must be admin to retrieve the members list of a channel (also known as "subscribers").
        For a more convenient way of getting chat members see :meth:`~Client.iter_chat_members`.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            offset (``int``, *optional*):
                Sequential number of the first member to be returned.
                Only applicable to supergroups and channels. Defaults to 0 [1]_.

            limit (``int``, *optional*):
                Limits the number of members to be retrieved.
                Only applicable to supergroups and channels.
                Defaults to 200, which is also the maximum server limit allowed per method call.

            query (``str``, *optional*):
                Query string to filter members based on their display names and usernames.
                Only applicable to supergroups and channels. Defaults to "" (empty string) [2]_.

            filter (``str``, *optional*):
                Filter used to select the kind of members you want to retrieve. Only applicable for supergroups
                and channels. It can be any of the followings:
                *"all"* - all kind of members,
                *"kicked"* - kicked (banned) members only,
                *"restricted"* - restricted members only,
                *"bots"* - bots only,
                *"recent"* - recent members only,
                *"administrators"* - chat administrators only.
                Only applicable to supergroups and channels.
                Defaults to *"all"*.

        .. [1] Server limit: on supergroups, you can get up to 10,000 members for a single query and up to 200 members
            on channels.

        .. [2] A query string is applicable only for *"all"*, *"kicked"* and *"restricted"* filters only.

        Returns:
            List of :obj:`ChatMember`: On success, a list of chat members is returned.

        Raises:
            ValueError: In case you used an invalid filter or a chat id that belongs to a user.

        Example:
            .. code-block:: python

                # Get first 200 recent members
                app.get_chat_members("pyrogramchat")

                # Get all administrators
                app.get_chat_members("pyrogramchat", filter="administrators")

                # Get all bots
                app.get_chat_members("pyrogramchat", filter="bots")
        """
        peer = self.resolve_peer(chat_id)

        if isinstance(peer, types.InputPeerChat):
            r = self.send(
                functions.messages.GetFullChat(
                    chat_id=peer.chat_id
                )
            )

            members = r.full_chat.participants.participants
            users = {i.id: i for i in r.users}

            return pyrogram.List(pyrogram.ChatMember._parse(self, member, users) for member in members)
        elif isinstance(peer, types.InputPeerChannel):
            filter = filter.lower()

            if filter == Filters.ALL:
                filter = types.ChannelParticipantsSearch(q=query)
            elif filter == Filters.KICKED:
                filter = types.ChannelParticipantsKicked(q=query)
            elif filter == Filters.RESTRICTED:
                filter = types.ChannelParticipantsBanned(q=query)
            elif filter == Filters.BOTS:
                filter = types.ChannelParticipantsBots()
            elif filter == Filters.RECENT:
                filter = types.ChannelParticipantsRecent()
            elif filter == Filters.ADMINISTRATORS:
                filter = types.ChannelParticipantsAdmins()
            else:
                raise ValueError("Invalid filter \"{}\"".format(filter))

            while True:
                try:
                    r = self.send(
                        functions.channels.GetParticipants(
                            channel=peer,
                            filter=filter,
                            offset=offset,
                            limit=limit,
                            hash=0
                        )
                    )

                    members = r.participants
                    users = {i.id: i for i in r.users}

                    return pyrogram.List(pyrogram.ChatMember._parse(self, member, users) for member in members)
                except FloodWait as e:
                    log.warning("Sleeping for {}s".format(e.x))
                    time.sleep(e.x)
        else:
            raise ValueError("The chat_id \"{}\" belongs to a user".format(chat_id))
