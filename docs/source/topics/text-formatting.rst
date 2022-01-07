Text Formatting
===============

.. role:: strike
    :class: strike

.. role:: underline
    :class: underline

.. role:: bold-underline
    :class: bold-underline

.. role:: strike-italic
    :class: strike-italic

Pyrogram uses a custom Markdown dialect for text formatting which adds some unique features that make writing styled
texts easier in both Markdown and HTML. You can send sophisticated text messages and media captions using a
variety of decorations that can also be nested in order to combine multiple styles together.

.. contents:: Contents
    :backlinks: none
    :depth: 1
    :local:

-----

Basic Styles
------------

When formatting your messages, you can choose between Markdown-style, HTML-style or both (default). The following is a
list of the basic styles currently supported by Pyrogram.

- **bold**
- *italic*
- :strike:`strike`
- :underline:`underline`
- spoiler
- `text URL <https://pyrogram.org>`_
- `user text mention <tg://user?id=123456789>`_
- ``inline fixed-width code``
- .. code-block:: text

    pre-formatted
      fixed-width
        code block

.. note::

    User text mentions are only guaranteed to work if you have already met the user (in groups or private chats).

Markdown Style
--------------

To strictly use this mode, pass "markdown" to the *parse_mode* parameter when using
:meth:`~pyrogram.Client.send_message`. Use the following syntax in your message:

.. code-block:: text

    **bold**

    __italic__

    --underline--

    ~~strike~~

    ||spoiler||

    [text URL](https://pyrogram.org/)

    [text user mention](tg://user?id=123456789)

    `inline fixed-width code`

    ```
    pre-formatted
      fixed-width
        code block
    ```

**Example**:

.. code-block:: python

    app.send_message(
        "me",
        (
            "**bold**, "
            "__italic__, "
            "--underline--, "
            "~~strike~~, "
            "||spoiler||, "
            "[URL](https://pyrogram.org), "
            "`code`, "
            "```"
            "for i in range(10):\n"
            "    print(i)"
            "```"
        ),
        parse_mode="markdown"
    )

HTML Style
----------

To strictly use this mode, pass "html" to the *parse_mode* parameter when using :meth:`~pyrogram.Client.send_message`.
The following tags are currently supported:

.. code-block:: text

    <b>bold</b>, <strong>bold</strong>

    <i>italic</i>, <em>italic</em>

    <u>underline</u>

    <s>strike</s>, <del>strike</del>, <strike>strike</strike>

    <spoiler>spoiler</spoiler>

    <a href="https://pyrogram.org/">text URL</a>

    <a href="tg://user?id=123456789">inline mention</a>

    <code>inline fixed-width code</code>

    <pre>
    pre-formatted
      fixed-width
        code block
    </pre>

**Example**:

.. code-block:: python

    app.send_message(
        "me",
        (
            "<b>bold</b>, "
            "<i>italic</i>, "
            "<u>underline</u>, "
            "<s>strike</s>, "
            "<spoiler>spoiler</spoiler>, "
            "<a href=\"https://pyrogram.org/\">URL</a>, "
            "<code>code</code>\n\n"
            "<pre>"
            "for i in range(10):\n"
            "    print(i)"
            "</pre>"
        ),
        parse_mode="html"
    )

.. note::

    All ``<``, ``>`` and ``&`` symbols that are not a part of a tag or an HTML entity must be replaced with the
    corresponding HTML entities (``<`` with ``&lt;``, ``>`` with ``&gt;`` and ``&`` with ``&amp;``). You can use this
    snippet to quickly escape those characters:

    .. code-block:: python

        import html

        text = "<my text>"
        text = html.escape(text)

        print(text)

    .. code-block:: text

        &lt;my text&gt;

Different Styles
----------------

By default, when ignoring the *parse_mode* parameter, both Markdown and HTML styles are enabled together.
This means you can combine together both syntaxes in the same text:

.. code-block:: python

    app.send_message("me", "**bold**, <i>italic</i>")

Result:

    **bold**, *italic*

If you don't like this behaviour you can always choose to only enable either Markdown or HTML in strict mode by passing
"markdown" or "html" as argument to the *parse_mode* parameter.

.. code-block::

    app.send_message("me", "**bold**, <i>italic</i>", parse_mode="markdown")
    app.send_message("me", "**bold**, <i>italic</i>", parse_mode="html")

Result:

    **bold**, <i>italic</i>

    \*\*bold**, *italic*

In case you want to completely turn off the style parser, simply pass ``None`` to *parse_mode*. The text will be sent
as-is.

.. code-block:: python

    app.send_message("me", "**bold**, <i>italic</i>", parse_mode=None)

Result:

    \*\*bold**, <i>italic</i>

Nested and Overlapping Entities
-------------------------------

You can also style texts with more than one decoration at once by nesting entities together. For example, you can send
a text message with both :bold-underline:`bold and underline` styles, or a text that has both :strike-italic:`italic and
strike` styles, and you can still combine both Markdown and HTML together.

Here there are some example texts you can try sending:

**Markdown**:

- ``**bold, --underline--**``
- ``**bold __italic --underline ~~strike~~--__**``
- ``**bold __and** italic__``

**HTML**:

- ``<b>bold, <u>underline</u></b>``
- ``<b>bold <i>italic <u>underline <s>strike</s></u></i></b>``
- ``<b>bold <i>and</b> italic</i>``

**Combined**:

- ``--you can combine <i>HTML</i> with **Markdown**--``
- ``**and also <i>overlap** --entities</i> this way--``
