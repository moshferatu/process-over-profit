import os

from discord import Intents
from discord.ext.commands import Bot

intents = Intents.all()
intents.members = True

bot = Bot(intents=intents, command_prefix='!')

@bot.command()
async def test(context):
  await context.send('Test was successful!')

@bot.command()
async def boot(context, message_link):
  message_link_components = message_link.split('/')
  channel_id = message_link_components[-2]
  message_id = message_link_components[-1]
  channel = await bot.fetch_channel(channel_id)
  message = await channel.fetch_message(message_id)
  
  checked_in_members = set()
  for reaction in message.reactions:
    checked_in_members.update([member async for member in reaction.users()])
  # This returns the users from every server the bot is in.
  # Ideally, this would only return the users in the current server.
  # Since the bot is only running on one server for now, leaving as is.
  all_members = set(bot.get_all_members())
  members_to_boot = all_members - checked_in_members
  
  # Don't boot the bots.
  bots = set(member for member in all_members if member.bot)
  members_to_boot = members_to_boot - bots

  await context.send('Members to boot: ' + str([member.name for member in members_to_boot]))

# Bot token needs to be added to environment variables when running.
bot.run(os.environ['DISCORD_BOT_TOKEN'])