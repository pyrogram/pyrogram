<p align="center">
    <a href="https://github.com/pyrogram/pyrogram">
        <img src="https://i.imgur.com/BOgY9ai.png" alt="Pyrogram">
    </a>
    <br>
    <b>Telegram MTProto Library for Python</b>
    <br>
    <a href="https://docs.pyrogram.org">
        Documentation
    </a>
    •
    <a href="https://docs.pyrogram.org/releases">
        Releases
    </a>
    •
    <a href="https://t.me/pyrogram">
        Community
    </a>
</p>

## Pyrogram

``` python
from pyrogram import Client, filters

app = Client("my_account")


@app.on_message(filters.private)
async def hello(client, message):
    await message.reply(f"Hello from Pyrogram!")


app.run()
```

> ✨ Many thanks to the sponsors and everyone who starred the project! Your support is appreciated.

**Pyrogram** is a modern, asynchronous [MTProto](https://docs.pyrogram.org/topics/mtproto-vs-botapi) library for
building [Telegram](https://telegram.org/) client applications in Python. It enables you to easily interact with
the main Telegram API through a user account (custom client) or a bot identity (bot API alternative).

### Key Features

- **Ready**: Install Pyrogram with pip and start building your applications right away.
- **Easy**: Makes the Telegram API simple and intuitive, while still allowing advanced usages.
- **Elegant**: Low-level details are abstracted and re-presented in a more convenient way.
- **Type-hinted**: Types and methods are all type-hinted, enabling excellent editor support.
- **Asynchronous**: Fully asynchronous (also usable synchronously if wanted, for convenience).
- **Powerful**: Full access to Telegram's API to execute any official client action and more.

### Requirements

- Python 3.6 or higher.
- A [Telegram API key](https://docs.pyrogram.org/intro/setup#api-keys).

### Installing

``` bash
pip3 install pyrogram
```

### Resources

- Check out the docs at https://docs.pyrogram.org to learn more about Pyrogram, get started right
away and discover more in-depth material for building your client applications.
- Join the official channel at https://t.me/pyrogram to stay tuned for news and updates.
