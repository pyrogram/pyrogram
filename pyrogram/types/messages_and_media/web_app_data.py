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


class WebAppData(Object):
    """Contains data sent from a `Web App <https://core.telegram.org/bots/webapps>`_ to the bot.

    Parameters:
        data (``str``):
            The data.

        button_text (``str``):
            Text of the *web_app* keyboard button, from which the Web App was opened.

    """

    def __init__(
        self,
        *,
        data: str,
        button_text: str,
    ):
        super().__init__()

        self.data = data
        self.button_text = button_text

    @staticmethod
    def _parse(action: "raw.types.MessageActionWebViewDataSentMe"):
        return WebAppData(
            data=action.data,
            button_text=action.text
        )
