import discord, pickle, asyncio, os, data.botResponses as botResponses, datetime as dt
from discord import Interaction, Role, Member, Guild
from dataclasses import dataclass

@dataclass
class PendingEntry:
    userId: int
    roleId: int
    time: dt.datetime

filepath = "modules/roleManager/data/rolesPendingRemoval.pkl"

def getRolesPendingRemoval() -> list[PendingEntry]:
    if os.path.isfile(filepath) and os.path.getsize(filepath) > 0:
        with open(filepath, 'r+b') as f:
            return pickle.load(f)
    return []

def queuePendingRemovals(server: Guild, rolesPendingRemoval: list[PendingEntry]) -> callable:
    queue = []
    for pendingEntry in rolesPendingRemoval:
        async def buff():
            now, due = dt.datetime.now(), pendingEntry.time
            await asyncio.sleep(0 if due < now else (due - now).seconds)
            user = server.get_member(pendingEntry.userId)
            role = server.get_role(pendingEntry.roleId)
            await user.remove_roles(role)
            await user.send(content=botResponses.ROLE_REMOVED.format(role.name))
            rolesPendingRemoval.remove(pendingEntry)
            dumpRolesPendingRemoval(rolesPendingRemoval)
        queue.append(buff())
    return queue

def dumpRolesPendingRemoval(list: list) -> None:
    with open(filepath, 'w+b') as f:
        pickle.dump(list, f)

async def roleSelectionView(guild: discord.Guild, filterKey: callable, max_values: int = 25) -> discord.ui.View:
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

async def giveTemporaryRole(roleQueue: list[PendingEntry], i9n: Interaction, user: Member, role: Role, duration: int):
    SECONDS_PER_MINUTE : int = 60
    await user.add_roles(role)
    await i9n.response.send_message(botResponses.ROLE_GIVEN.format(role.name))
    t = dt.datetime.now() + dt.timedelta(minutes = duration)
    roleQueue.append(PendingEntry(user.id, role.id, t))
    dumpRolesPendingRemoval(roleQueue)
    await asyncio.sleep(duration*SECONDS_PER_MINUTE)
    await user.remove_roles(role)
    await user.send(content=botResponses.ROLE_REMOVED.format(role.name))