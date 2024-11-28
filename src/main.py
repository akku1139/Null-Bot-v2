import discord
from dotenv import load_dotenv
import os
from bot import Bot
from log_handler import DiscordWebHookHandler
from logging import getLogger
import uvloop

load_dotenv()
TOKEN = os.environ["DISCORD_TOKEN"]

bot = Bot(
  command_prefix = "!",
  intents = discord.Intents.all()
)

log = getLogger("main")

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
  async with client:
    await client.start(TOKEN)

if __name__ == "__main__":
  uvloop.run(main())
