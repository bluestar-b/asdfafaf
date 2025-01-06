import discord
from discord.ext import commands
from discord.commands import slash_command
from lib.accessloader import is_authorized


class SendDM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="senddm", description="Send a direct message to a user (restricted to authorized users).")
    async def senddm(self, ctx, user: discord.User, msg: str):
        if not is_authorized(str(ctx.author.id)):
            return await ctx.respond(f"Unauthorized attempt by {ctx.author.mention}. You are not allowed to use this command.")

        try:
            await user.send(msg)
            embed = discord.Embed(
                title="DM Sent",
                description=f"Message sent to {user.mention}",
                color=discord.Color.green()
            )
            embed.add_field(name="Message", value=f"```\n{msg}\n```", inline=False)
            await ctx.respond(embed=embed)
        except Exception as e:
            await ctx.respond(f"Failed to send DM: {e}")


def setup(bot):
    bot.add_cog(SendDM(bot))
