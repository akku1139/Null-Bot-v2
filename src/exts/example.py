from discord.ext import commands
from src.bot import Bot

import logging
log = logging.getLogger(__name__)

class ExampleCog(commands.Cog, name = __name__):
  def __init__(self, bot: Bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    log.info("loaded")

async def setup(bot: Bot):
  await bot.add_cog(ExampleCog(bot))

async def teardown(bot: Bot):
  log.info("unloaded")
