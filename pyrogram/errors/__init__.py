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

from .exceptions import *
from .rpc_error import UnknownError


class SecurityError(Exception):
    """Generic security error."""

    @classmethod
    def check(cls, cond: bool):
        """Raises this exception if the condition is false"""
        if not cond:
            raise cls


class SecurityCheckMismatch(SecurityError):
    """Raised when a security check mismatch occurs."""

    def __init__(self):
        super().__init__("A security check mismatch has occurred.")


class CDNFileHashMismatch(SecurityError):
    """Raised when a CDN file hash mismatch occurs."""

    def __init__(self):
        super().__init__("A CDN file hash mismatch has occurred.")
