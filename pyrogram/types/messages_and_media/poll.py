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

from datetime import datetime
from typing import List, Union, Optional

import pyrogram
from pyrogram import raw, enums, utils
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

        type (:obj:`~pyrogram.enums.PollType`, *optional*):
            Poll type.

        allows_multiple_answers (``bool``, *optional*):
            True, if the poll allows multiple answers.

        chosen_option_id (``int``, *optional*):
            0-based index of the chosen option), None in case of no vote yet.

        correct_option_id (``int``, *optional*):
            0-based identifier of the correct answer option.
            Available only for polls in the quiz mode, which are closed, or was sent (not forwarded) by the bot or to
            the private chat with the bot.

        explanation (``str``, *optional*):
            Text that is shown when a user chooses an incorrect answer or taps on the lamp icon in a quiz-style poll,
            0-200 characters.

        explanation_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            Special entities like usernames, URLs, bot commands, etc. that appear in the explanation.

        open_period (``int``, *optional*):
            Amount of time in seconds the poll will be active after creation.

        close_date (:py:obj:`~datetime.datetime`, *optional*):
            Point in time when the poll will be automatically closed.
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
        type: "enums.PollType" = None,
        allows_multiple_answers: bool = None,
        chosen_option_id: Optional[int] = None,
        correct_option_id: Optional[int] = None,
        explanation: Optional[str] = None,
        explanation_entities: Optional[List["types.MessageEntity"]] = None,
        open_period: Optional[int] = None,
        close_date: Optional[datetime] = None
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
        self.chosen_option_id = chosen_option_id
        self.correct_option_id = correct_option_id
        self.explanation = explanation
        self.explanation_entities = explanation_entities
        self.open_period = open_period
        self.close_date = close_date

    @staticmethod
    def _parse(client, media_poll: Union["raw.types.MessageMediaPoll", "raw.types.UpdateMessagePoll"]) -> "Poll":
        poll: raw.types.Poll = media_poll.poll
        poll_results: raw.types.PollResults = media_poll.results
        results: List[raw.types.PollAnswerVoters] = poll_results.results

        chosen_option_id = None
        correct_option_id = None
        options = []

        for i, answer in enumerate(poll.answers):
            voter_count = 0

            if results:
                result = results[i]
                voter_count = result.voters

                if result.chosen:
                    chosen_option_id = i

                if result.correct:
                    correct_option_id = i

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
            type=enums.PollType.QUIZ if poll.quiz else enums.PollType.REGULAR,
            allows_multiple_answers=poll.multiple_choice,
            chosen_option_id=chosen_option_id,
            correct_option_id=correct_option_id,
            explanation=poll_results.solution,
            explanation_entities=[
                types.MessageEntity._parse(client, i, {})
                for i in poll_results.solution_entities
            ] if poll_results.solution_entities else None,
            open_period=poll.close_period,
            close_date=utils.timestamp_to_datetime(poll.close_date),
            client=client
        )

    @staticmethod
    def _parse_update(client, update: "raw.types.UpdateMessagePoll"):
        if update.poll is not None:
            return Poll._parse(client, update)

        results = update.results.results
        chosen_option_id = None
        correct_option_id = None
        options = []

        for i, result in enumerate(results):
            if result.chosen:
                chosen_option_id = i

            if result.correct:
                correct_option_id = i

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
            chosen_option_id=chosen_option_id,
            correct_option_id=correct_option_id,
            client=client
        )
