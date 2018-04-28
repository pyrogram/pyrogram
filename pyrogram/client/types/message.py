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

from pyrogram.api.core import Object


class Message(Object):
    """This object represents a message.

    Attributes:
        ID: ``0xb0700003``

    Args:
        message_id (``int``):
            Unique message identifier inside this chat.
            
        client (:obj:`Client <pyrogram.Client>`, *optional*):
            The client instance this message is bound to.

        date (``int``, *optional*):
            Date the message was sent in Unix time.

        chat (:obj:`Chat <pyrogram.Chat>`, *optional*):
            Conversation the message belongs to.

        from_user (:obj:`User <pyrogram.User>`, *optional*):
            Sender, empty for messages sent to channels.

        forward_from (:obj:`User <pyrogram.User>`, *optional*):
            For forwarded messages, sender of the original message.

        forward_from_chat (:obj:`Chat <pyrogram.Chat>`, *optional*):
            For messages forwarded from channels, information about the original channel.

        forward_from_message_id (``int``, *optional*):
            For messages forwarded from channels, identifier of the original message in the channel.

        forward_signature (``str``, *optional*):
            For messages forwarded from channels, signature of the post author if present.

        forward_date (``int``, *optional*):
            For forwarded messages, date the original message was sent in Unix time.

        reply_to_message (:obj:`Message <pyrogram.Message>`, *optional*):
            For replies, the original message. Note that the Message object in this field will not contain
            further reply_to_message fields even if it itself is a reply.

        edit_date (``int``, *optional*):
            Date the message was last edited in Unix time.

        media_group_id (``str``, *optional*):
            The unique identifier of a media message group this message belongs to.

        author_signature (``str``, *optional*):
            Signature of the post author for messages in channels.

        text (``str``, *optional*):
            For text messages, the actual UTF-8 text of the message, 0-4096 characters.

        entities (List of :obj:`MessageEntity <pyrogram.MessageEntity>`, *optional*):
            For text messages, special entities like usernames, URLs, bot commands, etc. that appear in the text.

        caption_entities (List of :obj:`MessageEntity <pyrogram.MessageEntity>`, *optional*):
            For messages with a caption, special entities like usernames, URLs, bot commands, etc. that appear
            in the caption.

        audio (:obj:`Audio <pyrogram.Audio>`, *optional*):
            Message is an audio file, information about the file.

        document (:obj:`Document <pyrogram.Document>`, *optional*):
            Message is a general file, information about the file.

        game (:obj:`Game <pyrogram.Game>`, *optional*):
            Message is a game, information about the game. More about games.

        photo (List of :obj:`PhotoSize <pyrogram.PhotoSize>`, *optional*):
            Message is a photo, available sizes of the photo.

        sticker (:obj:`Sticker <pyrogram.Sticker>`, *optional*):
            Message is a sticker, information about the sticker.

        video (:obj:`Video <pyrogram.Video>`, *optional*):
            Message is a video, information about the video.

        voice (:obj:`Voice <pyrogram.Voice>`, *optional*):
            Message is a voice message, information about the file.

        video_note (:obj:`VideoNote <pyrogram.VideoNote>`, *optional*):
            Message is a video note, information about the video message.

        caption (``str``, *optional*):
            Caption for the audio, document, photo, video or voice, 0-200 characters.

        contact (:obj:`Contact <pyrogram.Contact>`, *optional*):
            Message is a shared contact, information about the contact.

        location (:obj:`Location <pyrogram.Location>`, *optional*):
            Message is a shared location, information about the location.

        venue (:obj:`Venue <pyrogram.Venue>`, *optional*):
            Message is a venue, information about the venue.

        new_chat_members (List of :obj:`User <pyrogram.User>`, *optional*):
            New members that were added to the group or supergroup and information about them
            (the bot itself may be one of these members).

        left_chat_member (:obj:`User <pyrogram.User>`, *optional*):
            A member was removed from the group, information about them (this member may be the bot itself).

        new_chat_title (``str``, *optional*):
            A chat title was changed to this value.

        new_chat_photo (List of :obj:`PhotoSize <pyrogram.PhotoSize>`, *optional*):
            A chat photo was change to this value.

        delete_chat_photo (``bool``, *optional*):
            Service message: the chat photo was deleted.

        group_chat_created (``bool``, *optional*):
            Service message: the group has been created.

        supergroup_chat_created (``bool``, *optional*):
            Service message: the supergroup has been created.
            This field can't be received in a message coming through updates, because bot can't be a member of a
            supergroup when it is created. It can only be found in reply_to_message if someone replies to a very
            first message in a directly created supergroup.

        channel_chat_created (``bool``, *optional*):
            Service message: the channel has been created.
            This field can't be received in a message coming through updates, because bot can't be a member of a
            channel when it is created. It can only be found in reply_to_message if someone replies to a very
            first message in a channel.

        migrate_to_chat_id (``int``, *optional*):
            The group has been migrated to a supergroup with the specified identifier.
            This number may be greater than 32 bits and some programming languages may have difficulty/silent defects
            in interpreting it. But it is smaller than 52 bits, so a signed 64 bit integer or double-precision float
            type are safe for storing this identifier.

        migrate_from_chat_id (``int``, *optional*):
            The supergroup has been migrated from a group with the specified identifier.
            This number may be greater than 32 bits and some programming languages may have difficulty/silent defects
            in interpreting it. But it is smaller than 52 bits, so a signed 64 bit integer or double-precision float
            type are safe for storing this identifier.

        pinned_message (:obj:`Message <pyrogram.Message>`, *optional*):
            Specified message was pinned.
            Note that the Message object in this field will not contain further reply_to_message fields even if it
            is itself a reply.

        invoice (:obj:`Invoice <pyrogram.Invoice>`, *optional*):
            Message is an invoice for a payment, information about the invoice. More about payments.

        successful_payment (:obj:`SuccessfulPayment <pyrogram.SuccessfulPayment>`, *optional*):
            Message is a service message about a successful payment, information about the payment. More about payments.

        connected_website (``str``, *optional*):
            The domain name of the website on which the user has logged in. More about Telegram Login.

        views (``int``, *optional*):
            Channel post views.

        via_bot (:obj:`User <pyrogram.User>`):
            Via bot.
            
        outgoing (``bool``, *optional*):
            Whether the message is incoming or outgoing.
            Messages received from other chats are incoming (*outgoing* is False).
            Messages sent from yourself to other chats are outgoing (*outgoing* is True).
            An exception is made for your own personal chat; messages sent there will be incoming.

        matches (``list``, *optional*):
            A list containing all `Match Objects <https://docs.python.org/3/library/re.html#match-objects>`_ that match
            the text of this message. Only applicable when using :obj:`Filters.regex <pyrogram.Filters.regex>`.

        command (``list``, *optional*):
            A list containing the command and its arguments, if any.
            E.g.: "/start 1 2 3" would produce ["start", "1", "2", "3"].
            Only applicable when using :obj:`Filters.command <pyrogram.Filters.command>`.
    """

    # TODO: Document missing arguments

    ID = 0xb0700003

    def __init__(
            self,
            message_id: int,
            client=None,
            date: int = None,
            chat=None,
            from_user=None,
            forward_from=None,
            forward_from_chat=None,
            forward_from_message_id: int = None,
            forward_signature: str = None,
            forward_date: int = None,
            reply_to_message=None,
            edit_date: int = None,
            media_group_id: str = None,
            author_signature: str = None,
            text: str = None,
            entities: list = None,
            caption_entities: list = None,
            audio=None,
            document=None,
            game=None,
            photo=None,
            sticker=None,
            video=None,
            voice=None,
            video_note=None,
            caption: str = None,
            contact=None,
            location=None,
            venue=None,
            new_chat_members: list = None,
            left_chat_member=None,
            new_chat_title: str = None,
            new_chat_photo=None,
            delete_chat_photo: bool = None,
            group_chat_created: bool = None,
            supergroup_chat_created: bool = None,
            channel_chat_created: bool = None,
            migrate_to_chat_id: int = None,
            migrate_from_chat_id: int = None,
            pinned_message=None,
            invoice=None,
            successful_payment=None,
            connected_website=None,
            views: int = None,
            via_bot=None,
            outgoing: bool = None,
            matches: list = None,
            command: list = None,
            reply_markup=None,
    ):
        self.message_id = message_id  # int
        self.client = client
        self.date = date  # int
        self.chat = chat  # Chat
        self.from_user = from_user  # flags.0?User
        self.forward_from = forward_from  # flags.1?User
        self.forward_from_chat = forward_from_chat  # flags.2?Chat
        self.forward_from_message_id = forward_from_message_id  # flags.3?int
        self.forward_signature = forward_signature  # flags.4?string
        self.forward_date = forward_date  # flags.5?int
        self.reply_to_message = reply_to_message  # flags.6?Message
        self.edit_date = edit_date  # flags.7?int
        self.media_group_id = media_group_id  # flags.8?string
        self.author_signature = author_signature  # flags.9?string
        self.text = text  # flags.10?string
        self.entities = entities  # flags.11?Vector<MessageEntity>
        self.caption_entities = caption_entities  # flags.12?Vector<MessageEntity>
        self.audio = audio  # flags.13?Audio
        self.document = document  # flags.14?Document
        self.game = game  # flags.15?Game
        self.photo = photo  # flags.16?Vector<PhotoSize>
        self.sticker = sticker  # flags.17?Sticker
        self.video = video  # flags.18?Video
        self.voice = voice  # flags.19?Voice
        self.video_note = video_note  # flags.20?VideoNote
        self.caption = caption  # flags.21?string
        self.contact = contact  # flags.22?Contact
        self.location = location  # flags.23?Location
        self.venue = venue  # flags.24?Venue
        self.new_chat_members = new_chat_members  # flags.25?Vector<User>
        self.left_chat_member = left_chat_member  # flags.26?User
        self.new_chat_title = new_chat_title  # flags.27?string
        self.new_chat_photo = new_chat_photo  # flags.28?Vector<PhotoSize>
        self.delete_chat_photo = delete_chat_photo  # flags.29?true
        self.group_chat_created = group_chat_created  # flags.30?true
        self.supergroup_chat_created = supergroup_chat_created  # flags.31?true
        self.channel_chat_created = channel_chat_created  # flags.32?true
        self.migrate_to_chat_id = migrate_to_chat_id  # flags.33?int
        self.migrate_from_chat_id = migrate_from_chat_id  # flags.34?int
        self.pinned_message = pinned_message  # flags.35?Message
        self.invoice = invoice  # flags.36?Invoice
        self.successful_payment = successful_payment  # flags.37?SuccessfulPayment
        self.connected_website = connected_website  # flags.38?string
        self.views = views  # flags.39?int
        self.via_bot = via_bot  # flags.40?User
        self.outgoing = outgoing
        self.matches = matches
        self.command = command,
        self.reply_markup = reply_markup
