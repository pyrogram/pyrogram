"""This example demonstrates a basic API usage"""

from pyrogram import Client

# Create a new Client instance
app = Client("my_account")

with app:
    # Send a message, Markdown is enabled by default
    app.send_message("me", "Hi there! I'm using **Pyrogram**")

    # Send a location
    app.send_location("me", 51.500729, -0.124583)

    # Send a sticker
    app.send_sticker("me", "CAADBAADzg4AAvLQYAEz_x2EOgdRwBYE")
