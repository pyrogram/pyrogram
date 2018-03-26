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

import sys

__copyright__ = "Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>".replace(
    "\xe8",
    "e" if sys.getfilesystemencoding() == "ascii" else "\xe8"
)
__license__ = "GNU Lesser General Public License v3 or later (LGPLv3+)"
__version__ = "0.6.4"

from .api.errors import Error
from .client import ChatAction
from .client import Client
from .client import ParseMode
from .client.input_media import InputMedia
from .client.input_phone_contact import InputPhoneContact
from .client import Emoji
from .api.types.pyrogram import *
