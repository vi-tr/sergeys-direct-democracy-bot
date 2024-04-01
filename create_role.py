from discord import Permissions, Client, TextChannel, VoiceChannel, StageChannel, Colour, Role
import asyncio

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


async def create_role(
        client: Client, 
        ctx: TextChannel | VoiceChannel | StageChannel,
        role_perm: str,
        r, g, b,
        *role_name_args) -> Role | bool:
    
    role_name = ' '.join(role_name_args)
    role_type = CustomRole.get_role_permissions_factory(role_perm)

    try:
        if (not role_type):
            await ctx.reply(f'Типа роли {role_type} не существует в списке возможных ролей!')
            return False

#вот это оставляет желать лучшего, лабы Кемрика на Go на меня плохо влияют
        elif (int(r) > 255 or int(g) > 255 or int(b) > 255 or int(r) < 0 or int(g) < 0 or int(b) < 0):
            await ctx.reply("Введен неверный формат цвета в RGB :(")
            return False

        else:
            role = Role(
                name=role_name, 
                color=Colour.from_rgb(int(r), int(g), int(b)),
                permissions=role_type
            )

            return role
    except:
        await ctx.reply("Вероятно, параметры комманды /add_role были введены в неверном порядке. Попробуйте снова.")
        return False


