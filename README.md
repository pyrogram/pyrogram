<p align="center">
    <a href="https://github.com/pyrogram/pyrogram">
        <img src="https://i.imgur.com/BOgY9ai.png" alt="Pyrogram">
    </a>
    <br>
    <b>Telegram MTProto API Framework for Python</b>
    <br>
    <a href="https://docs.pyrogram.org">
        Documentation
    </a>
    •
    <a href="https://github.com/pyrogram/pyrogram/releases">
        Releases
    </a>
    •
    <a href="https://t.me/Pyrogram">
        Community
    </a>
</p>

## Pyrogram

``` python
from pyrogram import Client, filters

app = Client("my_account")


@app.on_message(filters.private)
async def hello(client, message):
    await message.reply_text(f"Hello {message.from_user.mention}")


app.run()
```

**Pyrogram** is a modern, elegant and easy-to-use [Telegram](https://telegram.org/) client library framework written
from the ground up in Python and C. It enables you to easily create custom Telegram client applications for both user
and bot identities (bot API alternative) via the [MTProto API](https://docs.pyrogram.org/topics/mtproto-vs-botapi).

### Features

- **Easy**: You can install Pyrogram with pip and start building your applications right away.
- **Elegant**: Low-level details are abstracted and re-presented in a much nicer and easier way.
- **Fast**: Crypto parts are boosted up by [TgCrypto](https://github.com/pyrogram/tgcrypto), a high-performance library
  written in pure C.
- **Asynchronous**: Allows both synchronous and asynchronous models to fit all usage needs.
- **Documented**: API methods, types and public interfaces are all [well documented](https://docs.pyrogram.org).
- **Type-hinted**: Types and methods are all type-hinted, enabling excellent editor support.
- **Updated**, to make use of the latest Telegram API version and features.
- **Bot API-like**: Similar to the Bot API in its simplicity, but much more powerful and detailed.
- **Pluggable**: The Smart Plugin system allows to write components with minimal boilerplate code.
- **Comprehensive**: Execute any advanced action an official client is able to do, and even more.

### Requirements

- Python 3.6 or higher.
- A [Telegram API key](https://docs.pyrogram.org/intro/setup#api-keys).

### Installing

``` bash
pip3 install pyrogram
```

### Resources

- The docs contain lots of resources to help you get started with Pyrogram: https://docs.pyrogram.org.
- Seeking extra help? Come join and ask our community: https://t.me/pyrogram.
- For other kind of inquiries, you can send a [message](https://t.me/haskell) or an [e-mail](mailto:dan@pyrogram.org).

### Copyright & License

- Copyright (C) 2017-2021 Dan <<https://github.com/delivrance>>
- Licensed under the terms of the [GNU Lesser General Public License v3 or later (LGPLv3+)](COPYING.lesser)
