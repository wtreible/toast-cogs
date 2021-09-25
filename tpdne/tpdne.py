from redbot.core import checks, Config
from redbot.core.i18n import Translator, cog_i18n
import discord
from redbot.core import commands
import asyncio
import requests
import io

_ = Translator("TPDNE", __file__)

class TPDNE(commands.Cog):
  """Mocks users or creates mocking text a la the spongebob meme"""

  def __init__(self, bot):
    self.bot = bot
    self.request_url = "https://thispersondoesnotexist.com/image"
    
  @commands.command(alias=['tpdne', 'TPDNE'])
  async def thispersondoesnotexist(self, ctx, *args):
    """Uses an AI model to generate pictures of people who don't really exist."""
    img_bytes = self.get_online_person()
    img_fp = io.BytesIO(img_bytes)
    embed_img = discord.File(img_fp, f"thispersondoesnotexist.jpg")
    await ctx.send(file=embed_img)

  def get_online_person(self) -> bytes:
    """Get a picture of a fictional person from the ThisPersonDoesNotExist webpage.
    :return: the image as bytes
    """
    r = requests.get(self.request_url, headers={'User-Agent': 'My User Agent 1.0'}).content
    return r
    
  def save_picture(picture: bytes, file: str = None) -> int:
    """Save a picture to a file.
    The picture must be provided as it content as bytes.
    The filename must be provided as a str with the absolute or relative path where to store it.
    :param picture: picture content as bytes
    :param file: filename as string, relative or absolute path (optional)
    :return: int returned by file.write
    """
    with open(file, "wb") as f:
      return f.write(picture)