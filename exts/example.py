from discord.ext import commands

import logging
log = logging.getLogger(__name__)

class ExampleCog(commands.Cog, name = __name__):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

async def setup(bot: commands.Bot):
  log.info("loaded")
  await bot.add_cog(ExampleCog(bot))

async def teardown(_bot: commands.Bot):
  log.info("unloaded")
