import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.environ["MONGODB_URI"]
assert MONGODB_URI is not None, "MONGODB_URI is not set"

DISCORD_BOT_TOKEN = os.environ["DISCORD_TOKEN"]
assert DISCORD_BOT_TOKEN is not None, "DISCORD_TOKEN is not set"

GUILD_ID = os.environ["GUILD_ID"]
assert GUILD_ID is not None, "GUILD_ID is not set"
