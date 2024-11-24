from discord.ext import commands
from src.bot import Bot

import logging
log = logging.getLogger(__name__)

class NewsManagerCog(commands.Cog, name = __name__):
  def __init__(self, bot: Bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    log.info("loaded")

  @commands.Cog.listener()
  async def on_thread_update(self, _before, after):
    if after.parent_id == 1289987225617956988: # if news
      if after.archived:
        await after.edit(archived=False)
        log.info(f'Reopen thread: [{after.name}]({after.jump_url})')

async def setup(bot: Bot):
  await bot.add_cog(NewsManagerCog(bot))

async def teardown(_bot: Bot):
  log.info("unloaded")
