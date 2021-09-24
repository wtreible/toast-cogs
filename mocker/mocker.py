from redbot.core import checks, Config
from redbot.core.i18n import Translator, cog_i18n
import discord
from redbot.core import commands
import asyncio

_ = Translator("Mocker", __file__)

class Mocker(commands.Cog):
  """Mocks users or creates mocking text a la the spongebob meme"""

  def __init__(self, bot):
    self.bot = bot
  
  @commands.command()
  async def mockme(self, ctx, *args):
    """A command that sends the Spongebob Mocking meme text."""
    await ctx.send(self._mock_string(' '.join(args).lower()))
    
  @commands.command()
  async def mockthem(self, ctx):
    """A command that Spongebob mocks the previous message."""
    if _check_if_reply(self, ctx.message):
      msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
      await ctx.send(self._mock_string(msg.content.lower()))
    else:
      ind = 0
      async for msg in ctx.message.channel.history(limit=10):
        if msg.author != ctx.author.id and ind > 0:
          await ctx.send(self._mock_string(msg.content.lower()))
          break
        ind+=1
      
  def _mock_string(self, msg):
    out_msg = ''
    cap_flag = False
    for ch in msg:
      if ch.isalpha():
        if cap_flag:
          out_msg += ch.upper()
          cap_flag = False
        else:
          out_msg += ch
          cap_flag = True
      else:
        out_msg += ch
    return out_msg
    
  def _check_if_reply(self, m):
    if m.reference is not None:
      return True
    return False