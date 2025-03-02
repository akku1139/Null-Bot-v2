from jishaku.cog import Jishaku
from discord.ext import commands

import logging
log = logging.getLogger(__name__)

async def setup(bot: commands.Bot):
  log.info("loaded")
  # I don't recommend doing this!
  await bot.add_cog(Jishaku(bot=bot))

async def teardown(_bot: commands.Bot):
  log.info("unloaded")
