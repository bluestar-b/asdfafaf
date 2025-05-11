import discord
import docker
from discord.ext import commands
from discord.commands import slash_command
from datetime import datetime, timezone


class DockerMonitor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = docker.from_env()

    @slash_command(name="docker", description="View Docker container status with CPU and RAM usage")
    async def docker_status(self, ctx, container_id: str = None):
        if container_id:
            try:
                container = self.client.containers.get(container_id)
                embed = await self.get_container_info(container)
            except docker.errors.NotFound:
                embed = discord.Embed(
                    title="❌ Container Not Found",
                    description=f"No container found with ID: `{container_id}`",
                    color=discord.Color.red()
                )
        else:
            containers = self.client.containers.list(all=True)

            if not containers:
                await ctx.respond("🚫 No Docker containers found.")
                return

            embed = discord.Embed(
                title="🐳 Docker Container Status",
                color=discord.Color.blurple()
            )

            for container in containers:
                embed.add_field(
                    name=f"{container.name} ({container.status})",
                    value=(f"**Image:** `{container.image.tags[0] if container.image.tags else container.image.short_id}`\n"
                           f"**ID:** `{container.short_id}`\n"
                           f"**Uptime:** `{str(datetime.now(timezone.utc) - datetime.fromisoformat(container.attrs['State']['StartedAt'].replace('Z', '+00:00'))).split('.')[0]}`"
                    ),
                    inline=False
                )

        await ctx.respond(embed=embed)

    async def get_container_info(self, container):
        started = container.attrs["State"]["StartedAt"]
        started_dt = datetime.fromisoformat(started.replace("Z", "+00:00"))
        uptime = datetime.now(timezone.utc) - started_dt

        stats = container.stats(stream=False)
        cpu_percent = self.get_cpu_percent(stats)
        mem_usage = stats["memory_stats"]["usage"]
        mem_limit = stats["memory_stats"].get("limit", 1)
        mem_percent = (mem_usage / mem_limit) * 100

        image_size = container.image.attrs["Size"] / (1024**2)

        container_command = " ".join(container.attrs["Config"]["Cmd"])

        embed = discord.Embed(
            title=f"🐳 {container.name} ({container.short_id})",
            color=discord.Color.green()
        )

        embed.add_field(name="⚙️ Status", value=container.status, inline=False)
        embed.add_field(name="⏱️ Uptime", value=f"{str(uptime).split('.')[0]}", inline=False)
        embed.add_field(name="💾 Image Size", value=f"{image_size:.2f} MB", inline=False)
        embed.add_field(name="📜 Command", value=container_command or "No command specified", inline=False)
        embed.add_field(name="💻 CPU Usage", value=f"{cpu_percent:.2f}%", inline=False)
        embed.add_field(name="🧠 RAM Usage", value=f"{mem_percent:.2f}%", inline=False)

        # Check for ports
        ports = container.attrs.get("NetworkSettings", {}).get("Ports", {})
        if ports:
            ports_info = "\n".join([f"{port}: {mapping}" for port, mapping in ports.items()])
            embed.add_field(name="🌐 Ports", value=ports_info, inline=False)
        else:
            embed.add_field(name="🌐 Ports", value="No exposed ports", inline=False)
        return embed

    def get_cpu_percent(self, stats):
        cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - stats["precpu_stats"]["cpu_usage"]["total_usage"]
        system_delta = stats["cpu_stats"]["system_cpu_usage"] - stats["precpu_stats"]["system_cpu_usage"]
        if system_delta > 0.0 and cpu_delta > 0.0:
            return (cpu_delta / system_delta) * len(stats["cpu_stats"]["cpu_usage"].get("percpu_usage", [])) * 100.0
        return 0.0


def setup(bot):
    bot.add_cog(DockerMonitor(bot))
