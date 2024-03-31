from bot import *
from role_dict import *

@bot.command(name='add_role')
async def add_role(ctx,role_type, r, g, b, *role_name_args, ):

    role_name = ' '.join(role_name_args)
    try:    
        if (not role_type in role_dict):
            await ctx.reply(f'Типа роли {role_type} не существует в списке возможных ролей!')
#вот это оставляет желать лучшего, лабы Кемрика на го на меня плохо влияют
        elif (int(r) > 255 or int(g) > 255 or int(b) > 255 or int(r) < 0 or int(g) < 0 or int(b) < 0):
            await ctx.reply("Введен неверный формат цвета в RGB :(")
        else:
            permissions = role_dict[role_type]

            role = ctx.guild.create_role(
                name=role_name, 
                color=discord.Colour.from_rgb(int(r), int(g), int(b)),
                permissions=permissions
            )

            await role
            await ctx.reply("Роль была создана!")
    except:
        await ctx.reply("Вероятно, параметры комманды !add_role были введены в неверном порядке. Попробуйте снова.")
