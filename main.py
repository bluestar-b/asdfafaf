import os
import discord
import time
from dotenv import load_dotenv
from discord.ext import commands
from lib.accessloader import is_authorized  # Import your authorization function

load_dotenv()
intents = discord.Intents.all()

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"🚀 {bot.user.name} is online!")
    print(f"🔧 Bot ID: {bot.user.id}")
    print(f"🌐 Connected to {len(bot.guilds)} servers")
    print(f"🤖 Running on Pycord v{discord.__version__}")

for filename in os.listdir('./cogs'):
    if filename.endswith('_cog.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f"📑 Loaded cogs.{filename[:-3]}")

@bot.slash_command(name="reload", description="Reload a specific cog or all cogs.")
async def reload(ctx, cog_name: str = None):
    if not is_authorized(str(ctx.author.id)):  # Check if user is authorized
        return await ctx.respond("You are not authorized to use this command.")

    start_time = time.time()

    if cog_name:
        return await reload_single_cog(ctx, cog_name, start_time)

    return await reload_all_cogs(ctx, start_time)

async def reload_single_cog(ctx, cog_name, start_time):
    try:
        bot.reload_extension(f'cogs.{cog_name}')
        reload_time = round((time.time() - start_time) * 1000)
        await ctx.respond(f"✅ Reloaded cog: {cog_name} in {reload_time} ms")
    except Exception as e:
        await ctx.respond(f"❌ Error reloading cog: {e}")

async def reload_all_cogs(ctx, start_time):
    total_reload_time = 0
    reload_details = []

    for filename in os.listdir('./cogs'):
        if filename.endswith('_cog.py'):
            cog_name = filename[:-3]
            cog_start_time = time.time()
            bot.reload_extension(f'cogs.{cog_name}')
            cog_reload_time = round((time.time() - cog_start_time) * 1000)
            reload_details.append(f"{cog_name} reloaded in {cog_reload_time} ms")
            total_reload_time += cog_reload_time

    total_reload_time = round(total_reload_time)
    reload_details.append(f"Total reload time for all cogs: {total_reload_time} ms")
    await ctx.respond("\n".join(reload_details))

if __name__ == '__main__':
    bot.run(os.getenv("BOT_TOKEN"))
