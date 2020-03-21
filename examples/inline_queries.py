"""This example shows how to handle inline queries.
Two results are generated when users invoke the bot inline mode, e.g.: @pyrogrambot hi.
It uses the @on_inline_query decorator to register an InlineQueryHandler.
"""

from uuid import uuid4

from pyrogram import (
    Client, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
)

app = Client("my_bot", bot_token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")


@app.on_inline_query()
def answer(client, inline_query):
    inline_query.answer(
        results=[
            InlineQueryResultArticle(
                id=uuid4(),
                title="Installation",
                input_message_content=InputTextMessageContent(
                    "Here's how to install **Pyrogram**"
                ),
                url="https://docs.pyrogram.org/intro/install",
                description="How to install Pyrogram",
                thumb_url="https://i.imgur.com/JyxrStE.png",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Open website", url="https://docs.pyrogram.org/intro/install")]
                    ]
                )
            ),
            InlineQueryResultArticle(
                id=uuid4(),
                title="Usage",
                input_message_content=InputTextMessageContent(
                    "Here's how to use **Pyrogram**"
                ),
                url="https://docs.pyrogram.org/start/invoking",
                description="How to use Pyrogram",
                thumb_url="https://i.imgur.com/JyxrStE.png",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Open website", url="https://docs.pyrogram.org/start/invoking")]
                    ]
                )
            )
        ],
        cache_time=1
    )


app.run()  # Automatically start() and idle()
