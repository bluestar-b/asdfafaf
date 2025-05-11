import discord
import subprocess
from discord.ext import commands
from discord.commands import slash_command

class SystemdMonitor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="systemd", description="List all active systemd services")
    async def systemd(self, ctx):
        try:
            systemd_output = subprocess.check_output("systemctl list-units --type=service --state=active", shell=True, text=True)
            lines = systemd_output.strip().split("\n")
            services = []

            for line in lines[1:]:
                parts = line.split(maxsplit=4)
                if len(parts) >= 5:
                    unit, load, active, sub, description = parts[0], parts[1], parts[2], parts[3], parts[4]
                    services.append({
                        "unit": unit,
                        "load": load,
                        "active": active,
                        "sub": sub,
                        "description": description
                    })

            if not services:
                await ctx.respond("🚫 No active systemd services found.")
                return

            embed = discord.Embed(
                title="🔧 Active Systemd Services",
                description="Here are the active systemd services on this system:",
                color=discord.Color.green()
            )

            for service in services[:10]:
                embed.add_field(
                    name=f"⚙️ {service['unit']}",
                    value=(
                        f"🔹 **Load:** {service['load']}\n"
                        f"🟢 **Active:** {service['active']}\n"
                        f"🔲 **Sub-state:** {service['sub']}\n"
                        f"📝 **Description:** {service['description']}"
                    ),
                    inline=False
                )

            await ctx.respond(embed=embed)

        except Exception as e:
            await ctx.respond(f"❌ Error: {e}")

def setup(bot):
    bot.add_cog(SystemdMonitor(bot))
