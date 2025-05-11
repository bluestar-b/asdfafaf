import discord
import psutil
from discord.ext import commands
from discord.commands import slash_command

class TopCPUConsumers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="top", description="View top CPU-consuming processes")
    async def top_processes(self, ctx):
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'username']):
                try:
                    if proc.info['cpu_percent'] > 0.10 and 'systemd' not in proc.info['name']:
                        processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue

            processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:10]

            process_info = ""
            for proc in processes:
                process_info += f"**PID:** {proc['pid']} | **Name:** {proc['name']} | **CPU Usage:** {proc['cpu_percent']:.2f}% | **User:** {proc['username']}\n"

            if not process_info:
                process_info = "No processes with significant CPU usage (above 0.10%) were found."

            embed = discord.Embed(
                title="⚡ Top CPU Consumers",
                description=process_info,
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed)
        except Exception as e:
            await ctx.respond(f"❌ Error: {e}")

def setup(bot):
    bot.add_cog(TopCPUConsumers(bot))
