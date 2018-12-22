# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>
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

from typing import Union, List

import pyrogram
from pyrogram.api import functions, types
from pyrogram.client.ext import BaseClient


class SendPoll(BaseClient):
    # TODO: Docs
    def send_poll(self,
                  chat_id: Union[int, str],
                  question: str,
                  options: List[str],
                  disable_notification: bool = None,
                  reply_to_message_id: int = None,
                  reply_markup: Union["pyrogram.InlineKeyboardMarkup",
                                      "pyrogram.ReplyKeyboardMarkup",
                                      "pyrogram.ReplyKeyboardRemove",
                                      "pyrogram.ForceReply"] = None) -> "pyrogram.Message":
        r = self.send(
            functions.messages.SendMedia(
                peer=self.resolve_peer(chat_id),
                media=types.InputMediaPoll(
                    poll=types.Poll(
                        id=0,
                        question=question,
                        answers=[
                            types.PollAnswer(text=o, option=bytes([i]))
                            for i, o in enumerate(options)
                        ]
                    )
                ),
                message="",
                silent=disable_notification or None,
                reply_to_msg_id=reply_to_message_id,
                random_id=self.rnd_id(),
                reply_markup=reply_markup.write() if reply_markup else None
            )
        )

        for i in r.updates:
            if isinstance(i, (types.UpdateNewMessage, types.UpdateNewChannelMessage)):
                return pyrogram.Message._parse(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats}
                )
