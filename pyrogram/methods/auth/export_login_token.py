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
import base64
import logging
from typing import Union, List

from pyrogram import raw
from pyrogram import types
from pyrogram.scaffold import Scaffold

log = logging.getLogger(__name__)


class ExportLoginToken(Scaffold):
    async def export_login_token(
        self,
        *,
        api_id: int = None,
        api_hash: str = None,
        except_ids: List[int] = None
    ) -> Union["types.User", str]:
        """Generate a login token, for login via QR code.

        Parameters:
            api_id (``int`` | ``str``, *optional*):
                The *api_id* part of your Telegram API Key, as integer. E.g.: "12345".
                This is an alternative way to pass it if you don't want to use the *config.ini* file.

            api_hash (``str``, *optional*):
                The *api_hash* part of your Telegram API Key, as string. E.g.: "0123456789abcdef0123456789abcdef".
                This is an alternative way to set it if you don't want to use the *config.ini* file.

            except_ids (``str``):
                List of already logged-in user IDs, to prevent logging in twice with the same user.

        Returns:
            :obj:`~pyrogram.types.User` | str: On success, in case the
            authorization completed, the user is returned, otherwise the link for QR code in format of "tg://login?token=base64encodedtoken".

        """

        if except_ids is None:
            except_ids = []

        r = await self.send(
            raw.functions.auth.ExportLoginToken(
                api_id=api_id or self.api_id,
                api_hash=api_hash or self.api_hash,
                except_ids=except_ids
            )
        )

        log.info(f'Result is: {r.__class__.__name__}')

        if isinstance(r, raw.types.auth.LoginToken):
            return f"tg://login?token={base64.urlsafe_b64encode(r.token).decode()}"

        if isinstance(r, raw.types.auth.LoginTokenMigrateTo):
            r = await self.send(
                raw.functions.auth.ImportLoginToken(
                    token=r.token,
                )
            )

        if isinstance(r, raw.types.auth.LoginTokenSuccess):
            await self.storage.user_id(r.user.id)
            await self.storage.is_bot(False)

            return types.User._parse(self, r.user)
