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

from .block_user import BlockUser
from .check_username import CheckUsername
from .delete_profile_photos import DeleteProfilePhotos
from .get_chat_photos import GetChatPhotos
from .get_chat_photos_count import GetChatPhotosCount
from .get_common_chats import GetCommonChats
from .get_default_emoji_statuses import GetDefaultEmojiStatuses
from .get_me import GetMe
from .get_users import GetUsers
from .set_emoji_status import SetEmojiStatus
from .set_profile_photo import SetProfilePhoto
from .set_username import SetUsername
from .unblock_user import UnblockUser
from .update_birthday import UpdateBirthday
from .update_personal_channel import UpdatePersonalChannel
from .update_profile import UpdateProfile
from .update_status import UpdateStatus


class Users(
    BlockUser,
    CheckUsername,
    GetCommonChats,
    GetChatPhotos,
    SetProfilePhoto,
    DeleteProfilePhotos,
    GetUsers,
    GetMe,
    SetUsername,
    GetChatPhotosCount,
    UnblockUser,
    UpdateBirthday,
    UpdatePersonalChannel,
    UpdateProfile,
    UpdateStatus,
    GetDefaultEmojiStatuses,
    SetEmojiStatus
):
    pass
