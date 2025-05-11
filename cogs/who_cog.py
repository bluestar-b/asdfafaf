import discord
import subprocess
from discord.ext import commands
from discord.commands import slash_command


class SystemMonitor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="who", description="See who's online on the Linux system")
    async def who(self, ctx):
        try:
            # Execute the 'who' command to get user info
            who_output = subprocess.check_output("who", shell=True, text=True)
            
            if not who_output:
                await ctx.respond("😕 No users are currently logged in.")
                return
            
            # Prepare the response
            embed = discord.Embed(
                title="👥 Who's Online",
                description=who_output,
                color=discord.Color.blurple()
            )
            await ctx.respond(embed=embed)
        except Exception as e:
            await ctx.respond(f"❌ Error: {e}")


def setup(bot):
    bot.add_cog(SystemMonitor(bot))
