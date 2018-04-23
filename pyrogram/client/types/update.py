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

from pyrogram.api.core import Object


class Update(Object):
    """This object represents an incoming update.At most one of the optional parameters can be present in any given update.

    Attributes:
        ID: ``0xb0700000``

    Args:
        update_id (``int`` ``32-bit``):
            The update's unique identifier. Update identifiers start from a certain positive number and increase sequentially. This ID becomes especially handy if you're using Webhooks, since it allows you to ignore repeated updates or to restore the correct update sequence, should they get out of order. If there are no new updates for at least a week, then identifier of the next update will be chosen randomly instead of sequentially.

        message (:obj:`Message <pyrogram.types.Message>`, optional):
            New incoming message of any kind — text, photo, sticker, etc.

        edited_message (:obj:`Message <pyrogram.types.Message>`, optional):
            New version of a message that is known to the bot and was edited.

        channel_post (:obj:`Message <pyrogram.types.Message>`, optional):
            New incoming channel post of any kind — text, photo, sticker, etc.

        edited_channel_post (:obj:`Message <pyrogram.types.Message>`, optional):
            New version of a channel post that is known to the bot and was edited.

        inline_query (:obj:`InlineQuery <pyrogram.types.InlineQuery>`, optional):
            New incoming inline query.

        chosen_inline_result (:obj:`ChosenInlineResult <pyrogram.types.ChosenInlineResult>`, optional):
            The result of an inline query that was chosen by a user and sent to their chat partner. Please see our documentation on the feedback collecting for details on how to enable these updates for your bot.

        callback_query (:obj:`CallbackQuery <pyrogram.types.CallbackQuery>`, optional):
            New incoming callback query.

        shipping_query (:obj:`ShippingQuery <pyrogram.types.ShippingQuery>`, optional):
            New incoming shipping query. Only for invoices with flexible price.

        pre_checkout_query (:obj:`PreCheckoutQuery <pyrogram.types.PreCheckoutQuery>`, optional):
            New incoming pre-checkout query. Contains full information about checkout.

    """
    ID = 0xb0700000

    def __init__(self, update_id, message=None, edited_message=None, channel_post=None, edited_channel_post=None, inline_query=None, chosen_inline_result=None, callback_query=None, shipping_query=None, pre_checkout_query=None):
        self.update_id = update_id  # int
        self.message = message  # flags.0?Message
        self.edited_message = edited_message  # flags.1?Message
        self.channel_post = channel_post  # flags.2?Message
        self.edited_channel_post = edited_channel_post  # flags.3?Message
        self.inline_query = inline_query  # flags.4?InlineQuery
        self.chosen_inline_result = chosen_inline_result  # flags.5?ChosenInlineResult
        self.callback_query = callback_query  # flags.6?CallbackQuery
        self.shipping_query = shipping_query  # flags.7?ShippingQuery
        self.pre_checkout_query = pre_checkout_query  # flags.8?PreCheckoutQuery
