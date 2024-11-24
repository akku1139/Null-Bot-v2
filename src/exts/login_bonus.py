# Super thanks https://github.com/kintsuba/misskey-login-bonus-bot

from discord.ext import commands, tasks
from src.bot import Bot

import os.path
import json

import aiofiles

import logging
log = logging.getLogger(__name__)

DATAPATH = f'{os.path.dirname(__file__)}/../../data/login_bonus.json'

class LoginBonusCog(commands.Cog, name = __name__):
  def __init__(self, bot: Bot):
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

  @commands.Cog.listener()
  async def on_message(self, msg):
    if msg.author.bot:
      return

    c = msg.content

    if (
      "ログボ" in c
      or "ログインボーナス" in c
      or "ろぐいんぼーなす" in c
      or "ろぐぼ" in c
      or "login" in c
    ):
      await msg.reply("Wip: ログインを確認しました!")

async def setup(bot: Bot):
  log.info("loaded")
  await bot.add_cog(LoginBonusCog(bot))

async def teardown(_bot: Bot):
  log.info("unloaded")
