from .mocker import Mocker

def setup(bot):
    bot.add_cog(Mocker(bot))