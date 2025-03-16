import hikari
#import miru
import arc

from ..bot import BOT

from loguru import logger

from bot.config import Config

plugin: arc.GatewayPlugin = arc.GatewayPlugin("Ping")
version: float = 1.0



@plugin.include
@arc.slash_command("ping", "Get's bot Latency to discord Servers")
async def ping(ctx: arc.GatewayContext, /) -> None:
    """Responds to user calling command with bot latency to discord"""
    botPing: float= float(str(BOT.heartbeat_latency*100)[:-10])
    pingEmbed: hikari.Embed = hikari.Embed()
    
    pingEmbed.title = "Ping!"
    if botPing < 35: pingEmbed.color = hikari.Color(int("15cdf2", 16))
    elif botPing < 50: pingEmbed.color = hikari.Color(int("d2f884", 16))
    elif botPing > 50: pingEmbed.color = hikari.Color(int("c73ea2", 16))
    elif botPing > 200: pingEmbed.color = hikari.Color(int("ff0000", 16))

    if botPing > 200:
        pingEmbed.add_field(name="Latency!??!?!?!", value=f'{botPing} Ms', inline=True)
        pingEmbed.add_field(name="WHY!!!!", value="Is your server running in a chinese basement???")
    else:
        pingEmbed.add_field(name="Latency", value=f'{botPing} Ms')
    pingEmbed.set_author(name="NaterBot", icon=str(Config.config.bot.botpfp))

    await ctx.respond(embed=pingEmbed)






@arc.loader
def load(client: arc.GatewayClient) -> None:
    logger.info(f"Loading {plugin.name} Plugin")
    client.add_plugin(plugin)

@arc.unloader
def unloader(client: arc.GatewayClient) -> None:
    logger.info(f"Un-Loading {plugin.name} Plugin")
    client.remove_plugin(plugin)
