#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2020 Dan <https://github.com/delivrance>
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

from typing import Union

import pyrogram
from pyrogram.api import functions
from pyrogram.session import Auth, Session
from pyrogram.errors import AuthBytesInvalid
from pyrogram.client.ext import BaseClient, utils


class EditInlineText(BaseClient):
    async def edit_inline_text(
        self,
        inline_message_id: str,
        text: str,
        parse_mode: Union[str, None] = object,
        disable_web_page_preview: bool = None,
        reply_markup: "pyrogram.InlineKeyboardMarkup" = None
    ) -> bool:
        """Edit the text of inline messages.

        Parameters:
            inline_message_id (``str``):
                Identifier of the inline message.

            text (``str``):
                New text of the message.

            parse_mode (``str``, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.
                Pass "markdown" or "md" to enable Markdown-style parsing only.
                Pass "html" to enable HTML-style parsing only.
                Pass None to completely disable style parsing.

            disable_web_page_preview (``bool``, *optional*):
                Disables link previews for links in this message.

            reply_markup (:obj:`InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Bots only

                # Simple edit text
                app.edit_inline_text(inline_message_id, "new text")

                # Take the same text message, remove the web page preview only
                app.edit_inline_text(
                    inline_message_id, message.text,
                    disable_web_page_preview=True)
        """

        unpacked = utils.unpack_inline_message_id(inline_message_id)

        if unpacked.dc_id != self.storage.dc_id():
            session = Session(self, unpacked.dc_id, await Auth(self, unpacked.dc_id).create(), is_media=True)

            await session.start()

            for _ in range(3):
                exported_auth = await self.send(
                    functions.auth.ExportAuthorization(
                        dc_id=unpacked.dc_id
                    )
                )

                try:
                    await session.send(
                        functions.auth.ImportAuthorization(
                            id=exported_auth.id,
                            bytes=exported_auth.bytes
                        )
                    )
                except AuthBytesInvalid:
                    continue
                else:
                    break
            else:
                await session.stop()
                raise AuthBytesInvalid

            await session.send(
                functions.messages.EditInlineBotMessage(
                    id=unpacked,
                    no_webpage=disable_web_page_preview or None,
                    reply_markup=reply_markup.write() if reply_markup else None,
                    **await self.parser.parse(text, parse_mode)
                )
            )

            await session.stop()
        else:
            await self.send(
                functions.messages.EditInlineBotMessage(
                    id=unpacked,
                    no_webpage=disable_web_page_preview or None,
                    reply_markup=reply_markup.write() if reply_markup else None,
                    **await self.parser.parse(text, parse_mode)
                )
            )