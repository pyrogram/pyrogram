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
from os import stat
from struct import unpack
from imghdr import what
from tempfile import NamedTemporaryFile
from urllib.request import urlretrieve

from pyrogram import raw
from pyrogram import types
from pyrogram.scaffold import Scaffold


class SendInvoice(Scaffold):
    async def send_invoice(
        self,
        chat_id: Union[int, str],
        title: str,
        description: str,
        invoice: "types.Invoice",
        payload: Union[str, bytes],
        provider: str,
        provider_data: str,
        start_param: str,
        photo: str = None
    ):
        """Send an invoice.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

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

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the sent inline result message is returned.

        Example:
            .. code-block:: python
                app.send_invoice(
                    chat_id=chat_id,
                    title="Magic Pen",
                    description="WOW! This pen is magic...",
                    invoice=Invoice(
                        currency="EUR",
                        prices=[
                            LabeledPrice(label="The pen", amount=1000),
                            LabeledPrice(label="Shipping", amount=500)
                        ],
                        shipping_address_requested=True
                    ),
                    payload="magicpen",
                    provider=provider_token,
                    provider_data=provider_data,
                    start_param="buypen"
                )
        """

        width = None
        height = None
        ext = None
        mime_type = None
        file_size = None

        if photo:
            def get_image_size_ext(filename: str):
                with open(filename, 'rb') as fhandle:
                    head = fhandle.read(24)
                    if len(head) != 24:
                        return
                    ext = what(None, head)
                    if ext == 'png':
                        check = unpack('>i', head[4:8])[0]
                        if check != 0x0d0a1a0a:
                            return
                        width, height = unpack('>ii', head[16:24])
                    elif ext == 'gif':
                        width, height = unpack('<HH', head[6:10])
                    elif ext == 'jpeg':
                        try:
                            fhandle.seek(0)
                            size = 2
                            ftype = 0
                            while not 0xc0 <= ftype <= 0xcf or ftype in (0xc4, 0xc8, 0xcc):
                                fhandle.seek(size, 1)
                                byte = fhandle.read(1)
                                while ord(byte) == 0xff:
                                    byte = fhandle.read(1)
                                ftype = ord(byte)
                                size = unpack('>H', fhandle.read(2))[0] - 2
                            fhandle.seek(1, 1)
                            height, width = unpack('>HH', fhandle.read(4))
                        except Exception:
                            return
                    else:
                        return

                    return width, height, f".{ext}"


            tf = NamedTemporaryFile()
            urlretrieve(photo, tf.name)

            x = get_image_size_ext(tf.name)
            if x:
                width, height, ext = x
                mime_type = self.extensions_to_mime_types.get(ext)
                file_size = stat(tf.name).st_size

        r = await self.send(
            raw.functions.messages.SendMedia(
                peer=await self.resolve_peer(chat_id),
                media=types.InputMediaInvoice(
                    title=title,
                    description=description,
                    photo=types.InputWebDocument(
                        url=photo,
                        file_size=file_size,
                        mime_type=mime_type,
                        attributes=[raw.types.DocumentAttributeImageSize(
                            w=width, h=height
                        )]
                    ) if photo else None,
                    invoice=invoice,
                    payload=payload,
                    provider=provider,
                    provider_data=provider_data,
                    start_param=start_param
                ).write(),
                message="",
                random_id=self.rnd_id()
            )
        )

        for i in r.updates:
            if isinstance(i, (raw.types.UpdateNewMessage, raw.types.UpdateNewChannelMessage)):
                return await types.Message._parse(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats}
                )
