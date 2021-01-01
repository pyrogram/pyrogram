#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2021 Dan <https://github.com/delivrance>
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


class SentCode(Object):
    """Contains info on a sent confirmation code.

    Parameters:
        type (``str``):
            Type of the current sent code.
            Can be *"app"* (code sent via Telegram), *"sms"* (code sent via SMS), *"call"* (code sent via voice call) or
            *"flash_call"* (code is in the last 5 digits of the caller's phone number).

        phone_code_hash (``str``):
            Confirmation code identifier useful for the next authorization steps (either
            :meth:`~pyrogram.Client.sign_in` or :meth:`~pyrogram.Client.sign_up`).

        next_type (``str``):
            Type of the next code to be sent with :meth:`~pyrogram.Client.resend_code`.
            Can be *"sms"* (code will be sent via SMS), *"call"* (code will be sent via voice call) or *"flash_call"*
            (code will be in the last 5 digits of caller's phone number).

        timeout (``int``):
            Delay in seconds before calling :meth:`~pyrogram.Client.resend_code`.
    """

    def __init__(
        self, *,
        type: str,
        phone_code_hash: str,
        next_type: str = None,
        timeout: int = None
    ):
        super().__init__()

        self.type = type
        self.phone_code_hash = phone_code_hash
        self.next_type = next_type
        self.timeout = timeout

    @staticmethod
    def _parse(sent_code: raw.types.auth.SentCode) -> "SentCode":
        type = sent_code.type

        if isinstance(type, raw.types.auth.SentCodeTypeApp):
            type = "app"
        elif isinstance(type, raw.types.auth.SentCodeTypeSms):
            type = "sms"
        elif isinstance(type, raw.types.auth.SentCodeTypeCall):
            type = "call"
        elif isinstance(type, raw.types.auth.SentCodeTypeFlashCall):
            type = "flash_call"

        next_type = sent_code.next_type

        if isinstance(next_type, raw.types.auth.CodeTypeSms):
            next_type = "sms"
        elif isinstance(next_type, raw.types.auth.CodeTypeCall):
            next_type = "call"
        elif isinstance(next_type, raw.types.auth.CodeTypeFlashCall):
            next_type = "flash_call"

        return SentCode(
            type=type,
            phone_code_hash=sent_code.phone_code_hash,
            next_type=next_type,
            timeout=sent_code.timeout
        )
