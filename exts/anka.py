from discord.ext import commands

import re
import uuid

import logging
log = logging.getLogger(__name__)

class AnkaCog(commands.Cog, name = __name__):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.ankas = {}

  @commands.group()
  async def anka(self, ctx):
    if ctx.invoked_subcommand is not None:
      return

    res = []
    for _k, v in self.ankas.items():
      if v["msg"].channel.id == ctx.channel.id:
        res.append(f'>>{v["target"]} ({v["count"]}/{v["target"]}) {v["msg"].jump_url}')

    await ctx.reply(f'{len(res)}個の安価が進行中です!\n' + "\n".join(res))

  @commands.Cog.listener()
  async def on_user_message(self, msg):
    rm = []
    m = ""
    for k, v in self.ankas.items():
      if v["msg"].channel.id == msg.channel.id:
        v["count"] += 1
        if v["count"] == v["target"]: # and k not in rm
          rm.append(k)
          m += f'[>>{v["target"]}]({v["msg"].jump_url}) <@{v["msg"].author.id}>\n'

    if m != "":
      await msg.reply("安価されました\n" + m)

    for k in rm:
      del self.ankas[k]

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

async def setup(bot: commands.Bot):
  log.info("loaded")
  await bot.add_cog(AnkaCog(bot))

async def teardown(_bot: commands.Bot):
  log.info("unloaded")
