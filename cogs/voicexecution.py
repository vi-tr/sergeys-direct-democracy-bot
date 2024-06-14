import discord
from discord.ext import commands

from vote import vote, Importance

# While testing ALL functions of this bot found out vote being not confirmed (pop() returns none) if there is not sufficient amount of votes (but not zero) when vote is expired
# not sure if it should work like that, but just for others to know that this is kind of a problem when we are to test it, due to lack of users online (especially at late nighttime)
# probably fix is needed or some edit at that point

class Voicexecution(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command("cutegory") #works with txt categories too #need to make external?
    async def delete_category(self, ctx, category: commands.CategoryChannelConverter):
        guild = ctx.guild

        category_name = category.name

        if category_name is None:
            await ctx.send(f"Категория '{category_name}' не найдена на сервере.")
            return

        choice = await vote(self.bot, ctx, f"Сносим категорию {category_name} и все ее содержимое с сервера?",
                            ["Да", "Нет"], symbols='thumbs', importance=Importance.minor)
        if choice.pop() == 1:
            await ctx.send("Голосование провалилось")
            return
        else:
            for channel in category.channels:
                await channel.delete()
            await category.delete()
            await ctx.send(f"Категория '{category_name}' успешно удалена вместе со своим содержимым!")

    @commands.command("voicexecution")
    async def delete_voicechannel(self, ctx, category: commands.CategoryChannelConverter, channel_name: str):
        guild = ctx.guild
        category_name = category.name

        channel = discord.utils.get(category.voice_channels, name=channel_name)

        if channel is None:
            await ctx.send(f"Голосовой канал '{channel_name}' не найден в категории '{category_name}'.")
            return

        choice = await vote(self.bot, ctx, f"Сносим голосовой канал {channel_name} из категории {category_name}?",
                            ["Да", "Нет"], symbols='thumbs', importance=Importance.minor)
        if choice.pop() == 1:
            await ctx.send("Голосование провалилось")
            return
        else:
            await channel.delete()
            await ctx.send(f"Голосовой канал '{channel_name}' успешно удален из категории '{category_name}'!")

    @delete_voicechannel.error #local exeptions section (global one instead would make much more sense but idk how to get it working (i tried))
    async def vcerror(self, ctx, error):
            # no ideas what to specialize
        await ctx.send(f"Непредвиденная ошибка: {error}")

async def setup(bot):
    await bot.add_cog(Voicexecution(bot))
