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

import re

from .filter import Filter


def build(name: str, func: callable, **kwargs) -> type:
    d = {"__call__": func}
    d.update(kwargs)

    return type(name, (Filter,), d)()


class Filters:
    text = build("Text", lambda _, m: bool(m.text and not m.text.startswith("/")))

    @staticmethod
    def command(command: str or list):
        return build(
            "Command",
            lambda _, m: bool(
                m.text
                and m.text.startswith("/")
                and (m.text[1:].split()[0] in _.c)
            ),
            c=(
                {command}
                if not isinstance(command, list)
                else {c for c in command}
            )
        )

    reply = build("Reply", lambda _, m: bool(m.reply_to_message))
    forwarded = build("Forwarded", lambda _, m: bool(m.forward_date))
    caption = build("Caption", lambda _, m: bool(m.caption))
    edited = build("Edited", lambda _, m: bool(m.edit_date))

    audio = build("Audio", lambda _, m: bool(m.audio))
    document = build("Document", lambda _, m: bool(m.document))
    photo = build("Photo", lambda _, m: bool(m.photo))
    sticker = build("Sticker", lambda _, m: bool(m.sticker))
    video = build("Video", lambda _, m: bool(m.video))
    voice = build("Voice", lambda _, m: bool(m.voice))
    video_note = build("Voice", lambda _, m: bool(m.video_note))
    contact = build("Contact", lambda _, m: bool(m.contact))
    location = build("Location", lambda _, m: bool(m.location))
    venue = build("Venue", lambda _, m: bool(m.venue))

    private = build("Private", lambda _, m: bool(m.chat.type == "private"))
    group = build("Group", lambda _, m: bool(m.chat.type in {"group", "supergroup"}))
    channel = build("Channel", lambda _, m: bool(m.chat.type == "channel"))

    @staticmethod
    def regex(pattern, flags: int = 0):
        return build(
            "Regex", lambda _, m: bool(_.p.search(m.text or "")),
            p=re.compile(pattern, flags)
        )

    @staticmethod
    def user(user: int or str or list):
        return build(
            "User",
            lambda _, m: bool(m.from_user
                              and (m.from_user.id in _.u
                                   or (m.from_user.username
                                       and m.from_user.username.lower() in _.u))),
            u=(
                {user.lower().strip("@") if type(user) is str else user}
                if not isinstance(user, list)
                else {i.lower().strip("@") if type(i) is str else i for i in user}
            )
        )

    @staticmethod
    def chat(chat: int or str or list):
        return build(
            "Chat",
            lambda _, m: bool(m.chat
                              and (m.chat.id in _.c
                                   or (m.chat.username
                                       and m.chat.username.lower() in _.c))),
            c=(
                {chat.lower().strip("@") if type(chat) is str else chat}
                if not isinstance(chat, list)
                else {i.lower().strip("@") if type(i) is str else i for i in chat}
            )
        )

    class _Service(Filter):
        new_chat_members = build("NewChatMembers", lambda _, m: bool(m.new_chat_members))
        left_chat_member = build("LeftChatMember", lambda _, m: bool(m.left_chat_member))
        new_chat_title = build("NewChatTitle", lambda _, m: bool(m.new_chat_title))
        new_chat_photo = build("NewChatPhoto", lambda _, m: bool(m.new_chat_photo))
        delete_chat_photo = build("DeleteChatPhoto", lambda _, m: bool(m.delete_chat_photo))
        group_chat_created = build("GroupChatCreated", lambda _, m: bool(m.group_chat_created))
        supergroup_chat_created = build("SupergroupChatCreated", lambda _, m: bool(m.supergroup_chat_created))
        channel_chat_created = build("ChannelChatCreated", lambda _, m: bool(m.channel_chat_created))
        migrate_to_chat_id = build("MigrateToChatId", lambda _, m: bool(m.migrate_to_chat_id))
        migrate_from_chat_id = build("MigrateFromChatId", lambda _, m: bool(m.migrate_from_chat_id))
        pinned_message = build("PinnedMessage", lambda _, m: bool(m.pinned_message))

        def __call__(self, message):
            return bool(
                self.new_chat_members(message)
                or self.left_chat_member(message)
                or self.new_chat_title(message)
                or self.new_chat_photo(message)
                or self.delete_chat_photo(message)
                or self.group_chat_created(message)
                or self.supergroup_chat_created(message)
                or self.channel_chat_created(message)
                or self.migrate_to_chat_id(message)
                or self.migrate_from_chat_id(message)
                or self.pinned_message(message)
            )

    service = _Service()
