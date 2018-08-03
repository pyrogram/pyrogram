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

import os

from pyrogram.api import functions, types
from pyrogram.client.ext import BaseClient, utils
from pyrogram.client.types import (
    InputMediaPhoto
)


class EditMessageMedia(BaseClient):
    def edit_message_media(self,
                           chat_id: int or str,
                           message_id: int,
                           media,
                           reply_markup=None):
        style = self.html if media.parse_mode.lower() == "html" else self.markdown
        caption = media.caption

        if isinstance(media, InputMediaPhoto):
            if os.path.exists(media.media):
                media = self.send(
                    functions.messages.UploadMedia(
                        peer=self.resolve_peer(chat_id),
                        media=types.InputMediaUploadedPhoto(
                            file=self.save_file(media.media)
                        )
                    )
                )

                media = types.InputMediaPhoto(
                    id=types.InputPhoto(
                        id=media.photo.id,
                        access_hash=media.photo.access_hash
                    )
                )
            elif media.media.startswith("http"):
                media = types.InputMediaPhotoExternal(
                    url=media.media
                )

        r = self.send(
            functions.messages.EditMessage(
                peer=self.resolve_peer(chat_id),
                id=message_id,
                reply_markup=reply_markup.write() if reply_markup else None,
                media=media,
                **style.parse(caption)
            )
        )

        for i in r.updates:
            if isinstance(i, (types.UpdateEditMessage, types.UpdateEditChannelMessage)):
                return utils.parse_messages(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats}
                )
