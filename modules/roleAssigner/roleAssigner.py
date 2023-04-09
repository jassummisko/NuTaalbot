import discord

async def roleSelectionView(guild: discord.Guild, filterKey: callable, max_values: int = 25):
    roles = [role for role in filter(filterKey, guild.roles)]
    dropdown = discord.ui.Select(
        max_values = min([len(roles), max_values]),
        placeholder = "Choose an option",
        options = [discord.SelectOption(label=role.name) for role in roles]
    )
    
    async def callback(i9n: discord.Interaction):
        rolesToAdd = [role for role in roles if role.name in dropdown.values]
        member = guild.get_member(i9n.user.id)
        await member.add_roles(*rolesToAdd)
        await i9n.response.send_message(f"Added roles {', '.join([role.name for role in rolesToAdd])}")

    dropdown.callback = callback
    view = discord.ui.View()
    view.add_item(dropdown)
    return view