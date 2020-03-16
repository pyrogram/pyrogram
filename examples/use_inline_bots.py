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

"""This example shows how to query an inline bot (as user)"""

from pyrogram import Client

# Create a new Client
app = Client("my_account")

with app:
    # Get bot results for "Fuzz Universe" from the inline bot @vid
    bot_results = app.get_inline_bot_results("vid", "Fuzz Universe")

    # Send the first result (bot_results.results[0]) to your own chat (Saved Messages)
    app.send_inline_bot_result("me", bot_results.query_id, bot_results.results[0].id)
