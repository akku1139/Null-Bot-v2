from discord.ext import commands
from src.bot import Bot

import re
import uuid

import logging
log = logging.getLogger(__name__)

class AnkaCog(commands.Cog, name = __name__):
  def __init__(self, bot: Bot):
    self.bot = bot
    self.ankas = {}

  @commands.group()
  async def anka(self, ctx):
    res = []
    for _k, v in self.ankas.items():
      if v["msg"].channel.id == ctx.channel.id:
        res.append(f'>>{v["target"]} ({v["count"]}/{v["target"]})')

    await ctx.reply(f'{len(res)}個の安価が進行中です!' + "\n".join(res))

  @commands.Cog.listener()
  async def on_ready(self):
    log.info("loaded")

  @commands.Cog.listener()
  async def on_message(self, msg):
    if msg.author.bot:
      return

    rm = []
    for k, v in self.ankas.items():
      if v["msg"].channel.id == msg.channel.id:
        v["count"] += 1
        if v["count"] == v["target"]:
          rm.append(k)
          v["msg"].reply(f'>>{v["target"]} {msg.jump_url}')

    for k in rm:
      del self.ankas["k"]

    t = re.findall(">>(\\d+)", msg.content)
    for p in t:
      u = int(p)
      if 0 < u < 50:
        self.ankas[str(uuid.uuid4())] = {
          "msg": msg,
          "target": u,
          "count": 0,
        }

  @anka.command(hidden=True)
  @commands.is_owner()
  async def showall(self, ctx):
    await ctx.reply(str(self.ankas))

async def setup(bot: Bot):
  await bot.add_cog(AnkaCog(bot))

async def teardown(bot: Bot):
  await bot.remove_cog("AnkaCog")
  log.info("unloaded")
