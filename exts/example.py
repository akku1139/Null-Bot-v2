from discord.ext import commands
from bot import Bot

import logging
log = logging.getLogger(__name__)

class ExampleCog(commands.Cog, name = __name__):
  def __init__(self, bot: Bot):
    self.bot = bot

async def setup(bot: Bot):
  log.info("loaded")
  await bot.add_cog(ExampleCog(bot))

async def teardown(_bot: Bot):
  log.info("unloaded")
