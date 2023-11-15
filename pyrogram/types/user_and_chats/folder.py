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

from typing import List, Union

import pyrogram
from pyrogram import raw
from pyrogram import types
from ..object import Object
from ... import utils


class Folder(Object):
    """A user's folder.

    Parameters:
        id (``int``):
            The folder id.

        title (``str``):
            The folder title.

        pinned_peers (List of :obj:`~pyrogram.types.Chat`):
            A list of pinned chats in folder.

        included_peers (List of :obj:`~pyrogram.types.Chat`):
            A list of included chats in folder.

        excluded_peers (List of :obj:`~pyrogram.types.Chat`, *optional*):
            A list of excluded chats in folder.

        contacts (``bool``, *optional*):
            True, if the folder includes contacts.

        non_contacts (``bool``, *optional*):
            True, if the folder includes non contacts.

        groups (``bool``, *optional*):
            True, if the folder includes groups.

        broadcasts (``bool``, *optional*):
            True, if the folder includes broadcasts.

        bots (``bool``, *optional*):
            True, if the folder includes bots.

        exclude_muted (``bool``, *optional*):
            True, if the folder exclude muted.

        exclude_read (``bool``, *optional*):
            True, if the folder exclude read.

        exclude_archived (``bool``, *optional*):
            True, if the folder exclude archived.

        emoji (``str``, *optional*):
            Folder emoji.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int,
        title: str,
        pinned_peers: List["types.Chat"] = None,
        included_peers: List["types.Chat"] = None,
        excluded_peers: List["types.Chat"] = None,
        contacts: bool = None,
        non_contacts: bool = None,
        groups: bool = None,
        broadcasts: bool = None,
        bots: bool = None,
        exclude_muted: bool = None,
        exclude_read: bool = None,
        exclude_archived: bool = None,
        emoji: str = None,
        has_my_invites: bool = None
    ):
        super().__init__(client)

        self.id = id
        self.title = title
        self.pinned_peers = pinned_peers
        self.included_peers = included_peers
        self.excluded_peers = excluded_peers
        self.contacts = contacts
        self.non_contacts = non_contacts
        self.groups = groups
        self.broadcasts = broadcasts
        self.bots = bots
        self.exclude_muted = exclude_muted
        self.exclude_read = exclude_read
        self.exclude_archived = exclude_archived
        self.emoji = emoji
        self.has_my_invites = has_my_invites


    @staticmethod
    def _parse(client, folder: "raw.types.DialogFilter", peers) -> "Folder":
        # TODO: Change types.Chat._parse to types.Dialog._parse

        return Folder(
            id=folder.id,
            title=folder.title,
            pinned_peers=types.List(types.Chat._parse_chat(client, peers.get(utils.get_input_peer_id(i), None)) for i in folder.pinned_peers) or None,
            included_peers=types.List(types.Chat._parse_chat(client, peers.get(utils.get_input_peer_id(i), None)) for i in folder.include_peers) or None,
            excluded_peers=types.List(types.Chat._parse_chat(client, peers.get(utils.get_input_peer_id(i), None)) for i in folder.exclude_peers) or None if getattr(folder, "exclude_peers", None) else None,
            contacts=getattr(folder, "contacts", None),
            non_contacts=getattr(folder, "non_contacts", None),
            groups=getattr(folder, "groups", None),
            broadcasts=getattr(folder, "broadcasts", None),
            bots=getattr(folder, "bots", None),
            exclude_muted=getattr(folder, "exclude_muted", None),
            exclude_read=getattr(folder, "exclude_read", None),
            exclude_archived=getattr(folder, "exclude_archived", None),
            emoji=folder.emoticon or None,
            has_my_invites=getattr(folder, "has_my_invites", None),
            client=client
        )

    async def delete(self):
        """Bound method *delete* of :obj:`~pyrogram.types.Folder`.

        Use as a shortcut for:

        .. code-block:: python

            await client.delete_folder(123456789)

        Example:
            .. code-block:: python

               await folder.delete()

        Returns:
            True on success.
        """

        return await self._client.delete_folder(self.id)

    async def update_peers(self, pinned_peers: List[Union[int, str]], included_peers: List[Union[int, str]], excluded_peers: List[Union[int, str]]):
        """Bound method *update_peers* of :obj:`~pyrogram.types.Folder`.

        Use as a shortcut for:

        .. code-block:: python

            await client.update_folder(123456789, ...)

        Example:
            .. code-block:: python

               await folder.update_peers(...)

        Returns:
            True on success.
        """

        return await self._client.update_folder(
            folder_id=self.id,
            title=self.title,
            pinned_peers=pinned_peers,
            included_peers=included_peers,
            excluded_peers=excluded_peers,
            contacts=self.contacts,
            non_contacts=self.non_contacts,
            groups=self.groups,
            broadcasts=self.broadcasts,
            bots=self.bots,
            exclude_muted=self.exclude_muted,
            exclude_read=self.exclude_read,
            exclude_archived=self.exclude_archived,
            emoji=self.emoji
        )

    async def pin_chat(self, chat_id: Union[int, str]):
        """Bound method *pin_chat* of :obj:`~pyrogram.types.Folder`.

        Use as a shortcut for:

        .. code-block:: python

            await client.update_folder(123456789, ...)

        Example:
            .. code-block:: python

               await folder.pin_chat(chat_id)

        Returns:
            True on success.
        """

        return await self.update_peers(
            pinned_peers=[i.id for i in self.pinned_peers] if self.pinned_peers else [] + [chat_id],
            included_peers=[i.id for i in self.included_peers] if self.included_peers else [] + [chat_id],
            excluded_peers=[i.id for i in self.excluded_peers] if self.excluded_peers else [],
        )

    async def include_chat(self, chat_id: Union[int, str]):
        """Bound method *include_chat* of :obj:`~pyrogram.types.Folder`.

        Use as a shortcut for:

        .. code-block:: python

            await client.update_folder(123456789, ...)

        Example:
            .. code-block:: python

               await folder.include_chat(chat_id)

        Returns:
            True on success.
        """

        return await self.update_peers(
            pinned_peers=[i.id for i in self.pinned_peers] if self.pinned_peers else [],
            included_peers=[i.id for i in self.included_peers] if self.included_peers else [] + [chat_id],
            excluded_peers=[i.id for i in self.excluded_peers] if self.excluded_peers else [],
        )

    async def exclude_chat(self, chat_id: Union[int, str]):
        """Bound method *exclude_chat* of :obj:`~pyrogram.types.Folder`.

        Use as a shortcut for:

        .. code-block:: python

            await client.update_folder(123456789, ...)

        Example:
            .. code-block:: python

               await folder.exclude_chat(chat_id)

        Returns:
            True on success.
        """

        return await self.update_peers(
            pinned_peers=[i.id for i in self.pinned_peers] if self.pinned_peers else [],
            included_peers=[i.id for i in self.included_peers] if self.included_peers else [],
            excluded_peers=[i.id for i in self.excluded_peers] if self.excluded_peers else [] + [chat_id],
        )

    async def export_link(self):
        """Bound method *export_link* of :obj:`~pyrogram.types.Folder`.

        Use as a shortcut for:

        .. code-block:: python

            await client.export_link(123456789)

        Example:
            .. code-block:: python

               await folder.export_folder_link(chat_id)

        Returns:
            ``str``: On success, a link to the folder as string is returned.
        """

        return await self._client.export_folder_link(
            folder_id=self.id
        )
