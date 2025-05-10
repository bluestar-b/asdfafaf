import discord
import subprocess
import time
from discord.ext import commands
from discord.commands import slash_command
from lib.accessloader import is_authorized
from io import StringIO


class Exec(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="exec", description="Execute a command (restricted to specific users).")
    async def exec(self, ctx, command: str):
        if not is_authorized(str(ctx.author.id)):
            return await ctx.respond(f"Unauthorized attempt by {ctx.author.mention}. You are not allowed to use this command.")

        start_time = time.time()

        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=16)
            output = result.stdout if result.stdout else result.stderr
            if not output:
                output = "No output or error."
        except Exception as e:
            output = f"Error executing command: {e}"

        end_time = time.time()
        execution_time = round((end_time - start_time) * 1000)
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        embed = discord.Embed(
            title="Execution Result",
            color=discord.Color.blue()
        )
        embed.add_field(name="Command", value=f"```\n{command}\n```", inline=False)
        embed.add_field(name="Time", value=f"{current_time} • {execution_time} ms", inline=False)

        if len(output) > 1024:
            file = discord.File(fp=StringIO(output), filename="output.txt")
            await ctx.respond(embed=embed, file=file)
        else:
            embed.add_field(name="Output", value=f"```\n{output}\n```", inline=False)
            await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Exec(bot))
