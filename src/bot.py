from discord.ext import commands

class Bot(commands.Bot):
  async def is_owner(self, user):
      if 1 == 0:  # Implement your own conditions here
          return True
       # Else fall back to the original
      return await super().is_owner(user)  
