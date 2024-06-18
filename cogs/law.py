import discord
from discord.ext import commands
from vote import vote, Importance
from datetime import datetime
import os
import json

laws_dict = {} #default value

#ОЧЕНЬ ГРУБЫЙ КОСТЫЛЬ(data deployment and collecting zone)
def get_path(guildid):
    #Creating global law dir (if doesnt exist already) where all .json law files will exist
    os.makedirs('./lawfiles', exist_ok=True)
    #Getting signed laws of your ds server
    return os.path.join(os.getcwd(),'lawfiles', f'laws_{guildid}.json')

def save_laws(guildid):
    filepath = get_path(guildid)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(laws_dict, f, ensure_ascii=False, indent=4) #Dumping current law dict to a signed .json in READABLE format (not 1 str)

def load_laws(guildid):
    global laws_dict
    filepath = get_path(guildid)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            laws_dict = json.load(f) #Loading saved .json laws of the server, if found
    except FileNotFoundError:
        laws_dict = {} #Else: returning nothing

class Democracy(commands.Cog):
    def __init__(self, bot): #idk how to make this an external module properly (commands.Cog.listener() or other stuff just makes the bot double the commands)
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
        choice = await vote(self.bot, ctx, f"Добавить ли закон {law_name}?\nОписание закона:\n{description}", ["Да", "Нет"], importance=Importance.minor)
        if choice.pop()==1:
            await ctx.send("Голосование провалилось")
            return

        laws_dict[law_name] = {
            'keyword' : keyword,
            'description' : description,
            'enforce' : enforce,
            'date_added' : datetime.now().strftime("%Y-%m-%d")
        }

        save_laws(ctx.guild.id) #Saving current law list to .json after every addition
        await ctx.send(f'Закон "{law_name}" добавлен.\nОписание: {description}\nВлияет на модерацию:{"Да" if enforce else "Нет"}.')

    @commands.command(name='remove_law')
    async def remove_law(self, ctx, law_name: str):

        if law_name not in laws_dict:
            await ctx.send(f"Закон с названием {law_name} не существует.")
            return

        choice = await vote(self.bot, ctx, f"Удалить ли закон {law_name}?", ["Да", "Нет"], importance=Importance.minor)
        if choice.pop()==1:
            await ctx.send("Голосование провалилось")
            return

        del laws_dict[law_name]

        save_laws(ctx.guild.id) #And after every deletion
        await ctx.send(f'Закон "{law_name}" удален.')

    @commands.command('laws')
    async def get_law(self, ctx, law_name=None):
        load_laws(ctx.guild.id) #Getting law list for a server
        if law_name:
            law = laws_dict.get(law_name, None)
            if law:
                response = (
                    f'Закон {law_name} от {law["date_added"]}\n'
                    f'(ключевое слово: "{law["keyword"]}")\n'
                    f'Влияет на модерацию: {"Да" if law["enforce"] else "Нет"}\n\n'
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
    @get_law.error #local exeptions section (global one instead would make much more sense but idk how to get it working (i tried))
    @add_law.error
    @remove_law.error
    async def lawerror(self, ctx, error):
            # no ideas what to specialize
        await ctx.send(f"Непредвиденная ошибка: {error}")

async def setup(bot):
    await bot.add_cog(Democracy(bot))
