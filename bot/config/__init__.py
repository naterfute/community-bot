'''App's config using Pydantic base models at bot.config'''
import tomllib
from os import path
from loguru import logger
from pydantic import BaseModel, ValidationError
from typing import Any
import requests
import os
from dotenv import load_dotenv

class DefaultConfig(BaseModel):
    token: str
    botpfp: str

class DatabaseConfig(BaseModel):
    engine: str
    host: str
    port: int
    username: str
    password: str
    database: str

class GitConfig(BaseModel):
    repo: str
    localdir: str = "blazium"

class MessageConfig(BaseModel):
    activity: str

class VersionConfig(BaseModel):
    version: str
    major: int
    minor: int
    branch: str

class LoggingConfig(BaseModel):
    debug: bool
    trace: bool

class configuration(BaseModel):
    logging: LoggingConfig
    bot: DefaultConfig
    database: DatabaseConfig
    git: GitConfig
    message: MessageConfig
    VERSION: VersionConfig



class Config:
    config: configuration
    @classmethod
    def loadConfig(cls) -> None:
        """Loads, Fetches, and Validates config from a pre-determined file"""
        load_dotenv()
        config: dict[str, Any] = {
            'logging':
                    {
                'debug': os.getenv("DEBUG"),
                'trace': os.getenv("TRACE")

            },
            'bot': 
                {'token': os.getenv("TOKEN"),
                 'botpfp': os.getenv("BOTPFP")
                 },
            'database': 
                {'engine': os.getenv("ENGINE"),
                'host': os.getenv("HOST"),
                'port': os.getenv("PORT"),
                'username': os.getenv("DBUSERNAME"),
                'password': os.getenv("PASSWORD"),
                'database': os.getenv("DATABASE")
                 },
            'git':
                {'repo': os.getenv("REPO_URL"),
                 'localdir': "blazium",

                },
            'message': 
                {'activity': os.getenv("ACTIVITY")},
        }


        configfile: str = path.join("bot", "app.toml")

        with open(configfile, 'rb') as file:
            fileconfig = tomllib.load(file)

        for x in fileconfig.values():
            config["VERSION"] = x
        try:
            cls.config = configuration(**config)
        except ValidationError as exc:
            print(repr(exc.errors()[0]['type']))
            #> 'missing'




    class Version:

        @classmethod
        def compareLatest(cls) -> str:
            """Gets NateQK's Current version and compares to latest release"""


            CurrentMajor = Config.config.VERSION.major
            CurrentMinor = Config.config.VERSION.minor
            CurrentBranch = Config.config.VERSION.branch

            CurrentVersion = f"{CurrentMajor}.{CurrentMinor}{CurrentBranch if CurrentBranch != 'dev' else ''}"

            # TODO:
            # Ping github Looking for latest version
            # I'm working on getting a webserver setup
            # using github pages so this is easy
            LatestVersion=cls.latestVersion() # Ping github and look for latest version
            if CurrentVersion != LatestVersion:
                Response: str = f"""
                Latest Version: {LatestVersion}
                Current Version: {CurrentVersion}
                """
                return Response
            else:
                return CurrentVersion

        @classmethod
        def latestVersion(cls) -> str:
            """Gets NateQK's latest version"""
            try:
                req: requests.Response = requests.get("https://nateqk.github.io/latest/latest.json")
                reqjson: Any = req.json()

            except requests.HTTPError as e:
                logger.error(f"Somethig went terribly wrong with your request to check latest bot version: {e}")
                return f"{e}"

            logger.debug(req.json())
            return f"{reqjson['version']['major']}.{reqjson['version']['minor']}"


