from alembic.config import Config as alConf
from alembic import command
from bot.config import Config as conf
from bot.database.database import DBTypes
from loguru import logger



def migrate():
    config = conf.config
    logger.debug(config.database) 
    # NOTE: Setup alembic config
    engineType = getattr(DBTypes, config.database.engine)
    alembic_cfg = alConf()
    alembic_cfg.set_main_option("script_location", "bot/database/alembic")
    alembic_cfg.set_main_option("prepend_sys_path", ".")

    if not str(config.database.password) == str(""):
        alembic_cfg.set_main_option("sqlalchemy.url", f'{engineType["database"]}+{engineType["driver"]}://{config.database.username}:{config.database.password}@{config.database.host}:{config.database.port}/{config.database.database}')
    else:
        alembic_cfg.set_main_option("sqlalchemy.url", f'{engineType["database"]}+{engineType["driver"]}://{config.database.username}@{config.database.host}:{config.database.port}/{config.database.database}')



    # NOTE: Upgrade database tables to latest version
    command.upgrade(alembic_cfg, "head")

