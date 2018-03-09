from pyrogram import Client

# Create a new Client
client = Client("example")

# Start the Client
client.start()

# Get bot results for "Fuzz Universe" from the inline bot @vid
bot_results = client.get_inline_bot_results("vid", "Fuzz Universe")
# Send the first result (bot_results.results[0]) to your own chat (Saved Messages)
client.send_inline_bot_result("me", bot_results.query_id, bot_results.results[0].id)

# Stop the client
client.stop()
