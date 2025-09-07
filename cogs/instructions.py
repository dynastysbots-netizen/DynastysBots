import discord
from discord import app_commands
from discord.ext import commands

ALLOWED_ROLE_IDS = [1414127177129132042, 1414127341025890354, 1414127481438605312]

class Instructions(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="instructions", description="Get bot setup instructions")
    async def instructions(self, interaction: discord.Interaction):
        # Check if user has an allowed role
        if not any(role.id in ALLOWED_ROLE_IDS for role in interaction.user.roles):
            await interaction.response.send_message(
                "You do not have permission to use this command.", ephemeral=True
            )
            return

        embed = discord.Embed(
            title="Bot Setup Instructions",
            description="Thank you for purchasing a bot from us! Below are detailed instructions to get your bot started.\n\n"
                        "These instructions assume you are using a hosting service for your bot.\n"
                        "(Disclaimer: Some things may appear differently or be worded differently.)",
            color=0x0179e0
        )

        embed.add_field(
            name="Step 1: Clone the Repository",
            value="On your hosting panel or through SSH, clone the repository.\n"
                  "```git clone https://github.com/USERNAME/PRIVATE-REPO.git```\n"
                  "> Replace `USERNAME/PRIVATE-REPO` with the link provided to you.",
            inline=False
        )

        embed.add_field(
            name="Step 2: Install Python & Dependencies",
            value="- Ensure your bot host supports Python 3.12+\n"
                  "- Install dependencies (may appear as 'Python install' or 'Requirements File' in some hosting services)\n"
                  "```pip install -r requirements.txt```",
            inline=False
        )

        embed.add_field(
            name="Step 3: Configure the Bot Token",
            value="- Create a `.env` file in the root folder of your project (should **NOT** be under dist/)\n"
                  "- Add your bot token line as shown below:\n"
                  "```TOKEN=enter-token-here```\n"
                  "- If you do not know how to create a Discord application, watch this video: [YouTube Link](https://www.youtube.com/watch?v=zrNloK9b1ro&t=6s)\n"
                  "- To use the repository you need a Access Token which will be provided seperately, this will usually be named Git Access Token\n"
                  "- Enable all Privileged Gateway Intents and, when generating your invite link inside OAuth2, select `bot` and the permissions instructed.",
            inline=False
        )

        embed.add_field(
            name="Step 4: Start the Bot",
            value="Navigate to the Startup Command section or inside the console, enter and/or run:\n"
                  "```python dist/main.py```",
            inline=False
        )

        embed.add_field(
            name="Step 5: Support",
            value="If any issues occur during or after setup, create a support ticket or ask in <#1414126679684546660>",
            inline=False
        )

        await interaction.response.send_message(embed=embed, ephemeral=False)

async def setup(bot: commands.Bot):
    await bot.add_cog(Instructions(bot))
