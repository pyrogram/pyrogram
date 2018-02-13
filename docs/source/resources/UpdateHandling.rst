Update Handling
===============

Updates are events that happen in your Telegram account (incoming messages, new channel posts, user name changes, ...)
and can be handled by using a callback function, that is, a function called every time an :obj:`Update` is received from
Telegram.

To set an update handler simply call :obj:`set_update_handler <pyrogram.Client.set_update_handler>`
by passing the name of your defined callback function as argument *before* you start the Client.

Here's a complete example on how to set it up:

.. code-block:: python

    from pyrogram import Client


    def update_handler(client, update, users, chats):
        print(update)

    def main()
        client = Client(session_name="example")
        client.set_update_handler(update_handler)

        client.start()
        client.idle()

    if __name__ == "__main__":
        main()

The last line of the main() function, :obj:`client.idle() <pyrogram.Client.idle>`, is not strictly necessary but highly
recommended; it will block your script execution until you press :obj:`CTRL`:obj:`C` and automatically call the
:obj:`stop <pyrogram.Client.stop>` method which stops the Client and gently close the underlying connection.

Examples
--------

-   Simple Echo example for **Private Messages**:

    .. code-block:: python

        from pyrogram.api import types

            if isinstance(update, types.UpdateNewMessage): # Filter by UpdateNewMessage (PM and Groups)
                message = update.message  # type: types.Message

                if isinstance(message, types.Message):  # Filter by Message to exclude MessageService and MessageEmpty
                    if isinstance(message.to_id, types.PeerUser):  # Private Messages (Message from user)
                        client.send_message(message.from_id, message.message, reply_to_message_id=message.id)



-   Advanced Echo example for both **Private Messages** and **Basic Groups** (with mentions).

    .. code-block:: python

        from pyrogram.api import types

        def update_handler(client, update, users, chats):
            if isinstance(update, types.UpdateNewMessage):  # Filter by UpdateNewMessage (PM and Chats)
                message = update.message

                if isinstance(message, types.Message):  # Filter by Message to exclude MessageService and MessageEmpty
                    if isinstance(message.to_id, types.PeerUser):  # Private Messages
                        text = '[{}](tg://user?id={}) said "{}" to me ([{}](tg://user?id={}))'.format(
                            users[message.from_id].first_name,
                            users[message.from_id].id,
                            message.message,
                            users[message.to_id.user_id].first_name,
                            users[message.to_id.user_id].id
                        )

                        client.send_message(
                            message.from_id,  # Send the message to the private chat (from_id)
                            text,
                            reply_to_message_id=message.id
                        )
                    else:  # Group chats
                        text = '[{}](tg://user?id={}) said "{}" in **{}** group'.format(
                            users[message.from_id].first_name,
                            users[message.from_id].id,
                            message.message,
                            chats[message.to_id.chat_id].title
                        )

                        client.send_message(
                            message.to_id,  # Send the message to the group chat (to_id)
                            text,
                            reply_to_message_id=message.id
                        )

-   Advanced Echo example for **Supergroups** (with mentions):

    .. code-block:: python

        from pyrogram.api import types

        def update_handler(client, update, users, chats):
            if isinstance(update, types.UpdateNewChannelMessage):  # Filter by UpdateNewChannelMessage (Channels/Supergroups)
                message = update.message

                if isinstance(message, types.Message):  # Filter by Message to exclude MessageService and MessageEmpty
                    if chats[message.to_id.channel_id].megagroup:  # Only handle messages from Supergroups not Channels
                        text = '[{}](tg://user?id={}) said "{}" in **{}** supergroup'.format(
                            users[message.from_id].first_name,
                            users[message.from_id].id,
                            message.message,
                            chats[message.to_id.channel_id].title
                        )

                        client.send_message(
                            message.to_id,
                            text,
                            reply_to_message_id=message.id
                        )

.. warning::
    The Advanced Examples above will make you reply to **all** new messages in private chats and in every single
    group/supergroup you are in. Make sure you add an extra check to filter them:

    .. code-block:: python

        # Filter Groups by ID
        if message.to_id.chat_id == MY_GROUP_ID:
            ...

        # Filter Supergroups by ID
        if message.to_id.channel_id == MY_SUPERGROUP_ID:
            ...

        # Filter Supergroups by Username
        if chats[message.to_id.channel_id].username == MY_SUPERGROUP_USERNAME:
            ...