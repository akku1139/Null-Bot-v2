import discord

import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.environ["DISCORD_TOKEN"]

from bot import Bot
from log_handler import DiscordWebHookHandler

import logging
logging.getLogger().addHandler(logging.StreamHandler())

import uvloop

bot = Bot(
  command_prefix = "!",
  intents = discord.Intents.all()
)

log = logging.getLogger("main")

@bot.event
async def setup_hook():
  for cog in os.listdir("src/exts/"):
    if cog.endswith(".py"):
      await bot.load_extension(f"src.exts.{cog[:-3]}")
  log.info("exts loaded")

async def main():
  discord.utils.setup_logging(
    handler = DiscordWebHookHandler(),
    root = True
  )
  async with bot:
    await bot.start(TOKEN)

if __name__ == "__main__":
  uvloop.run(main())
