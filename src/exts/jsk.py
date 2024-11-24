from src.bot import Bot
from jishaku.cog import Jishaku

import logging
log = logging.getLogger(__name__)

async def setup(bot: Bot):
  # I don't recommend doing this!
  await bot.add_cog(Jishaku(bot=bot))

async def teardown(_bot: Bot):
  log.info("unloaded")
