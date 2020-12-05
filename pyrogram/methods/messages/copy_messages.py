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

import logging
from functools import partial
from typing import Union, Iterable, List

from pyrogram import types
from pyrogram.scaffold import Scaffold

log = logging.getLogger(__name__)


class CopyMessage(Scaffold):
    async def copy_messages(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_id: Union[int, Iterable[int]],
        caption: str = None,
        parse_mode: Union[str, None] = object,
        caption_entities: List["types.MessageEntity"] = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        schedule_date: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None
    ) -> List["types.Message"]:
        """Copy messages of any kind.

        The method is analogous to the method :meth:`~Client.forward_messages`, but the copied message doesn't have a
        link to the original message.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            from_chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the source chat where the original message was sent.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                Message identifier in the chat specified in *from_chat_id*.

            caption (``string``, *optional*):
                New caption for media, 0-1024 characters after entities parsing.
                If not specified, the original caption is kept.
                Pass "" (empty string) to remove the caption.

            parse_mode (``str``, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.
                Pass "markdown" or "md" to enable Markdown-style parsing only.
                Pass "html" to enable HTML-style parsing only.
                Pass None to completely disable style parsing.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the new caption, which can be specified instead of __parse_mode__.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            schedule_date (``int``, *optional*):
                Date when the message will be automatically sent. Unix time.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the copied message is returned.

        Example:
            .. code-block:: python

                # Copy a message
                app.copy_messages("me", "pyrogram", 20)

        """
        message: types.Message = await self.get_messages(from_chat_id, message_id)

        if message.service:
            log.warning(f"Service messages cannot be copied. "
                        f"chat_id: {message.chat.id}, message_id: {message.message_id}")
        elif message.game and not await self.storage.is_bot():
            log.warning(f"Users cannot send messages with Game media type. "
                        f"chat_id: {message.chat.id}, message_id: {message.message_id}")
        elif message.text:
            return await self.send_message(
                chat_id,
                text=message.text,
                entities=message.entities,
                disable_web_page_preview=not message.web_page,
                disable_notification=disable_notification,
                schedule_date=schedule_date
            )
        elif message.media:
            send_media = partial(
                self.send_cached_media,
                chat_id=chat_id,
                disable_notification=disable_notification,
                reply_to_message_id=reply_to_message_id,
                schedule_date=schedule_date,
                reply_markup=reply_markup
            )

            if message.photo:
                file_id = message.photo.file_id
            elif message.audio:
                file_id = message.audio.file_id
            elif message.document:
                file_id = message.document.file_id
            elif message.video:
                file_id = message.video.file_id
            elif message.animation:
                file_id = message.animation.file_id
            elif message.voice:
                file_id = message.voice.file_id
            elif message.sticker:
                file_id = message.sticker.file_id
            elif message.video_note:
                file_id = message.video_note.file_id
            elif message.contact:
                return await self.send_contact(
                    chat_id,
                    phone_number=message.contact.phone_number,
                    first_name=message.contact.first_name,
                    last_name=message.contact.last_name,
                    vcard=message.contact.vcard,
                    disable_notification=disable_notification,
                    schedule_date=schedule_date
                )
            elif message.location:
                return await self.send_location(
                    chat_id,
                    latitude=message.location.latitude,
                    longitude=message.location.longitude,
                    disable_notification=disable_notification,
                    schedule_date=schedule_date
                )
            elif message.venue:
                return await self.send_venue(
                    chat_id,
                    latitude=message.venue.location.latitude,
                    longitude=message.venue.location.longitude,
                    title=message.venue.title,
                    address=message.venue.address,
                    foursquare_id=message.venue.foursquare_id,
                    foursquare_type=message.venue.foursquare_type,
                    disable_notification=disable_notification,
                    schedule_date=schedule_date
                )
            elif message.poll:
                return await self.send_poll(
                    chat_id,
                    question=message.poll.question,
                    options=[opt.text for opt in message.poll.options],
                    disable_notification=disable_notification,
                    schedule_date=schedule_date
                )
            elif message.game:
                return await self.send_game(
                    chat_id,
                    game_short_name=message.game.short_name,
                    disable_notification=disable_notification
                )
            else:
                raise ValueError("Unknown media type")

            if message.sticker or message.video_note:  # Sticker and VideoNote should have no caption
                return await send_media(file_id=file_id)
            else:
                return await send_media(
                    file_id=file_id,
                    caption=caption if caption is not None else message.caption,
                    parse_mode=parse_mode,
                    caption_entities=caption_entities or message.caption_entities
                )
        else:
            raise ValueError("Can't copy this message")
