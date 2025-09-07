import discord
from discord.ext import commands

AUTO_ROLE_ID = 1414127672786681857

class AutoRole(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        role = member.guild.get_role(AUTO_ROLE_ID)
        if role:
            try:
                await member.add_roles(role, reason="Auto-role for new members")
                print(f"Assigned {role.name} to {member.name}")
            except discord.Forbidden:
                print(f"Missing permissions to assign role {role.name} to {member.name}")
            except Exception as e:
                print(f"Failed to assign role: {e}")
        else:
            print(f"Role ID {AUTO_ROLE_ID} not found in {member.guild.name}")

async def setup(bot: commands.Bot):
    await bot.add_cog(AutoRole(bot))
