# Super thanks https://github.com/kintsuba/misskey-login-bonus-bot

from discord.ext import commands, tasks
from src.bot import Bot

import os.path
import json
# import datetime

import aiofiles

import logging
log = logging.getLogger(__name__)

DATAPATH = f'{os.path.dirname(__file__)}/../../data/login_bonus.json'
KEYWORDS = ["ログボ", "ろぐぼ", "ログインボーナス", "ろぐいんぼーなす", "ログインボーニャス", "ろぐい んぼーにゃす", "login"]

class LoginBonusCog(commands.Cog, name = __name__):
  def __init__(self, bot: Bot):
    self.bot = bot
    self.data = {}

  # looks not working...
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
    log.info("login_bonus.json saved")

  @commands.Cog.listener()
  async def user_message(self, msg):
    if any(keyword in msg.content for keyword in KEYWORDS):
      self.data.setdefault(
        str(msg.author.id),
        {
          "last": "",
          "total": 0,
        }
      )
      # get last login date
      # https://qiita.com/dkugi/items/8c32cc481b365c277ec2
      # https://note.nkmk.me/python-datetime-usage/#datetoday
      await msg.add_reaction("⭕")
      await msg.reply("Wip: ログインを確認しました!")

async def setup(bot: Bot):
  log.info("loaded")
  await bot.add_cog(LoginBonusCog(bot))

async def teardown(_bot: Bot):
  log.info("unloaded")
