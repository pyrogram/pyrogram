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

from pyrogram import raw, utils
from ..object import Object


class SentWebAppMessage(Object):
    """Contains information about an inline message sent by a `Web App <https://core.telegram.org/bots/webapps>`_ on behalf of a user.

    Parameters:
        inline_message_id (``str``):
            Identifier of the sent inline message.
            Available only if there is an inline keyboard attached to the message.
    """

    def __init__(
        self, *,
        inline_message_id: str,
    ):
        super().__init__()

        self.inline_message_id = inline_message_id

    @staticmethod
    def _parse(obj: "raw.types.WebViewMessageSent"):
        return SentWebAppMessage(inline_message_id=utils.pack_inline_message_id(obj.msg_id))
