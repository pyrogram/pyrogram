"""This example demonstrates a basic API usage"""

from pyrogram import Client

# Create a new Client instance
app = Client("my_account")

# Start the Client before calling any API method
app.start()

# Send a message to yourself, Markdown is enabled by default
app.send_message("me", "Hi there! I'm using **Pyrogram**")

# Send a location to yourself
app.send_location("me", 51.500729, -0.124583)

# Stop the client when you're done
app.stop()
