from discord.ext import commands
from src.bot import Bot

import random
import datetime

import logging
log = logging.getLogger(__name__)

timeout_messages = [
  "されたけりゃさせてやるよ（震え声）",
  "とおっ",
  "じゃあばよ",
  "では、さらばだ。",
  "やったる。",
  "殺ったる (確信)",
  "ヤッたる (変な目)",
]

class TOCog(commands.Cog, name = __name__):
  def __init__(self, bot: Bot):
    self.bot = bot

  @commands.Cog.listener()
  async def user_message(self, message):
    msg = message.content
    if msg in [
      "Timeoutされたーい", "TOされたーい", "タイムアウトされたーい", "timeoutされたーい", "タイムアウトされたい", "Timeoutされたい", "TOされたい", "timeoutされたい"
    ]:
      await message.author.timeout(datetime.timedelta(minutes=5), reason="Timeoutされたーい")
      await message.reply(random.choice(timeout_messages))

async def setup(bot: Bot):
  log.info("loaded")
  await bot.add_cog(TOCog(bot))

async def teardown(_bot: Bot):
  log.info("unloaded")
