from typing import (
    Any,
    Coroutine,
    Dict,
    Hashable,
    Union,
    Callable,
    TypeVar,
    Optional,
    TYPE_CHECKING,
)
import discord
T = TypeVar('T')

__all__ = (
    'has_role_custom',
)  
def has_role_custom(item: Union[int, str], /) -> Callable[[T], T]:

    async def predicate(interaction: discord.Interaction) -> bool:
        if isinstance(interaction.user, discord.User):
            raise discord.app_commands.errors.NoPrivateMessage

        if isinstance(item, int):
            role = interaction.user.get_role(item)
        else:
            role = discord.utils.get(interaction.user.roles, name=item)

        if role is None:
            await interaction.channel.send(f"{interaction.user.mention} you do not have the required role to do that.")
            raise discord.app_commands.errors.MissingRole(item)
        return True

    return discord.app_commands.checks.check(predicate)
