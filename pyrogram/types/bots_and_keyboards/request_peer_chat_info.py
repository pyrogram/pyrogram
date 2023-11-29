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

from ..object import Object


class RequestPeerTypeChatInfo(Object):
    """Contains information about a chat peer type.

    Parameters:
        is_creator (``bool``):
            If True, returns the list of chats where this user is a chat creator.

        is_bot_participant (``bool``):
            If True, returns the list of chats where this bot is participant.

        has_username (``bool``):
            If True, returns the list of chats where chat has username.

        has_forum (``bool``):
           If True, returns the list of chats where forum topcis is enabled.
    """

    def __init__(
        self, *,
        is_creator: bool = None,
        is_bot_participant: bool = None,
        has_username: bool = None,
        has_forum: bool = None,

    ):
        super().__init__()

        self.is_creator = is_creator
        self.is_bot_participant = is_bot_participant
        self.has_username = has_username
        self.has_forum = has_forum
