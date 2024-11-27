from discord.ext import commands
import discord
from src.bot import Bot

import aiohttp

import logging
log = logging.getLogger(__name__)

class NekoCog(commands.Cog, name = __name__):
  def __init__(self, bot: Bot):
    self.bot = bot

  @commands.command(description="TheCatAPIを使用してネコの画像を取得します")
  async def neko(self, ctx):
    cat = (await (await session.get("https://api.thecatapi.com/v1/images/search")).json())[0]
    async with aiohttp.ClientSession() as session:
      await ctx.reply(
        embed = discord.Embed().set_image(url = cat["url"]).set_footer(title = "id: "+cat["id"])
      )

async def setup(bot: Bot):
  log.info("loaded")
  await bot.add_cog(NekoCog(bot))

async def teardown(_bot: Bot):
  log.info("unloaded")
