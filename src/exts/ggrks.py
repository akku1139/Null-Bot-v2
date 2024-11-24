from discord.ext import commands
from src.bot import Bot

import urllib.parse

import logging
log = logging.getLogger(__name__)

class GgrksCog(commands.Cog, name = __name__):
  def __init__(self, bot: Bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    log.info("loaded")

  @commands.Cog.listener()
  async def on_message(self, msg):
    if msg.author.bot:
      return

    m = msg.content

    ggrks = m.removesuffix("って何?").removesuffix("って何？").removesuffix("ってなに？").removesuffix("ってなに？").removesuffix("って何").removesuffix("ってなに")
    if ggrks != m:
      await msg.reply(
        "自分で調べることは非常に重要です。\n"+
        "https://ggrks.world/" + ggrks.replace(" ", "+")
      )
      return

    ggrks = m.removesuffix(" 検索").removesuffix(" [search]").removesuffix("　検索").removesuffix("　[search]")
    if ggrks != m:
      await msg.reply("https://google.com/search?q=" + urllib.parse.quote_plus(ggrks))
      return

async def setup(bot: Bot):
  await bot.add_cog(GgrksCog(bot))

async def teardown(_bot: Bot):
  log.info("unloaded")
