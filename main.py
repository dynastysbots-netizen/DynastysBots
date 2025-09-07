# main.py
import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
from flask import Flask
import threading

# -------------- CONFIG --------------
load_dotenv()  # load variables from .env file
TOKEN = os.getenv("DISCORD_TOKEN")  # .env must contain DISCORD_TOKEN=your_token_here
PREFIX = "!"
INTENTS = discord.Intents.all()
GUILD_IDS = []  # optional: add guild IDs here for faster syncing
# ------------------------------------

# -------------- FLASK SERVER --------------
app = Flask(__name__)

@app.route("/")
def home():
    return "Dynasty Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=8080)
# ------------------------------------------

class DynastyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=PREFIX,
            intents=INTENTS,
            application_id=None
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
    # Start Flask server in background thread
    threading.Thread(target=run_flask).start()

    # Start Discord bot
    asyncio.run(main())


