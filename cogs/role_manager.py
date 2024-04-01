import discord
from discord.ext import commands
from discord.ext.commands import Cog
from create_role import create_role

class RoleManager(discord.ext.commands.Сog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='add_role')
    async def add_role(self, ctx, role_perm, r, g, b, *role_name_args):
        new_role = create_role(
            self.bot,
            ctx,
            role_perm,
            r, g, b,
            role_name_args
        )

        if not new_role:
            return False
        else:
            await ctx.guild.create_role(new_role)
            await ctx.reply(f"Роль {role_name_args} была успешно создана!")

async def setup(bot):
    await bot.add_cog(RoleManager(bot))