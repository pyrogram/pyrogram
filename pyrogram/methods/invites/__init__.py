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


from .delete_exported_chat_invite_link import DeleteExportedChatInviteLink
from .delete_revoked_exported_chat_invite_links import DeleteRevokedExportedChatInviteLinks
from .edit_exported_chat_invite_link import EditExportedChatInviteLink
from .export_chat_invite_link import ExportChatInviteLink
from .get_admins_with_invite_links import GetAdminsWithInviteLinks
from .get_chat_invite_link_importers import GetChatInviteLinkImporters
from .get_exported_chat_invite_links import GetExportedChatInviteLinks


class Invites(
    DeleteExportedChatInviteLink,
    DeleteRevokedExportedChatInviteLinks,
    EditExportedChatInviteLink,
    ExportChatInviteLink,
    GetAdminsWithInviteLinks,
    GetChatInviteLinkImporters,
    GetExportedChatInviteLinks,
):
    pass
