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

from base64 import b64encode
from struct import pack

import pyrogram
from pyrogram.api import types
from ..pyrogram_type import PyrogramType
from ..update import Update
from ..user_and_chats import User


class CallbackQuery(PyrogramType, Update):
    """This object represents an incoming callback query from a callback button in an inline keyboard.
    If the button that originated the query was attached to a message sent by the bot, the field message
    will be present. If the button was attached to a message sent via the bot (in inline mode),
    the field inline_message_id will be present. Exactly one of the fields data or game_short_name will be present.

    Args:
        id (``str``):
            Unique identifier for this query.

        from_user (:obj:`User <pyrogram.User>`):
            Sender.

        chat_instance (``str``, *optional*):
            Global identifier, uniquely corresponding to the chat to which the message with the callback button was
            sent. Useful for high scores in games.

        message (:obj:`Message <pyrogram.Message>`, *optional*):
            Message with the callback button that originated the query. Note that message content and message date will
            not be available if the message is too old.

        inline_message_id (``str``):
            Identifier of the message sent via the bot in inline mode, that originated the query.

        data (``bytes``, *optional*):
            Data associated with the callback button. Be aware that a bad client can send arbitrary data in this field.

        game_short_name (``str``, *optional*):
            Short name of a Game to be returned, serves as the unique identifier for the game.

    """

    __slots__ = ["id", "from_user", "chat_instance", "message", "inline_message_id", "data", "game_short_name"]

    def __init__(
        self,
        *,
        client: "pyrogram.client.ext.BaseClient",
        id: str,
        from_user: User,
        chat_instance: str,
        message: "pyrogram.Message" = None,
        inline_message_id: str = None,
        data: bytes = None,
        game_short_name: str = None
    ):
        super().__init__(client)

        self.id = id
        self.from_user = from_user
        self.chat_instance = chat_instance
        self.message = message
        self.inline_message_id = inline_message_id
        self.data = str(data, "utf-8")
        self.game_short_name = game_short_name

    @staticmethod
    async def _parse(client, callback_query, users) -> "CallbackQuery":
        message = None
        inline_message_id = None

        if isinstance(callback_query, types.UpdateBotCallbackQuery):
            peer = callback_query.peer

            if isinstance(peer, types.PeerUser):
                peer_id = peer.user_id
            elif isinstance(peer, types.PeerChat):
                peer_id = -peer.chat_id
            else:
                peer_id = int("-100" + str(peer.channel_id))

            message = await client.get_messages(peer_id, callback_query.msg_id)
        elif isinstance(callback_query, types.UpdateInlineBotCallbackQuery):
            inline_message_id = b64encode(
                pack(
                    "<iqq",
                    callback_query.msg_id.dc_id,
                    callback_query.msg_id.id,
                    callback_query.msg_id.access_hash
                ),
                b"-_"
            ).decode().rstrip("=")

        return CallbackQuery(
            id=str(callback_query.query_id),
            from_user=User._parse(client, users[callback_query.user_id]),
            message=message,
            inline_message_id=inline_message_id,
            chat_instance=str(callback_query.chat_instance),
            data=callback_query.data,
            game_short_name=callback_query.game_short_name,
            client=client
        )

    def answer(self, text: str = None, show_alert: bool = None, url: str = None, cache_time: int = 0):
        """Bound method *answer* of :obj:`CallbackQuery <pyrogram.CallbackQuery>`.

        Use this method as a shortcut for:

        .. code-block:: python

            client.answer_callback_query(
                callback_query.id,
                text="Hello",
                show_alert=True
            )

        Example:
            .. code-block:: python

                callback_query.answer("Hello", show_alert=True)

        Args:
            text (``str``):
                Text of the notification. If not specified, nothing will be shown to the user, 0-200 characters.

            show_alert (``bool``):
                If true, an alert will be shown by the client instead of a notification at the top of the chat screen.
                Defaults to False.

            url (``str``):
                URL that will be opened by the user's client.
                If you have created a Game and accepted the conditions via @Botfather, specify the URL that opens your
                game – note that this will only work if the query comes from a callback_game button.
                Otherwise, you may use links like t.me/your_bot?start=XXXX that open your bot with a parameter.

            cache_time (``int``):
                The maximum amount of time in seconds that the result of the callback query may be cached client-side.
                Telegram apps will support caching starting in version 3.14. Defaults to 0.
        """
        return self._client.answer_callback_query(
            callback_query_id=self.id,
            text=text,
            show_alert=show_alert,
            url=url,
            cache_time=cache_time
        )
