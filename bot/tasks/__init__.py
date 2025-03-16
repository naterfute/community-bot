from os import path
from bot.config import Config

config = Config.config


async def hourlyTasks():
    """A list of Tasks that need to run every hour"""
    from bot.github import download_directory, update_directory
    if not path.exists(config.git.localdir):
        download_directory(config.git.repo)

    else:
        update_directory()

