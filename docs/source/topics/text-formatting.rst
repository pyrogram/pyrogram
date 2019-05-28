Text Formatting
===============

Pyrogram, just like the `Telegram Bot API`_, natively supports basic Markdown and HTML formatting styles for text
messages and media captions.

Markdown style uses the same syntax as Telegram Desktop's and is enabled by default.

Beside bold, italic, and pre-formatted code, **Pyrogram does also support inline URLs and inline mentions of users**.

Markdown Style
--------------

To use this mode, pass "markdown" in the *parse_mode* field when using
:meth:`~pyrogram.Client.send_message`. Use the following syntax in your message:

.. code-block:: text

    **bold text**

    __italic text__

    [inline URL](https://docs.pyrogram.org/)

    [inline mention of a user](tg://user?id=23122162)

    `inline fixed-width code`

    ```block_language
    pre-formatted fixed-width code block
    ```


HTML Style
----------

To use this mode, pass "html" in the *parse_mode* field when using :meth:`~pyrogram.Client.send_message`.
The following tags are currently supported:

.. code-block:: text

    <b>bold</b>, <strong>bold</strong>

    <i>italic</i>, <em>italic</em>

    <a href="http://docs.pyrogram.org/">inline URL</a>

    <a href="tg://user?id=23122162">inline mention of a user</a>

    <code>inline fixed-width code</code>

    <pre>pre-formatted fixed-width code block</pre>

.. note:: Mentions are only guaranteed to work if you have already met the user (in groups or private chats).

Examples
--------

-   Markdown:

    .. code-block:: python

        app.send_message(
            chat_id="haskell",
            text=(
                "**bold**, "
                "__italic__, "
                "[mention](tg://user?id=23122162), "
                "[URL](https://docs.pyrogram.org), "
                "`code`, "
                "```"
                "for i in range(10):\n"
                "   print(i)```"
            )
        )

-   HTML:

    .. code-block:: python

        app.send_message(
            chat_id="haskell",
            text=(
                "<b>bold</b>, "
                "<i>italic</i>, "
                "<a href=\"tg://user?id=23122162\">mention</a>, "
                "<a href=\"https://pyrogram.org/\">URL</a>, "
                "<code>code</code>, "
                "<pre>"
                "for i in range(10):\n"
                "    print(i)"
                "</pre>"
            ),
            parse_mode="html"
        )

.. _Telegram Bot API: https://core.telegram.org/bots/api#formatting-options