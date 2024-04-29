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

import os
from typing import Union, BinaryIO, Callable

import pyrogram
from pyrogram import raw, types, utils, StopTransmission
from pyrogram.errors import FilePartMissing

class EditStoryMedia:
    async def edit_story_media(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        story_id: int,
        media: Union[str, BinaryIO] = None,
        duration: int = 0,
        width: int = 0,
        height: int = 0,
        thumb: Union[str, BinaryIO] = None,
        supports_streaming: bool = True,
        file_name: str = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "types.Story":
        """Edit story media.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".

            story_id (``int``):
                Story identifier in the chat specified in chat_id.

            media (``str`` | ``BinaryIO``, *optional*):
                Video or photo to send.
                Pass a file_id as string to send a animation that exists on the Telegram servers,
                pass a file path as string to upload a new animation that exists on your local machine, or
                pass a binary file-like object with its attribute ".name" set for in-memory uploads.

            duration (``int``, *optional*):
                Duration of sent video in seconds.

            width (``int``, *optional*):
                Video width.

            height (``int``, *optional*):
                Video height.

            thumb (``str`` | ``BinaryIO``, *optional*):
                Thumbnail of the video sent.
                The thumbnail should be in JPEG format and less than 200 KB in size.
                A thumbnail's width and height should not exceed 320 pixels.
                Thumbnails can't be reused and can be only uploaded as a new file.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Returns:
            :obj:`~pyrogram.types.Story`: On success, the edited story is returned.

        Example:
            .. code-block:: python

                # Replace the current media with a local photo
                await app.edit_story_media(chat_id, story_id, "new_photo.jpg")

                # Replace the current media with a local video
                await app.edit_story_media(chat_id, story_id, "new_video.mp4")
        """
        # TODO: media_areas

        try:
            if isinstance(media, str):
                if os.path.isfile(media):
                    thumb = await self.save_file(thumb)
                    file = await self.save_file(media, progress=progress, progress_args=progress_args)
                    mime_type = self.guess_mime_type(file.name)
                    if mime_type == "video/mp4":
                        media = raw.types.InputMediaUploadedDocument(
                            mime_type=mime_type,
                            file=file,
                            thumb=thumb,
                            attributes=[
                                raw.types.DocumentAttributeVideo(
                                    duration=duration,
                                    w=width,
                                    h=height,
                                ),
                                raw.types.DocumentAttributeFilename(file_name=file_name or os.path.basename(media))
                            ]
                        )
                    else:
                        media = raw.types.InputMediaUploadedPhoto(
                            file=file,
                        )
                else:
                    media = utils.get_input_media_from_file_id(media)
            else:
                thumb = await self.save_file(thumb)
                file = await self.save_file(media, progress=progress, progress_args=progress_args)
                mime_type = self.guess_mime_type(file.name)
                if mime_type == "video/mp4":
                    media = raw.types.InputMediaUploadedDocument(
                        mime_type=mime_type,
                        file=file,
                        thumb=thumb,
                        attributes=[
                            raw.types.DocumentAttributeVideo(
                                supports_streaming=supports_streaming or None,
                                duration=duration,
                                w=width,
                                h=height,
                            ),
                            raw.types.DocumentAttributeFilename(file_name=file_name or media.name)
                        ]
                    )
                else:
                    media = raw.types.InputMediaUploadedPhoto(
                        file=file,
                    )

            while True:
                try:
                    r = await self.invoke(
                        raw.functions.stories.EditStory(
                            peer=await self.resolve_peer(chat_id),
                            id=story_id,
                            media=media,
                        )
                    )
                except FilePartMissing as e:
                    await self.save_file(media, file_id=file.id, file_part=e.value)
                else:
                    for i in r.updates:
                        if isinstance(i, raw.types.UpdateStory):
                            return await types.Story._parse(
                                self,
                                i.story,
                                {i.id: i for i in r.users},
                                {i.id: i for i in r.chats},
                                i.peer
                            )
        except StopTransmission:
            return None
