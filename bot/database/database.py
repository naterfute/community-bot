''' 
bot/utils/database/postgresql.py
The database handler module.

Contains:
Database interactions
Connection Info

'''

from loguru import logger
from typing import TypedDict
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession, async_sessionmaker


from alembic.config import Config as alConf
from alembic import command
from bot.config import Config

config = Config.config

class DBInfo(TypedDict):
    database: str
    driver: str


class DBTypes():
    postgresql: DBInfo = {"database": "postgresql", "driver": "asyncpg"}
    mysql: DBInfo = {"database": "mysql", "driver": "aiomysql"}
    mariadb: DBInfo = {"database": "mysql", "driver": "aiomysql"}
    #sqlite: DBInfo = {"database": "sqlite", "driver": "aiosqlite"} # TODO: Implement logic that allows for sqlite to be used properly

class Migrate():
    def migrate(self):

        # NOTE: Setup alembic config
        engineType = getattr(DBTypes, config.database.engine)
        alembic_cfg = alConf()
        alembic_cfg.set_main_option("script_location", "bot/database/alembic")
        alembic_cfg.set_main_option("prepend_sys_path", ".")

        logger.debug(config.database)
        if not str(config.database.password) == str(""):
            alembic_cfg.set_main_option("sqlalchemy.url", f'{engineType["engine"]}+{engineType["driver"]}://{config.database.username}:{config.database.password}@{config.database.host}:{config.database.port}/{config.database.database}')
        else:
            alembic_cfg.set_main_option("sqlalchemy.url", f'{engineType["engine"]}+{engineType["driver"]}://{config.database.username}@{config.database.host}:{config.database.port}/{config.database.database}')



        # NOTE: Upgrade database tables to latest version
        command.upgrade(alembic_cfg, "head")






class Database:
    uri: str
    engine: AsyncEngine
    engineType: DBInfo
    failedConnectionEvents: int
    
    @classmethod
    async def connect(cls) -> AsyncEngine:
        try:
            cls.engineType = getattr(DBTypes, config.database.engine)
            logger.debug(f"""
                        Username: {config.database.username}
                        Password: {config.database.password}
                        Host: {config.database.host}
                        Database: {config.database.database}
                        Engine Info: {cls.engineType}
                """)
            cls.engine = create_async_engine(
                f"{cls.engineType['database']}+{cls.engineType['driver']}://{config.database.username}:{config.database.password}@{config.database.host}/{config.database.database}",
                pool_size=20,
                max_overflow=40,
                pool_timeout=30,
                pool_recycle=1800
            )
            cls.session = async_sessionmaker(cls.engine, class_=AsyncSession, expire_on_commit=False)

        except Exception as e:
            logger.error("Failed to connect to the database!")
            logger.error(e)

        return cls.engine




    @classmethod
    async def disconnect(cls) -> int:
        try:
            await cls.engine.dispose()
            return 1
        except Exception as _e:
            logger.error(f"Failed to dispose of database connection: {_e}")
            return 0


    @classmethod
    async def testCon(cls) -> int:
        try:
            async with cls.engine.connect() as _connection:
                return 0
        except Exception as e:
            print("Connection failed:", str(e))
            return 1

    @classmethod
    async def reconnect(cls) -> int:
        try:
            await cls.disconnect()
            await cls.connect()
            return 1
        except Exception as e:
            logger.error(e)
            return 0

