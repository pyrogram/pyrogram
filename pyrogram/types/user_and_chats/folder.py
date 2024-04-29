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
from pyrogram import enums
from pyrogram import raw
from pyrogram import types
from pyrogram import utils
from ..object import Object


class Folder(Object):
    """A user's folder.

    Parameters:
        id (``int``):
            The folder id.

        title (``str``):
            The folder title.

        included_chats (List of :obj:`~pyrogram.types.Chat`, *optional*):
            A list of included chats in folder.

        excluded_chats (List of :obj:`~pyrogram.types.Chat`, *optional*):
            A list of excluded chats in folder.

        pinned_chats (List of :obj:`~pyrogram.types.Chat`, *optional*):
            A list of pinned chats in folder.

        contacts (``bool``, *optional*):
            True, if the folder includes contacts.

        non_contacts (``bool``, *optional*):
            True, if the folder includes non contacts.

        groups (``bool``, *optional*):
            True, if the folder includes groups.

        channels (``bool``, *optional*):
            True, if the folder includes channels.

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

        color (:obj:`~pyrogram.enums.FolderColor`, *optional*)
            Chat reply color.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int,
        title: str,
        included_chats: List["types.Chat"] = None,
        excluded_chats: List["types.Chat"] = None,
        pinned_chats: List["types.Chat"] = None,
        contacts: bool = None,
        non_contacts: bool = None,
        groups: bool = None,
        channels: bool = None,
        bots: bool = None,
        exclude_muted: bool = None,
        exclude_read: bool = None,
        exclude_archived: bool = None,
        emoji: str = None,
        color: "enums.FolderColor" = None,
        has_my_invites: bool = None
    ):
        super().__init__(client)

        self.id = id
        self.title = title
        self.included_chats = included_chats
        self.excluded_chats = excluded_chats
        self.pinned_chats = pinned_chats
        self.contacts = contacts
        self.non_contacts = non_contacts
        self.groups = groups
        self.channels = channels
        self.bots = bots
        self.exclude_muted = exclude_muted
        self.exclude_read = exclude_read
        self.exclude_archived = exclude_archived
        self.emoji = emoji
        self.color = color
        self.has_my_invites = has_my_invites

    @staticmethod
    def _parse(client, folder: "raw.types.DialogFilter", users, chats) -> "Folder":
        included_chats = []
        excluded_chats = []
        pinned_chats = []

        for peer in folder.include_peers:
            try:
                included_chats.append(types.Chat._parse_dialog(client, peer, users, chats))
            except KeyError:
                pass

        if getattr(folder, "exclude_peers", None):
            for peer in folder.exclude_peers:
                try:
                    excluded_chats.append(types.Chat._parse_dialog(client, peer, users, chats))
                except KeyError:
                    pass

        for peer in folder.pinned_peers:
            try:
                pinned_chats.append(types.Chat._parse_dialog(client, peer, users, chats))
            except KeyError:
                pass

        return Folder(
            id=folder.id,
            title=folder.title,
            included_chats=types.List(included_chats) or None,
            excluded_chats=types.List(excluded_chats) or None,
            pinned_chats=types.List(pinned_chats) or None,
            contacts=getattr(folder, "contacts", None),
            non_contacts=getattr(folder, "non_contacts", None),
            groups=getattr(folder, "groups", None),
            channels=getattr(folder, "broadcasts", None),
            bots=getattr(folder, "bots", None),
            exclude_muted=getattr(folder, "exclude_muted", None),
            exclude_read=getattr(folder, "exclude_read", None),
            exclude_archived=getattr(folder, "exclude_archived", None),
            emoji=folder.emoticon or None,
            color=enums.FolderColor(getattr(folder, "color", None)),
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

    async def update(
        self,
        included_chats: List[Union[int, str]] = None,
        excluded_chats: List[Union[int, str]] = None,
        pinned_chats: List[Union[int, str]] = None,
        title: str = None,
        contacts: bool = None,
        non_contacts: bool = None,
        groups: bool = None,
        channels: bool = None,
        bots: bool = None,
        exclude_muted: bool = None,
        exclude_read: bool = None,
        exclude_archived: bool = None,
        emoji: str = None,
        color: "enums.FolderColor" = None
    ):
        """Bound method *update_peers* of :obj:`~pyrogram.types.Folder`.

        Use as a shortcut for:

        .. code-block:: python

            await client.update_folder(
                folder_id,
                title="New folder",
                included_chats=["me"]
            )

        Example:
            .. code-block:: python

               await folder.update(included_chats=["me"])

        Parameters:
            included_chats (``int`` | ``str`` | List of ``int`` or ``str``, *optional*):
                Users or chats that should added in the folder
                You can pass an ID (int), username (str) or phone number (str).
                Multiple users can be added by passing a list of IDs, usernames or phone numbers.

            excluded_chats (``int`` | ``str`` | List of ``int`` or ``str``, *optional*):
                Users or chats that should excluded from the folder
                You can pass an ID (int), username (str) or phone number (str).
                Multiple users can be added by passing a list of IDs, usernames or phone numbers.

            pinned_chats (``int`` | ``str`` | List of ``int`` or ``str``, *optional*):
                Users or chats that should pinned in the folder
                You can pass an ID (int), username (str) or phone number (str).
                Multiple users can be added by passing a list of IDs, usernames or phone numbers.

            title (``str``, *optional*):
                A folder title was changed to this value.

            contacts (``bool``, *optional*):
                Pass True if folder should contain contacts.

            non_contacts (``bool``, *optional*):
                Pass True if folder should contain non contacts.

            groups (``bool``, *optional*):
                Pass True if folder should contain groups.

            channels (``bool``, *optional*):
                Pass True if folder should contain channels.

            bots (``bool``, *optional*):
                Pass True if folder should contain bots.

            exclude_muted (``bool``, *optional*):
                Pass True if folder should exclude muted users.

            exclude_archived (``bool``, *optional*):
                Pass True if folder should exclude archived users.

            emoji (``str``, *optional*):
                Folder emoji.
                Pass None to leave the folder icon as default.

            color (:obj:`~pyrogram.enums.FolderColor`, *optional*):
                Color type.
                Pass :obj:`~pyrogram.enums.FolderColor` to set folder color.

        Returns:
            True on success.
        """
        if not included_chats:
            included_chats = [i.id for i in self.included_chats or []]

        if not included_chats:
            excluded_chats = [i.id for i in self.excluded_chats or []]

        if not included_chats:
            pinned_chats = [i.id for i in self.pinned_chats or []]

        return await self._client.update_folder(
            folder_id=self.id,
            title=title or self.title,
            included_chats=included_chats,
            excluded_chats=excluded_chats,
            pinned_chats=pinned_chats,
            contacts=contacts or self.contacts,
            non_contacts=non_contacts or self.non_contacts,
            groups=groups or self.groups,
            channels=channels or self.channels,
            bots=bots or self.bots,
            exclude_muted=exclude_muted or self.exclude_muted,
            exclude_read=exclude_read or self.exclude_read,
            exclude_archived=exclude_archived or self.exclude_archived,
            emoji=emoji or self.emoji,
            color=color or self.color
        )

    async def include_chat(self, chat_id: Union[int, str]):
        """Bound method *include_chat* of :obj:`~pyrogram.types.Folder`.

        Use as a shortcut for:

        .. code-block:: python

            await client.update_folder(
                folder_id=123456789,
                included_chats=[chat_id],
                excluded_chats=[...],
                pinned_chats=[...]
            )

        Example:
            .. code-block:: python

               await folder.include_chat(chat_id)

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target user/channel/supergroup
                (in the format @username).

        Returns:
            True on success.
        """

        return await self.update(
            included_chats=[i.id for i in self.included_chats or []] + [chat_id],
            excluded_chats=[i.id for i in self.excluded_chats or []],
            pinned_chats=[i.id for i in self.pinned_chats or []]
        )

    async def exclude_chat(self, chat_id: Union[int, str]):
        """Bound method *exclude_chat* of :obj:`~pyrogram.types.Folder`.

        Use as a shortcut for:

        .. code-block:: python

            await client.update_folder(
                folder_id=123456789,
                included_chats=[...],
                excluded_chats=[chat_id],
                pinned_chats=[...]
            )

        Example:
            .. code-block:: python

               await folder.exclude_chat(chat_id)

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target user/channel/supergroup
                (in the format @username).

        Returns:
            True on success.
        """

        return await self.update(
            included_chats=[i.id for i in self.included_chats or []],
            excluded_chats=[i.id for i in self.excluded_chats or []] + [chat_id],
            pinned_chats=[i.id for i in self.pinned_chats or []],
        )

    async def update_color(self, color: "enums.FolderColor"):
        """Bound method *update_color* of :obj:`~pyrogram.types.Folder`.

        Use as a shortcut for:

        .. code-block:: python

            await client.update_folder(
                folder_id=123456789,
                included_chats=[chat_id],
                excluded_chats=[chat_id],
                pinned_chats=[...],
                color=color
            )

        Example:
            .. code-block:: python

               await folder.update_color(enums.FolderColor.RED)

        Parameters:
            color (:obj:`~pyrogram.enums.FolderColor`, *optional*):
                Color type.
                Pass :obj:`~pyrogram.enums.FolderColor` to set folder color.

        Returns:
            True on success.
        """

        return await self.update(
            color=color
        )

    async def pin_chat(self, chat_id: Union[int, str]):
        """Bound method *pin_chat* of :obj:`~pyrogram.types.Folder`.

        Use as a shortcut for:

        .. code-block:: python

            await client.update_folder(
                folder_id=123456789,
                included_chats=[chat_id],
                excluded_chats=[chat_id],
                pinned_chats=[...]
            )

        Example:
            .. code-block:: python

               await folder.pin_chat(chat_id)

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target user/channel/supergroup
                (in the format @username).

        Returns:
            True on success.
        """

        return await self.update(
            included_chats=[i.id for i in self.included_chats or []] + [chat_id],
            excluded_chats=[i.id for i in self.excluded_chats or []],
            pinned_chats=[i.id for i in self.pinned_chats or []] + [chat_id]
        )

    async def remove_chat(self, chat_id: Union[int, str]):
        """Bound method *remove_chat* of :obj:`~pyrogram.types.Folder`.

        Remove chat from included, excluded and pinned chats.

        Use as a shortcut for:

        .. code-block:: python

            await client.update_folder(
                folder_id=123456789,
                included_chats=[...],
                excluded_chats=[...],
                pinned_chats=[...]
            )

        Example:
            .. code-block:: python

               await folder.remove_chat(chat_id)

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target user/channel/supergroup
                (in the format @username).

        Returns:
            True on success.
        """
        peer = await self._client.resolve_peer(chat_id)
        peer_id = utils.get_peer_id(peer)

        return await self.update(
            included_chats=[i.id for i in self.included_chats or [] if peer_id != i.id],
            excluded_chats=[i.id for i in self.excluded_chats or [] if peer_id != i.id],
            pinned_chats=[i.id for i in self.pinned_chats or [] if peer_id != i.id]
        )

    async def export_link(self):
        """Bound method *export_link* of :obj:`~pyrogram.types.Folder`.

        Use as a shortcut for:

        .. code-block:: python

            await client.export_folder_link(123456789)

        Example:
            .. code-block:: python

               await folder.export_link()

        Returns:
            ``str``: On success, a link to the folder as string is returned.
        """

        return await self._client.export_folder_link(
            folder_id=self.id
        )
