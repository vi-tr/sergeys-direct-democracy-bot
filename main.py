# Ia neznaiu kto kakoi imeet uroven' pintona poetomu inogda budu pisat' samie ochevidnie veshi
#A eshe u menia sletela ruskaia raskladka
#tak chto naslagdaites' latinicei, po vozmognosti todge pishite komenti
#tut importi
import discord
from discord import Intents, Client, Message
from typing import *
import os
from dotenv import load_dotenv

from discord import app_commands

load_dotenv()
TOKEN: Final[str] = os.getenv('BOT_TOKEN')

#инициализация бота должна находиться в глоабльной области видимости,
#так как из main обьект класса Client никто не увидит

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Eto tochka vhoda
def main():
    client.run(token=TOKEN)
#Anton Franssen is here XD
#26.03.2024

#Не знаю почему, но без аргумента intents у меня ничего не работает :)
#В любом случае, оно никак не должно помешать работе бота   

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def send(message: Message) -> None:
    if message.author == client.user:
        return
    
    if(message.content == "Testing message"):
        await message.channel.send("NO")

# Eto todge tochka vhoda
if __name__ == "__main__":
    main()
