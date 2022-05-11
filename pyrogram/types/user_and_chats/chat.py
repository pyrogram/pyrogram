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
from typing import Union, List, Optional, AsyncGenerator, BinaryIO

import pyrogram
from pyrogram import raw, enums
from pyrogram import types
from pyrogram import utils
from ..object import Object


class Chat(Object):
    """A chat.

    Parameters:
        id (``int``):
            Unique identifier for this chat.

        type (:obj:`~pyrogram.enums.ChatType`):
            Type of chat.

        is_verified (``bool``, *optional*):
            True, if this chat has been verified by Telegram. Supergroups, channels and bots only.

        is_restricted (``bool``, *optional*):
            True, if this chat has been restricted. Supergroups, channels and bots only.
            See *restriction_reason* for details.

        is_creator (``bool``, *optional*):
            True, if this chat owner is the current user. Supergroups, channels and groups only.

        is_scam (``bool``, *optional*):
            True, if this chat has been flagged for scam.

        is_fake (``bool``, *optional*):
            True, if this chat has been flagged for impersonation.

        is_support (``bool``):
            True, if this chat is part of the Telegram support team. Users and bots only.

        title (``str``, *optional*):
            Title, for supergroups, channels and basic group chats.

        username (``str``, *optional*):
            Username, for private chats, bots, supergroups and channels if available.

        first_name (``str``, *optional*):
            First name of the other party in a private chat, for private chats and bots.

        last_name (``str``, *optional*):
            Last name of the other party in a private chat, for private chats.

        photo (:obj:`~pyrogram.types.ChatPhoto`, *optional*):
            Chat photo. Suitable for downloads only.

        bio (``str``, *optional*):
            Bio of the other party in a private chat.
            Returned only in :meth:`~pyrogram.Client.get_chat`.

        description (``str``, *optional*):
            Description, for groups, supergroups and channel chats.
            Returned only in :meth:`~pyrogram.Client.get_chat`.

        dc_id (``int``, *optional*):
            The chat assigned DC (data center). Available only in case the chat has a photo.
            Note that this information is approximate; it is based on where Telegram stores the current chat photo.
            It is accurate only in case the owner has set the chat photo, otherwise the dc_id will be the one assigned
            to the administrator who set the current chat photo.

        has_protected_content (``bool``, *optional*):
            True, if messages from the chat can't be forwarded to other chats.

        invite_link (``str``, *optional*):
            Chat invite link, for groups, supergroups and channels.
            Returned only in :meth:`~pyrogram.Client.get_chat`.

        pinned_message (:obj:`~pyrogram.types.Message`, *optional*):
            Pinned message, for groups, supergroups channels and own chat.
            Returned only in :meth:`~pyrogram.Client.get_chat`.

        sticker_set_name (``str``, *optional*):
            For supergroups, name of group sticker set.
            Returned only in :meth:`~pyrogram.Client.get_chat`.

        can_set_sticker_set (``bool``, *optional*):
            True, if the group sticker set can be changed by you.
            Returned only in :meth:`~pyrogram.Client.get_chat`.

        members_count (``int``, *optional*):
            Chat members count, for groups, supergroups and channels only.
            Returned only in :meth:`~pyrogram.Client.get_chat`.

        restrictions (List of :obj:`~pyrogram.types.Restriction`, *optional*):
            The list of reasons why this chat might be unavailable to some users.
            This field is available only in case *is_restricted* is True.

        permissions (:obj:`~pyrogram.types.ChatPermissions` *optional*):
            Default chat member permissions, for groups and supergroups.

        distance (``int``, *optional*):
            Distance in meters of this group chat from your location.
            Returned only in :meth:`~pyrogram.Client.get_nearby_chats`.

        linked_chat (:obj:`~pyrogram.types.Chat`, *optional*):
            The linked discussion group (in case of channels) or the linked channel (in case of supergroups).
            Returned only in :meth:`~pyrogram.Client.get_chat`.

        send_as_chat (:obj:`~pyrogram.types.Chat`, *optional*):
            The default "send_as" chat.
            Returned only in :meth:`~pyrogram.Client.get_chat`.

        available_reactions (List of ``str``, *optional*):
            Available reactions in the chat.
            Returned only in :meth:`~pyrogram.Client.get_chat`.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int,
        type: "enums.ChatType",
        is_verified: bool = None,
        is_restricted: bool = None,
        is_creator: bool = None,
        is_scam: bool = None,
        is_fake: bool = None,
        is_support: bool = None,
        title: str = None,
        username: str = None,
        first_name: str = None,
        last_name: str = None,
        photo: "types.ChatPhoto" = None,
        bio: str = None,
        description: str = None,
        dc_id: int = None,
        has_protected_content: bool = None,
        invite_link: str = None,
        pinned_message=None,
        sticker_set_name: str = None,
        can_set_sticker_set: bool = None,
        members_count: int = None,
        restrictions: List["types.Restriction"] = None,
        permissions: "types.ChatPermissions" = None,
        distance: int = None,
        linked_chat: "types.Chat" = None,
        send_as_chat: "types.Chat" = None,
        available_reactions: List[str] = None
    ):
        super().__init__(client)

        self.id = id
        self.type = type
        self.is_verified = is_verified
        self.is_restricted = is_restricted
        self.is_creator = is_creator
        self.is_scam = is_scam
        self.is_fake = is_fake
        self.is_support = is_support
        self.title = title
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.photo = photo
        self.bio = bio
        self.description = description
        self.dc_id = dc_id
        self.has_protected_content = has_protected_content
        self.invite_link = invite_link
        self.pinned_message = pinned_message
        self.sticker_set_name = sticker_set_name
        self.can_set_sticker_set = can_set_sticker_set
        self.members_count = members_count
        self.restrictions = restrictions
        self.permissions = permissions
        self.distance = distance
        self.linked_chat = linked_chat
        self.send_as_chat = send_as_chat
        self.available_reactions = available_reactions

    @staticmethod
    def _parse_user_chat(client, user: raw.types.User) -> "Chat":
        peer_id = user.id

        return Chat(
            id=peer_id,
            type=enums.ChatType.BOT if user.bot else enums.ChatType.PRIVATE,
            is_verified=getattr(user, "verified", None),
            is_restricted=getattr(user, "restricted", None),
            is_scam=getattr(user, "scam", None),
            is_fake=getattr(user, "fake", None),
            is_support=getattr(user, "support", None),
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            photo=types.ChatPhoto._parse(client, user.photo, peer_id, user.access_hash),
            restrictions=types.List([types.Restriction._parse(r) for r in user.restriction_reason]) or None,
            dc_id=getattr(getattr(user, "photo", None), "dc_id", None),
            client=client
        )

    @staticmethod
    def _parse_chat_chat(client, chat: raw.types.Chat) -> "Chat":
        peer_id = -chat.id

        return Chat(
            id=peer_id,
            type=enums.ChatType.GROUP,
            title=chat.title,
            is_creator=getattr(chat, "creator", None),
            photo=types.ChatPhoto._parse(client, getattr(chat, "photo", None), peer_id, 0),
            permissions=types.ChatPermissions._parse(getattr(chat, "default_banned_rights", None)),
            members_count=getattr(chat, "participants_count", None),
            dc_id=getattr(getattr(chat, "photo", None), "dc_id", None),
            has_protected_content=getattr(chat, "noforwards", None),
            client=client
        )

    @staticmethod
    def _parse_channel_chat(client, channel: raw.types.Channel) -> "Chat":
        peer_id = utils.get_channel_id(channel.id)
        restriction_reason = getattr(channel, "restriction_reason", [])

        return Chat(
            id=peer_id,
            type=enums.ChatType.SUPERGROUP if getattr(channel, "megagroup", None) else enums.ChatType.CHANNEL,
            is_verified=getattr(channel, "verified", None),
            is_restricted=getattr(channel, "restricted", None),
            is_creator=getattr(channel, "creator", None),
            is_scam=getattr(channel, "scam", None),
            is_fake=getattr(channel, "fake", None),
            title=channel.title,
            username=getattr(channel, "username", None),
            photo=types.ChatPhoto._parse(client, getattr(channel, "photo", None), peer_id,
                                         getattr(channel, "access_hash", 0)),
            restrictions=types.List([types.Restriction._parse(r) for r in restriction_reason]) or None,
            permissions=types.ChatPermissions._parse(getattr(channel, "default_banned_rights", None)),
            members_count=getattr(channel, "participants_count", None),
            dc_id=getattr(getattr(channel, "photo", None), "dc_id", None),
            has_protected_content=getattr(channel, "noforwards", None),
            client=client
        )

    @staticmethod
    def _parse(
        client,
        message: Union[raw.types.Message, raw.types.MessageService],
        users: dict,
        chats: dict,
        is_chat: bool
    ) -> "Chat":
        from_id = utils.get_raw_peer_id(message.from_id)
        peer_id = utils.get_raw_peer_id(message.peer_id)
        chat_id = (peer_id or from_id) if is_chat else (from_id or peer_id)

        if isinstance(message.peer_id, raw.types.PeerUser):
            return Chat._parse_user_chat(client, users[chat_id])

        if isinstance(message.peer_id, raw.types.PeerChat):
            return Chat._parse_chat_chat(client, chats[chat_id])

        return Chat._parse_channel_chat(client, chats[chat_id])

    @staticmethod
    def _parse_dialog(client, peer, users: dict, chats: dict):
        if isinstance(peer, raw.types.PeerUser):
            return Chat._parse_user_chat(client, users[peer.user_id])
        elif isinstance(peer, raw.types.PeerChat):
            return Chat._parse_chat_chat(client, chats[peer.chat_id])
        else:
            return Chat._parse_channel_chat(client, chats[peer.channel_id])

    @staticmethod
    async def _parse_full(client, chat_full: Union[raw.types.messages.ChatFull, raw.types.users.UserFull]) -> "Chat":
        users = {u.id: u for u in chat_full.users}
        chats = {c.id: c for c in chat_full.chats}

        if isinstance(chat_full, raw.types.users.UserFull):
            full_user = chat_full.full_user

            parsed_chat = Chat._parse_user_chat(client, users[full_user.id])
            parsed_chat.bio = full_user.about

            if full_user.pinned_msg_id:
                parsed_chat.pinned_message = await client.get_messages(
                    parsed_chat.id,
                    message_ids=full_user.pinned_msg_id
                )
        else:
            full_chat = chat_full.full_chat
            chat_raw = chats[full_chat.id]

            if isinstance(full_chat, raw.types.ChatFull):
                parsed_chat = Chat._parse_chat_chat(client, chat_raw)
                parsed_chat.description = full_chat.about or None

                if isinstance(full_chat.participants, raw.types.ChatParticipants):
                    parsed_chat.members_count = len(full_chat.participants.participants)
            else:
                parsed_chat = Chat._parse_channel_chat(client, chat_raw)
                parsed_chat.members_count = full_chat.participants_count
                parsed_chat.description = full_chat.about or None
                # TODO: Add StickerSet type
                parsed_chat.can_set_sticker_set = full_chat.can_set_stickers
                parsed_chat.sticker_set_name = getattr(full_chat.stickerset, "short_name", None)

                linked_chat_raw = chats.get(full_chat.linked_chat_id, None)

                if linked_chat_raw:
                    parsed_chat.linked_chat = Chat._parse_channel_chat(client, linked_chat_raw)

                default_send_as = full_chat.default_send_as

                if default_send_as:
                    if isinstance(default_send_as, raw.types.PeerUser):
                        send_as_raw = users[default_send_as.user_id]
                    else:
                        send_as_raw = chats[default_send_as.channel_id]

                    parsed_chat.send_as_chat = Chat._parse_chat(client, send_as_raw)

            if full_chat.pinned_msg_id:
                parsed_chat.pinned_message = await client.get_messages(
                    parsed_chat.id,
                    message_ids=full_chat.pinned_msg_id
                )

            if isinstance(full_chat.exported_invite, raw.types.ChatInviteExported):
                parsed_chat.invite_link = full_chat.exported_invite.link

            parsed_chat.available_reactions = full_chat.available_reactions or None

        return parsed_chat

    @staticmethod
    def _parse_chat(client, chat: Union[raw.types.Chat, raw.types.User, raw.types.Channel]) -> "Chat":
        if isinstance(chat, raw.types.Chat):
            return Chat._parse_chat_chat(client, chat)
        elif isinstance(chat, raw.types.User):
            return Chat._parse_user_chat(client, chat)
        else:
            return Chat._parse_channel_chat(client, chat)

    async def archive(self):
        """Bound method *archive* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.archive_chats(-100123456789)

        Example:
            .. code-block:: python

                await chat.archive()

        Returns:
            True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.archive_chats(self.id)

    async def unarchive(self):
        """Bound method *unarchive* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.unarchive_chats(-100123456789)

        Example:
            .. code-block:: python

                await chat.unarchive()

        Returns:
            True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.unarchive_chats(self.id)

    # TODO: Remove notes about "All Members Are Admins" for basic groups, the attribute doesn't exist anymore
    async def set_title(self, title: str) -> bool:
        """Bound method *set_title* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.set_chat_title(
                chat_id=chat_id,
                title=title
            )

        Example:
            .. code-block:: python

                await chat.set_title("Lounge")

        Note:
            In regular groups (non-supergroups), this method will only work if the "All Members Are Admins"
            setting is off.

        Parameters:
            title (``str``):
                New chat title, 1-255 characters.

        Returns:
            ``bool``: True on success.

        Raises:
            RPCError: In case of Telegram RPC error.
            ValueError: In case a chat_id belongs to user.
        """

        return await self._client.set_chat_title(
            chat_id=self.id,
            title=title
        )

    async def set_description(self, description: str) -> bool:
        """Bound method *set_description* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.set_chat_description(
                chat_id=chat_id,
                description=description
            )

        Example:
            .. code-block:: python

                await chat.set_chat_description("Don't spam!")

        Parameters:
            description (``str``):
                New chat description, 0-255 characters.

        Returns:
            ``bool``: True on success.

        Raises:
            RPCError: In case of Telegram RPC error.
            ValueError: If a chat_id doesn't belong to a supergroup or a channel.
        """

        return await self._client.set_chat_description(
            chat_id=self.id,
            description=description
        )

    async def set_photo(
        self,
        *,
        photo: Union[str, BinaryIO] = None,
        video: Union[str, BinaryIO] = None,
        video_start_ts: float = None,
    ) -> bool:
        """Bound method *set_photo* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.set_chat_photo(
                chat_id=chat_id,
                photo=photo
            )

        Example:
            .. code-block:: python

                # Set chat photo using a local file
                await chat.set_photo(photo="photo.jpg")

                # Set chat photo using an existing Photo file_id
                await chat.set_photo(photo=photo.file_id)


                # Set chat video using a local file
                await chat.set_photo(video="video.mp4")

                # Set chat photo using an existing Video file_id
                await chat.set_photo(video=video.file_id)

        Parameters:
            photo (``str`` | ``BinaryIO``, *optional*):
                New chat photo. You can pass a :obj:`~pyrogram.types.Photo` file_id, a file path to upload a new photo
                from your local machine or a binary file-like object with its attribute
                ".name" set for in-memory uploads.

            video (``str`` | ``BinaryIO``, *optional*):
                New chat video. You can pass a :obj:`~pyrogram.types.Video` file_id, a file path to upload a new video
                from your local machine or a binary file-like object with its attribute
                ".name" set for in-memory uploads.

            video_start_ts (``float``, *optional*):
                The timestamp in seconds of the video frame to use as photo profile preview.

        Returns:
            ``bool``: True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
            ValueError: if a chat_id belongs to user.
        """

        return await self._client.set_chat_photo(
            chat_id=self.id,
            photo=photo,
            video=video,
            video_start_ts=video_start_ts
        )

    async def ban_member(
        self,
        user_id: Union[int, str],
        until_date: datetime = utils.zero_datetime()
    ) -> Union["types.Message", bool]:
        """Bound method *ban_member* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.ban_chat_member(
                chat_id=chat_id,
                user_id=user_id
            )

        Example:
            .. code-block:: python

                await chat.ban_member(123456789)

        Note:
            In regular groups (non-supergroups), this method will only work if the "All Members Are Admins" setting is
            off in the target group. Otherwise members may only be removed by the group's creator or by the member
            that added them.

        Parameters:
            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.
                For a contact that exists in your Telegram address book you can use his phone number (str).

            until_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the user will be unbanned.
                If user is banned for more than 366 days or less than 30 seconds from the current time they are
                considered to be banned forever. Defaults to epoch (ban forever).

        Returns:
            :obj:`~pyrogram.types.Message` | ``bool``: On success, a service message will be returned (when applicable), otherwise, in
            case a message object couldn't be returned, True is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.ban_chat_member(
            chat_id=self.id,
            user_id=user_id,
            until_date=until_date
        )

    async def unban_member(
        self,
        user_id: Union[int, str]
    ) -> bool:
        """Bound method *unban_member* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.unban_chat_member(
                chat_id=chat_id,
                user_id=user_id
            )

        Example:
            .. code-block:: python

                await chat.unban_member(123456789)

        Parameters:
            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.
                For a contact that exists in your Telegram address book you can use his phone number (str).

        Returns:
            ``bool``: True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.unban_chat_member(
            chat_id=self.id,
            user_id=user_id,
        )

    async def restrict_member(
        self,
        user_id: Union[int, str],
        permissions: "types.ChatPermissions",
        until_date: datetime = utils.zero_datetime(),
    ) -> "types.Chat":
        """Bound method *unban_member* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=ChatPermissions()
            )

        Example:
            .. code-block:: python

                await chat.restrict_member(user_id, ChatPermissions())

        Parameters:
            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.
                For a contact that exists in your Telegram address book you can use his phone number (str).

            permissions (:obj:`~pyrogram.types.ChatPermissions`):
                New user permissions.

            until_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the user will be unbanned.
                If user is banned for more than 366 days or less than 30 seconds from the current time they are
                considered to be banned forever. Defaults to epoch (ban forever).

        Returns:
            :obj:`~pyrogram.types.Chat`: On success, a chat object is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.restrict_chat_member(
            chat_id=self.id,
            user_id=user_id,
            permissions=permissions,
            until_date=until_date,
        )

    # Set None as privileges default due to issues with partially initialized module, because at the time Chat
    # is being initialized, ChatPrivileges would be required here, but was not initialized yet.
    async def promote_member(
        self,
        user_id: Union[int, str],
        privileges: "types.ChatPrivileges" = None
    ) -> bool:
        """Bound method *promote_member* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.promote_chat_member(
                chat_id=chat_id,
                user_id=user_id
            )

        Example:

            .. code-block:: python

                await chat.promote_member(123456789)

        Parameters:
            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.
                For a contact that exists in your Telegram address book you can use his phone number (str).

            privileges (:obj:`~pyrogram.types.ChatPrivileges`, *optional*):
                New user privileges.

        Returns:
            ``bool``: True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.promote_chat_member(
            chat_id=self.id,
            user_id=user_id,
            privileges=privileges
        )

    async def join(self):
        """Bound method *join* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.join_chat(123456789)

        Example:
            .. code-block:: python

                await chat.join()

        Note:
            This only works for public groups, channels that have set a username or linked chats.

        Returns:
            :obj:`~pyrogram.types.Chat`: On success, a chat object is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.join_chat(self.username or self.id)

    async def leave(self):
        """Bound method *leave* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.leave_chat(123456789)

        Example:
            .. code-block:: python

                await chat.leave()

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.leave_chat(self.id)

    async def export_invite_link(self):
        """Bound method *export_invite_link* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            client.export_chat_invite_link(123456789)

        Example:
            .. code-block:: python

                chat.export_invite_link()

        Returns:
            ``str``: On success, the exported invite link is returned.

        Raises:
            ValueError: In case the chat_id belongs to a user.
        """

        return await self._client.export_chat_invite_link(self.id)

    async def get_member(
        self,
        user_id: Union[int, str],
    ) -> "types.ChatMember":
        """Bound method *get_member* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.get_chat_member(
                chat_id=chat_id,
                user_id=user_id
            )

        Example:
            .. code-block:: python

                await chat.get_member(user_id)

        Returns:
            :obj:`~pyrogram.types.ChatMember`: On success, a chat member is returned.
        """

        return await self._client.get_chat_member(
            self.id,
            user_id=user_id
        )

    def get_members(
        self,
        query: str = "",
        limit: int = 0,
        filter: "enums.ChatMembersFilter" = enums.ChatMembersFilter.SEARCH
    ) -> Optional[AsyncGenerator["types.ChatMember", None]]:
        """Bound method *get_members* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            async for member in client.get_chat_members(chat_id):
                print(member)

        Example:
            .. code-block:: python

                async for member in chat.get_members():
                    print(member)

        Parameters:
            query (``str``, *optional*):
                Query string to filter members based on their display names and usernames.
                Only applicable to supergroups and channels. Defaults to "" (empty string).
                A query string is applicable only for :obj:`~pyrogram.enums.ChatMembersFilter.SEARCH`,
                :obj:`~pyrogram.enums.ChatMembersFilter.BANNED` and :obj:`~pyrogram.enums.ChatMembersFilter.RESTRICTED`
                filters only.

            limit (``int``, *optional*):
                Limits the number of members to be retrieved.

            filter (:obj:`~pyrogram.enums.ChatMembersFilter`, *optional*):
                Filter used to select the kind of members you want to retrieve. Only applicable for supergroups
                and channels.

        Returns:
            ``Generator``: On success, a generator yielding :obj:`~pyrogram.types.ChatMember` objects is returned.
        """

        return self._client.get_chat_members(
            self.id,
            query=query,
            limit=limit,
            filter=filter
        )

    async def add_members(
        self,
        user_ids: Union[Union[int, str], List[Union[int, str]]],
        forward_limit: int = 100
    ) -> bool:
        """Bound method *add_members* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.add_chat_members(chat_id, user_id)

        Example:
            .. code-block:: python

                await chat.add_members(user_id)

        Returns:
            ``bool``: On success, True is returned.
        """

        return await self._client.add_chat_members(
            self.id,
            user_ids=user_ids,
            forward_limit=forward_limit
        )

    async def mark_unread(self, ) -> bool:
        """Bound method *mark_unread* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.mark_unread(chat_id)

        Example:
            .. code-block:: python

                await chat.mark_unread()

        Returns:
            ``bool``: On success, True is returned.
        """

        return await self._client.mark_chat_unread(self.id)

    async def set_protected_content(self, enabled: bool) -> bool:
        """Bound method *set_protected_content* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.set_chat_protected_content(chat_id, enabled)

        Parameters:
            enabled (``bool``):
                Pass True to enable the protected content setting, False to disable.

        Example:
            .. code-block:: python

                await chat.set_protected_content(enabled)

        Returns:
            ``bool``: On success, True is returned.
        """

        return await self._client.set_chat_protected_content(
            self.id,
            enabled=enabled
        )

    async def unpin_all_messages(self) -> bool:
        """Bound method *unpin_all_messages* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            client.unpin_all_chat_messages(chat_id)

        Example:
            .. code-block:: python

                chat.unpin_all_messages()

        Returns:
            ``bool``: On success, True is returned.
        """

        return await self._client.unpin_all_chat_messages(self.id)
