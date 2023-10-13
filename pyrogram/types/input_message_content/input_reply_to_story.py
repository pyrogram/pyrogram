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

from pyrogram import raw
from ..object import Object


class InputReplyToStory(Object):
    """Contains information about a target replied story.

    Parameters:
        user_id (:obj:`~pyrogram.raw.types.InputUser`):
            An InputUser.
            
        story_id (``int``):
            Unique identifier for the target story.
    """

    def __init__(
        self, *,
        user_id: "raw.types.InputUser" = None,
        story_id: int = None
    ):
        super().__init__()

        self.user_id = user_id
        self.story_id = story_id

    def write(self):
        return raw.types.InputReplyToStory(
            user_id=self.user_id,
            story_id=self.story_id
        ).write()
