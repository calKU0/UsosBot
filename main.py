import discord
from discord.ext import commands
import json
import os
import keys as k

bot = commands.Bot(command_prefix="!", intents = discord.Intents.all()) 

@bot.event
async def on_ready():
    try:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.load_extension(f"cogs.{filename[:-3]}")
        
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")

        await bot.change_presence(activity=discord.Game(name="Chlanie"))
        print("We've logged in as {0.user}".format(bot))

    except Exception as e:
        print(f"Failed to sync commands: {e}")

bot.run(k.secrets("bot_token"))
