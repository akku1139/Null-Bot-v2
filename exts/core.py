from discord.ext import commands

import logging
log = logging.getLogger(__name__)

class CoreCog(commands.Cog, name = __name__):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_message(self, msg):
    if msg.author.bot:
      return
    self.bot.dispatch("user_message", msg)

async def setup(bot: commands.Bot):
  log.info("loaded")
  await bot.add_cog(CoreCog(bot))

async def teardown(_bot: commands.Bot):
  log.info("unloaded")
