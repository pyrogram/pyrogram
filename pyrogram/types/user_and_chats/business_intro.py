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

from pyrogram import types, raw
from ..object import Object


class BusinessIntro(Object):
    """Information about intro of this user.

    Parameters:
        title (``str``, *optional*):
            Title text of the business intro.

        text (``str``, *optional*):
            Message text of the business intro.

        sticker (:obj:`~pyrogram.types.Sticker`, *optional*):
            Sticker of the business intro.

    """

    def __init__(
        self,
        *,
        title: str = None,
        text: str = None,
        sticker: "types.Sticker" = None
    ):
        super().__init__()

        self.title = title
        self.text = text
        self.sticker = sticker


    @staticmethod
    async def _parse(
        client,
        business_intro: "raw.types.BusinessIntro"
    ) -> "BusinessIntro":
        if not business_intro:
            return None
        
        doc = getattr(business_intro, "sticker", None)
        sticker = None

        if doc and isinstance(doc, raw.types.Document):
            sticker = await types.Sticker._parse(
                client,
                doc,
                {type(i): i for i in doc.attributes}
            )

        return BusinessIntro(
            title=getattr(business_intro, "title", None),
            text=getattr(business_intro, "description", None),
            sticker=sticker
        )
