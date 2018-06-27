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

from pyrogram import Client, Emoji, Filters

"""This is the Welcome Bot in @PyrogramChat.

It uses the Emoji module to easily add emojis in your text messages and Filters
to make it only work for specific messages in a specific chat 
"""

app = Client("my_account")


@app.on_message(Filters.chat("PyrogramChat") & Filters.new_chat_members)
def welcome(client, message):
    # Build the new members list (with mentions) by using their first_name
    new_members = ", ".join([
        "[{}](tg://user?id={})".format(i.first_name, i.id)
        for i in message.new_chat_members
    ])

    # Build the welcome message by using an emoji and the list we built above
    text = "{} Welcome to [Pyrogram](https://docs.pyrogram.ml/)'s group chat {}!".format(
        Emoji.SPARKLES,
        new_members
    )

    # Send the welcome message
    client.send_message(
        message.chat.id, text,
        reply_to_message_id=message.message_id,
        disable_web_page_preview=True
    )


app.run()  # Automatically start() and idle()
