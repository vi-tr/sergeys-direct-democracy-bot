import discord
from discord.ext import commands

from vote import vote, Importance


class Textermination(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command("textermination")
    async def delete_text_channel(self, ctx, category: commands.CategoryChannelConverter, channel_name: str):
        guild = ctx.guild
        category_name = category.name  # commands.CategoryChannelConverter принимает и ID и имя канала, так что это запись вполне оправдана

        channel = discord.utils.get(category.text_channels, name=channel_name)

        if channel is None:
            await ctx.send(f"Текстовый канал '{channel_name}' не найден в категории '{category_name}'.")
            return

        choice = await vote(self.bot, ctx, f"Сносим текстовый канал {channel_name} из категории {category_name}?",
                            ["Да", "Нет"], symbols='thumbs', importance=Importance.medium)
        if choice.pop() == 1:
            await ctx.send("Голосование провалилось")
            return
        else:
            await channel.delete()
            await ctx.send(f"Текстовый канал '{channel_name}' успешно удален из категории '{category_name}'!")

    @delete_text_channel.error #local exeptions section (global one instead would make much more sense but idk how to get it working (i tried))
    async def txterror(self, ctx, error):
            # no ideas what to specialize
        await ctx.send(f"Непредвиденная ошибка: {error}")

async def setup(bot):
    await bot.add_cog(Textermination(bot))
