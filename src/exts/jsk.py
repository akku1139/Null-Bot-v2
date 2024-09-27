from src.bot import Bot
from jishaku.cog import Jishaku

async def setup(bot: Bot):
  # I don't recommend doing this!
  await bot.add_cog(Jishaku(bot=bot))
