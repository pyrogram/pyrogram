from typing import Union

from pyrogram.raw.functions.account import UpdateNotifySettings
from pyrogram.raw.types import InputNotifyPeer, InputPeerNotifySettings
from pyrogram.scaffold import Scaffold


class UpdateChatNotifications(Scaffold):
    async def update_chat_notifications(
        self,
        chat_id: Union[int, str],
        show_previews: bool = None,
        silent: bool = None,
        mute_until: int = None
    ) -> bool:
        """Update the notification settings for the selected chat

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            show_previews (``bool``, *optional*):
                If the text of the message shall be displayed in notification.

            silent (``bool``, *optional*):
                If the chat shall be muted.

            mute_until (``int``, *optional*):
                When notifications shall be switched off. Unix time.
                Default to forever.

        Returns:
            ``bool``: True on success, False otherwise.

        Example:
            .. code-block:: python

                # Mute a chat permanently
                app.update_chat_notifications(chat_id, silent=True)

                # Mute a chat for 10 minutes
                from time import time

                app.update_chat_notifications(
                    chat_id,
                    silent=True,
                    mute_until=time() + 600
                )

                # Unmute a chat
                app.update_chat_notifications(chat_id, silent=False)
        """

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
