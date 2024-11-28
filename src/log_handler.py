import logging
import os
from discord import Webhook
import aiohttp
import urllib.request

def splitter(log: str, max_length: int = 1990):
  """
  文字列を指定位置以内で最も長くなる改行で分割する

  Args:
      log (str): 分割するログ文字列
      max_length (int, optional): 最大文字数. Defaults to 1990.

  Returns:
      list: 分割された文字列のリスト
  """

  result = []
  if len(log) <= max_length:
    return [log]

  # リミット付近の改行位置を探す
  for i in range(max_length - 1, -1, -1):
    print(i)
    if log[i] == '\n':
      result.append(log[:i+1])
      print(result)
      return result + splitter(log[i+1:], max_length)

  # 改行が見つからない場合は、max_lengthで強制的に分割
  result.append(log[:max_length])
  print(result)
  return result + splitter(log[max_length:], max_length)

class DiscordWebHookHandler(logging.Handler):
  def __init__(self):
    async def fake_webhook(msg):
      urllib.request.urlopen(
        urllib.request.Request(
          self.webhook,
          data=json.dumps({
            "content": "sync webhook:\n" + msg
          }).encode(),
          headers={
            "Content-Type": "application/json",
            "User-Agent": "DiscordBot (private use) Python-urllib/3.10",
          },
        )
      ).close()

    self.webhook = fake_webhook

    async def setup_webhook(this):
      async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(os.environ["LOG_WEBHOOK"], session=session)
        this.webhook = webhook.send

    asyncio.create_task(setup_webhook(self))
    super().__init__()

  def emit(self, record):
    try:
      for chunk in splitter(self.format(record)):
        asyncio.create_task(self.webhook("```js\n" + chunk + "\n```"))
    except Exception: # pylint: disable=broad-exception-caught
      self.handleError(record)
