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


class LoginUrl(Object):
    """Represents a parameter of the inline keyboard button used to automatically authorize a user.

    Serves as a great replacement for the Telegram Login Widget when the user is coming from Telegram.
    All the user needs to do is tap/click a button and confirm that they want to log in.

    Parameters:
        url (``str``):
            An HTTP URL to be opened with user authorization data added to the query string when the button is pressed.
            If the user refuses to provide authorization data, the original URL without information about the user will
            be opened. The data added is the same as described in
            `Receiving authorization data <https://core.telegram.org/widgets/login#receiving-authorization-data>`.

            **NOTE**: You **must** always check the hash of the received data to verify the authentication and the
            integrity of the data as described in
            `Checking authorization <https://core.telegram.org/widgets/login#checking-authorization>`_.

        forward_text (``str``, *optional*):
            New text of the button in forwarded messages.

        bot_username (``str``, *optional*):
            Username of a bot, which will be used for user authorization.
            See `Setting up a bot <https://core.telegram.org/widgets/login#setting-up-a-bot>`_ for more details.
            If not specified, the current bot's username will be assumed. The url's domain must be the same as the
            domain linked with the bot.
            See `Linking your domain to the bot <https://core.telegram.org/widgets/login#linking-your-domain-to-the-bot>`_
            for more details.

        request_write_access (``str``, *optional*):
            Pass True to request the permission for your bot to send messages to the user.

        button_id (``int``):
            Button identifier.
    """

    def __init__(
        self, *,
        url: str,
        forward_text: str = None,
        bot_username: str = None,
        request_write_access: str = None,
        button_id: int = None
    ):
        super().__init__()

        self.url = url
        self.forward_text = forward_text
        self.bot_username = bot_username
        self.request_write_access = request_write_access
        self.button_id = button_id

    @staticmethod
    def read(b: "raw.types.KeyboardButtonUrlAuth") -> "LoginUrl":
        return LoginUrl(
            url=b.url,
            forward_text=b.fwd_text,
            button_id=b.button_id
        )

    def write(self, text: str, bot: "raw.types.InputUser"):
        return raw.types.InputKeyboardButtonUrlAuth(
            text=text,
            url=self.url,
            bot=bot,
            fwd_text=self.forward_text,
            request_write_access=self.request_write_access
        )
