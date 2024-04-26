import discord
from discord.ext import commands
from discord import Permissions, TextChannel, VoiceChannel, StageChannel
from vote import *

class CustomRole():
    def __init__(self):
        self.admin = Permissions.elevated()
        self.moderator = Permissions(
            kick_members=True, 
            manage_channels=True,
            moderate_members=True,
            mute_members=True,
            move_members=True
        )
        self.member = Permissions.membership()

        self.perm_dict = {
            "admin": self.admin,
            "moderator": self.moderator,
            "member": self.member
        }

    def get_role_permissions_factory(self, role_type : str) -> Permissions | bool:
        if (not role_type in self.perm_dict):
            return False
        return self.perm_dict[role_type]


class AddRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='add_role')
    async def create_role(
            self,
            ctx: TextChannel | VoiceChannel | StageChannel,
            role_perm: str,
            r, g, b,
            *role_name_args):
        
        role_obj = CustomRole()
        
        role_name = ' '.join(role_name_args)
        role_type = role_obj.get_role_permissions_factory(role_perm)

        try:
            if (not role_type):
                await ctx.reply(f'Типа роли {role_type} не существует в списке возможных ролей!')

            elif (int(r) > 255 or int(g) > 255 or int(b) > 255 or int(r) < 0 or int(g) < 0 or int(b) < 0):
                await ctx.reply("Введен неверный формат цвета в RGB :(")

            else:
                role = ctx.guild.create_role(
                name=role_name, 
                color=discord.Colour.from_rgb(int(r), int(g), int(b)),
                permissions=role_type
                )
                await role

                phrases = ["Роль успешно создана!", "Голосование провалилось."]
                
                choice = await vote(self.bot, ctx, f"Создаем роль {role_name}?", ["Да", "Нет"], symbols='letters',importance=Importance.minor)
                await ctx.reply(phrases[choice.pop()])
                
        except:
            await ctx.reply("Вероятно, параметры комманды /add_role были введены в неверном порядке. Попробуйте снова.")

async def setup(bot):
    await bot.add_cog(AddRole(bot))
