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

import logging
from typing import List

import pyrogram
from pyrogram import raw
from pyrogram import types
from pyrogram.errors import PhoneMigrate, NetworkMigrate
from pyrogram.session import Session, Auth

log = logging.getLogger(__name__)


class SendCode:
    async def send_code(
        self: "pyrogram.Client",
        phone_number: str,
        current_number: bool = None,
        allow_flashcall: bool = None,
        allow_app_hash: bool = None,
        allow_missed_call: bool = None,
        allow_firebase: bool = None,
        logout_tokens: List[bytes] = None,
        token: str = None,
        app_sandbox: bool = None,
    ) -> "types.SentCode":
        """Send the confirmation code to the given phone number.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            phone_number (``str``):
                Phone number in international format (includes the country prefix).

            current_number (``bool``, *optional*):
                Whether the phone number is the current one.
                Defaults to None.

            allow_flashcall (``bool``, *optional*):
                Whether to allow a flash call.
                Defaults to None.

            allow_app_hash (``bool``, *optional*):
                Whether to allow an app hash.
                Defaults to None.

            allow_missed_call (``bool``, *optional*):
                Whether to allow a missed call.
                Defaults to None.

            allow_firebase (``bool``, *optional*):
                Whether to allow firebase.
                Defaults to None.

            logout_tokens (List of ``bytes``, *optional*):
                List of logout tokens.
                Defaults to None.

            token (``str``, *optional*):
                Token.
                Defaults to None.

            app_sandbox (``bool``, *optional*):
                Whether to use the app sandbox.
                Defaults to None.

        Returns:
            :obj:`~pyrogram.types.SentCode`: On success, an object containing information on the sent confirmation code
            is returned.

        Raises:
            BadRequest: In case the phone number is invalid.
        """
        phone_number = phone_number.strip(" +")

        while True:
            try:
                r = await self.invoke(
                    raw.functions.auth.SendCode(
                        phone_number=phone_number,
                        api_id=self.api_id,
                        api_hash=self.api_hash,
                        settings=raw.types.CodeSettings(
                            allow_flashcall=allow_flashcall,
                            current_number=current_number,
                            allow_app_hash=allow_app_hash,
                            allow_missed_call=allow_missed_call,
                            allow_firebase=allow_firebase,
                            logout_tokens=logout_tokens,
                            token=token,
                            app_sandbox=app_sandbox
                        )
                    )
                )
            except (PhoneMigrate, NetworkMigrate) as e:
                await self.session.stop()

                await self.storage.dc_id(e.value)
                await self.storage.auth_key(
                    await Auth(
                        self, await self.storage.dc_id(),
                        await self.storage.test_mode()
                    ).create()
                )
                self.session = Session(
                    self, await self.storage.dc_id(),
                    await self.storage.auth_key(), await self.storage.test_mode()
                )

                await self.session.start()
            else:
                return types.SentCode._parse(r)
