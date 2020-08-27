from typing import Union
from datetime import datetime, timedelta

from pyrogram.raw.functions.account import UpdateNotifySettings
from pyrogram.raw.types import InputNotifyPeer, InputPeerNotifySettings
from pyrogram.scaffold import Scaffold


class UpdateChatNotifications(Scaffold):
    async def update_chat_notifications(
        self,
        chat_id: Union[int, str],
        show_previews: bool = None,
        silent: bool = None,
        mute_until: Union[int, datetime, timedelta] = None
    ) -> bool:
        """Update the notification settings for the selected chat

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            show_previews (``bool``, *optional*):
                If the text of the message shall be displayed in notification.

            silent (``bool``, *optional*):
                If the chat shall be muted.

            mute_until (``int`` | ``datetime.datetime`` | ``datetime.timdelta``, *optional*):
                Unix timestamp, datetime or timedelta object that sets up when notifications shall be switched off.
                Default to forever.

        Returns:
            ``bool``: True on success, False otherwise.

        Example:
            .. code-block:: python

                # Mute a chat permanently
                app.update_chat_notifications(chat_id, silent=True)

                # Mute a chat for 10 minutes
                from datetime import timedelta

                app.update_chat_notifications(
                    chat_id,
                    silent=True
                    mute_until=timedelta(minutes=10)
                )

                # Unmute a chat
                app.update_chat_notifications(chat_id, silent=False)
        """

        if isinstance(mute_until, datetime):
            mute_until = mute_until.timestamp()

        if isinstance(mute_until, timedelta):
            now = datetime.now()
            mute_until = now.timestamp() + mute_until.total_seconds()

        peer = await self.resolve_peer(chat_id)

        r = await self.send(
            UpdateNotifySettings(
                peer=InputNotifyPeer(peer=peer),
                settings=InputPeerNotifySettings(
                    show_previews=show_previews or None,
                    silent=silent or None,
                    mute_until=mute_until or None
                )
            )
        )

        return r
