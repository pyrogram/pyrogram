# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2019 Dan Tès <https://github.com/delivrance>
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

import binascii
import struct
from typing import Union

import pyrogram
from pyrogram.api import functions, types
from pyrogram.errors import FileIdInvalid
from pyrogram.client.ext import BaseClient, utils


class SendCachedMedia(BaseClient):
    async def send_cached_media(
        self,
        chat_id: Union[int, str],
        file_id: str,
        caption: str = "",
        parse_mode: str = "",
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_markup: Union[
            "pyrogram.InlineKeyboardMarkup",
            "pyrogram.ReplyKeyboardMarkup",
            "pyrogram.ReplyKeyboardRemove",
            "pyrogram.ForceReply"
        ] = None
    ) -> Union["pyrogram.Message", None]:
        """Send any media stored on the Telegram servers using a file_id.

        This convenience method works with any valid file_id only.
        It does the same as calling the relevant method for sending media using a file_id, thus saving you from the
        hassle of using the correct method for the media the file_id is pointing to.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            file_id (``str``):
                Media to send.
                Pass a file_id as string to send a media that exists on the Telegram servers.

            caption (``bool``, *optional*):
                Media caption, 0-1024 characters.

            parse_mode (``str``, *optional*):
                Pass "markdown" or "html" if you want Telegram apps to show bold, italic, fixed-width text or inline
                URLs in your caption. Defaults to "markdown".

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            reply_markup (:obj:`InlineKeyboardMarkup` | :obj:`ReplyKeyboardMarkup` | :obj:`ReplyKeyboardRemove` | :obj:`ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            :obj:`Message`: On success, the sent media message is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        style = self.html if parse_mode.lower() == "html" else self.markdown

        try:
            decoded = utils.decode(file_id)
            fmt = "<iiqqqqi" if len(decoded) > 24 else "<iiqq"
            unpacked = struct.unpack(fmt, decoded)
        except (AssertionError, binascii.Error, struct.error):
            raise FileIdInvalid from None
        else:
            media_type = BaseClient.MEDIA_TYPE_ID.get(unpacked[0], None)

            if not media_type:
                raise FileIdInvalid("Unknown media type: {}".format(unpacked[0]))

            if media_type == "photo":
                media = types.InputMediaPhoto(
                    id=types.InputPhoto(
                        id=unpacked[2],
                        access_hash=unpacked[3],
                        file_reference=b""
                    )
                )
            else:
                media = types.InputMediaDocument(
                    id=types.InputDocument(
                        id=unpacked[2],
                        access_hash=unpacked[3],
                        file_reference=b""
                    )
                )

        r = await self.send(
            functions.messages.SendMedia(
                peer=await self.resolve_peer(chat_id),
                media=media,
                silent=disable_notification or None,
                reply_to_msg_id=reply_to_message_id,
                random_id=self.rnd_id(),
                reply_markup=reply_markup.write() if reply_markup else None,
                **await style.parse(caption)
            )
        )

        for i in r.updates:
            if isinstance(i, (types.UpdateNewMessage, types.UpdateNewChannelMessage)):
                return await pyrogram.Message._parse(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats}
                )
