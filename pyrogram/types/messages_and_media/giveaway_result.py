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
from typing import List

import pyrogram
from pyrogram import errors, raw, utils
from pyrogram import types
from ..object import Object


class GiveawayResult(Object):
    """An giveaway result.

    Parameters:
        chat (List of :obj:`~pyrogram.types.Chat`):
            Channel which host the giveaway.

        quantity (``int``):
            Total number of subscriptions in this giveaway.

        winners_count (``int``):
            Number of winners who claimed their gift.

        unclaimed_count (``int``):
            Unclaimed giveaway subscriptions count.

        winners (List of :obj:`~pyrogram.types.User`):
            A list of giveaway winners.

        months (``int``):
            Number of months for which a subscription is given.

        until_date (:py:obj:`~datetime.datetime`):
            Date when the giveaway will end.

        launch_message_id (``int``):
            Identifier of the original message with the giveaway.

        launch_message (:obj:`~pyrogram.types.Message`, *optional*):
            Returns the original giveaway start message.
            If the channel is private, returns None

        description (``str``, *optional*):
            Prize description.

        only_new_subscribers (``bool``, *optional*):
            True, if this giveaway is for new subscribers only.

        is_refunded (``bool``, *optional*):
            True, if this giveaway was refunded.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        chat: "types.Chat",
        quantity: int,
        winners_count: int,
        unclaimed_count: int,
        winners: List["types.User"],
        months: int,
        until_date: datetime,
        launch_message_id: int,
        launch_message: "types.Message" = None,
        description: str = None,
        only_new_subscribers: bool = None,
        is_refunded: bool = None
    ):
        super().__init__(client)

        self.chat = chat
        self.quantity = quantity
        self.winners_count = winners_count
        self.unclaimed_count = unclaimed_count
        self.winners = winners
        self.months = months
        self.until_date = until_date
        self.launch_message_id = launch_message_id
        self.launch_message = launch_message
        self.description = description
        self.only_new_subscribers = only_new_subscribers
        self.is_refunded = is_refunded

    @staticmethod
    async def _parse(
        client,
        giveaway_result: "raw.types.MessageMediaGiveawayResults",
        users: dict,
        chats: dict
    ) -> "GiveawayResult":
        launch_message = None

        try:
            launch_message = await client.get_messages(
                utils.get_channel_id(giveaway_result.channel_id),
                giveaway_result.launch_msg_id,
                replies=0
            )
        except (errors.ChannelPrivate, errors.ChannelInvalid):
            pass

        return GiveawayResult(
            chat=types.Chat._parse_channel_chat(client, chats[giveaway_result.channel_id]),
            quantity=giveaway_result.winners_count + giveaway_result.unclaimed_count,
            winners_count=giveaway_result.winners_count,
            unclaimed_count=giveaway_result.unclaimed_count,
            winners=types.List(types.User._parse(client, users.get(i)) for i in giveaway_result.winners) or None,
            months=giveaway_result.months,
            until_date=utils.timestamp_to_datetime(giveaway_result.until_date),
            launch_message_id=giveaway_result.launch_msg_id,
            only_new_subscribers=getattr(giveaway_result, "only_new_subscribers", None),
            is_refunded=getattr(giveaway_result, "refunded", None),
            launch_message=launch_message,
            description=getattr(giveaway_result, "prize_description", None) or None,
            client=client
        )
