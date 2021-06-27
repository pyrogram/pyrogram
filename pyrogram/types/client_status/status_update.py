#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2021 Dan <https://github.com/delivrance>
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

from enum import Enum
from typing import Optional

import pyrogram
from ..object import Object
from ..update import Update

class StatusUpdateRaw(Enum):
    UNKNOWN = 0
    READY = 1
    STOPPING = 2
    CONNECTED = 3
    DISCONNECTED = 4

    def _packet(self):
        return self, None, None


class StatusUpdate(Object, Update):
    """A client status update.

    Parameters:
        connected (``bool``):
            True if the client successfully connected, False if client got disconnected.

        ready (``bool``):
            Will be set True once the client is ready to process user-defined handlers.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client",
        type : StatusUpdateRaw = StatusUpdateRaw.UNKNOWN,
        ready : Optional[bool] = None,
        connected : Optional[bool] = None,
    ):
        super().__init__(client)

        self.type = type
        self.ready = ready
        self.connected = connected

    @staticmethod
    def _parse(client, event_raw:StatusUpdateRaw) -> "StatusUpdate":
        if event_raw == StatusUpdateRaw.READY:
            return StatusUpdate(client, event_raw, ready=True)
        if event_raw == StatusUpdateRaw.STOPPING:
            return StatusUpdate(client, event_raw, ready=False)
        if event_raw == StatusUpdateRaw.CONNECTED:
            return StatusUpdate(client, event_raw, connected=True)
        if event_raw == StatusUpdateRaw.DISCONNECTED:
            return StatusUpdate(client, event_raw, connected=False)
        return StatusUpdate(client, event_raw)
