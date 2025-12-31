import logging
import os
import asyncio
import json
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
    super().__init__()

    # 送信バッファ
    self.queue: asyncio.Queue[str] = asyncio.Queue(maxsize=1000)

    async def fake_webhook(msg):
      with ( urllib.request.urlopen(
        urllib.request.Request(
          os.environ["LOG_WEBHOOK"],
          data=json.dumps({
            "content": "sync webhook:\n" + msg
          }).encode(),
          headers={
            "Content-Type": "application/json",
            "User-Agent": "DiscordBot (private use) Python-urllib/3.10",
          },
        )
      ) ) as _req:
        return

    self.webhook = fake_webhook

    async def setup_webhook(this):
      session = aiohttp.ClientSession()
      webhook = Webhook.from_url(os.environ["LOG_WEBHOOK"], session=session)
      this.webhook = webhook.send

    async def worker(this):
      """
      キューに溜まったログを順番に送信するワーカー
      """
      while True:
        msg = await this.queue.get()
        try:
          await this.webhook(msg)
          # Discord webhook はだいたい 5req / 2sec 程度
          await asyncio.sleep(0.5)
        except Exception:
          # 送信失敗時は捨てる（ログでログ死を防ぐ）
          pass
        finally:
          this.queue.task_done()

    # 非同期初期化
    asyncio.create_task(setup_webhook(self))
    asyncio.create_task(worker(self))

  def emit(self, record):
    """
    emitでは「送信しない」
    キューに積むだけ
    """
    try:
      formatted = self.format(record)
      for chunk in splitter(formatted):
        payload = "```js\n" + chunk + "\n```"
        try:
          self.queue.put_nowait(payload)
        except asyncio.QueueFull:
          # バッファ溢れたら潔く捨てる
          pass
    except Exception:
      self.handleError(record)
