#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2020 Dan <https://github.com/delivrance>
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

from typing import Union

import pyrogram
from pyrogram import raw
from pyrogram import types
from ..object import Object


class MediaInvoice(Object):
    """Generated invoice of a bot payment

    Parameters:
        title (``str``):
            Product name, 1-32 characters.

        description (``str``):
            Product description, 1-255 characters.

        photo (List of :obj:`~pyrogram.types.WebDocument`):
            Photo to do

        test (``bool``):
            True if the invoice is a test one. False otherwise.

        currency (``str``):
            Three-letter ISO 4217 currency code

        total_amount (``int``):
            Sum of the prices of the product in the smallest units of the currency.

        shipping_address_requested (``bool``):
            True if the order requires the user's shipping address. False otherwise.

        start_param (``str``):
            Unique bot deep-linking parameter that can be used to generate this invoice.

        receipt_msg_id (``int``, *optional*):
            Message ID of receipt
    """
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        title: str = None,
        description: str = None,
        photo: "raw.types.WebDocument" = None,
        test: bool = None,
        currency: str = None,
        total_amount: int = None,
        shipping_address_requested: bool = None,
        start_param: str = None,
        receipt_msg_id: int = None
    ):
        super().__init__(client)

        self.title = title
        self.description = description
        self.photo = photo
        self.test = test
        self.currency = currency
        self.total_amount = total_amount
        self.shipping_address_requested = shipping_address_requested
        self.start_param = start_param
        self.receipt_msg_id = receipt_msg_id


    @staticmethod
    def _parse(client, media_invoice: "raw.types.MessageMediaInvoice") -> "MediaInvoice":
        if isinstance(media_invoice, raw.types.MessageMediaInvoice):
            return MediaInvoice(
                title=media_invoice.title,
                description=media_invoice.description,
                photo=types.WebDocument._parse(client, media_invoice.photo),
                test=media_invoice.test,
                currency=media_invoice.currency,
                total_amount=media_invoice.total_amount,
                shipping_address_requested=media_invoice.shipping_address_requested,
                start_param=media_invoice.start_param,
                receipt_msg_id=media_invoice.receipt_msg_id,
                client=client
            )
