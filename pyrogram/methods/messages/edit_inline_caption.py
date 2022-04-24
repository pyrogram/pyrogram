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

from typing import Optional

import pyrogram
from pyrogram import types, enums


class EditInlineCaption:
    async def edit_inline_caption(
        self: "pyrogram.Client",
        inline_message_id: str,
        caption: str,
        parse_mode: Optional["enums.ParseMode"] = None,
        reply_markup: "types.InlineKeyboardMarkup" = None
    ) -> bool:
        """Edit the caption of inline media messages.

        Parameters:
            inline_message_id (``str``):
                Identifier of the inline message.

            caption (``str``):
                New caption of the media message.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Bots only
                await app.edit_inline_caption(inline_message_id, "new media caption")
        """
        return await self.edit_inline_text(
            inline_message_id=inline_message_id,
            text=caption,
            parse_mode=parse_mode,
            reply_markup=reply_markup
        )
