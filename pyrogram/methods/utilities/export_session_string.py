#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from pyrogram.scaffold import Scaffold


class ExportSessionString(Scaffold):
    async def export_session_string(self):
        """Export the current authorized session as a serialized string.

        Session strings are useful for storing in-memory authorized sessions in a portable, serialized string.
        More detailed information about session strings can be found at the dedicated page of
        :doc:`Storage Engines <../../topics/storage-engines>`.

        Returns:
            ``str``: The session serialized into a printable, url-safe string.

        Example:
            .. code-block:: python

                from pyrogram import Client

                app = Client("my_account")

                with app:
                    print(app.export_session_string())
        """
        return await self.storage.export_session_string()
