import discord
from discord.ext import commands
import asyncio
import os
from flask import Flask, send_from_directory
import threading
from dotenv import load_dotenv

# -------------- CONFIG --------------
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = "!"
INTENTS = discord.Intents.all()
GUILD_IDS = []
# ------------------------------------

# Flask setup
app = Flask(__name__)

@app.route("/")
def home():
    return "Dynasty Bot is running!"

@app.route("/transcripts/<filename>")
def transcripts(filename):
    return send_from_directory("transcripts", filename)

def run_flask():
    app.run(host="0.0.0.0", port=8080)

class DynastyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=PREFIX,
            intents=INTENTS,
            application_id=None
        )

    async def setup_hook(self):
        # Load cogs
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded cog: {filename}")

        # Sync commands
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
    # Run Flask in a separate thread
    threading.Thread(target=run_flask).start()
    asyncio.run(main())



