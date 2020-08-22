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

from typing import Union, Iterable, List

from pyrogram import raw
from pyrogram import types
from pyrogram.scaffold import Scaffold


class ForwardMessages(Scaffold):
    async def forward_messages(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_ids: Union[int, Iterable[int]],
        disable_notification: bool = None,
        as_copy: bool = False,
        remove_caption: bool = False,
        schedule_date: int = None
    ) -> List["types.Message"]:
        """Forward messages of any kind.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            from_chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the source chat where the original message was sent.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_ids (``iterable``):
                A list of Message identifiers in the chat specified in *from_chat_id* or a single message id.
                Iterators and Generators are also accepted.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            as_copy (``bool``, *optional*):
                Pass True to forward messages without the forward header (i.e.: send a copy of the message content so
                that it appears as originally sent by you).
                Defaults to False.

            remove_caption (``bool``, *optional*):
                If set to True and *as_copy* is enabled as well, media captions are not preserved when copying the
                message. Has no effect if *as_copy* is not enabled.
                Defaults to False.

            schedule_date (``int``, *optional*):
                Date when the message will be automatically sent. Unix time.

        Returns:
            :obj:`~pyrogram.types.Message` | List of :obj:`~pyrogram.types.Message`: In case *message_ids* was an
            integer, the single forwarded message is returned, otherwise, in case *message_ids* was an iterable,
            the returned value will be a list of messages, even if such iterable contained just a single element.

        Example:
            .. code-block:: python
                :emphasize-lines: 2,5,8

                # Forward a single message
                app.forward_messages("me", "pyrogram", 20)

                # Forward multiple messages at once
                app.forward_messages("me", "pyrogram", [3, 20, 27])

                # Forward messages as copy
                app.forward_messages("me", "pyrogram", 20, as_copy=True)
        """

        is_iterable = not isinstance(message_ids, int)
        message_ids = list(message_ids) if is_iterable else [message_ids]

        if as_copy:
            forwarded_messages = []

            for chunk in [message_ids[i:i + 200] for i in range(0, len(message_ids), 200)]:
                messages = await self.get_messages(chat_id=from_chat_id, message_ids=chunk)

                for message in messages:
                    forwarded_messages.append(
                        await message.forward(
                            chat_id,
                            disable_notification=disable_notification,
                            as_copy=True,
                            remove_caption=remove_caption,
                            schedule_date=schedule_date
                        )
                    )

            return types.List(forwarded_messages) if is_iterable else forwarded_messages[0]
        else:
            r = await self.send(
                raw.functions.messages.ForwardMessages(
                    to_peer=await self.resolve_peer(chat_id),
                    from_peer=await self.resolve_peer(from_chat_id),
                    id=message_ids,
                    silent=disable_notification or None,
                    random_id=[self.rnd_id() for _ in message_ids],
                    schedule_date=schedule_date
                )
            )

            forwarded_messages = []

            users = {i.id: i for i in r.users}
            chats = {i.id: i for i in r.chats}

            for i in r.updates:
                if isinstance(i, (raw.types.UpdateNewMessage,
                                  raw.types.UpdateNewChannelMessage,
                                  raw.types.UpdateNewScheduledMessage)):
                    forwarded_messages.append(
                        await types.Message._parse(
                            self, i.message,
                            users, chats
                        )
                    )

            return types.List(forwarded_messages) if is_iterable else forwarded_messages[0]
