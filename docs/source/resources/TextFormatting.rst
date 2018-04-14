Text Formatting
===============

Pyrogram, just like `Telegram Bot API`_, supports basic Markdown and HTML formatting styles for messages and media captions;
Markdown uses the same syntax as Telegram Desktop's and is enabled by default.
Beside bold, italic, and pre-formatted code, **Pyrogram does also support inline URLs and inline mentions of users**.

Markdown Style
--------------

To use this mode, pass :obj:`MARKDOWN <pyrogram.ParseMode.MARKDOWN>` or "markdown" in the *parse_mode* field when using
:obj:`send_message() <pyrogram.Client.send_message>`. Use the following syntax in your message:

.. code::

    **bold text**

    __italic text__

    [inline URL](http://www.example.com/)

    [inline mention of a user](tg://user?id=123456789)

    `inline fixed-width code`

    ```block_language
    pre-formatted fixed-width code block
    ```

HTML Style
----------

To use this mode, pass :obj:`HTML <pyrogram.ParseMode.HTML>` or "html" in the *parse_mode* field when using
:obj:`send_message() <pyrogram.Client.send_message>`. The following tags are currently supported:

.. code::

    <b>bold</b>, <strong>bold</strong>

    <i>italic</i>, <em>italic</em>

    <a href="http://www.example.com/">inline URL</a>

    <a href="tg://user?id=123456789">inline mention of a user</a>

    <code>inline fixed-width code</code>

    <pre>pre-formatted fixed-width code block</pre>

.. note:: Mentions are only guaranteed to work if you have already contacted the user.

Examples
--------

-   Markdown inline entities (bold, italic, ...):

    .. code-block:: python

        app.send_message(
            chat_id="me",
            text=(
                "**bold**, "
                "__italic__, "
                "[mention](tg://user?id=23122162), "
                "[url](https://pyrogram.ml), "
                "`code`"
            )
        )

-   Markdown code blocks:

    .. code-block:: python

        app.send_message(
            chat_id="me",
            text=(
                # Code block language is optional
                "``` python\n"
                "for i in range(10):\n"
                "   print(i)\n"
                "```"
            )
        )

-   HTML example:

    .. code-block:: python

        from pyrogram import ParseMode

        app.send_message(
            chat_id="me",
            text=(
                "<b>bold</b>, <strong>bold</strong>, "
                "<i>italic</i>, <em>italic</em>, "
                "<a href=\"https://pyrogram.ml/\">inline URL</a>, "
                "<a href=\"tg://user?id=23122162\">inline mention of a user</a>, "
                "<code>inline fixed-width code</code>, "
                "<pre>pre-formatted fixed-width code block</pre>"
            ),
            parse_mode=ParseMode.HTML
        )

.. _Telegram Bot API: https://core.telegram.org/bots/api#formatting-options