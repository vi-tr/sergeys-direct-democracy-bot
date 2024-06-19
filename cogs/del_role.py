import discord
from discord.ext import commands
from discord import Permissions, TextChannel, VoiceChannel, StageChannel
from vote import *

class DeleteRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='delete_role')
    async def del_role(self, ctx, *role_name_args):
        phrases = ["Роль успешно уничтожена!", "Голосование провалилось."]
        role_name = ' '.join(role_name_args)
        try:
            choice = await vote(self.bot, ctx, f"Уничтожаем роль {role_name}?",  ["Да", "Нет"],  symbols='thumbs', importance=Importance.medium)

            choice_res = choice.pop()

            if(choice_res == 0):
                await discord.utils.get(ctx.guild.roles, name=role_name).delete()

            await ctx.reply(phrases[choice_res])
        except:
            await ctx.reply("Такой роли нет на сервере(.")

async def setup(bot):
    await bot.add_cog(DeleteRole(bot))
