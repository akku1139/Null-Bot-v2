import discord
from dotenv import load_dotenv
import os
import subprocess
from bot import Bot
from log_handler import DiscordWebHookHandler
from logging import getLogger

load_dotenv()
TOKEN = os.environ["DISCORD_TOKEN"]

bot = Bot(
  command_prefix = "!",
  intents = discord.Intents.all()
)

discord.utils.setup_logging(
  handler = DiscordWebHookHandler(),
  root = True
)
log = getLogger("main")

@bot.event
async def setup_hook():
  for cog in os.listdir("src/exts/"):
    if cog.endswith(".py"):
      await bot.load_extension(f"src.exts.{cog[:-3]}")
  log.info("exts loaded")

if __name__ == "__main__":
  try:
    bot.run(TOKEN, log_handler=None)
  except Exception as e: # pylint: disable=broad-exception-caught
    log.error(e)
    stdout = subprocess.run(["git","pull"], capture_output=True, text=True, check=False).stdout
    log.info("git pull\n"+stdout) # pylint: disable=logging-not-lazy
