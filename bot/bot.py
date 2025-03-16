'''Base bot containing things such as

BOT,
client,
and some listen events for starting the bot
'''
import hikari
import arc
import miru
from os import path
from sys import stderr
from loguru import logger
from typing import Any
from .github import files, download_directory, update_directory
from .tasks import hourlyTasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler # type: ignore
from .config import Config
from bot.database.migrate import migrate

Config.loadConfig()

migrate()


def debug_init(trace: bool = False, debug: bool = False):
    logger.remove()
    if debug:
        logger.add(stderr, level='DEBUG')
    elif trace:
        logger.add(stderr, level='TRACE')
    else:
        logger.add(stderr, level='INFO')
        pass
    pass

debug_init(Config.config.logging.trace, Config.config.logging.debug)
def test_logging():
    logger.debug("Debug is Working")
    logger.trace("Trace is Working")
    logger.error("Error is Working")
    logger.info("Info is Working")
    logger.warning("Warning is Working")
    logger.success("Success is Working")
    logger.critical("Critical is Working")


test_logging()

BOT: hikari.GatewayBot = hikari.GatewayBot(
    token=Config.config.bot.token,
    intents=hikari.Intents.ALL,
)

client: arc.GatewayClient = arc.GatewayClient(BOT)
miruClient: miru.Client = miru.Client.from_arc(client)


client.load_extensions_from(path.join("bot", "extensions"))

@client.listen()
async def on_startup(event: arc.StartedEvent[Any]) -> None:

    download_directory()
    update_directory()
    files.getFiles()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(hourlyTasks, 'cron', minute=0) #type: ignore
    scheduler.start()
    logger.info(f"Bot Version: {Config.config.VERSION}")
