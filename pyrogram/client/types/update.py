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
    """This object represents an incoming update.
    At most one of the optional parameters can be present in any given update.

    Args:
        message (:obj:`Message <pyrogram.Message>`, *optional*):
            New incoming message of any kind — text, photo, sticker, etc.

        edited_message (:obj:`Message <pyrogram.Message>`, *optional*):
            New version of a message that is known to the bot and was edited.

        deleted_messages (:obj:`Messages <pyrogram.Messages>`, *optional*):
            Deleted messages.

        channel_post (:obj:`Message <pyrogram.Message>`, *optional*):
            New incoming channel post of any kind — text, photo, sticker, etc.

        edited_channel_post (:obj:`Message <pyrogram.Message>`, *optional*):
            New version of a channel post that is known to the bot and was edited.

        deleted_channel_posts (:obj:`Messages <pyrogram.Messages>`, *optional*):
            Deleted channel posts.

        inline_query (:obj:`InlineQuery <pyrogram.InlineQuery>`, *optional*):
            New incoming inline query.

        chosen_inline_result (:obj:`ChosenInlineResult <pyrogram.ChosenInlineResult>`, *optional*):
            The result of an inline query that was chosen by a user and sent to their chat partner.
            Please see our documentation on the feedback collecting for details on how to enable these updates
            for your bot.

        callback_query (:obj:`CallbackQuery <pyrogram.CallbackQuery>`, *optional*):
            New incoming callback query.

        shipping_query (:obj:`ShippingQuery <pyrogram.ShippingQuery>`, *optional*):
            New incoming shipping query. Only for invoices with flexible price.

        pre_checkout_query (:obj:`PreCheckoutQuery <pyrogram.PreCheckoutQuery>`, *optional*):
            New incoming pre-checkout query. Contains full information about checkout.
    """

    ID = 0xb0700000

    def __init__(
            self,
            message=None,
            edited_message=None,
            deleted_messages=None,
            channel_post=None,
            edited_channel_post=None,
            deleted_channel_posts=None,
            inline_query=None,
            chosen_inline_result=None,
            callback_query=None,
            shipping_query=None,
            pre_checkout_query=None
    ):
        self.message = message
        self.edited_message = edited_message
        self.deleted_messages = deleted_messages
        self.channel_post = channel_post
        self.edited_channel_post = edited_channel_post
        self.deleted_channel_posts = deleted_channel_posts
        self.inline_query = inline_query
        self.chosen_inline_result = chosen_inline_result
        self.callback_query = callback_query
        self.shipping_query = shipping_query
        self.pre_checkout_query = pre_checkout_query
