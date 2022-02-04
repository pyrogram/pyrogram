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

from typing import List, Union

import pyrogram
from pyrogram import raw
from pyrogram import types
from ..object import Object
from ..update import Update


class Poll(Object, Update):
    """A Poll.

    Parameters:
        id (``str``):
            Unique poll identifier.

        question (``str``):
            Poll question, 1-255 characters.

        options (List of :obj:`~pyrogram.types.PollOption`):
            List of poll options.

        total_voter_count (``int``):
            Total number of users that voted in the poll.

        is_closed (``bool``):
            True, if the poll is closed.

        is_anonymous (``bool``, *optional*):
            True, if the poll is anonymous

        type (``str``, *optional*):
            Poll type, currently can be "regular" or "quiz".

        allows_multiple_answers (``bool``, *optional*):
            True, if the poll allows multiple answers.

        chosen_option (``int``, *optional*):
            Index of your chosen option (0-9), None in case you haven't voted yet.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: str,
        question: str,
        options: List["types.PollOption"],
        total_voter_count: int,
        is_closed: bool,
        is_anonymous: bool = None,
        type: str = None,
        allows_multiple_answers: bool = None,
        # correct_option_id: int,
        chosen_option: int = None
    ):
        super().__init__(client)

        self.id = id
        self.question = question
        self.options = options
        self.total_voter_count = total_voter_count
        self.is_closed = is_closed
        self.is_anonymous = is_anonymous
        self.type = type
        self.allows_multiple_answers = allows_multiple_answers
        # self.correct_option_id = correct_option_id
        self.chosen_option = chosen_option

    @staticmethod
    def _parse(client, media_poll: Union["raw.types.MessageMediaPoll", "raw.types.UpdateMessagePoll"]) -> "Poll":
        poll = media_poll.poll  # type: raw.types.Poll
        results = media_poll.results.results
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
                types.PollOption(
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
            total_voter_count=media_poll.results.total_voters,
            is_closed=poll.closed,
            is_anonymous=not poll.public_voters,
            type="quiz" if poll.quiz else "regular",
            allows_multiple_answers=poll.multiple_choice,
            chosen_option=chosen_option,
            client=client
        )

    @staticmethod
    def _parse_update(client, update: "raw.types.UpdateMessagePoll"):
        if update.poll is not None:
            return Poll._parse(client, update)

        results = update.results.results
        chosen_option = None
        options = []

        for i, result in enumerate(results):
            if result.chosen:
                chosen_option = i

            options.append(
                types.PollOption(
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
            total_voter_count=update.results.total_voters,
            is_closed=False,
            chosen_option=chosen_option,
            client=client
        )
