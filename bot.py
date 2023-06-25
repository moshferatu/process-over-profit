import os
import requests

from datetime import datetime
from discord import Intents
from discord.ext.commands import Bot
from dotenv import load_dotenv

load_dotenv()

intents = Intents.all()
intents.members = True

bot = Bot(intents=intents, command_prefix='!')

@bot.command()
async def test(context):
  await context.send('Test was successful!')

do_not_boot_roles = ['DNB', 'MASTER DEBATERS', 'MODS', 'PROS']

def batch_members(members, batch_size):
  for i in range(0, len(members), batch_size):
    yield members[i:i + batch_size]

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

  # Don't boot members belonging to privileged roles (e.g., MODS).
  do_not_boot_members = set(member for member in members_to_boot 
                         if any(role.name in do_not_boot_roles for role in member.roles))
  members_to_boot = members_to_boot - do_not_boot_members

  sorted_members_to_boot = sorted(members_to_boot, key=lambda member: member.display_name.lower())

  if not sorted_members_to_boot:
    await context.send('No members to :boot:')
    return

  # Send multiple messages, if necessary, in order to avoid Discord API message length limit.
  for member_batch in batch_members(sorted_members_to_boot, 50):
    member_mentions = ', '.join([member.mention for member in member_batch])
    await context.send(member_mentions)

# Forex Factory news calendar.
news_url = 'https://nfs.faireconomy.media/ff_calendar_thisweek.json'

def get_date_time(date_str):
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")

@bot.command()
async def news(context):
  now = datetime.now()
  news_response = requests.get(news_url)
  if news_response.status_code == 200:
      this_weeks_news_events = news_response.json()
      todays_news_events = [event for event in this_weeks_news_events
                            if get_date_time(event['date']).date() == now.date()
                            and event['country'] == 'USD']
      if not todays_news_events:
         await context.send('No news for ' + now.strftime('%B %d'))
         return
      news_events_by_time = dict()
      for news_event in todays_news_events:
          news_date_time = get_date_time(news_event['date'])
          news_time = news_date_time.strftime('%I:%M %p ET')
          news_title = news_event['title']
          if news_date_time < datetime.now(news_date_time.tzinfo):
            news_title = '~~' + news_title + '~~'
          if news_time not in news_events_by_time:
              news_events_by_time[news_time] = list()
          news_events_by_time[news_time].append(news_title)
      news_response = '# News for ' + now.strftime('%B %d')
      for news_time in news_events_by_time.keys():
          news_response += '\n## {time}'.format(time = news_time)
          for news_event in news_events_by_time[news_time]:
              news_response += '\n* {event}'.format(event = news_event)
      await context.send(news_response)
  else:
      await context.send('Error fetching news for ' + now.strftime('%B %d'))

# Bot token needs to be added to environment variables when running.
bot.run(os.environ['DISCORD_BOT_TOKEN'])