import discord
from discord.ext import commands
from vote import vote, Importance
from datetime import datetime

laws_dict = {}

class Democracy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        @bot.event
        async def on_message(message):
            if message.author == bot.user:
                return
        
            for law in laws_dict.values():
                if law['enforce'] and law['keyword'] in message.content:
                    await message.channel.send(f'{message.author.name} ликвидирован.')
                    await message.author.kick(reason=f'Нарушение закона: {law["description"]}')
                    break
            await bot.process_commands(message)

    @commands.command(name='add_law')
    async def add_law(self, ctx, keyword: str, law_name: str, description: str, enforce: bool = True):
        if law_name in laws_dict:
            await ctx.send(f"Закон с названием {law_name} уже существует.")
            return
        choice = await vote(self.bot, ctx, f"Добавить ли закон {law_name}?\nОписание закона:\n{description}", ["Да", "Нет"], symbols='thumbs', importance=Importance.minor)
        if choice.pop()==1:
            await ctx.send("Голосование провалилось")
            return
        
        laws_dict[law_name] = {
            'keyword' : keyword,
            'description' : description,
            'enforce' : enforce,
            'date_added' : datetime.now().strftime("%Y-%m-%d")
        }

        await ctx.send(f'Закон "{law_name}" добавлен.\nОписание: {description}\nВлияет на модерацию:{"Да" if enforce else "Нет"}.')
    
    @commands.command(name='remove_law')
    async def remove_law(self, ctx, law_name: str):
        
        if law_name not in laws_dict:
            await ctx.send(f"Закон с названием {law_name} не существует.")
            return
        
        choice = await vote(self.bot, ctx, f"Удалить ли закон {law_name}?", ["Да", "Нет"], symbols='thumbs', importance=Importance.medium)
        if choice.pop()==1:
            await ctx.send("Голосование провалилось")
            return
        
        del laws_dict[law_name]

        await ctx.send(f'Закон "{law_name}" удален.')
    
    @commands.command('laws')
    async def get_law(self, ctx, law_name=None):
        if law_name:
            law = laws_dict.get(law_name, None)
            if law:
                response = (
                    f'Закон {law_name} от {law["date_added"]}\n\n'
                    f'Влияет на модерацию: {"Да" if law["enforce"] else "Нет"}\n'
                    f'Описание: {law["description"]}'
                )
            else:
                response = f'Закон с названием "{law_name}" не найден.'
        else:
            if not laws_dict:
                response = 'Законов не существует.'
            else:
                response = 'Список законов:\n' + '\n'.join(f'{name}: {law["description"]}' for name, law in laws_dict.items())
        await ctx.send(response)

async def setup(bot):
    await bot.add_cog(Democracy(bot))