import discord
from discord.ext import commands
from discord import app_commands

# Invoice Cog
class Invoice(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="invoice", description="Create an invoice for a client.")
    @app_commands.describe(amount="Enter the amount in USD")
    async def invoice(self, interaction: discord.Interaction, amount: float):
        # Create embed
        embed = discord.Embed(
            title="Dynasty's Bot Development | Invoice Created",
            description=(
                "Once the payment has been processed, please attach a screenshot without cutting out how much you sent "
                "and to who for the fastest delivery. Leave reason for payment message blank.\n\n"
                f"**Amount Due**\n"
                f"${amount:.2f} USD\n\n"
                "**Payment Agreement**\n"
                "By processing the payment, you are agreeing to the Terms of Service listed in "
                "<#1414125860864266311>"
            ),
            color=0x0179e0
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/1410327912028176509/1414135356022063164/ChatGPT_Image_Sep_7_2025_12_48_05_AM.png?ex=68be77ae&is=68bd262e&hm=c234ff79ced93b3571fbc9791be25225ec4aff78b8871c13f99a503529104115&"
        )

        # Create Venmo button
        view = discord.ui.View()
        venmo_button = discord.ui.Button(
            label="Pay with Venmo",
            url="https://venmo.com/dynasty_olson",
            style=discord.ButtonStyle.link
        )
        view.add_item(venmo_button)

        await interaction.response.send_message(embed=embed, view=view)

# Cog setup
async def setup(bot: commands.Bot):
    await bot.add_cog(Invoice(bot))
