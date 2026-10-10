from discord.ext import commands
import discord

import logging
log = logging.getLogger(__name__)

class ExampleCog(commands.Cog, name = __name__):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_member_join(self, member: discord.Member):
    if member.guild.id != 1255359848644608035:
      return

    if member.bot:
      role_id = 1172443916474265632
    else:
      role_id = 1172444634195185725

    role = member.guild.get_role(role_id)
    if role is None:
      raise ValueError("Couldn't fetch role")

    await member.add_roles(role, reason="auto-role")

async def setup(bot: commands.Bot):
  log.info("loaded")
  await bot.add_cog(ExampleCog(bot))

async def teardown(_bot: commands.Bot):
  log.info("unloaded")
