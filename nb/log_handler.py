import logging
import os
from discord import SyncWebhook

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
    self.webhook = SyncWebhook.from_url(
      os.environ['LOG_WEBHOOK']
    )
    self.console = logging.StreamHandler()
    super().__init__()

  def emit(self, record):
    self.console.emit(record)
    try:
      for chunk in splitter(self.format(record)):
        self.webhook.send("```js\n" + chunk + "\n```")
    except Exception:
      self.handleError(record)
