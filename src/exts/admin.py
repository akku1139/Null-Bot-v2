from discord.ext import commands
from src.bot import Bot

import subprocess

import logging
log = logging.getLogger(__name__)

class AdminCog(commands.Cog, name=__name__, command_attrs={ "hidden": True }):
  def __init__(self, bot: Bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    log.info("loaded")

  @commands.command()
  @commands.is_owner()
  async def update(self, ctx):
    await ctx.reply("🔁 Starting update")

    l  = "$ git pull\n"
    l += subprocess.run(["git","pull"], capture_output=True, text=True, check=False).stdout
    l += "\n$ git pull --depth=1\n"
    l += subprocess.run(["git","pull","--depth=1"], capture_output=True, text=True, check=False).stdout
    l += "\n$ git log\n"
    l += subprocess.run(["git","log"], capture_output=True, text=True, check=False).stdout

    log.info(l)

    await ctx.reply(f"```\n{l}```")

async def setup(bot: Bot):
  await bot.add_cog(AdminCog(bot))

async def teardown(_bot: Bot):
  log.info("unloaded")
