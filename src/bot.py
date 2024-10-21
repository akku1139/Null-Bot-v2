from discord.ext import commands
from logging import getLogger
log = getLogger("bot")

class Bot(commands.Bot):
  async def is_owner(self, user):
    ret = False
    if 1 == 0:  # Implement your own conditions here
      ret = True
    # Else fall back to the original
    ret = await super().is_owner(user)
    log.info(f"owner check {user.name} ({user.id}): {ret}")
    return ret
