import discord
import psutil
import platform
import time
from discord.ext import commands
from discord.commands import slash_command


class SysInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="sysinfo", description="Get system information")
    async def sysinfo(self, ctx):
        # Collect system information
        system_info = {
            "Host": platform.node(),
            "OS": platform.platform(),
            "Kernel": platform.release(),
            "CPU": self.get_cpu_info(),
            "RAM": self.get_memory_info(),
            "Storage": self.get_disk_info(),
            "Uptime": self.get_uptime()
        }

        # Create embed for displaying the information
        embed = discord.Embed(
            title="📈System Information📈",
            color=discord.Color.blue()
        )

        for field_name, field_value in system_info.items():
            embed.add_field(name=self.format_field_name(field_name), value=field_value, inline=False)

        embed.set_footer(text="👩‍💻 Developed by blueskychan_")
        embed.add_field(name="Check Realtime Server Usage", value="[Click here](https://status.fusemeow.codes/)", inline=False)

        await ctx.respond(embed=embed)

    def get_cpu_info(self):
        cpu_count = psutil.cpu_count(logical=False)
        cpu_freq = psutil.cpu_freq().current  # Current CPU frequency
        cpu_percent = psutil.cpu_percent(interval=1)
        return f"{cpu_count} cores @ {cpu_freq}MHz (CPU Load: {cpu_percent}%)"

    def get_memory_info(self):
        memory_info = psutil.virtual_memory()
        return f"{memory_info.used / (1024**3):.2f}GB / {memory_info.total / (1024**3):.2f}GB ({memory_info.percent}%)"

    def get_disk_info(self):
        disk_info = psutil.disk_usage('/')
        return f"{disk_info.used / (1024**3):.2f}GB / {disk_info.total / (1024**3):.2f}GB ({disk_info.percent}%)"

    def get_uptime(self):
        uptime_seconds = time.time() - psutil.boot_time()
        return self.format_uptime(uptime_seconds)

    def format_uptime(self, uptime_seconds):
        days = uptime_seconds // 86400
        hours = (uptime_seconds % 86400) // 3600
        minutes = (uptime_seconds % 3600) // 60
        return f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes"

    def format_field_name(self, field_name):
        emojis = {
            "Host": "🖥️",
            "OS": "🕹️",
            "Kernel": "⚙️",
            "CPU": "🔲",
            "RAM": "📶",
            "Storage": "💾",
            "Uptime": "🏃‍♀️"
        }
        emoji = emojis.get(field_name, "")
        return f"{emoji} {field_name}"


def setup(bot):
    bot.add_cog(SysInfo(bot))
