from discord.ext import commands
from src.bot import Bot

import logging
log = logging.getLogger(__name__)

class CountingCog(commands.Cog, name = __name__):
  def __init__(self, bot: Bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_reaction_add(self, reaction, user):
    if user.id == 510016054391734273: # counting bot
      await reaction.message.add_reaction(reaction.emoji)

async def setup(bot: Bot):
  log.info("loaded")
  await bot.add_cog(CountingCog(bot))

async def teardown(_bot: Bot):
  log.info("unloaded")
