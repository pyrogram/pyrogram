inline_queries
==============

This example shows how to handle inline queries.

Two results are generated when users invoke the bot inline mode, e.g.: @pyrogrambot hi.
It uses the @on_inline_query decorator to register an InlineQueryHandler.

.. code-block:: python

    from pyrogram import Client
    from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent,
                                InlineKeyboardMarkup, InlineKeyboardButton)

    app = Client("my_bot", bot_token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")


    @app.on_inline_query()
    def answer(client, inline_query):
        inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    title="Installation",
                    input_message_content=InputTextMessageContent(
                        "Here's how to install **Pyrogram**"
                    ),
                    url="https://docs.pyrogram.org/intro/install",
                    description="How to install Pyrogram",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton(
                                "Open website",
                                url="https://docs.pyrogram.org/intro/install"
                            )]
                        ]
                    )
                ),
                InlineQueryResultArticle(
                    title="Usage",
                    input_message_content=InputTextMessageContent(
                        "Here's how to use **Pyrogram**"
                    ),
                    url="https://docs.pyrogram.org/start/invoking",
                    description="How to use Pyrogram",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton(
                                "Open website",
                                url="https://docs.pyrogram.org/start/invoking"
                            )]
                        ]
                    )
                )
            ],
            cache_time=1
        )


    app.run()  # Automatically start() and idle()