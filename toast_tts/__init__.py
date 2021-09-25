from .toast-tts import ToastTTS

def setup(bot):
  bot.add_cog(ToastTTS(bot))
