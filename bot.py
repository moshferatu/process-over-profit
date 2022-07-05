import os

from discord import Intents
from discord.ext.commands import Bot

intents = Intents.default()
intents.members = True

bot = Bot(intents=intents, command_prefix='!')

@bot.command()
async def test(context):
  await context.send('Test was successful!')

@bot.command()
async def boot(context, message_link):
  # TODO: Whitelist users that can run this command.
  message_link_components = message_link.split('/')
  channel_id = message_link_components[-2]
  message_id = message_link_components[-1]
  channel = await bot.fetch_channel(channel_id)
  message = await channel.fetch_message(message_id)
  
  checked_in_members = set()
  for reaction in message.reactions:
    checked_in_members.update([member for member in await reaction.users().flatten()])
  all_members = set(member for member in bot.get_all_members())
  members_to_boot = all_members - checked_in_members

  # TODO: Don't think it's possible to boot an admin, but exclude them anyways.
  
  # Don't boot the bots.
  bots = set(member for member in all_members if member.bot)
  members_to_boot = members_to_boot - bots

  # TODO: Actually boot people.
  await context.send('Members to boot: ' + str([member.name for member in members_to_boot]))

bot.run(os.environ['DISCORD_BOT_TOKEN'])