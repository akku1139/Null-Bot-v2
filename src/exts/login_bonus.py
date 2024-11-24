# Super thanks https://github.com/kintsuba/misskey-login-bonus-bot

from discord.ext import commands, tasks
from src.bot import Bot

import os.path
import json

import aiofiles

import logging
log = logging.getLogger(__name__)

DATAPATH = f'{os.path.dirname(__file__)}/../../data/login_bonus.json'
data = {}

async def save_data():
  async with aiofiles.open(DATAPATH, mode="w") as f:
    await f.write(json.dumps(data, indent=2, ensure_ascii=False))

class LoginBonusCog(commands.Cog, name = __name__):
  def __init__(self, bot: Bot):
    self.bot = bot

  @tasks.loop(hours=5)
  async def save_data_cog():
    await save_data()

  @commands.Cog.listener()
  async def on_ready(self):
    log.info("loaded")

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
      msg.reply("Wip: ログインを確認しました!")

async def setup(bot: Bot):
  global data
  async with aiofiles.open(DATAPATH, mode="r") as f:
    contents = await f.read()
  data = json.loads(contents)

  await bot.add_cog(LoginBonusCog(bot))

async def teardown(_bot: Bot):
  await save_data()
  log.info("unloaded")
