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

from typing import List, Union

import pyrogram
from pyrogram.api import types
from .poll_option import PollOption
from ..object import Object
from ..update import Update


class Poll(Object, Update):
    """A Poll.

    Parameters:
        id (``str``):
            Unique poll identifier.

        question (``str``):
            Poll question, 1-255 characters.

        options (List of :obj:`PollOption`):
            List of poll options.

        is_closed (``bool``):
            True, if the poll is closed.

        total_voters (``int``):
            Total count of voters for this poll.

        chosen_option (``int``, *optional*):
            Index of your chosen option (0-9), None in case you haven't voted yet.
    """

    __slots__ = ["id", "question", "options", "is_closed", "total_voters", "chosen_option"]

    def __init__(
        self,
        *,
        client: "pyrogram.BaseClient" = None,
        id: str,
        question: str,
        options: List[PollOption],
        is_closed: bool,
        total_voters: int,
        chosen_option: int = None
    ):
        super().__init__(client)

        self.id = id
        self.question = question
        self.options = options
        self.is_closed = is_closed
        self.total_voters = total_voters
        self.chosen_option = chosen_option

    @staticmethod
    def _parse(client, media_poll: Union[types.MessageMediaPoll, types.UpdateMessagePoll]) -> "Poll":
        poll = media_poll.poll
        results = media_poll.results.results
        total_voters = media_poll.results.total_voters
        chosen_option = None
        options = []

        for i, answer in enumerate(poll.answers):
            voter_count = 0

            if results:
                result = results[i]
                voter_count = result.voters

                if result.chosen:
                    chosen_option = i

            options.append(
                PollOption(
                    text=answer.text,
                    voter_count=voter_count,
                    data=answer.option,
                    client=client
                )
            )

        return Poll(
            id=str(poll.id),
            question=poll.question,
            options=options,
            is_closed=poll.closed,
            total_voters=total_voters,
            chosen_option=chosen_option,
            client=client
        )

    @staticmethod
    def _parse_update(client, update: types.UpdateMessagePoll):
        if update.poll is not None:
            return Poll._parse(client, update)

        results = update.results.results
        chosen_option = None
        options = []

        for i, result in enumerate(results):
            if result.chosen:
                chosen_option = i

            options.append(
                PollOption(
                    text="",
                    voter_count=result.voters,
                    data=result.option,
                    client=client
                )
            )

        return Poll(
            id=str(update.poll_id),
            question="",
            options=options,
            is_closed=False,
            total_voters=update.results.total_voters,
            chosen_option=chosen_option,
            client=client
        )
