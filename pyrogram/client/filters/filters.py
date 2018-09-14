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

import re

from .filter import Filter
from ..types.bots import InlineKeyboardMarkup, ReplyKeyboardMarkup


def create(name: str, func: callable, **kwargs) -> type:
    """Use this method to create a Filter.

    Custom filters give you extra control over which updates are allowed or not to be processed by your handlers.

    Args:
        name (``str``):
            Your filter's name. Can be anything you like.

        func (``callable``):
            A function that accepts two arguments *(filter, update)* and returns a Boolean: True if the update should be
            handled, False otherwise.
            The "update" argument type will vary depending on which `Handler <Handlers.html>`_ is coming from.
            For example, in a :obj:`MessageHandler <pyrogram.MessageHandler>` the update type will be
            a :obj:`Message <pyrogram.Message>`; in a :obj:`CallbackQueryHandler <pyrogram.CallbackQueryHandler>` the
            update type will be a :obj:`CallbackQuery <pyrogram.CallbackQuery>`. Your function body can then access the
            incoming update and decide whether to allow it or not.

        **kwargs (``any``, *optional*):
            Any keyword argument you would like to pass. Useful for custom filters that accept parameters (e.g.:
            :meth:`Filters.command`, :meth:`Filters.regex`).
    """
    # TODO: unpack kwargs using **kwargs into the dict itself. For Python 3.5+ only
    d = {"__call__": func}
    d.update(kwargs)

    return type(name, (Filter,), d)()


class Filters:
    """This class provides access to all library-defined Filters available in Pyrogram.

    The Filters listed here are intended to be used with the :obj:`MessageHandler <pyrogram.MessageHandler>` only.
    At the moment, if you want to filter updates coming from different `Handlers <Handlers.html>`_ you have to create
    your own filters with :meth:`Filters.create` and use them in the same way.
    """

    create = create

    bot = create("Bot", lambda _, m: bool(m.from_user and m.from_user.is_bot))
    """Filter messages coming from bots"""

    incoming = create("Incoming", lambda _, m: not m.outgoing)
    """Filter incoming messages."""

    outgoing = create("Outgoing", lambda _, m: m.outgoing)
    """Filter outgoing messages."""

    text = create("Text", lambda _, m: bool(m.text))
    """Filter text messages."""

    reply = create("Reply", lambda _, m: bool(m.reply_to_message))
    """Filter messages that are replies to other messages."""

    forwarded = create("Forwarded", lambda _, m: bool(m.forward_date))
    """Filter messages that are forwarded."""

    caption = create("Caption", lambda _, m: bool(m.caption))
    """Filter media messages that contain captions."""

    edited = create("Edited", lambda _, m: bool(m.edit_date))
    """Filter edited messages."""

    audio = create("Audio", lambda _, m: bool(m.audio))
    """Filter messages that contain :obj:`Audio <pyrogram.api.types.pyrogram.Audio>` objects."""

    document = create("Document", lambda _, m: bool(m.document))
    """Filter messages that contain :obj:`Document <pyrogram.api.types.pyrogram.Document>` objects."""

    photo = create("Photo", lambda _, m: bool(m.photo))
    """Filter messages that contain :obj:`Photo <pyrogram.api.types.pyrogram.PhotoSize>` objects."""

    sticker = create("Sticker", lambda _, m: bool(m.sticker))
    """Filter messages that contain :obj:`Sticker <pyrogram.api.types.pyrogram.Sticker>` objects."""

    animation = create("GIF", lambda _, m: bool(m.animation))
    """Filter messages that contain :obj:`Animation <pyrogram.api.types.pyrogram.Animation>` objects."""

    video = create("Video", lambda _, m: bool(m.video))
    """Filter messages that contain :obj:`Video <pyrogram.api.types.pyrogram.Video>` objects."""

    voice = create("Voice", lambda _, m: bool(m.voice))
    """Filter messages that contain :obj:`Voice <pyrogram.api.types.pyrogram.Voice>` note objects."""

    video_note = create("Voice", lambda _, m: bool(m.video_note))
    """Filter messages that contain :obj:`VideoNote <pyrogram.api.types.pyrogram.VideoNote>` objects."""

    contact = create("Contact", lambda _, m: bool(m.contact))
    """Filter messages that contain :obj:`Contact <pyrogram.api.types.pyrogram.Contact>` objects."""

    location = create("Location", lambda _, m: bool(m.location))
    """Filter messages that contain :obj:`Location <pyrogram.api.types.pyrogram.Location>` objects."""

    venue = create("Venue", lambda _, m: bool(m.venue))
    """Filter messages that contain :obj:`Venue <pyrogram.api.types.pyrogram.Venue>` objects."""

    private = create("Private", lambda _, m: bool(m.chat and m.chat.type == "private"))
    """Filter messages sent in private chats."""

    group = create("Group", lambda _, m: bool(m.chat and m.chat.type in {"group", "supergroup"}))
    """Filter messages sent in group or supergroup chats."""

    channel = create("Channel", lambda _, m: bool(m.chat and m.chat.type == "channel"))
    """Filter messages sent in channels."""

    new_chat_members = create("NewChatMembers", lambda _, m: bool(m.new_chat_members))
    """Filter service messages for new chat members."""

    left_chat_member = create("LeftChatMember", lambda _, m: bool(m.left_chat_member))
    """Filter service messages for members that left the chat."""

    new_chat_title = create("NewChatTitle", lambda _, m: bool(m.new_chat_title))
    """Filter service messages for new chat titles."""

    new_chat_photo = create("NewChatPhoto", lambda _, m: bool(m.new_chat_photo))
    """Filter service messages for new chat photos."""

    delete_chat_photo = create("DeleteChatPhoto", lambda _, m: bool(m.delete_chat_photo))
    """Filter service messages for deleted photos."""

    group_chat_created = create("GroupChatCreated", lambda _, m: bool(m.group_chat_created))
    """Filter service messages for group chat creations."""

    supergroup_chat_created = create("SupergroupChatCreated", lambda _, m: bool(m.supergroup_chat_created))
    """Filter service messages for supergroup chat creations."""

    channel_chat_created = create("ChannelChatCreated", lambda _, m: bool(m.channel_chat_created))
    """Filter service messages for channel chat creations."""

    migrate_to_chat_id = create("MigrateToChatId", lambda _, m: bool(m.migrate_to_chat_id))
    """Filter service messages that contain migrate_to_chat_id."""

    migrate_from_chat_id = create("MigrateFromChatId", lambda _, m: bool(m.migrate_from_chat_id))
    """Filter service messages that contain migrate_from_chat_id."""

    pinned_message = create("PinnedMessage", lambda _, m: bool(m.pinned_message))
    """Filter service messages for pinned messages."""

    reply_keyboard = create("ReplyKeyboard", lambda _, m: isinstance(m.reply_markup, ReplyKeyboardMarkup))
    """Filter messages containing reply keyboard markups"""

    inline_keyboard = create("InlineKeyboard", lambda _, m: isinstance(m.reply_markup, InlineKeyboardMarkup))
    """Filter messages containing inline keyboard markups"""

    @staticmethod
    def command(command: str or list,
                prefix: str = "/",
                separator: str = " ",
                case_sensitive: bool = False):
        """Filter commands, i.e.: text messages starting with "/" or any other custom prefix.

        Args:
            command (``str`` | ``list``):
                The command or list of commands as string the filter should look for.
                Examples: "start", ["start", "help", "settings"]. When a message text containing
                a command arrives, the command itself and its arguments will be stored in the *command*
                field of the :class:`Message <pyrogram.Message>`.

            prefix (``str``, *optional*):
                The command prefix. Defaults to "/" (slash).
                Examples: /start, .help, !settings.

            separator (``str``, *optional*):
                The command arguments separator. Defaults to " " (white space).
                Examples: /start first second, /start-first-second, /start.first.second.

            case_sensitive (``bool``, *optional*):
                Pass True if you want your command(s) to be case sensitive. Defaults to False.
                Examples: when True, command="Start" would trigger /Start but not /start.
        """

        def f(_, m):
            if m.text and m.text.startswith(_.p):
                t = m.text.split(_.s)
                c, a = t[0][len(_.p):], t[1:]
                c = c if _.cs else c.lower()
                m.command = ([c] + a) if c in _.c else None

            return bool(m.command)

        return create(
            "Command",
            f,
            c={command if case_sensitive
               else command.lower()}
            if not isinstance(command, list)
            else {c if case_sensitive
                  else c.lower()
                  for c in command},
            p=prefix,
            s=separator,
            cs=case_sensitive
        )

    @staticmethod
    def regex(pattern, flags: int = 0):
        """Filter messages that match a given RegEx pattern.

        Args:
            pattern (``str``):
                The RegEx pattern as string, it will be applied to the text of a message. When a pattern matches,
                all the `Match Objects <https://docs.python.org/3/library/re.html#match-objects>`_
                are stored in the *matches* field of the :class:`Message <pyrogram.Message>` itself.

            flags (``int``, *optional*):
                RegEx flags.
        """

        def f(_, m):
            m.matches = [i for i in _.p.finditer(m.text or "")]
            return bool(m.matches)

        return create("Regex", f, p=re.compile(pattern, flags))

    # noinspection PyPep8Naming
    class user(Filter, set):
        """Filter messages coming from one or more users.

        You can use `set bound methods <https://docs.python.org/3/library/stdtypes.html#set>`_ to manipulate the
        users container.

        Args:
            users (``int`` | ``str`` | ``list``):
                Pass one or more user ids/usernames to filter the users.
                Defaults to None (no users).
        """

        def __init__(self, users: int or str or list = None):
            users = [] if users is None else users if type(users) is list else [users]
            super().__init__(
                {i.lower().strip("@") if type(i) is str else i for i in users}
                if type(users) is list else
                {users.lower().strip("@") if type(users) is str else users}
            )

        def __call__(self, message):
            return bool(
                message.from_user
                and (message.from_user.id in self
                     or (message.from_user.username
                         and message.from_user.username.lower() in self))
            )

    # noinspection PyPep8Naming
    class chat(Filter, set):
        """Filter messages coming from one or more chats.

        You can use `set bound methods <https://docs.python.org/3/library/stdtypes.html#set>`_ to manipulate the
        chats container.

        Args:
            chats (``int`` | ``str`` | ``list``):
                Pass one or more chat ids/usernames to filter the chats.
                Defaults to None (no chats).
        """

        def __init__(self, chats: int or str or list = None):
            chats = [] if chats is None else chats if type(chats) is list else [chats]
            super().__init__(
                {i.lower().strip("@") if type(i) is str else i for i in chats}
                if type(chats) is list else
                {chats.lower().strip("@") if type(chats) is str else chats}
            )

        def __call__(self, message):
            return bool(
                message.chat
                and (message.chat.id in self
                     or (message.chat.username
                         and message.chat.username.lower() in self))
            )

    service = create(
        "Service",
        lambda _, m: bool(
            Filters.new_chat_members(m)
            or Filters.left_chat_member(m)
            or Filters.new_chat_title(m)
            or Filters.new_chat_photo(m)
            or Filters.delete_chat_photo(m)
            or Filters.group_chat_created(m)
            or Filters.supergroup_chat_created(m)
            or Filters.channel_chat_created(m)
            or Filters.migrate_to_chat_id(m)
            or Filters.migrate_from_chat_id(m)
            or Filters.pinned_message(m)
        )
    )
    """Filter all service messages."""

    media = create(
        "Media",
        lambda _, m: bool(
            Filters.audio(m)
            or Filters.document(m)
            or Filters.photo(m)
            or Filters.sticker(m)
            or Filters.video(m)
            or Filters.animation(m)
            or Filters.voice(m)
            or Filters.video_note(m)
            or Filters.contact(m)
            or Filters.location(m)
            or Filters.venue(m)
        )
    )
    """Filter all media messages."""
