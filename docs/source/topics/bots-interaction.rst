Bots Interaction
================

Users can interact with other bots via plain text messages as well as inline queries.

.. contents:: Contents
    :backlinks: none
    :local:

-----

Inline Bots
-----------

-   If a bot accepts inline queries, you can call it by using
    :meth:`~pyrogram.Client.get_inline_bot_results` to get the list of its inline results for a query:

    .. code-block:: python

        # Get bot results for "Fuzz Universe" from the inline bot @vid
        bot_results = app.get_inline_bot_results("vid", "Fuzz Universe")

    .. figure:: https://i.imgur.com/IAqLs54.png
        :width: 90%
        :align: center
        :figwidth: 60%

        ``get_inline_bot_results()`` is the equivalent action of writing ``@vid Fuzz Universe`` and getting the
        results list.

-   After you retrieved the bot results, you can use
    :meth:`~pyrogram.Client.send_inline_bot_result` to send a chosen result to any chat:

    .. code-block:: python

        # Send the first result to your own chat
        app.send_inline_bot_result(
            "me",
            bot_results.query_id,
            bot_results.results[0].id
        )

    .. figure:: https://i.imgur.com/wwxr7B7.png
        :width: 90%
        :align: center
        :figwidth: 60%

        ``send_inline_bot_result()`` is the equivalent action of choosing a result from the list and sending it
        to a chat.
