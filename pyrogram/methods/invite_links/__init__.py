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


from .create_chat_invite_link import CreateChatInviteLink
from .delete_chat_admin_invite_links import DeleteChatAdminInviteLinks
from .delete_chat_invite_link import DeleteChatInviteLink
from .edit_chat_invite_link import EditChatInviteLink
from .export_chat_invite_link import ExportChatInviteLink
from .get_chat_admins_with_invite_links import GetChatAdminsWithInviteLinks
from .get_chat_invite_link import GetChatInviteLink
from .get_chat_invite_link_members import GetChatInviteLinkMembers
from .get_chat_invite_link_members_count import GetChatInviteLinkMembersCount
from .get_chat_admin_invite_links import GetChatAdminInviteLinks
from .get_chat_admin_invite_links_count import GetChatAdminInviteLinksCount
from .revoke_chat_invite_link import RevokeChatInviteLink


class InviteLinks(
    RevokeChatInviteLink,
    DeleteChatInviteLink,
    EditChatInviteLink,
    CreateChatInviteLink,
    GetChatInviteLinkMembers,
    GetChatInviteLinkMembersCount,
    GetChatAdminInviteLinks,
    ExportChatInviteLink,
    DeleteChatAdminInviteLinks,
    GetChatAdminInviteLinksCount,
    GetChatAdminsWithInviteLinks,
    GetChatInviteLink
):
    pass