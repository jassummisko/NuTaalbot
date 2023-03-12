import discord

async def roleSelectionView(guild: discord.guild, filterKey: callable, max_values: int = 25):
    roleFilter = filter(filterKey, guild.roles)
    roles = [role for role in roleFilter]
    testDropdown = discord.ui.Select(
        max_values = min([len(roles), max_values]),
        placeholder = "Choose a language",
        options = [discord.SelectOption(label=role.name) for role in roles]
    )
    
    async def callback(i9n: discord.Interaction):
        rolesToAdd = [role for role in roles if role.name in testDropdown.values]
        await i9n.user.add_roles(*rolesToAdd)
        await i9n.response.send_message(f"Added roles {', '.join([role.name for role in rolesToAdd])}")

    testDropdown.callback = callback
    view = discord.ui.View()
    view.add_item(testDropdown)
    return view