import discord
from discord.ext import commands
from discord import app_commands

# ---------------- CONFIG ----------------
TICKET_PANEL_CHANNEL_ID = 1414125765888315493  # replace with your panel channel ID
TICKET_CATEGORY_ID = 1414126373160620033      # replace with your ticket category ID
SUPPORT_ROLE_ID = 1414127481438605312         # support team role
DEV_ROLE_ID = 1414127481438605312             # developer role
COLOR = 0x0179e0
FOOTER_TEXT = "Dynasty's Bot Development"
FOOTER_ICON = "https://cdn.discordapp.com/attachments/1410327912028176509/1414135356022063164/ChatGPT_Image_Sep_7_2025_12_48_05_AM.png?ex=68be77ae&is=68bd262e&hm=c234ff79ced93b3571fbc9791be25225ec4aff78b8871c13f99a503529104115&"
THUMBNAIL = FOOTER_ICON
# ----------------------------------------

class TicketDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Purchase Ticket", description="Open a commission ticket"),
            discord.SelectOption(label="Support Ticket", description="Open a support ticket")
        ]
        super().__init__(placeholder="Select a ticket type...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        category = guild.get_channel(TICKET_CATEGORY_ID)
        ticket_type = self.values[0]

        # Name format
        if ticket_type == "Purchase Ticket":
            channel_name = f"commission-{interaction.user.name}"
        else:
            channel_name = f"support-{interaction.user.name}"

        # Check if channel exists
        existing = discord.utils.get(guild.channels, name=channel_name)
        if existing:
            await interaction.response.send_message("You already have an open ticket.", ephemeral=True)
            return

        # Permissions
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True),
            guild.get_role(SUPPORT_ROLE_ID): discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.get_role(DEV_ROLE_ID): discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }

        # Create channel
        ticket_channel = await guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites
        )

        # Ticket embed
        if ticket_type == "Purchase Ticket":
            embed = discord.Embed(
                title=f"Commission Ticket Opened | {interaction.user.id}",
                description=(
                    "Thank you for putting in your request. Please remain patient for Staff or Development to respond\n\n"
                    "In the meantime, please provide the kind of bot you want, instructions, and specific requests you have. "
                    "If possible, provide examples.\n\n"
                    "**Commission Status:** Open"
                ),
                color=COLOR
            )
        else:
            embed = discord.Embed(
                title=f"Support Ticket Opened | {interaction.user.id}",
                description=(
                    "Thank you for putting in your request. Please remain patient for Staff or Development to respond\n\n"
                    "In the meantime, please provide your inquiry below."
                ),
                color=COLOR
            )

        embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
        embed.set_thumbnail(url=THUMBNAIL)

        # Close buttons
        view = TicketCloseView()
        await ticket_channel.send(content=interaction.user.mention, embed=embed, view=view)

        await interaction.response.send_message(f"{ticket_type} created: {ticket_channel.mention}", ephemeral=True)


class TicketDropdownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketDropdown())


class TicketCloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.danger)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="Ticket Closed",
            description=f"Closed by {interaction.user.mention}",
            color=COLOR
        )
        embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
        await interaction.channel.send(embed=embed)
        await interaction.channel.delete()

    @discord.ui.button(label="Close with Reason", style=discord.ButtonStyle.secondary)
    async def close_with_reason(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = TicketCloseReasonModal()
        await interaction.response.send_modal(modal)


class TicketCloseReasonModal(discord.ui.Modal, title="Close Ticket with Reason"):
    reason = discord.ui.TextInput(label="Reason", style=discord.TextStyle.paragraph, required=True)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Ticket Closed",
            description=f"Closed by {interaction.user.mention}\n**Reason:** {self.reason.value}",
            color=COLOR
        )
        embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
        await interaction.channel.send(embed=embed)
        await interaction.channel.delete()


class TicketSystem(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Automatically send ticket panel on bot startup
        self.bot.loop.create_task(self.send_ticket_panel_on_startup())

    async def send_ticket_panel_on_startup(self):
        await self.bot.wait_until_ready()
        guilds = self.bot.guilds
        for guild in guilds:
            channel = guild.get_channel(TICKET_PANEL_CHANNEL_ID)
            if not channel:
                continue

            # Delete previous messages
            try:
                async for message in channel.history(limit=10):
                    await message.delete()
            except Exception:
                pass

            embed = discord.Embed(
                title="Dynasty's Bot Development | Ticket Panel",
                description=(
                    "Select the following option below to create a ticket.\n\n"
                    "Do not ping Staff or Developers until 24 hours+ has passed without a response.\n\n"
                    "After creating your ticket, follow the directions provided upon creation."
                ),
                color=COLOR
            )
            embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
            embed.set_thumbnail(url=THUMBNAIL)

            view = TicketDropdownView()
            await channel.send(embed=embed, view=view)

    # Optional slash command to refresh manually if needed
    @app_commands.command(name="ticketpanel", description="Refresh the ticket panel")
    async def ticketpanel(self, interaction: discord.Interaction):
        await self.send_ticket_panel_on_startup()
        await interaction.response.send_message("Ticket panel refreshed.", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(TicketSystem(bot))
