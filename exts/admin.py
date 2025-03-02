from discord.ext import commands

import asyncio

import logging
log = logging.getLogger(__name__)

async def run(cmd):
  proc = await asyncio.create_subprocess_shell(
    cmd,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE
  )

  stdout, _stderr = await proc.communicate()

  # print(f'[{cmd!r} exited with {proc.returncode}]')
  if stdout:
    return stdout.decode()
  return "\n"
  # if stderr:
  #   print(f'[stderr]\n{stderr.decode()}')

async def run_log(cmd: str) -> str:
  return f'$ {cmd} \n{await run(cmd)}\n'

class AdminCog(commands.Cog, name=__name__, command_attrs={ "hidden": True }):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.command()
  @commands.is_owner()
  async def update(self, ctx):
    msg = await ctx.reply("🔁 Starting update")

    l = ""
    l += await run_log("git pull")
    l += await run_log("git pull --depth=1")
    l += await run_log("git log")

    log.info(l)

    await msg.edit(content=f"```\n{l}```")

async def setup(bot: commands.Bot):
  log.info("loaded")
  await bot.add_cog(AdminCog(bot))

async def teardown(_bot: commands.Bot):
  log.info("unloaded")
