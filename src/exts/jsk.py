from src.bot import Bot
from jishaku.cog import Jishaku

async def setup(bot: Bot):
  # I don't recommend doing this!
  await bot.add_cog(Jishaku(bot=bot))

async def teardown(bot: Bot):
  await bot.remove_cog(Jishaku(bot=bot))
  log.info("unloaded")
