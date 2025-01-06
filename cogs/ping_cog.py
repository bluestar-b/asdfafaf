import discord
import subprocess
from discord.ext import commands
from discord.commands import slash_command


def ping_cloudflare():
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "1.1.1.1"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output = result.stdout
        if "time=" in output:
            latency = output.split("time=")[1].split(" ")[0]
            return float(latency)
        else:
            return None
    except Exception as e:
        print(f"Error pinging Cloudflare: {e}")
        return None


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="ping", description="Check bot latency and network ping to Cloudflare.")
    async def ping(self, ctx):
        bot_latency = round(self.bot.latency * 1000)
        
        cloudflare_ping = ping_cloudflare()
        if cloudflare_ping is None:
            cloudflare_ping = "Timed out"
        else:
            cloudflare_ping = f"{round(cloudflare_ping)} ms"

        embed = discord.Embed(
            title="Pong!",
            color=discord.Color.green()
        )
        embed.add_field(name="Bot Latency", value=f"{bot_latency} ms", inline=False)
        embed.add_field(name="Network Ping (Cloudflare)", value=cloudflare_ping, inline=False)
        
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Ping(bot))
