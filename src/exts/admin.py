from discord.ext import commands
from src.bot import Bot

import subprocess

import logging
log = logging.getLogger(__name__)

async def run(cmd):
  proc = await asyncio.create_subprocess_shell(
    cmd,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE
  )

  stdout, stderr = await proc.communicate()

  # print(f'[{cmd!r} exited with {proc.returncode}]')
  if stdout:
    return stdout.decode()
  else:
    return "\n"
  # if stderr:
  #   print(f'[stderr]\n{stderr.decode()}')

class AdminCog(commands.Cog, name=__name__, command_attrs={ "hidden": True }):
  def __init__(self, bot: Bot):
    self.bot = bot

  @commands.command()
  @commands.is_owner()
  async def update(self, ctx):
    msg = await ctx.reply("🔁 Starting update")

    l  = "$ git pull\n"
    l += await run("git pull", capture_output=True, text=True, check=False)
    l += "\n$ git pull --depth=1\n"
    l += await run("git pull --depth=1", capture_output=True, text=True, check=False)
    l += "\n$ git log\n"
    l += await run("git log", capture_output=True, text=True, check=False)

    log.info(l)

    await msg.edit(content=f"```\n{l}```")

async def setup(bot: Bot):
  log.info("loaded")
  await bot.add_cog(AdminCog(bot))

async def teardown(_bot: Bot):
  log.info("unloaded")
