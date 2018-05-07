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

from pyrogram import Client, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

"""This example will show you how to send normal and inline keyboards.

You must log-in as a regular bot in order to send keyboards (use the token from @BotFather).
Any attempt in sending keyboards with a user account will be simply ignored by the server.

send_message() is used as example, but a keyboard can be sent with any other send_* methods,
like send_audio(), send_document(), send_location(), etc...
"""

# Create a client using your bot token
app = Client("123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
app.start()

app.send_message(
    "haskell",  # Edit this
    "This is a ReplyKeyboardMarkup example",
    reply_markup=ReplyKeyboardMarkup(
        [
            ["A", "B", "C", "D"],  # First row
            ["E", "F", "G"],  # Second row
            ["H", "I"],  # Third row
            ["J"]  # Fourth row
        ],
        resize_keyboard=True  # Make the keyboard smaller
    )
)

app.send_message(
    "haskell",  # Edit this
    "This is a InlineKeyboardMarkup example",
    reply_markup=InlineKeyboardMarkup(
        [
            [  # First row
                # Generates a callback query when pressed
                InlineKeyboardButton("Button", callback_data="data"),
                # Opens a web URL
                InlineKeyboardButton("URL", url="https://docs.pyrogram.ml"),
            ],
            [  # Second row
                # Opens the inline interface of a bot in another chat with a pre-defined query
                InlineKeyboardButton("Choose chat", switch_inline_query="pyrogram"),
                # Same as the button above, but the inline interface is opened in the current chat
                InlineKeyboardButton("Inline here", switch_inline_query_current_chat="pyrogram"),
            ]
        ]
    )
)

app.stop()
