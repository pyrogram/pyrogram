from pyrogram import Client

"""This example demonstrates a simple API methods usage"""

# Create a new Client
app = Client("my_account")

# Start the Client
app.start()

# Send a message to yourself, Markdown is enabled by default
app.send_message("me", "Hi there! I'm using **Pyrogram**")

# Send a location to yourself
app.send_location("me", 51.500729, -0.124583)

# Stop the client
app.stop()
