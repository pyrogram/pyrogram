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

from .delete_photos import DeletePhotos
from .get_me import GetMe
from .get_user_dc import GetUserDC
from .get_user_photos import GetUserPhotos
from .get_user_photos_count import GetUserPhotosCount
from .get_users import GetUsers
from .set_photo import SetPhoto
from .update_username import UpdateUsername


class Users(
    GetUserPhotos,
    SetPhoto,
    DeletePhotos,
    GetUsers,
    GetMe,
    UpdateUsername,
    GetUserPhotosCount,
    GetUserDC
):
    pass
