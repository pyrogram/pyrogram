#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2021 Dan <https://github.com/delivrance>
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

from pyrogram import raw
from ..object import Object


class ChatPermissions(Object):
    """A chat default permissions and a single member permissions within a chat.

    Some permissions make sense depending on the context: default chat permissions, restricted/kicked member or
    administrators in groups or channels.

    .. note::

        Pyrogram's chat permission are much more detailed. In particular, you can restrict sending stickers, animations,
        games and inline bot results individually, allowing a finer control.

        If you wish to have the same permissions as seen in official apps or in bot API's *"can_send_other_messages"*
        simply set these arguments to True: ``can_send_stickers``, ``can_send_animations``, ``can_send_games`` and
        ``can_use_inline_bots``.

    Parameters:
        can_send_messages (``bool``, *optional*):
            True, if the user is allowed to send text messages, contacts, locations and venues.

        can_send_media_messages (``bool``, *optional*):
            True, if the user is allowed to send audios, documents, photos, videos, video notes and voice notes, implies
            can_send_messages.

        can_send_stickers (``bool``, *optional*):
            True, if the user is allowed to send stickers, implies can_send_media_messages.

        can_send_animations (``bool``, *optional*):
            True, if the user is allowed to send animations (GIFs), implies can_send_media_messages.

        can_send_games (``bool``, *optional*):
            True, if the user is allowed to send games, implies can_send_media_messages.

        can_use_inline_bots (``bool``, *optional*):
            True, if the user is allowed to use inline bots, implies can_send_media_messages.

        can_add_web_page_previews (``bool``, *optional*):
            True, if the user is allowed to add web page previews to their messages, implies can_send_media_messages.

        can_send_polls (``bool``, *optional*):
            True, if the user is allowed to send polls, implies can_send_messages.

        can_change_info (``bool``, *optional*):
            True, if the user is allowed to change the chat title, photo and other settings.
            Ignored in public supergroups.

        can_invite_users (``bool``, *optional*):
            True, if the user is allowed to invite new users to the chat.

        can_pin_messages (``bool``, *optional*):
            True, if the user is allowed to pin messages.
            Ignored in public supergroups.
    """

    def __init__(
        self,
        *,
        can_send_messages: bool = None,  # Text, contacts, locations and venues
        can_send_media_messages: bool = None,  # Audios, documents, photos, videos, video notes and voice notes
        can_send_stickers: bool = None,
        can_send_animations: bool = None,
        can_send_games: bool = None,
        can_use_inline_bots: bool = None,
        can_add_web_page_previews: bool = None,
        can_send_polls: bool = None,
        can_change_info: bool = None,
        can_invite_users: bool = None,
        can_pin_messages: bool = None
    ):
        super().__init__(None)

        self.can_send_messages = can_send_messages
        self.can_send_media_messages = can_send_media_messages
        self.can_send_stickers = can_send_stickers
        self.can_send_animations = can_send_animations
        self.can_send_games = can_send_games
        self.can_use_inline_bots = can_use_inline_bots
        self.can_add_web_page_previews = can_add_web_page_previews
        self.can_send_polls = can_send_polls
        self.can_change_info = can_change_info
        self.can_invite_users = can_invite_users
        self.can_pin_messages = can_pin_messages

    @staticmethod
    def _parse(denied_permissions: "raw.types.ChatBannedRights") -> "ChatPermissions":
        if isinstance(denied_permissions, raw.types.ChatBannedRights):
            return ChatPermissions(
                can_send_messages=not denied_permissions.send_messages,
                can_send_media_messages=not denied_permissions.send_media,
                can_send_stickers=not denied_permissions.send_stickers,
                can_send_animations=not denied_permissions.send_gifs,
                can_send_games=not denied_permissions.send_games,
                can_use_inline_bots=not denied_permissions.send_inline,
                can_add_web_page_previews=not denied_permissions.embed_links,
                can_send_polls=not denied_permissions.send_polls,
                can_change_info=not denied_permissions.change_info,
                can_invite_users=not denied_permissions.invite_users,
                can_pin_messages=not denied_permissions.pin_messages
            )
