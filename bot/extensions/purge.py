'''Purge command, basically nothing else'''
import hikari
import arc
#import miru
import datetime
from loguru import logger

from ..bot import BOT
plugin: arc.GatewayPlugin = arc.GatewayPlugin("Purge")
version: float = 1.0



@plugin.include
@arc.with_hook(arc.user_limiter(60, 5))
@arc.with_hook(arc.has_permissions(hikari.Permissions.MANAGE_MESSAGES))
@arc.slash_command("purge", "Purges a select amount of messages. Only works on messages younger than 14 days")
async def purge(
    ctx: arc.GatewayContext,
    purge_length: arc.Option[int, arc.IntParams(description="How many messages to Delete?", min=1, max=500)] # type: ignore
) -> None:

    bulk_delete_limit: datetime.datetime = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=14)
    purgeEmbed: hikari.Embed = hikari.Embed(title="Deleted Messages", color='#f23914')
    iterator = (
        BOT.rest.fetch_messages(ctx.channel_id)
        .take_while(lambda message: message.created_at > bulk_delete_limit)
        .limit(purge_length)
    )

    await BOT.rest.delete_messages(ctx.channel_id, iterator)
    await ctx.respond(embed=purgeEmbed, flags=hikari.MessageFlag.EPHEMERAL)





@purge.set_error_handler
async def error_handler(ctx: arc.GatewayContext, exc: Exception) -> None:
    logger.error(type(exc))
    logger.error(exc)
    if isinstance(exc, arc.errors.UnderCooldownError):
        await ctx.respond(exc, flags=hikari.MessageFlag.EPHEMERAL)
        return




@arc.loader
def load(client: arc.GatewayClient) -> None:
    logger.info(f"Loading {plugin.name} Plugin")
    client.add_plugin(plugin)

@arc.unloader
def unload(client: arc.GatewayClient) -> None:
    logger.info(f"Un-Loading {plugin.name} Plugin")
    client.remove_plugin(plugin)
