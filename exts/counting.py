from discord.ext import commands
import asyncio

import logging
log = logging.getLogger(__name__)

class CountingCog(commands.Cog, name = __name__):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.count: int = 0

  @commands.Cog.listener()
  async def on_reaction_add(self, reaction, user):
    if user.id == 510016054391734273: # counting bot
      match reaction.emoji:
        case "✅" | "💯":
          self.count += 1
        case "❌":
          self.count = 0

      await asyncio.sleep(0.7)
      await reaction.message.add_reaction(reaction.emoji)

  @commands.group(aliases=["c"])
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
    await ctx.reply(f"now: {self.count}")

  @counting.command()
  async def next(self, ctx):
    await ctx.reply(f"next: {self.count + 1}")

async def setup(bot: commands.Bot):
  log.info("loaded")
  await bot.add_cog(CountingCog(bot))

async def teardown(_bot: commands.Bot):
  log.info("unloaded")
