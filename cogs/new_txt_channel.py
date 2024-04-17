import discord
from discord.ext import commands

from vote import vote, Importance


class NewTXTChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command("create_txt_channel")
    async def create_text_channel(self, ctx, category_name: str, channel_name: str):
        guild = ctx.guild
        category = discord.utils.get(guild.categories, name=category_name)

        choice = await vote(self.bot, ctx, f"Создать ли текстовый канал {channel_name} в категории {category_name}",
                            ["Да", "Нет"], symbols='thumbs', importance=Importance.medium)
        if choice.pop() == 1:
            await ctx.send("Голосование провалилось")
            return
        else:
            if category is None:
                category = await guild.create_category(category_name)
                await ctx.send(f"Категория '{category_name}' создана.")

            await guild.create_text_channel(channel_name, category=category)
            await ctx.send(f"Текстовый канал '{channel_name}' успешно создан в категории '{category_name}'!")


async def setup(bot):
    await bot.add_cog(NewTXTChannel(bot))
