import hikari
import arc
from loguru import logger
from datetime import datetime
from bot.config import Config
from bot.github import download_directory, update_directory, files
from bot.parsers.xml import xmlParser
import requests
from pydantic import BaseModel as base
from pydantic import Field
from os import path
from typing import Any
#import Levenshtein
from rapidfuzz import process, fuzz
from typing import Optional
import re


config = Config.config

#def get_best_match(input_word: str) -> Any:
#    best_match = min(files.validNames, key=lambda word: Levenshtein.distance(input_word, word))
#    return best_match

def get_best_match(input_word: str, score_cutoff: float = 70) -> Optional[str]:
    result = process.extractOne(input_word, files.validNames, scorer=fuzz.ratio, score_cutoff=score_cutoff) #type: ignore
    return result[0] if result else None 


async def parse_xml_nodes(description: str) -> str:
  """
  ---
  Parses node names from the description and hardcodes a link to the docs in them
  """
  descriptionreturn: str = re.sub(r"", "", description)
  
  return descriptionreturn

async def parse_xml_description(description: str) -> str:

  descriptionreturn: str = re.sub(r"\[b\]", "** ", description)
  descriptionreturn: str = re.sub(r"\[/b\]", "**\n", descriptionreturn)
  descriptionreturn: str = re.sub(r"\[i\]", "*", descriptionreturn)
  descriptionreturn: str = re.sub(r"\[/i\]", "*", descriptionreturn)
  descriptionreturn: str = re.sub(r"\[code\]", "`", descriptionreturn)
  descriptionreturn: str = re.sub(r"\[/code\]", "`", descriptionreturn)

  return descriptionreturn



class reactionsDict(base):
  url: str
  total_count: int
  plus1: Any = Field(alias="+1")
  minus1: Any = Field(alias="-1")
  laugh: int
  hooray: int
  confused: int
  heart: int
  rocket: int
  eyes: int

class prDict(base):
  url: str
  html_url: str
  diff_url: str
  patch_url: str
  merged_at: str | None


class userDict(base):
  login: str
  id: int
  node_id: str
  avatar_url: str
  gravatar_id: str
  url: str
  html_url: str
  followers_url: str
  following_url: str
  gists_url: str
  starred_url: str
  subscriptions_url: str
  organizations_url: str
  repos_url: str
  events_url: str
  received_events_url: str
  userType: str | None = None
  user_view_type: str
  site_admin: bool


class internalIssues(base):
  url: str
  repository_url: str
  labels_url: str | None
  comments_url: str
  events_url: str
  html_url: str
  id: int
  none_id: str | None = None
  number: int
  title: str
  user: userDict
  labels: list[str] | None
  state: str
  locked: bool
  assignee: str | None
  assignees: list[str]
  milestone: str | None
  comments: int
  created_at: str 
  updated_at: str
  closed_at: str | None
  author_association: str
  active_lock_reason: str | None
  draft: bool
  pull_request: prDict
  body: str | None
  closed_by: str | None
  reactions: reactionsDict
  timeline_url: str
  performed_via_github_app: str | None
  state_reason: str | None = None



plugin: arc.GatewayPlugin = arc.GatewayPlugin("blazium")

#scheduler: AsyncIOScheduler = AsyncIOScheduler()
timeChoices: list[str]  = ["m", "h", "d"]
# TODO: This should be moved to something configurable using {org-name} and {repo-name}
issuesUrl: str = "https://api.github.com/repos/blazium-engine/blazium/issues"

async def steal_time(time:str) -> datetime:
  print(time)


  return datetime.now()



#@plugin.include
#@arc.slash_command("issues", "Cycle Through Github issues in the github")
async def issues(ctx: arc.GatewayContext) -> None:
  headers: dict[str, str] = {
    "accept": "application/vnd.github.raw+json"
  }
  response = requests.get(issuesUrl, headers=headers)
  if response.status_code == 200:
    pass
  elif response.status_code == 422:
    await ctx.respond("Validation failed, or the endpoint has been spammed.")
    return
  else:
    await ctx.respond(f"An error has occured, We got a status code of {response.status_code} ping Naterfute or Bioblaze Payne")
    return
  issue: internalIssues
  issues: internalIssues = internalIssues(**response.json()[0])

  for issue in response.json():
    issue = internalIssues(**issue) # type: ignore
  await ctx.respond(issues.html_url)
  #logger.error(issues)


@plugin.include
@arc.slash_command("links","Responds with a link to all the stores blazium is on!")
async def links(ctx: arc.GatewayContext) -> None:
  em: hikari.Embed = hikari.Embed(title="Blazium Store Pages")
  # TODO: Replace hardcoded links with links put into the database through a command
  # It should be done in such a way that it's not inconveinent or slow,
  # the command should do the following
  # - Start a modal using hikari-miru
  # Ask the following questions
  # - Title
  # - Description
  # When Submitted We put a new entry in the database with this info, probably a new row

  em.set_author(name="NaterBot", icon=str(config.bot.botpfp))
  em.add_field("Github", "https://github.com/blazium-engine/blazium/releases")
  em.add_field("Itch.io", "https://blaziumengine.itch.io/")
  em.add_field("Steam", "https://store.steampowered.com/app/3293450/Blazium_Engine/")
  em.set_footer("Blazium Community Bot", icon=str(config.bot.botpfp))
  await ctx.respond(embed=em)


@plugin.include
@arc.with_hook(arc.guild_only)
@arc.with_hook(arc.has_permissions(hikari.Permissions.ADMINISTRATOR))
@arc.slash_command("updateclasses", "This command will auto-run Every hour on the hour")
async def updateBlaziumClasses(ctx: arc.GatewayContext) -> None:
  await ctx.defer()
  job: int
  if not path.exists(config.git.localdir):
    job = download_directory(config.git.repo)

  else:
    job = update_directory()
  
  if job == 1:
    await ctx.respond("Successfully updated/downloaded files")
  elif job == 0:
    await ctx.respond("An error occured when updating files. Check logs and contact <@358720980669038592>")


@plugin.include
@arc.with_hook(arc.guild_only)
@arc.slash_command("node", "Describes a node to you, with links to tutorials if available")
async def requestClass(
    ctx: arc.GatewayContext,
    nodename: arc.Option[str, arc.StrParams()]):
  try:
    name = files.nodes[f"{nodename.lower()}.xml"]
  except KeyError:
    match: str | None = get_best_match(nodename.lower())
    if not match == None:
      await ctx.respond(f"The node you specified does not exist! Were you searching for `{match[:-4]}`?")
    else:
      await ctx.respond(f"The node you specified does not exist!")

    return
  xml: Any = xmlParser.parseNode(name) # type: ignore

  requestEmbed: hikari.Embed = hikari.Embed(title=xml["name"], url=f"https://github.com/blazium-engine/blazium/blob/blazium-dev/doc/classes/{xml['name']}.xml", description=str(await parse_xml_description(xml["description"])))
  requestEmbed.set_author(name="NaterBot", icon=config.bot.botpfp, url="https://github.com/nateQK/NateQK")
  requestEmbed.color = hikari.Color(int("7732D9", 16))

  if xml["inherits"] != None:
    requestEmbed.add_field(name="Inherits", value=xml["inherits"])
  tutstr: str = ""
  
  for tutorial in xml['tutorials']:
    tutstr = tutstr + f"[{tutorial['title']}]({tutorial['url']})\n"

  requestEmbed.add_field(name="Tutorials", value=tutstr)
  requestEmbed.set_footer("This message is Auto Generated Using Blaizum Docs | Blazium Community Bot")

  await ctx.respond(embed=requestEmbed)


@arc.loader
def load(client: arc.GatewayClient) -> None:
    logger.info(f"Loading {plugin.name} Plugin")
    client.add_plugin(plugin)

@arc.unloader
def unloader(client: arc.GatewayClient) -> None:
    logger.info(f"Un-Loading {plugin.name} Plugin")
    client.remove_plugin(plugin)
