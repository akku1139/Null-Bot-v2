from discord.ext import commands
from src.bot import Bot

import logging
log = logging.getLogger(__name__)

class CountingCog(commands.Cog, name = __name__):
  def __init__(self, bot: Bot):
    self.bot = bot
    self.count: int = 0

  @commands.Cog.listener()
  async def on_reaction_add(self, reaction, user):
    if user.id == 510016054391734273: # counting bot
      match reaction.emoji:
        case "✅":
          self.count += 1
        case "❌":
          self.count = 0

      await reaction.message.add_reaction(reaction.emoji)

  @commands.group()
  async def counting(self, ctx):
    pass

  @counting.command(hidden=True)
  @commands.is_owner()
  async def setcount(self, ctx, count: int):
    if count < 0:
      await ctx.reply("0以上の整数を渡してください")
      return
    self.count = count
    await ctx.reply(f"カウントが更新されました: {count}")

  @counting.command()
  async def now(self, ctx):
    await ctx.reply(f"next: {self.count}")

  @counting.command()
  async def next(self, ctx):
    await ctx.reply(f"next: {self.count + 1}")

async def setup(bot: Bot):
  log.info("loaded")
  await bot.add_cog(CountingCog(bot))

async def teardown(_bot: Bot):
  log.info("unloaded")
