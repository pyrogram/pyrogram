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

from typing import List, Union

import pyrogram
from pyrogram import enums, raw, types

class EditStoryPrivacy:
    async def edit_story_privacy(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        story_id: int,
        privacy: "enums.StoriesPrivacyRules" = None,
        allowed_users: List[Union[int, str]] = None,
        disallowed_users: List[Union[int, str]] = None,
    ) -> "types.Story":
        """Edit the privacy of story.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            story_id (``int``):
                Story identifier in the chat specified in chat_id.

            privacy (:obj:`~pyrogram.enums.StoriesPrivacyRules`, *optional*):
                Story privacy.

            allowed_users (List of ``int`` | ``str``, *optional*):
                List of user_id or chat_id of chat users who are allowed to view stories.
                Note: chat_id available only with :obj:`~pyrogram.enums.StoriesPrivacyRules.SELECTED_USERS`.
                Works with :obj:`~pyrogram.enums.StoriesPrivacyRules.CLOSE_FRIENDS`
                and :obj:`~pyrogram.enums.StoriesPrivacyRules.SELECTED_USERS` only

            disallowed_users (List of ``int`` | ``str``, *optional*):
                List of user_id whos disallow to view the stories.
                Note: Works with :obj:`~pyrogram.enums.StoriesPrivacyRules.PUBLIC`
                and :obj:`~pyrogram.enums.StoriesPrivacyRules.CONTACTS` only

        Returns:
            :obj:`~pyrogram.types.Story`: On success, the edited story is returned.

        Example:
            .. code-block:: python

                # Edit story privacy to public
                await app.edit_story_privacy(chat_id, story_id, enums.StoriesPrivacyRules.PUBLIC)

                # Edit the privacy of the story to allow selected users to view the story
                await app.edit_story_privacy(
                    chat_id,
                    story_id,
                    enums.StoriesPrivacyRules.SELECTED_USERS,
                    allowed_users=[123, 456]
                )
        """
        privacy_rules = []

        if privacy:
            if privacy == enums.StoriesPrivacyRules.PUBLIC:
                privacy_rules.append(raw.types.InputPrivacyValueAllowAll())
                if disallowed_users:
                    users = [await self.resolve_peer(user_id) for user_id in disallowed_users]
                    privacy_rules.append(raw.types.InputPrivacyValueDisallowUsers(users=users))
            elif privacy == enums.StoriesPrivacyRules.CONTACTS:
                privacy_rules = [raw.types.InputPrivacyValueAllowContacts()]
                if disallowed_users:
                    users = [await self.resolve_peer(user_id) for user_id in disallowed_users]
                    privacy_rules.append(raw.types.InputPrivacyValueDisallowUsers(users=users))
            elif privacy == enums.StoriesPrivacyRules.CLOSE_FRIENDS:
                privacy_rules = [raw.types.InputPrivacyValueAllowCloseFriends()]
                if allowed_users:
                    users = [await self.resolve_peer(user_id) for user_id in allowed_users]
                    privacy_rules.append(raw.types.InputPrivacyValueAllowUsers(users=users))
            elif privacy == enums.StoriesPrivacyRules.SELECTED_USERS:
                _allowed_users = []
                _allowed_chats = []

                for user in allowed_users:
                    peer = await self.resolve_peer(user)
                    if isinstance(peer, raw.types.InputPeerUser):
                        _allowed_users.append(peer)
                    elif isinstance(peer, (raw.types.InputPeerChat, raw.types.InputPeerChannel)):
                        _allowed_chats.append(peer)

                if _allowed_users:
                    privacy_rules.append(raw.types.InputPrivacyValueAllowUsers(users=_allowed_users))
                if _allowed_chats:
                    privacy_rules.append(raw.types.InputPrivacyValueAllowChatParticipants(chats=_allowed_chats))
        else:
            privacy_rules.append(raw.types.InputPrivacyValueAllowAll())


        r = await self.invoke(
            raw.functions.stories.EditStory(
                peer=await self.resolve_peer(chat_id),
                id=story_id,
                privacy_rules=privacy_rules,
            )
        )

        for i in r.updates:
            if isinstance(i, raw.types.UpdateStory):
                return await types.Story._parse(
                    self,
                    i.story,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                    i.peer
                )
