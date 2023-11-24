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

from pyrogram import raw, types, utils
from ..object import Object


class GiftCode(Object):
    """Contains gift code data.

    Parameters:
        via_giveaway (``bool``):
            True if the gift code is received via giveaway.

        unclaimed (``bool``):
            True if the gift code is unclaimed.

        boost_peer (:obj:`~pyrogram.types.Chat`):
            The channel where the gift code was won.

        months (``int``):
            Number of months of subscription.

        slug (``str``):
            Identifier of gift code.
            You can combine it with `t.me/giftcode/{slug}`
            to get link for this gift.
    """

    def __init__(
        self,
        *,
        via_giveaway: bool,
        unclaimed: bool,
        boost_peer,
        months: int,
        slug: str
    ):
        super().__init__()

        self.via_giveaway = via_giveaway
        self.unclaimed = unclaimed
        self.boost_peer = boost_peer
        self.months = months
        self.slug = slug

    @staticmethod
    def _parse(client, giftcode: "raw.types.MessageActionGiftCode", chats):
        peer = chats.get(utils.get_raw_peer_id(giftcode.boost_peer))

        return GiftCode(
            via_giveaway=giftcode.via_giveaway,
            unclaimed=giftcode.unclaimed,
            boost_peer=types.Chat._parse_chat(client, peer) if peer else None,
            months=giftcode.months,
            slug=giftcode.slug
        )

    @property
    def link(self) -> str:
        return f"https://t.me/giftcode/{self.slug}"
