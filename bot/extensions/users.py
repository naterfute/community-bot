'''Purge command, basically nothing else'''
import hikari
import arc
#import miru
from loguru import logger

# from bot.bot import BOT

plugin: arc.GatewayPlugin = arc.GatewayPlugin("users")
version: float = 1.0



@plugin.include
@arc.slash_command("user", "Get Information about a user")
async def purge(
    ctx: arc.GatewayContext,
    user: arc.Option[hikari.User | None, arc.UserParams("A User")]
) -> None:

    pass





@purge.set_error_handler
async def error_handler(ctx: arc.GatewayContext, exc: Exception) -> None:
    logger.error(type(exc))
    logger.error(exc)
    
    if isinstance(exc, arc.errors.UnderCooldownError):
        await ctx.respond(exc, flags=hikari.MessageFlag.EPHEMERAL)
        return
    else:
        await ctx.respond("An Error Occured, Contact naterfute")




@arc.loader
def load(client: arc.GatewayClient) -> None:
    logger.info(f"Loading {plugin.name} Plugin")
    client.add_plugin(plugin)

@arc.unloader
def unload(client: arc.GatewayClient) -> None:
    logger.info(f"Un-Loading {plugin.name} Plugin")
    client.remove_plugin(plugin)

