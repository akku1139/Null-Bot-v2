import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

from log_handler import DiscordWebHookHandler

import logging
#import uvloop
import asyncio

load_dotenv()
TOKEN = os.environ["DISCORD_TOKEN"]

logging.getLogger().addHandler(logging.StreamHandler())

bot = commands.Bot(
  command_prefix = "!",
  intents = discord.Intents.all()
)

log = logging.getLogger("main")

@bot.event
async def setup_hook():
  for cog in os.listdir("exts/"):
    if cog.endswith(".py"):
      await bot.load_extension(f"exts.{cog[:-3]}")
  log.info("exts loaded")

async def main():
  discord.utils.setup_logging(
    handler = DiscordWebHookHandler(),
    root = True
  )
  async with bot:
    await bot.start(TOKEN)

if __name__ == "__main__":
  asyncio.run(main())
