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

import pyrogram
from pyrogram import raw
from pyrogram import types
from ..object import Object


class Game(Object):
    """A game.
    Use BotFather to create and edit games, their short names will act as unique identifiers.

    Parameters:
        id (``int``):
            Unique identifier of the game.

        title (``str``):
            Title of the game.

        short_name (``str``):
            Unique short name of the game.

        description (``str``):
            Description of the game.

        photo (:obj:`~pyrogram.types.Photo`):
            Photo that will be displayed in the game message in chats.

        animation (:obj:`~pyrogram.types.Animation`, *optional*):
            Animation that will be displayed in the game message in chats.
            Upload via BotFather.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int,
        title: str,
        short_name: str,
        description: str,
        photo: "types.Photo",
        animation: "types.Animation" = None
    ):
        super().__init__(client)

        self.id = id
        self.title = title
        self.short_name = short_name
        self.description = description
        self.photo = photo
        self.animation = animation

    @staticmethod
    def _parse(client, message: "raw.types.Message") -> "Game":
        game: "raw.types.Game" = message.media.game
        animation = None

        if game.document:
            attributes = {type(i): i for i in game.document.attributes}

            file_name = getattr(
                attributes.get(
                    raw.types.DocumentAttributeFilename, None
                ), "file_name", None
            )

            animation = types.Animation._parse(
                client,
                game.document,
                attributes.get(raw.types.DocumentAttributeVideo, None),
                file_name
            )

        return Game(
            id=game.id,
            title=game.title,
            short_name=game.short_name,
            description=game.description,
            photo=types.Photo._parse(client, game.photo),
            animation=animation,
            client=client
        )
