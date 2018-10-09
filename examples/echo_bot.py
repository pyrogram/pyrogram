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

from pyrogram import Client, Filters

"""This simple echo bot replies to every private text message.

It uses the @on_message decorator to register a MessageHandler and applies two filters on it:
Filters.text and Filters.private to make sure it will reply to private text messages only.
"""

app = Client("my_account")


@app.on_message(Filters.text & Filters.private)
def echo(client, message):
    message.reply(message.text, quote=True)


app.run()  # Automatically start() and idle()
