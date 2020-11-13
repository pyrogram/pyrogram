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


class InputMediaInvoice(Object):
    """Invoice of a bot payment.


    Parameters:
        title (``str``):
            Product name, 1-32 characters.

        description (``str``):
            Product description, 1-255 characters.

        invoice (``:obj:`~pyrogram.types.Invoice``):
            The actual invoice.

        payload (``str`` | ``bytes``):
            Bot-defined invoice payload, 1-128 bytes.
            This will not be displayed to the user, use for your internal processes.

        provider (``str``):
            Payments provider token, obtained via @Botfather

        provider_data (``str``):
            JSON-encoded data about the invoice, which will be shared with the payment provider.
            A detailed description of required fields should be provided by the payment provider.

        start_param (``str``):
            Unique bot deep-linking parameter that can be used to generate this invoice

        photo  (``str``, *optional*):
            URL of the product photo for the invoice.
    """
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        title: str,
        description: str,
        invoice: "types.Invoice",
        payload: Union[str, bytes],
        provider: str,
        provider_data: str,
        start_param: str,
        photo: "types.InputWebDocument" = None
    ):
        super().__init__(client)

        self.title = title
        self.description = description
        self.invoice = invoice
        self.payload = payload
        self.provider = provider
        self.provider_data = provider_data
        self.start_param = start_param
        self.photo = photo

    def write(self):
        return raw.types.InputMediaInvoice(
            title=self.title,
            description=self.description,
            photo=self.photo.write() if self.photo else None,
            invoice=self.invoice.write(),
            payload=self.payload.encode() if isinstance(self.payload, str) else self.payload,
            provider=self.provider,
            provider_data=raw.types.DataJSON(data=self.provider_data),
            start_param=self.start_param
        )
