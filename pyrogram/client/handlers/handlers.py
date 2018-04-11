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

from .handler import Handler


class MessageHandler(Handler):
    """The Message handler class. It is used to handle text, media and service messages coming from
    any chat (private, group, channel).

    Args:
        callback (``callable``):
            Pass a function that will be called when a new Message arrives. It takes *(client, message)*
            as positional arguments (look at the section below for a detailed description).

        filters (:obj:`Filters <pyrogram.Filters>`):
            Pass one or more filters to allow only a subset of messages to be passed
            in your callback function.

    Other parameters:
        client (:obj:`Client <pyrogram.Client>`):
            The Client itself, useful when you want to call other API methods inside the message handler.

        message (:obj:`Message <pyrogram.api.types.pyrogram.Message>`):
            The received message.
    """

    def __init__(self, callback: callable, filters=None):
        super().__init__(callback, filters)

    def check(self, message):
        return (
            self.filters(message)
            if self.filters
            else True
        )


class RawUpdateHandler(Handler):
    """The Raw Update handler class. It is used to handle raw updates.

    Args:
        callback (``callable``):
            A function that will be called when a new update is received from the server. It takes
            *(client, update, users, chats)* as positional arguments (look at the section below for
            a detailed description).

    Other Parameters:
        client (:class:`Client <pyrogram.Client>`):
            The Client itself, useful when you want to call other API methods inside the update handler.

        update (``Update``):
            The received update, which can be one of the many single Updates listed in the *updates*
            field you see in the :obj:`Update <pyrogram.api.types.Update>` type.

        users (``dict``):
            Dictionary of all :obj:`User <pyrogram.api.types.User>` mentioned in the update.
            You can access extra info about the user (such as *first_name*, *last_name*, etc...) by using
            the IDs you find in the *update* argument (e.g.: *users[1768841572]*).

        chats (``dict``):
            Dictionary of all :obj:`Chat <pyrogram.api.types.Chat>` and
            :obj:`Channel <pyrogram.api.types.Channel>` mentioned in the update.
            You can access extra info about the chat (such as *title*, *participants_count*, etc...)
            by using the IDs you find in the *update* argument (e.g.: *chats[1701277281]*).

    Note:
        The following Empty or Forbidden types may exist inside the *users* and *chats* dictionaries.
        They mean you have been blocked by the user or banned from the group/channel.

        - :obj:`UserEmpty <pyrogram.api.types.UserEmpty>`
        - :obj:`ChatEmpty <pyrogram.api.types.ChatEmpty>`
        - :obj:`ChatForbidden <pyrogram.api.types.ChatForbidden>`
        - :obj:`ChannelForbidden <pyrogram.api.types.ChannelForbidden>`
    """

    def __init__(self, callback: callable):
        super().__init__(callback)
