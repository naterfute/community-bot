#import hikari
#import miru
#from typing import Any
import arc
#from sqlalchemy import select
#from bot.database.models import Economy, Users
#from bot.database.database import Database
#from ..bot import BOT

from loguru import logger

#from ..utils import configBOT

plugin: arc.GatewayPlugin = arc.GatewayPlugin("Economy")
version: float = 1.0


#@plugin.include
#@arc.slash_command("balance", "Checks your current balance")
#async def balance(ctx: arc.GatewayContext) -> None:
#    bal = (
#        select(Economy).
#        where(Economy.uid == ctx.user.id)
#      )
#    user_economy: Any = result.scalar_one_or_none() # type: ignore
#    type(bal)
#
#    if user_economy is None:
#        await ctx.respond("You don't have an account in the economy system yet!")
#        return None
#
#    await ctx.respond(user_economy)



#@plugin.include
#@arc.slash_command("newuser", "adds a new user")
#async def newuser(ctx: arc.GatewayContext):
#  await ctx.defer()
#
#  async with Database.session() as conn:
#    # Check if the user already exists
#    existing_user = await conn.get(Users, ctx.user.id)
#    if existing_user:
#        await ctx.respond("User already exists in the database!")
#        return
#    
#    # Create a new user instance
#    new_user = Users(uid=str(ctx.user.id))
#    
#    # Add the new user to the session and commit the transaction
#    conn.add(new_user)
#    try:
#        await conn.commit()
#        await ctx.respond(f"User <@{ctx.user.id}> has been added successfully!")
#    except Exception as e:
#        # Rollback in case of an error and notify the user
#        await conn.rollback()
#        await ctx.respond(f"Failed to add the user. Error: {str(e)}")




@arc.loader
def load(client: arc.GatewayClient) -> None:
    logger.info(f"Loading {plugin.name} Plugin")
    client.add_plugin(plugin)

@arc.unloader
def unloader(client: arc.GatewayClient) -> None:
    logger.info(f"Un-Loading {plugin.name} Plugin")
    client.remove_plugin(plugin)

