import io
import logging
from typing import Optional, TYPE_CHECKING

import discord
from discord.ext.commands import BadArgument, Converter
from gtts import gTTS
from gtts.lang import _fallback_deprecated_lang, tts_langs
from redbot.core import Config, commands
from redbot.core.bot import Red
from redbot.core.commands import Cog

log = logging.getLogger("red.fox_v3.tts")

if TYPE_CHECKING:
  ISO639Converter = str
else:
  class ISO639Converter(Converter):
    async def convert(self, ctx, lang) -> str:
      try:
        langs = tts_langs()
        if _fallback_deprecated_lang(lang) not in langs:
          raise BadArgument("Language not supported: %s" % lang)
      except RuntimeError as e:
        log.debug(str(e), exc_info=True)
        log.warning(str(e))

      return lang


class ToastTTS(Cog):
  """
  Send Text-to-Speech messages
  """

  def __init__(self, bot: Red, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.bot = bot

    self.config = Config.get_conf(self, identifier=9811198108111121, force_registration=True)
    default_global = {}
    default_guild = {"language": "en"}

    self.config.register_global(**default_global)
    self.config.register_guild(**default_guild)

  async def red_delete_data_for_user(self, **kwargs):
    """Nothing to delete"""
    return

  @commands.mod()
  @commands.command()
  async def ttsset(self, ctx: commands.Context, lang: ISO639Converter):
    """
    Sets the default language for TTS in this guild.

    Default is `en` for English
    """
    await self.config.guild(ctx.guild).language.set(lang)
    await ctx.send(f"Default tts language set to {lang}")

  @commands.command()
  async def ttslangs(self, ctx: commands.Context):
    avail_langs = str(list(tts_langs()))
    ref_url = "https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes"
    await ctx.send(f"Available languages: {avail_langs}\n >> For reference: {ref_url}")

  @commands.command()
  async def tts(
    self, ctx: commands.Context, lang: Optional[ISO639Converter] = None, *, text: str
  ):
    """
    Send Text to speech messages as an mp3
    """
    if lang is None:
      lang = await self.config.guild(ctx.guild).language()
    await ctx.send(file=self._make_tts_mp3(text, lang))
  
  @commands.command()
  async def ttsthem(
    self, ctx: commands.Context, lang: Optional[ISO639Converter] = None
  ):
    """
    Send Text to speech messages as an mp3
    """
    if lang is None:
      lang = await self.config.guild(ctx.guild).language()
    if self._check_if_reply(ctx.message):
      msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
      text = msg.content
      await ctx.send(file=self._make_tts_mp3(text, lang))
    else:
      ind = 0
      async for msg in ctx.message.channel.history(limit=10):
        if msg.author != ctx.author.id and ind > 0:
          text = msg.content
          await ctx.send(file=self._make_tts_mp3(text, lang))
          break
        ind+=1
    
  def _make_tts_mp3(self, text, lang):
    mp3_fp = io.BytesIO()
    tts = gTTS(text, lang=lang)
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    out_text = "_".join(text.split())
    return discord.File(mp3_fp, f"{out_text}.mp3")
  
  def _check_if_reply(self, m):
    if m.reference is not None:
      return True
    return False