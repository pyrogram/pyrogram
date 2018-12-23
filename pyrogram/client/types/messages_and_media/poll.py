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

from typing import List

import pyrogram
from pyrogram.api import types
from ..pyrogram_type import PyrogramType


class PollOption(PyrogramType):
    def __init__(self,
                 *,
                 client: "pyrogram.client.ext.BaseClient",
                 text: str,
                 voters: int):
        super().__init__(client)

        self.text = text
        self.voters = voters


class Poll(PyrogramType):
    def __init__(self,
                 *,
                 client: "pyrogram.client.ext.BaseClient",
                 id: int,
                 closed: bool,
                 question: str,
                 options: List[PollOption],
                 option_chosen: int = None,
                 total_voters: int):
        super().__init__(client)

        self.id = id
        self.closed = closed
        self.question = question
        self.options = options
        self.option_chosen = option_chosen
        self.total_voters = total_voters

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
                client=client
            ))

        return Poll(
            id=poll.id,
            closed=poll.closed,
            question=poll.question,
            options=options,
            option_chosen=option_chosen,
            total_voters=total_voters,
            client=client
        )
