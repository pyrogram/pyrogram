# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2019 Dan Tès <https://github.com/delivrance>
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

import sys

if sys.version_info[:3] in [(3, 5, 0), (3, 5, 1), (3, 5, 2)]:
    from .vendor import typing

    # Monkey patch the standard "typing" module because Python versions from 3.5.0 to 3.5.2 have a broken one.
    sys.modules["typing"] = typing

__version__ = "0.14.0-develop"
__license__ = "GNU Lesser General Public License v3 or later (LGPLv3+)"
__copyright__ = "Copyright (C) 2017-2019 Dan <https://github.com/delivrance>"

from .errors import RPCError
from .client import *
from .client.handlers import *
from .client.types import *
