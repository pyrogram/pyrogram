# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2019 Dan Tès <https://github.com/delivrance>
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
from .animation import Animation
from .photo import Photo
from ..pyrogram_type import PyrogramType


class Game(PyrogramType):
    """This object represents a game.
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

        photo (:obj:`Photo`):
            Photo that will be displayed in the game message in chats.

        animation (:obj:`Animation`, *optional*):
            Animation that will be displayed in the game message in chats.
            Upload via BotFather.
    """

    __slots__ = ["id", "title", "short_name", "description", "photo", "animation"]

    def __init__(
        self,
        *,
        client: "pyrogram.client.ext.BaseClient",
        id: int,
        title: str,
        short_name: str,
        description: str,
        photo: Photo,
        animation: Animation = None
    ):
        super().__init__(client)

        self.id = id
        self.title = title
        self.short_name = short_name
        self.description = description
        self.photo = photo
        self.animation = animation

    @staticmethod
    def _parse(client, message: types.Message) -> "Game":
        game = message.media.game  # type: types.Game
        animation = None

        if game.document:
            attributes = {type(i): i for i in game.document.attributes}

            file_name = getattr(
                attributes.get(
                    types.DocumentAttributeFilename, None
                ), "file_name", None
            )

            animation = Animation._parse(
                client,
                game.document,
                attributes.get(types.DocumentAttributeVideo, None),
                file_name
            )

        return Game(
            id=game.id,
            title=game.title,
            short_name=game.short_name,
            description=game.description,
            photo=Photo._parse(client, game.photo),
            animation=animation,
            client=client
        )
