"""
bot.utils.github.py
Bad Programming, this file only has some github interactions"""
import os
from os import listdir
from bot.config import Config
from git import Repo, GitCommandError
from loguru import logger
import pathlib

repo_url = "https://github.com/blazium-engine/blazium.git"
local_file = pathlib.Path(__file__).parent.resolve()

class files():

    @classmethod
    def getFiles(cls) -> dict[str, str]:
        fileStruct: dict[str, str] = {}
        validNames: list[str] = []
        for file in listdir(os.path.join(local_file, "blazium", "doc", "classes")):
            fileStruct[f"{file.lower()}"] = file
            validNames.append(f"{file.lower()}")
        cls.nodes = fileStruct
        cls.validNames = validNames

        return fileStruct


def download_directory(repo_url: str | None = None, local_dir: str = os.path.join(str(local_file), "blazium")) -> int:
    """
    Downloads all files in a specific GitHub repository directory.
    :param repo_url: Repository url in the format 'https://github.com/blazium-engine/blazium.git'
    :param local_dir: Local directory to save the files
    ---
    Returns 1 For Success
    Returns 0 For Failure
    """

    try:
        if not repo_url:
            repo_url = Config.config.git.repo
        repo = Repo.clone_from(
            url=repo_url,
            to_path=local_dir,
            multi_options=["--depth", "1", "--no-checkout"]
        )

        repo.git.sparse_checkout("set", "doc/classes")
        repo.git.checkout("blazium-dev")
    except GitCommandError as e:
        pass
    except Exception as e:
        logger.critical(e)
        return 0
    finally:
        logger.success("Finished Git command")
    files.getFiles()
    return 1

def update_directory(local_dir: str=os.path.join("blazium")) -> int:
    """
    Update the git repo to latest head
    :param local_dir: Local directory of git repo
    ---
    Returns 1 For Success
    Returns 0 For Failure
    """
    try:
        repo = Repo(local_dir)

        repo.git.pull()
        files.getFiles()
        return 1
    except Exception as e:
        logger.error(f"An Error Occured when updating repo {e}")
        return 0


