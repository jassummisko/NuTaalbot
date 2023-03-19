from discord import Interaction, Role, Member, Guild
from dataclasses import dataclass
import pickle, asyncio, os, data.quotes as quotes, datetime as dt

@dataclass
class PendingEntry:
    userId: int
    roleId: int
    time: dt.datetime

filepath = "data/rolesPendingRemoval.pkl"

def getRolesPendingRemoval() -> list[PendingEntry]:
    if os.path.isfile(filepath) and os.path.getsize(filepath) > 0:
        with open(filepath, 'r+b') as f:
            return pickle.load(f)
    return []

def queuePendingRemovals(server: Guild, rolesPendingRemoval: list[PendingEntry]) -> callable:
    queue = []
    for pendingEntry in rolesPendingRemoval:
        async def buff():
            now = dt.datetime.now()
            due = pendingEntry.time
            await asyncio.sleep(0 if due < now else (due - now).seconds)
            user = server.get_member(pendingEntry.userId)
            role = server.get_role(pendingEntry.roleId)
            await user.remove_roles(role)
            await user.send(content=quotes.ROLE_REMOVED.format(role.name))
            rolesPendingRemoval.remove(pendingEntry)
            dumpRolesPendingRemoval(rolesPendingRemoval)
        queue.append(buff())
    return queue

def dumpRolesPendingRemoval(list: list) -> None:
    with open(filepath, 'w+b') as f:
        pickle.dump(list, f)

async def giveTemporaryRole(roleQueue: list[PendingEntry], i9n: Interaction, user : Member, role : Role, duration : int) -> None:
    SECONDS_PER_MINUTE : int = 60
    await user.add_roles(role)
    await i9n.response.send_message(quotes.ROLE_GIVEN.format(role.name))
    t = dt.datetime.now() + dt.timedelta(minutes = duration)
    roleQueue.append(PendingEntry(user.id, role.id, t))
    dumpRolesPendingRemoval(roleQueue)
    await asyncio.sleep(duration*SECONDS_PER_MINUTE)
    await user.remove_roles(role)
    await user.send(content=quotes.ROLE_REMOVED.format(role.name))