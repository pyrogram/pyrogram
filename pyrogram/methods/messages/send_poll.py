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
from typing import Union, List

import pyrogram
from pyrogram import raw, utils
from pyrogram import types, enums


class SendPoll:
    async def send_poll(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        question: str,
        options: List[str],
        is_anonymous: bool = True,
        type: "enums.PollType" = enums.PollType.REGULAR,
        allows_multiple_answers: bool = None,
        correct_option_id: int = None,
        explanation: str = None,
        explanation_parse_mode: "enums.ParseMode" = None,
        explanation_entities: List["types.MessageEntity"] = None,
        open_period: int = None,
        close_date: datetime = None,
        is_closed: bool = None,
        disable_notification: bool = None,
        protect_content: bool = None,
        reply_to_message_id: int = None,
        schedule_date: datetime = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None
    ) -> "types.Message":
        """Send a new poll.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            question (``str``):
                Poll question, 1-255 characters.

            options (List of ``str``):
                List of answer options, 2-10 strings 1-100 characters each.

            is_anonymous (``bool``, *optional*):
                True, if the poll needs to be anonymous.
                Defaults to True.

            type (:obj`~pyrogram.enums.PollType`, *optional*):
                Poll type, :obj:`~pyrogram.enums.PollType.QUIZ` or :obj:`~pyrogram.enums.PollType.REGULAR`.
                Defaults to :obj:`~pyrogram.enums.PollType.REGULAR`.

            allows_multiple_answers (``bool``, *optional*):
                True, if the poll allows multiple answers, ignored for polls in quiz mode.
                Defaults to False.

            correct_option_id (``int``, *optional*):
                0-based identifier of the correct answer option, required for polls in quiz mode.

            explanation (``str``, *optional*):
                Text that is shown when a user chooses an incorrect answer or taps on the lamp icon in a quiz-style
                poll, 0-200 characters with at most 2 line feeds after entities parsing.

            explanation_parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            explanation_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the poll explanation, which can be specified instead of
                *parse_mode*.

            open_period (``int``, *optional*):
                Amount of time in seconds the poll will be active after creation, 5-600.
                Can't be used together with *close_date*.

            close_date (:py:obj:`~datetime.datetime`, *optional*):
                Point in time when the poll will be automatically closed.
                Must be at least 5 and no more than 600 seconds in the future.
                Can't be used together with *open_period*.

            is_closed (``bool``, *optional*):
                Pass True, if the poll needs to be immediately closed.
                This can be useful for poll preview.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the sent poll message is returned.

        Example:
            .. code-block:: python

                await app.send_poll(chat_id, "Is this a poll question?", ["Yes", "No", "Maybe"])
        """

        solution, solution_entities = (await utils.parse_text_entities(
            self, explanation, explanation_parse_mode, explanation_entities
        )).values()

        r = await self.invoke(
            raw.functions.messages.SendMedia(
                peer=await self.resolve_peer(chat_id),
                media=raw.types.InputMediaPoll(
                    poll=raw.types.Poll(
                        id=self.rnd_id(),
                        question=question,
                        answers=[
                            raw.types.PollAnswer(text=text, option=bytes([i]))
                            for i, text in enumerate(options)
                        ],
                        closed=is_closed,
                        public_voters=not is_anonymous,
                        multiple_choice=allows_multiple_answers,
                        quiz=type == enums.PollType.QUIZ or False,
                        close_period=open_period,
                        close_date=utils.datetime_to_timestamp(close_date)
                    ),
                    correct_answers=[bytes([correct_option_id])] if correct_option_id is not None else None,
                    solution=solution,
                    solution_entities=solution_entities or []
                ),
                message="",
                silent=disable_notification,
                reply_to_msg_id=reply_to_message_id,
                random_id=self.rnd_id(),
                schedule_date=utils.datetime_to_timestamp(schedule_date),
                noforwards=protect_content,
                reply_markup=await reply_markup.write(self) if reply_markup else None
            )
        )

        for i in r.updates:
            if isinstance(i, (raw.types.UpdateNewMessage,
                              raw.types.UpdateNewChannelMessage,
                              raw.types.UpdateNewScheduledMessage)):
                return await types.Message._parse(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                    is_scheduled=isinstance(i, raw.types.UpdateNewScheduledMessage)
                )
