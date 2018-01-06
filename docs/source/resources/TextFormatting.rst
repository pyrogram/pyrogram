Text Formatting
===============

Pyrogram, just like `Telegram Bot API`_, supports basic Markdown formatting for messages;
it uses the same syntax as Telegram Desktop's and is enabled by default.
Beside bold, italic, and pre-formatted code, **Pyrogram does also support inline URLs and inline mentions of users**.

Here is the complete syntax you can use when sending or editing messages:

.. code::

    **bold text**

    __italic text__

    [inline URL](http://www.example.com/)

    [inline mention of a user](tg://user?id=123456789)

    `inline fixed-width code`

    ```block_language
    pre-formatted fixed-width code block
    ```

Code Snippets
-------------

-   Inline entities (bold, italic, ...):

    .. code-block:: python

        client.send_message(
            chat_id="me",
            text="**bold**, __italic__, [mention](tg://user?id=23122162), [url](https://pyrogram.ml), `code`"
        )

    .. note:: Mentions are only guaranteed to work if you have already contacted the user.

-   Code blocks:

    .. code-block:: python

        client.send_message(
            chat_id="me",
            text=(
                # Code block language is optional
                "``` python\n"
                "for i in range(10):\n"
                "   print(i)\n"
                "```"
            )
        )

.. _Telegram Bot API: https://core.telegram.org/bots/api#formatting-options