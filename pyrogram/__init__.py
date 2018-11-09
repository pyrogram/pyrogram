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

import sys

__copyright__ = "Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>".replace(
    "\xe8",
    "e" if sys.getfilesystemencoding() != "utf-8" else "\xe8"
)
__license__ = "GNU Lesser General Public License v3 or later (LGPLv3+)"
__version__ = "0.9.2.dev1"

from .api.errors import Error
from .client.types import (
    Audio, Chat, ChatMember, ChatMembers, ChatPhoto, Contact, Document, InputMediaPhoto,
    InputMediaVideo, InputMediaDocument, InputMediaAudio, InputMediaAnimation, InputPhoneContact,
    Location, Message, MessageEntity, Dialog, Dialogs, Photo, PhotoSize, Sticker, Update, User, UserStatus,
    UserProfilePhotos, Venue, Animation, Video, VideoNote, Voice, CallbackQuery, Messages, ForceReply,
    InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove,
    InlineQuery, InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent, InlineQueryResultCachedAudio
)
from .client import (
    Client, ChatAction, ParseMode, Emoji,
    MessageHandler, DeletedMessagesHandler, CallbackQueryHandler,
    RawUpdateHandler, DisconnectHandler, UserStatusHandler, Filters
)
