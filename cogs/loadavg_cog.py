import discord
import os
from discord.ext import commands
from discord.commands import slash_command


class LoadAvg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="loadavg", description="Get system load average (1, 5, 15 min)")
    async def loadavg(self, ctx):
        if hasattr(os, "getloadavg"):
            load1, load5, load15 = os.getloadavg()
            embed = discord.Embed(
                title="📊 Load Average",
                description=(
                    f"**1 min:** `{load1:.2f}`\n"
                    f"**5 min:** `{load5:.2f}`\n"
                    f"**15 min:** `{load15:.2f}`"
                ),
                color=discord.Color.orange()
            )
        else:
            embed = discord.Embed(
                title="❌ Load Average Not Supported",
                description="This command only works on Unix-like systems (Linux/macOS).",
                color=discord.Color.red()
            )

        embed.set_footer(text="👩‍💻 Developed by blueskychan_")
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(LoadAvg(bot))
