import asyncio
import os
import pty
import shlex
import subprocess
from typing import Optional

import discord
from discord.ext import commands
import logging

log = logging.getLogger(__name__)

# 許可するユーザーID（自分のIDに置き換える）
ALLOWED_USER_IDS = {1218933751950872728}


def is_authorized(ctx):
  return ctx.author.id in ALLOWED_USER_IDS or ctx.author.id == ctx.bot.owner_id


class ShellSession:
  """PTY を使った対話型プロセスのセッション管理"""

  def __init__(self, ctx, command, loop, cog):
    self.ctx = ctx
    self.command = command
    self.loop = loop
    self.cog = cog

    # PTY を開く
    self.master_fd, self.slave_fd = pty.openpty()
    os.set_blocking(self.master_fd, False)

    try:
      self.proc = subprocess.Popen(
        command,
        stdin=self.slave_fd,
        stdout=self.slave_fd,
        stderr=self.slave_fd,
        preexec_fn=os.setsid,
        close_fds=True,
      )
    except Exception as e:
      os.close(self.master_fd)
      os.close(self.slave_fd)
      raise e

    os.close(self.slave_fd)

    self.buffer = b""
    self.closed = False
    self._flush_task = None
    self.loop.add_reader(self.master_fd, self._read_callback)

  def _read_callback(self):
    if self.closed:
      return
    try:
      data = os.read(self.master_fd, 4096)
    except BlockingIOError:
      return
    except OSError:
      self._close()
      asyncio.create_task(self.ctx.send("**シェルが終了しました（エラー）**"))
      return

    if data:
      self.buffer += data
      if self._flush_task is None or self._flush_task.done():
        self._flush_task = asyncio.create_task(self._flush_output())
    else:
      self._close()
      asyncio.create_task(self.ctx.send("**シェルが終了しました（EOF）**"))

  async def _flush_output(self):
    await asyncio.sleep(0.1)
    if self.closed:
      return
    if self.buffer:
      text = self.buffer.decode("utf-8", errors="replace")
      self.buffer = b""
      while text:
        chunk = text[:1990]
        text = text[1990:]
        await self.ctx.send(f"```\n{chunk}\n```")
      self._flush_task = None

  def write(self, data: str):
    if self.closed:
      return
    try:
      os.write(self.master_fd, data.encode())
    except OSError:
      self._close()

  def _close(self):
    if self.closed:
      return
    self.closed = True
    self.loop.remove_reader(self.master_fd)
    try:
      os.close(self.master_fd)
    except OSError:
      pass

    try:
      self.proc.terminate()
      self.proc.wait(timeout=1)
    except Exception:
      try:
        self.proc.kill()
        self.proc.wait()
      except Exception:
        pass

    if self.cog:
      self.cog._remove_session(self.ctx.channel.id, self.ctx.author.id)


class PseudoSSHCog(commands.Cog, name=__name__):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.sessions = {}

  def _remove_session(self, channel_id, user_id):
    self.sessions.pop((channel_id, user_id), None)

  async def cog_unload(self):
    for session in self.sessions.values():
      session._close()
    self.sessions.clear()

  @commands.group(name="ssh", invoke_without_command=False)
  @commands.check(is_authorized)
  async def ssh(self, ctx):
    """SSH風対話型シェルコマンドグループ"""
    if ctx.invoked_subcommand is None:
      await ctx.send_help(ctx.command)

  @ssh.command(name="start", aliases=["connect", "open"])
  async def ssh_start(self, ctx, *, command: str = ""):
    """対話型シェルを開始する。例: !ssh start ssh user@host"""
    if (ctx.channel.id, ctx.author.id) in self.sessions:
      await ctx.send("既にセッションが存在します。`!ssh stop` で終了してください。")
      return

    if not command:
      args = ["/bin/bash"]
    else:
      args = shlex.split(command)
      if not args:
        args = ["/bin/bash"]

    loop = asyncio.get_running_loop()
    try:
      session = ShellSession(ctx, args, loop, self)
    except Exception as e:
      await ctx.send(f"プロセスの起動に失敗しました: {e}")
      return

    self.sessions[(ctx.channel.id, ctx.author.id)] = session
    await ctx.send(
      "**シェルセッションを開始しました。**\n"
      "以降、このチャンネルでのあなたのメッセージはすべてプロセスに送信されます。\n"
      "終了するには `exit` を送るか、`!ssh stop` を実行してください。"
    )

  @ssh.command(name="stop", aliases=["close", "end"])
  async def ssh_stop(self, ctx):
    """アクティブなシェルセッションを強制終了する"""
    key = (ctx.channel.id, ctx.author.id)
    session = self.sessions.pop(key, None)
    if session:
      session._close()
      await ctx.send("セッションを終了しました。")
    else:
      await ctx.send("アクティブなセッションはありません。")

  @ssh.command(name="status")
  async def ssh_status(self, ctx):
    """現在のセッション状態を表示"""
    key = (ctx.channel.id, ctx.author.id)
    if key in self.sessions:
      await ctx.send("セッションがアクティブです。")
    else:
      await ctx.send("アクティブなセッションはありません。")

  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author.bot:
      return

    # コマンドプレフィックス付きのメッセージはシェルに送らない
    if message.content.startswith("!"):
      return

    key = (message.channel.id, message.author.id)
    session = self.sessions.get(key)
    if session:
      session.write(message.content + "\n")


async def setup(bot: commands.Bot):
  log.info("loaded")
  await bot.add_cog(PseudoSSHCog(bot))


async def teardown(_bot: commands.Bot):
  log.info("unloaded")