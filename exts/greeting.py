from discord.ext import commands

import logging
log = logging.getLogger(__name__)

class GreetingCog(commands.Cog, name = __name__):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_user_message(self, msg):
    match msg.content:
      case "おはよう" | "おは":
        await msg.reply("おは")
      case "おやすみ":
        await msg.reply("おやすみ")

async def setup(bot: commands.Bot):
  log.info("loaded")
  await bot.add_cog(GreetingCog(bot))

async def teardown(_bot: commands.Bot):
  log.info("unloaded")
