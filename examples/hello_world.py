from pyrogram import Client

# Create a new Client
client = Client("example")

# Start the Client
client.start()

# Send a message to yourself, Markdown is enabled by default
client.send_message("me", "Hi there! I'm using **Pyrogram**")

# Send a location to yourself
client.send_location("me", 51.500729, -0.124583)

# Stop the client
client.stop()
