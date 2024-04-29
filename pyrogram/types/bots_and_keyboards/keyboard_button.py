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

from typing import Union

from pyrogram import raw, types
from ..object import Object


class KeyboardButton(Object):
    """One button of the reply keyboard.
    For simple text buttons String can be used instead of this object to specify text of the button.
    Optional fields are mutually exclusive.

    Parameters:
        text (``str``):
            Text of the button. If none of the optional fields are used, it will be sent as a message when
            the button is pressed.

        request_contact (``bool``, *optional*):
            If True, the user's phone number will be sent as a contact when the button is pressed.
            Available in private chats only.

        request_location (``bool``, *optional*):
            If True, the user's current location will be sent when the button is pressed.
            Available in private chats only.

        request_poll (:obj:`~pyrogram.types.RequestPollInfo`, *optional*):
            If specified, the poll be sent when the button is pressed.

        request_peer (:obj:`~pyrogram.types.RequestPeerTypeChannelInfo` | :obj:`~pyrogram.types.RequestPeerTypeChatInfo` | :obj:`~pyrogram.types.RequestPeerTypeUserInfo`, *optional*):
            If specified, the requested peer will be sent when the button is pressed.

        web_app (:obj:`~pyrogram.types.WebAppInfo`, *optional*):
            If specified, the described `Web App <https://core.telegram.org/bots/webapps>`_ will be launched when the
            button is pressed. The Web App will be able to send a “web_app_data” service message. Available in private
            chats only.

    """

    def __init__(
        self,
        text: str,
        request_contact: bool = None,
        request_location: bool = None,
        request_poll: "types.RequestPollInfo" = None,
        request_peer: Union["types.RequestChannelInfo", "types.RequestChatInfo", "types.RequestUserInfo"] = None,
        web_app: "types.WebAppInfo" = None,
    ):
        super().__init__()

        self.text = str(text)
        self.request_contact = request_contact
        self.request_location = request_location
        self.request_poll = request_poll
        self.request_peer = request_peer
        self.web_app = web_app

    @staticmethod
    def read(b):
        if isinstance(b, raw.types.KeyboardButton):
            return b.text

        if isinstance(b, raw.types.KeyboardButtonRequestPhone):
            return KeyboardButton(
                text=b.text,
                request_contact=True
            )

        if isinstance(b, raw.types.KeyboardButtonRequestGeoLocation):
            return KeyboardButton(
                text=b.text,
                request_location=True
            )

        if isinstance(b, raw.types.KeyboardButtonRequestPoll):
            return KeyboardButton(
                text=b.text,
                request_poll=types.RequestPollInfo(is_quiz=b.quiz)
            )

        if isinstance(b, raw.types.KeyboardButtonRequestPeer):
            if isinstance(b.peer_type, raw.types.RequestPeerTypeBroadcast):
                user_privileges = getattr(b.peer_type, "user_admin_rights", None)
                bot_privileges = getattr(b.peer_type, "bot_admin_rights", None)

                return KeyboardButton(
                    text=b.text,
                    request_peer=types.RequestChannelInfo(
                        button_id=b.button_id,
                        is_creator=getattr(b.peer_type, "creator", None),
                        has_username=getattr(b.peer_type, "has_username", None),
                        user_privileges=types.ChatPrivileges._parse(user_privileges) if user_privileges else None,
                        bot_privileges=types.ChatPrivileges._parse(bot_privileges) if bot_privileges else None
                    )
                )

            if isinstance(b.peer_type, raw.types.RequestPeerTypeChat):
                user_privileges = getattr(b.peer_type, "user_admin_rights", None)
                bot_privileges = getattr(b.peer_type, "bot_admin_rights", None)

                return KeyboardButton(
                    text=b.text,
                    request_peer=types.RequestChatInfo(
                        button_id=b.button_id,
                        is_creator=getattr(b.peer_type, "creator", None),
                        is_bot_participant=getattr(b.peer_type, "bot_participant", None),
                        has_username=getattr(b.peer_type, "has_username", None),
                        has_forum=getattr(b.peer_type, "forum", None),
                        user_privileges=types.ChatPrivileges._parse(user_privileges) if user_privileges else None,
                        bot_privileges=types.ChatPrivileges._parse(bot_privileges) if bot_privileges else None
                    )
                )

            if isinstance(b.peer_type, raw.types.RequestPeerTypeUser):
                return KeyboardButton(
                    text=b.text,
                    request_peer=types.RequestUserInfo(
                        button_id=b.button_id,
                        is_bot=getattr(b.peer_type, "bot", None),
                        is_premium=getattr(b.peer_type, "premium", None),
                        max_quantity=getattr(b, "max_quantity", None)
                    )
                )

        if isinstance(b, raw.types.KeyboardButtonSimpleWebView):
            return KeyboardButton(
                text=b.text,
                web_app=types.WebAppInfo(
                    url=b.url
                )
            )

    def write(self):
        if self.request_contact:
            return raw.types.KeyboardButtonRequestPhone(text=self.text)
        elif self.request_location:
            return raw.types.KeyboardButtonRequestGeoLocation(text=self.text)
        elif self.request_poll:
            return raw.types.KeyboardButtonRequestPoll(
                text=self.text,
                quiz=self.request_poll.is_quiz
            )
        elif self.request_peer:
            if isinstance(self.request_peer, types.RequestChannelInfo):
                user_privileges = self.request_peer.user_privileges
                bot_privileges = self.request_peer.bot_privileges

                user_admin_rights = raw.types.ChatAdminRights(
                    change_info=user_privileges.can_change_info,
                    post_messages=user_privileges.can_post_messages,
                    post_stories=user_privileges.can_post_stories,
                    edit_messages=user_privileges.can_edit_messages,
                    edit_stories=user_privileges.can_post_stories,
                    delete_messages=user_privileges.can_delete_messages,
                    delete_stories=user_privileges.can_delete_stories,
                    ban_users=user_privileges.can_restrict_members,
                    invite_users=user_privileges.can_invite_users,
                    pin_messages=user_privileges.can_pin_messages,
                    add_admins=user_privileges.can_promote_members,
                    anonymous=user_privileges.is_anonymous,
                    manage_call=user_privileges.can_manage_video_chats,
                    other=user_privileges.can_manage_chat
                ) if user_privileges else None

                bot_admin_rights = raw.types.ChatAdminRights(
                    change_info=bot_privileges.can_change_info,
                    post_messages=bot_privileges.can_post_messages,
                    post_stories=bot_privileges.can_post_stories,
                    edit_messages=bot_privileges.can_edit_messages,
                    edit_stories=bot_privileges.can_post_stories,
                    delete_messages=bot_privileges.can_delete_messages,
                    delete_stories=bot_privileges.can_delete_stories,
                    ban_users=bot_privileges.can_restrict_members,
                    invite_users=bot_privileges.can_invite_users,
                    pin_messages=bot_privileges.can_pin_messages,
                    add_admins=bot_privileges.can_promote_members,
                    anonymous=bot_privileges.is_anonymous,
                    manage_call=bot_privileges.can_manage_video_chats,
                    other=bot_privileges.can_manage_chat
                ) if bot_privileges else None

                return raw.types.KeyboardButtonRequestPeer(
                    text=self.text,
                    button_id=self.request_peer.button_id,
                    peer_type=raw.types.RequestPeerTypeBroadcast(
                        creator=self.request_peer.is_creator,
                        has_username=self.request_peer.has_username,
                        user_admin_rights=user_admin_rights,
                        bot_admin_rights=bot_admin_rights
                    ),
                    max_quantity=1
                )

            if isinstance(self.request_peer, types.RequestChatInfo):
                user_privileges = self.request_peer.user_privileges
                bot_privileges = self.request_peer.bot_privileges

                user_admin_rights = raw.types.ChatAdminRights(
                    change_info=user_privileges.can_change_info,
                    post_messages=user_privileges.can_post_messages,
                    post_stories=user_privileges.can_post_stories,
                    edit_messages=user_privileges.can_edit_messages,
                    edit_stories=user_privileges.can_post_stories,
                    delete_messages=user_privileges.can_delete_messages,
                    delete_stories=user_privileges.can_delete_stories,
                    ban_users=user_privileges.can_restrict_members,
                    invite_users=user_privileges.can_invite_users,
                    pin_messages=user_privileges.can_pin_messages,
                    add_admins=user_privileges.can_promote_members,
                    anonymous=user_privileges.is_anonymous,
                    manage_call=user_privileges.can_manage_video_chats,
                    other=user_privileges.can_manage_chat
                ) if user_privileges else None

                bot_admin_rights = raw.types.ChatAdminRights(
                    change_info=bot_privileges.can_change_info,
                    post_messages=bot_privileges.can_post_messages,
                    post_stories=bot_privileges.can_post_stories,
                    edit_messages=bot_privileges.can_edit_messages,
                    edit_stories=bot_privileges.can_post_stories,
                    delete_messages=bot_privileges.can_delete_messages,
                    delete_stories=bot_privileges.can_delete_stories,
                    ban_users=bot_privileges.can_restrict_members,
                    invite_users=bot_privileges.can_invite_users,
                    pin_messages=bot_privileges.can_pin_messages,
                    add_admins=bot_privileges.can_promote_members,
                    anonymous=bot_privileges.is_anonymous,
                    manage_call=bot_privileges.can_manage_video_chats,
                    other=bot_privileges.can_manage_chat
                ) if bot_privileges else None

                return raw.types.KeyboardButtonRequestPeer(
                    text=self.text,
                    button_id=self.request_peer.button_id,
                    peer_type=raw.types.RequestPeerTypeChat(
                        creator=self.request_peer.is_creator,
                        bot_participant=self.request_peer.is_bot_participant,
                        has_username=self.request_peer.has_username,
                        forum=self.request_peer.has_forum,
                        user_admin_rights=user_admin_rights,
                        bot_admin_rights=bot_admin_rights
                    ),
                    max_quantity=1
                )

            if isinstance(self.request_peer, types.RequestUserInfo):
                return raw.types.KeyboardButtonRequestPeer(
                    text=self.text,
                    button_id=self.request_peer.button_id,
                    peer_type=raw.types.RequestPeerTypeUser(
                        bot=self.request_peer.is_bot,
                        premium=self.request_peer.is_premium
                    ),
                    max_quantity=self.request_peer.max_quantity
                )

        elif self.web_app:
            return raw.types.KeyboardButtonSimpleWebView(text=self.text, url=self.web_app.url)
        else:
            return raw.types.KeyboardButton(text=self.text)
