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
import re

import pyrogram
from pyrogram import raw, utils


class LeaveFolder:
    async def leave_folder(
        self: "pyrogram.Client",
        link: str,
        keep_chats: bool = True
    ) -> bool:
        """Leave a folder by its invite link.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            link (``str``):
                Invite link of the folder.

            keep_chats (``bool``, *optional*):
                If True, the chats from the folder will be kept in the user's account.
                Defaults to True.

        Returns:
            ``bool``: True, on success.

        Raises:
            AttributeError: In case the folder invite link does not exist in the user's account.
            BadRequest: In case the folder invite link not exists.
            ValueError: In case the folder invite link is invalid.

        Example:
            .. code-block:: python

                # leave folder
                app.leave_folder("t.me/addlist/ebXQ0Q0I3RnGQ")
        """
        match = re.match(r"^(?:https?://)?(?:www\.)?(?:t(?:elegram)?\.(?:org|me|dog)/(?:addlist/|\+))([\w-]+)$", link)

        if match:
            slug = match.group(1)
        elif isinstance(link, str):
            slug = link
        else:
            raise ValueError("Invalid folder invite link")

        r = await self.invoke(
            raw.functions.chatlists.CheckChatlistInvite(
                slug=slug
            )
        )

        await self.invoke(
            raw.functions.chatlists.LeaveChatlist(
                chatlist=raw.types.InputChatlistDialogFilter(
                    filter_id=r.filter_id
                ),
                peers=[
                    await self.resolve_peer(utils.get_peer_id(id))
                    for id in r.already_peers
                ] if not keep_chats else [],
            )
        )

        return True
