from discord.ext import commands
from src.bot import Bot

import logging
log = logging.getLogger(__name__)

class CoreCog(commands.Cog, name = __name__):
  def __init__(self, bot: Bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_message(self, msg):
    if msg.author.bot:
      return
    self.bot.dispatch("user_message", msg)

async def setup(bot: Bot):
  log.info("loaded")
  await bot.add_cog(CoreCog(bot))

async def teardown(_bot: Bot):
  log.info("unloaded")
