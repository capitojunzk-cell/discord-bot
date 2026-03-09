import os
import asyncio
import logging
import discord
from discord.ext import commands

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

async def main():
    token = os.getenv("TOKEN")

    if not token:
        print("TOKEN not found!")
        return

    async with bot:
        await bot.start(token)

asyncio.run(main())