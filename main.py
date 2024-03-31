# Ia neznaiu kto kakoi imeet uroven' pintona poetomu inogda budu pisat' samie ochevidnie veshi
#A eshe u menia sletela ruskaia raskladka
#tak chto naslagdaites' latinicei, po vozmognosti todge pishite komenti
#tut importi
from bot import *
import add_role
from typing import *
import os
from dotenv import load_dotenv

from discord import app_commands

load_dotenv()
TOKEN: Final[str] = os.getenv('BOT_TOKEN')

#инициализация бота должна находиться в глоабльной области видимости,
#так как из main обьект класса Client никто не увидит

# Eto tochka vhoda
def main():
    bot.run(token=TOKEN)
#Anton Franssen is here XD
#26.03.2024

#Не знаю почему, но без аргумента intents у меня ничего не работает :)
#В любом случае, оно никак не должно помешать работе бота   


async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Eto todge tochka vhoda
if __name__ == "__main__":
    main()
