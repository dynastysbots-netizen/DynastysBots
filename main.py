# main.py
import discord
from discord.ext import commands
import asyncio
import os

# -------------- CONFIG --------------
TOKEN = "temp"  # replace with your token
PREFIX = "!"                   # only needed if you want legacy prefix commands
INTENTS = discord.Intents.all()  # enable all intents
GUILD_IDS = []  # optional: add guild IDs here for faster syncing
# ------------------------------------

class DynastyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=PREFIX,
            intents=INTENTS,
            application_id=None  # leave None unless needed
        )

    async def setup_hook(self):
        # Load all cogs from cogs folder
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded cog: {filename}")

        # Sync commands (global or per-guild)
        if GUILD_IDS:
            for guild_id in GUILD_IDS:
                guild = discord.Object(id=guild_id)
                self.tree.copy_global_to(guild=guild)
                await self.tree.sync(guild=guild)
                print(f"Commands synced to guild {guild_id}")
        else:
            await self.tree.sync()
            print("Commands synced globally")

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------ Bot is online ------")

async def main():
    bot = DynastyBot()
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())

