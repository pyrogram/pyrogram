# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>
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

import pyrogram
from pyrogram.api import types
from .chat_photo import ChatPhoto
from ..pyrogram_type import PyrogramType


class Chat(PyrogramType):
    """This object represents a chat.

    Args:
        id (``int``):
            Unique identifier for this chat.

        type (``str``):
            Type of chat, can be either "private", "group", "supergroup" or "channel".

        title (``str``, *optional*):
            Title, for supergroups, channels and basic group chats.

        username (``str``, *optional*):
            Username, for private chats, supergroups and channels if available.

        first_name (``str``, *optional*):
            First name of the other party in a private chat.

        last_name (``str``, *optional*):
            Last name of the other party in a private chat.

        all_members_are_administrators (``bool``, *optional*):
            True if a basic group has "All Members Are Admins" enabled.

        photo (:obj:`ChatPhoto <pyrogram.ChatPhoto>`, *optional*):
            Chat photo. Suitable for downloads only.

        description (``str``, *optional*):
            Description, for supergroups and channel chats.
            Returned only in :meth:`get_chat() <pyrogram.Client.get_chat>`.

        invite_link (``str``, *optional*):
            Chat invite link, for supergroups and channel chats.
            Returned only in :meth:`get_chat() <pyrogram.Client.get_chat>`.

        pinned_message (:obj:`Message <pyrogram.Message>`, *optional*):
            Pinned message, for supergroups and channel chats.
            Returned only in :meth:`get_chat() <pyrogram.Client.get_chat>`.

        sticker_set_name (``str``, *optional*):
            For supergroups, name of group sticker set.
            Returned only in :meth:`get_chat() <pyrogram.Client.get_chat>`.

        can_set_sticker_set (``bool``, *optional*):
            True, if the group sticker set can be changed by you.
            Returned only in :meth:`get_chat() <pyrogram.Client.get_chat>`.

        members_count (``int``, *optional*):
            Chat members count, for groups and channels only.

        restriction_reason (``str``, *optional*):
            The reason why this chat might be unavailable to some users.
    """

    def __init__(self,
                 *,
                 client: "pyrogram.client.ext.BaseClient",
                 id: int,
                 type: str,
                 title: str = None,
                 username: str = None,
                 first_name: str = None,
                 last_name: str = None,
                 all_members_are_administrators: bool = None,
                 photo: ChatPhoto = None,
                 description: str = None,
                 invite_link: str = None,
                 pinned_message=None,
                 sticker_set_name: str = None,
                 can_set_sticker_set: bool = None,
                 members_count: int = None,
                 restriction_reason: str = None):
        super().__init__(client)

        self.id = id
        self.type = type
        self.title = title
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.all_members_are_administrators = all_members_are_administrators
        self.photo = photo
        self.description = description
        self.invite_link = invite_link
        self.pinned_message = pinned_message
        self.sticker_set_name = sticker_set_name
        self.can_set_sticker_set = can_set_sticker_set
        self.members_count = members_count
        self.restriction_reason = restriction_reason

    @staticmethod
    def _parse_user_chat(client, user: types.User) -> "Chat":
        return Chat(
            id=user.id,
            type="private",
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            photo=ChatPhoto._parse(client, user.photo),
            restriction_reason=user.restriction_reason,
            client=client
        )

    @staticmethod
    def _parse_chat_chat(client, chat: types.Chat) -> "Chat":
        admins_enabled = getattr(chat, "admins_enabled", None)

        if admins_enabled is not None:
            admins_enabled = not admins_enabled

        return Chat(
            id=-chat.id,
            type="group",
            title=chat.title,
            all_members_are_administrators=admins_enabled,
            photo=ChatPhoto._parse(client, getattr(chat, "photo", None)),
            client=client
        )

    @staticmethod
    def _parse_channel_chat(client, channel: types.Channel) -> "Chat":
        return Chat(
            id=int("-100" + str(channel.id)),
            type="supergroup" if channel.megagroup else "channel",
            title=channel.title,
            username=getattr(channel, "username", None),
            photo=ChatPhoto._parse(client, getattr(channel, "photo", None)),
            restriction_reason=getattr(channel, "restriction_reason", None),
            client=client
        )

    @staticmethod
    def _parse(client, message: types.Message or types.MessageService, users: dict, chats: dict) -> "Chat":
        if isinstance(message.to_id, types.PeerUser):
            return Chat._parse_user_chat(client, users[message.to_id.user_id if message.out else message.from_id])

        if isinstance(message.to_id, types.PeerChat):
            return Chat._parse_chat_chat(client, chats[message.to_id.chat_id])

        return Chat._parse_channel_chat(client, chats[message.to_id.channel_id])

    @staticmethod
    def _parse_dialog(client, peer, users: dict, chats: dict):
        if isinstance(peer, types.PeerUser):
            return Chat._parse_user_chat(client, users[peer.user_id])
        elif isinstance(peer, types.PeerChat):
            return Chat._parse_chat_chat(client, chats[peer.chat_id])
        else:
            return Chat._parse_channel_chat(client, chats[peer.channel_id])

    @staticmethod
    def _parse_full(client, chat_full: types.messages.ChatFull or types.UserFull) -> "Chat":
        if isinstance(chat_full, types.UserFull):
            parsed_chat = Chat._parse_user_chat(client, chat_full.user)
            parsed_chat.description = chat_full.about
        else:
            full_chat = chat_full.full_chat
            chat = None

            for i in chat_full.chats:
                if full_chat.id == i.id:
                    chat = i

            if isinstance(full_chat, types.ChatFull):
                parsed_chat = Chat._parse_chat_chat(client, chat)

                if isinstance(full_chat.participants, types.ChatParticipants):
                    parsed_chat.members_count = len(full_chat.participants.participants)
            else:
                parsed_chat = Chat._parse_channel_chat(client, chat)
                parsed_chat.members_count = full_chat.participants_count
                parsed_chat.description = full_chat.about or None
                # TODO: Add StickerSet type
                parsed_chat.can_set_sticker_set = full_chat.can_set_stickers
                parsed_chat.sticker_set_name = full_chat.stickerset

            if full_chat.pinned_msg_id:
                parsed_chat.pinned_message = client.get_messages(
                    parsed_chat.id,
                    message_ids=full_chat.pinned_msg_id
                )

            if isinstance(full_chat.exported_invite, types.ChatInviteExported):
                parsed_chat.invite_link = full_chat.exported_invite.link

        return parsed_chat
