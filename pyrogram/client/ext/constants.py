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


class Constants:
    # Text of the message to be sent, 1-4096 characters
    MAX_MESSAGE_LENGTH = 4096

    # Caption for the animation, audio, document, photo, video or voice, 0-1024 characters
    MAX_CAPTION_LENGTH = 1024

    # Ports currently supported for Webhooks: 443, 80, 88, 8443.
    SUPPORTED_WEBHOOK_PORTS = [443, 80, 88, 8443]

    # Use the Client.download_media() method. Please note that this will only work with files of up to 20 MB in size.
    # 5 MB max size for photos and 20 MB max for other types of content.
    MAX_FILESIZE_DOWNLOAD = int(20E6) # (20MB)

    # Bots can currently send files of any type of up to 50 MB in size, so yes, very large files won't work for now.
    # Sorry. This limit may be changed in the future.
    # 10 MB max size for photos, 50 MB for other files.
    MAX_FILESIZE_UPLOAD = int(50E6)  # (50MB)

    # When sending messages inside a particular chat, avoid sending more than one message per second.
    # We may allow short bursts that go over this limit, but eventually you'll begin receiving 429 errors.
    MAX_MESSAGES_PER_SECOND_PER_CHAT = 1

    # If you're sending bulk notifications to multiple users, the API will not allow more than 30 messages per second
    # or so. Consider spreading out notifications over large intervals of 8—12 hours for best results.
    MAX_MESSAGES_PER_SECOND = 30

    # Also note that your bot will not be able to send more than 20 messages per minute to the same group.
    MAX_MESSAGES_PER_MINUTE_PER_GROUP = 20

    # # Use the InlineQuery.answer() method. No more than 50 results per query are allowed.
    MAX_INLINE_QUERY_RESULTS = 50

    # Beyond this cap Telegram will simply ignore further formatting styles
    MAX_MESSAGE_ENTITIES = 100