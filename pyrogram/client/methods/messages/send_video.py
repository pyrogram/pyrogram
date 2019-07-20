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
import io
import os
from typing import Union

import pyrogram
from pyrogram.api import functions, types
from pyrogram.client.ext import BaseClient, utils
from pyrogram.errors import FilePartMissing


class SendVideo(BaseClient):
    def send_video(
        self,
        chat_id: Union[int, str],
        video: Union[str, io.IOBase],
        video: str,
        file_ref: str = None,
        caption: str = "",
        parse_mode: Union[str, None] = object,
        duration: int = 0,
        width: int = 0,
        height: int = 0,
        thumb: str = None,
        file_name: str = None,
        supports_streaming: bool = True,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        schedule_date: int = None,
        reply_markup: Union[
            "pyrogram.InlineKeyboardMarkup",
            "pyrogram.ReplyKeyboardMarkup",
            "pyrogram.ReplyKeyboardRemove",
            "pyrogram.ForceReply"
        ] = None,
        progress: callable = None,
        progress_args: tuple = ()
    ) -> Union["pyrogram.Message", None]:
        """Send video files.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            video (``str``):
                Video to send.
                Pass a file_id as string to send a video that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a video from the Internet, or
                pass a file path as string to upload a new video that exists on your local machine.
                pass a readable file-like object with .name

            file_ref (``str``, *optional*):
                A valid file reference obtained by a recently fetched media message.
                To be used in combination with a file id in case a file reference is needed.

            caption (``str``, *optional*):
                Video caption, 0-1024 characters.

            parse_mode (``str``, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.
                Pass "markdown" or "md" to enable Markdown-style parsing only.
                Pass "html" to enable HTML-style parsing only.
                Pass None to completely disable style parsing.

            duration (``int``, *optional*):
                Duration of sent video in seconds.

            width (``int``, *optional*):
                Video width.

            height (``int``, *optional*):
                Video height.

            thumb (``str``, *optional*):
                Thumbnail of the video sent.
                The thumbnail should be in JPEG format and less than 200 KB in size.
                A thumbnail's width and height should not exceed 320 pixels.
                Thumbnails can't be reused and can be only uploaded as a new file.

            file_name (``str``, *optional*):
                File name of the video sent.
                Defaults to file's path basename.

            supports_streaming (``bool``, *optional*):
                Pass True, if the uploaded video is suitable for streaming.
                Defaults to True.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            schedule_date (``int``, *optional*):
                Date when the message will be automatically sent. Unix time.

            reply_markup (:obj:`InlineKeyboardMarkup` | :obj:`ReplyKeyboardMarkup` | :obj:`ReplyKeyboardRemove` | :obj:`ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the *progress_args* parameter.
                You can either keep *\*args* or add every single extra argument in your function signature.

        Returns:
            :obj:`Message` | ``None``: On success, the sent video message is returned, otherwise, in case the upload
            is deliberately stopped with :meth:`~Client.stop_transmission`, None is returned.

        Example:
            .. code-block:: python

                # Send video by uploading from local file
                app.send_video("me", "video.mp4")

                # Add caption to the video
                app.send_video("me", "video.mp4", caption="recording")

                # Keep track of the progress while uploading
                def progress(current, total):
                    print("{:.1f}%".format(current * 100 / total))

                app.send_video("me", "video.mp4", progress=progress)
        """
        file = None

        try:
            if isinstance(video, str):
                if os.path.exists(video):
                    thumb = None if thumb is None else self.save_file(thumb)
                    file = self.save_file(video, progress=progress, progress_args=progress_args)
                    media = types.InputMediaUploadedDocument(
                        mime_type=self.guess_mime_type(video) or "video/mp4",
                        file=file,
                        thumb=thumb,
                        attributes=[
                            types.DocumentAttributeVideo(
                                supports_streaming=supports_streaming or None,
                                duration=duration,
                                w=width,
                                h=height
                            ),
                            types.DocumentAttributeFilename(file_name=file_name or os.path.basename(video))
                        ]
                    )
                elif video.startswith("http"):
                    media = types.InputMediaDocumentExternal(
                        url=video
                    )
                else:
                    media = utils.get_input_media_from_file_id(video, file_ref, 4)
            elif hasattr(video, "read"):
                thumb = None if thumb is None else self.save_file(thumb)
                file = self.save_file(video, progress=progress, progress_args=progress_args)
                media = types.InputMediaUploadedDocument(
                    mime_type=self.guess_mime_type(video.name) or "video/mp4",
                    file=file,
                    thumb=thumb,
                    attributes=[
                        types.DocumentAttributeVideo(
                            supports_streaming=supports_streaming or None,
                            duration=duration,
                            w=width,
                            h=height
                        ),
                        types.DocumentAttributeFilename(file_name=video.name)
                    ]
                )

            while True:
                try:
                    r = self.send(
                        functions.messages.SendMedia(
                            peer=self.resolve_peer(chat_id),
                            media=media,
                            silent=disable_notification or None,
                            reply_to_msg_id=reply_to_message_id,
                            random_id=self.rnd_id(),
                            schedule_date=schedule_date,
                            reply_markup=reply_markup.write() if reply_markup else None,
                            **self.parser.parse(caption, parse_mode)
                        )
                    )
                except FilePartMissing as e:
                    self.save_file(video, file_id=file.id, file_part=e.x)
                else:
                    for i in r.updates:
                        if isinstance(
                            i,
                            (types.UpdateNewMessage, types.UpdateNewChannelMessage, types.UpdateNewScheduledMessage)
                        ):
                            return pyrogram.Message._parse(
                                self, i.message,
                                {i.id: i for i in r.users},
                                {i.id: i for i in r.chats},
                                is_scheduled=isinstance(i, types.UpdateNewScheduledMessage)
                            )
        except BaseClient.StopTransmission:
            return None
