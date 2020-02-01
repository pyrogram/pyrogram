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

import pyrogram

from pyrogram.api import types
from pyrogram.client.types.object import Object
from pyrogram.client.types.user_and_chats import User


class GameHighScore(Object):
    """One row of the high scores table for a game.

    Parameters:
        user (:obj:`User`):
            User.

        score (``int``):
            Score.

        position (``position``, *optional*):
            Position in high score table for the game.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.BaseClient" = None,
        user: User,
        score: int,
        position: int = None
    ):
        super().__init__(client)

        self.user = user
        self.score = score
        self.position = position

    @staticmethod
    def _parse(client, game_high_score: types.HighScore, users: dict) -> "GameHighScore":
        users = {i.id: i for i in users}

        return GameHighScore(
            user=User._parse(client, users[game_high_score.user_id]),
            score=game_high_score.score,
            position=game_high_score.pos,
            client=client
        )

    @staticmethod
    def _parse_action(client, service: types.MessageService, users: dict):
        return GameHighScore(
            user=User._parse(client, users[service.from_id]),
            score=service.action.score,
            client=client
        )
