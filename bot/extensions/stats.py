import hikari
import miru
import arc
from typing import Any
from loguru import logger
import psutil
import platform
from datetime import datetime

import requests

from ..bot import BOT


plugin: arc.GatewayPlugin = arc.GatewayPlugin("Stats")
version: float = 1.0

launchTime = datetime.now()

def solveunit(input: int) -> Any:
    output: Any = ((input // 1024) // 1024) // 1024
    return int(output)


@plugin.include
@arc.with_hook(arc.user_limiter(360, 1))
@arc.slash_command("stars","Shows the star history of blazium")
async def stars(ctx: arc.GatewayContext):
    url = "https://api.star-history.com/svg?repos=blazium-engine/blazium&type=Timeline&theme=dark"
    response = requests.get(url)
    #logger.error(response.content)
    if not response.status_code == 200:
        logger.error(response)
        await ctx.respond("Failed to get Star Histroy Image")
    #pyvips.Image.svgload_buffer()

    await ctx.respond("Coming Soon!")



@plugin.include
@arc.with_hook(arc.user_limiter(360, 5))
@arc.slash_command("stats", "Get's info about the system hardware")
async def stats(ctx: arc.GatewayContext):

    if ctx.guild_id != None:
        members: int = await BOT.rest.fetch_members(ctx.guild_id).count()
    else: members: int = 0

    try:
        mem_usage = "{:.2f} MiB".format(
            __import__("psutil").Process(
            ).memory_full_info().uss / 1024 ** 2
        )
    except AttributeError:
        # NOTE: OS doesn't support retrieval of USS (probably BSD or Solaris)
        mem_usage = "{:.2f} MiB".format(
            __import__("psutil").Process(
            ).memory_full_info().rss / 1024 ** 2
        )
    freq = psutil.cpu_freq(percpu=False).current
    sysboot = datetime.fromtimestamp(psutil.boot_time()).strftime("%B %d, %Y at %I:%M:%S %p")
    uptime: Any = datetime.now() - launchTime
    hours, rem = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(rem, 60)
    days, hours = divmod(hours, 24)

    if days:
        time = "%s days, %s hours, %s minutes, and %s seconds" % (
            days,
            hours,
            minutes,
            seconds,
        )
    else:
        time = "%s hours, %s minutes, and %s seconds" % (
            hours, minutes, seconds)
    em = hikari.Embed(title="System Status", color=0x32441C)
    em.add_field(
        name=":desktop: CPU Usage",
        value=f"{psutil.cpu_percent():.2f}% ({psutil.cpu_count(logical=False)} Cores / {psutil.cpu_count(logical=True)} Threads) ({'{:0.2f}'.format(freq)} MHz) \nload avg: {psutil.getloadavg()}",
        inline=False,
    )
    em.add_field(
        name=":computer: System Memory Usage",
        value=f"**{psutil.virtual_memory().percent}%** Used",
        inline=False,
    )
    em.add_field(
        name=":dna: Kernel Version",
        value=platform.platform(aliased=True, terse=True),
        inline=False,
    )
    em.add_field(
        name=":gear: Library Version",
        value=f"hikari {hikari.__version__} + Arc {arc.__version__} + Miru {miru.__version__}",
        inline=False,
    )
    em.add_field(
        name="\U0001F4BE BOT Memory usage",
        value=mem_usage,
        inline=False
    )
    em.add_field(
        name=":minidisc: Disk Usage",
        value=f"Total Size: {solveunit(psutil.disk_usage('/').total)} GB \nCurrently Used: {solveunit(psutil.disk_usage('/').used)} GB",
        inline=False,
    )
    em.add_field(
        name="\U0001F553 BOT Uptime",
        value=time,
        inline=False
    )
    em.add_field(
        name="⏲️ Last System Boot Time",
        value=sysboot,
        inline=False
    )
    em.add_field(
        name="👥 Users",
        value=str(members),
        inline=False
    )
    await ctx.respond(embed=em)


@arc.loader
def load(client: arc.GatewayClient) -> None:
    logger.info(f"Loading {plugin.name} Plugin")
    client.add_plugin(plugin)

@arc.unloader
def unloader(client: arc.GatewayClient) -> None:
    logger.info(f"Un-Loading {plugin.name} Plugin")
    client.remove_plugin(plugin)
