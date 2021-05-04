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

from typing import List

import pyrogram
from pyrogram import raw
from pyrogram import types
from ..object import Object


class Invoice(Object):
    """An invoice.

    Parameters:
        currency (``str``):
            Three-letter ISO 4217 currency code

        prices (List of List of :obj:`~pyrogram.types.LabeledPrice`):
            Price breakdown, a list of components (e.g. product price, tax, discount, delivery cost, delivery tax, bonus, etc.)

        test (``bool``):
            True if the invoice is a test one. False otherwise.

        flexible (``bool``):
            True if the final price depends on the shipping method. False otherwise.

        name_requested (``bool``):
            True if the order requires the user's full name. False otherwise.

        phone_requested (``bool``):
            True if the order requires the user's phone. False otherwise.

        email_requested (``bool``):
            True if the order requires the user's email. False otherwise.

        shipping_address_requested (``bool``):
            True if the order requires the user's shipping address. False otherwise.

        phone_to_provider (``bool``):
            True if user's phone number should be sent to provider. False otherwise.

        email_to_provider (``bool``):
            True if user's email should be sent to provider. False otherwise.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        currency: str,
        prices: List["pyrogram.types.LabeledPrice"],
        test: bool = None,
        flexible: bool = None,
        name_requested: bool = None,
        phone_requested: bool = None,
        email_requested: bool = None,
        shipping_address_requested: bool = None,
        phone_to_provider: bool = None,
        email_to_provider: bool = None
    ):
        super().__init__(client)

        self.currency = currency
        self.prices = prices
        self.test = test
        self.flexible = flexible
        self.name_requested = name_requested
        self.phone_requested = phone_requested
        self.email_requested = email_requested
        self.shipping_address_requested = shipping_address_requested
        self.phone_to_provider = phone_to_provider
        self.email_to_provider = email_to_provider

    @staticmethod
    def _parse(client, invoice: "raw.types.Invoice") -> "Invoice":
        if isinstance(invoice, raw.types.Invoice):
            return Invoice(
                currency=invoice.currency,
                prices=[types.LabeledPrice._parse(i) for i in invoice.prices],
                test=invoice.test,
                flexible=invoice.flexible,
                name_requested=invoice.name_requested,
                phone_requested=invoice.phone_requested,
                email_requested=invoice.email_requested,
                shipping_address_requested=invoice.shipping_address_requested,
                phone_to_provider=invoice.phone_to_provider,
                email_to_provider=invoice.email_to_provider,
                client=client
            )

    def write(self):
        return raw.types.Invoice(
            currency=self.currency,
            prices=[i.write() for i in self.prices],
            test=self.test,
            name_requested=self.name_requested,
            phone_requested=self.phone_requested,
            email_requested=self.email_requested,
            shipping_address_requested=self.shipping_address_requested,
            flexible=self.flexible,
            phone_to_provider=self.phone_to_provider,
            email_to_provider=self.email_to_provider
        )
