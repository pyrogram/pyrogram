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

from typing import List

import pyrogram
from pyrogram.api import types
from .poll_option import PollOption
from ..pyrogram_type import PyrogramType


class Poll(PyrogramType):
    """This object represents a Poll.

    Args:
        id (``int``):
            The poll id in this chat.

        closed (``bool``):
            Whether the poll is closed or not.

        question (``str``):
            Poll question.

        options (List of :obj:`PollOption`):
            The available poll options.

        total_voters (``int``):
            Total amount of voters for this poll.

        option_chosen (``int``, *optional*):
            The index of your chosen option (in case you voted already), None otherwise.
    """

    def __init__(self,
                 *,
                 client: "pyrogram.client.ext.BaseClient",
                 id: int,
                 closed: bool,
                 question: str,
                 options: List[PollOption],
                 total_voters: int,
                 option_chosen: int = None):
        super().__init__(client)

        self.id = id
        self.closed = closed
        self.question = question
        self.options = options
        self.total_voters = total_voters
        self.option_chosen = option_chosen

    @staticmethod
    def _parse(client, media_poll: types.MessageMediaPoll) -> "Poll":
        poll = media_poll.poll
        results = media_poll.results.results
        total_voters = media_poll.results.total_voters
        option_chosen = None

        options = []

        for i, answer in enumerate(poll.answers):
            voters = 0

            if results:
                result = results[i]
                voters = result.voters

                if result.chosen:
                    option_chosen = i

            options.append(PollOption(
                text=answer.text,
                voters=voters,
                data=answer.option,
                client=client
            ))

        return Poll(
            id=poll.id,
            closed=poll.closed,
            question=poll.question,
            options=options,
            total_voters=total_voters,
            option_chosen=option_chosen,
            client=client
        )
