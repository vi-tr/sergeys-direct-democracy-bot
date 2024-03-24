# Ia neznaiu kto kakoi imeet uroven' pintona poetomu inogda budu pisat' samie ochevidnie veshi
#A eshe u menia sletela ruskaia raskladka
#tak chto naslagdaites' latinicei, po vozmognosti todge pishite komenti
#tut importi
import discord
import os

# Eto tochka vhoda
def main():
    client = discord.Client()
    client.run(os.getenv("TOKEN"))

# Eto todge tochka vhoda
if __name__ == "__main__":
    main()
