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

import pyrogram


class Disconnect:
    async def disconnect(
        self: "pyrogram.Client",
    ):
        """Disconnect the client from Telegram servers.

        Raises:
            ConnectionError: In case you try to disconnect an already disconnected client or in case you try to
                disconnect a client that needs to be terminated first.
        """
        if not self.is_connected:
            raise ConnectionError("Client is already disconnected")

        if self.is_initialized:
            raise ConnectionError("Can't disconnect an initialized client")

        await self.session.stop()
        await self.storage.close()
        self.is_connected = False
