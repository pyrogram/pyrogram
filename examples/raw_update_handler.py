from pyrogram import Client

"""This example shows how to handle raw updates"""

app = Client("my_account")


@app.on_raw_update()
def raw(client, update, users, chats):
    print(update)


app.start()
app.idle()
