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
    command = build("Command", lambda _, m: bool(m.text and m.text.startswith("/")))
    reply = build("Reply", lambda _, m: bool(m.reply_to_message))
    forwarded = build("Forwarded", lambda _, m: bool(m.forward_date))
    caption = build("Caption", lambda _, m: bool(m.caption))

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
    group = build("Group", lambda _, m: bool(m.chat.type in ("group", "supergroup")))
    channel = build("Channel", lambda _, m: bool(m.chat.type == "channel"))

    @staticmethod
    def regex(pattern, flags: int = 0):
        return build(
            "Regex", lambda _, m: bool(_.p.search(m.text or "")),
            p=re.compile(pattern, flags)
        )
