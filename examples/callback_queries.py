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

"""This example shows how to handle callback queries, i.e.: queries coming from inline button presses.

It uses the @on_callback_query decorator to register a CallbackQueryHandler.
"""

from pyrogram import Client

app = Client("my_bot", bot_token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")


@app.on_callback_query()
def answer(client, callback_query):
    callback_query.answer("Button contains: '{}'".format(callback_query.data), show_alert=True)


app.run()  # Automatically start() and idle()
