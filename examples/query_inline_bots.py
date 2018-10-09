from pyrogram import Client

"""This example shows how to query an inline bot"""

# Create a new Client
app = Client("my_account")

# Start the Client
app.start()

# Get bot results for "Fuzz Universe" from the inline bot @vid
bot_results = app.get_inline_bot_results("vid", "Fuzz Universe")
# Send the first result (bot_results.results[0]) to your own chat (Saved Messages)
app.send_inline_bot_result("me", bot_results.query_id, bot_results.results[0].id)

# Stop the client
app.stop()
