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

from typing import Union

from pyrogram.api import functions
from pyrogram.client.ext import BaseClient


class VotePoll(BaseClient):
    # TODO: Docs
    def vote_poll(self,
                  chat_id: Union[int, str],
                  message_id: id,
                  option: int) -> bool:
        self.send(
            functions.messages.SendVote(
                peer=self.resolve_peer(chat_id),
                msg_id=message_id,
                options=[bytes([option])]
            )
        )

        return True
