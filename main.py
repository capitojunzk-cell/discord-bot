import os
import asyncio
import logging
from discord import Intents
from discord.ext import commands
from discord.errors import HTTPException

# ----------------------------
# Setup logging
# ----------------------------
logging.basicConfig(level=logging.INFO)

# ----------------------------
# Setup bot intents
# ----------------------------
intents = Intents.default()
intents.message_content = True  # Enable lang kung kailangan mo basahin ang messages
bot = commands.Bot(command_prefix="!", intents=intents)

# ----------------------------
# Helper: Safe API call with exponential backoff
# ----------------------------
async def safe_api_call(coro, retries=5):
    """
    Wrap API calls to avoid hitting 429 rate limits.
    Retries with exponential backoff.
    """
    delay = 1
    for _ in range(retries):
        try:
            return await coro
        except HTTPException as e:
            if e.status == 429:
                logging.warning(f"Rate limited! Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
                delay *= 2  # exponential backoff
            else:
                raise
    logging.error("Max retries reached. Skipping this API call.")

# ----------------------------
# Bot events
# ----------------------------
@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user} (ID: {bot.user.id})')
    logging.info('------')

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Example: respond to "!hello"
    if message.content.lower() == "!hello":
        await safe_api_call(message.channel.send(f"Hello {message.author.mention}!"))

# ----------------------------
# Example command
# ----------------------------
@bot.command()
async def ping(ctx):
    await safe_api_call(ctx.send("Pong!"))

# ----------------------------
# Run bot
# ----------------------------
TOKEN = os.getenv("TOKEN")  # siguraduhing nakaset sa Render
if not TOKEN:
    logging.error("No TOKEN environment variable set!")
else:
    bot.run(TOKEN)