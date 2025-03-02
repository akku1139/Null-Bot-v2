from discord.ext import commands, tasks

import aiofiles
import json
import os

import logging
log = logging.getLogger(__name__)

DATAPATH = f'{os.path.dirname(__file__)}/../../data/anki.json'

class AnkiCog(commands.Cog, name = __name__):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.data = {}

  async def cog_load(self):
    async with aiofiles.open(DATAPATH, mode="r") as f:
      contents = await f.read()
    self.data = json.loads(contents)
    self.save_data.start()

  async def cog_unload(self):
    await self.save_data()

  @tasks.loop(hours=5)
  async def save_data(self):
    async with aiofiles.open(DATAPATH, mode="w") as f:
      await f.write(json.dumps(self.data, indent=2, ensure_ascii=False))
    log.info("anki.json saved")

async def setup(bot: commands.Bot):
  log.info("loaded")
  await bot.add_cog(AnkiCog(bot))

async def teardown(_bot: commands.Bot):
  log.info("unloaded")
