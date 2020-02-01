# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2020 Dan <https://github.com/delivrance>
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

"""This example will show you how to send normal and inline keyboards (as bot).

You must log-in as a regular bot in order to send keyboards (use the token from @BotFather).
Any attempt in sending keyboards with a user account will be simply ignored by the server.

send_message() is used as example, but a keyboard can be sent with any other send_* methods,
like send_audio(), send_document(), send_location(), etc...
"""

from pyrogram import Client, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

# Create a client using your bot token
app = Client("my_bot", bot_token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")

with app:
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
                    InlineKeyboardButton(  # Generates a callback query when pressed
                        "Button",
                        callback_data=b"data"  # Note how callback_data must be bytes
                    ),
                    InlineKeyboardButton(  # Opens a web URL
                        "URL",
                        url="https://docs.pyrogram.org"
                    ),
                ],
                [  # Second row
                    InlineKeyboardButton(  # Opens the inline interface
                        "Choose chat",
                        switch_inline_query="pyrogram"
                    ),
                    InlineKeyboardButton(  # Opens the inline interface in the current chat
                        "Inline here",
                        switch_inline_query_current_chat="pyrogram"
                    )
                ]
            ]
        )
    )
