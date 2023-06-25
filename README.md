# Process over Profit Bot

The bot is currently capable of the following:

* Reporting the economic news events for the current day as obtained from Forex Factory.
* Enumerating the list of users who haven't performed a check-in and are thus in danger of being booted.

## Dependencies

This bot depends on the following Python packages:

* discord.py (for obvious reasons)
* python-dotenv (for loading the bot token from the local environment)
* requests (for querying economic news)

Install them with the following command:

```sh
pip install discord.py python-dotenv requests
```

## Environment Setup

Prior to running the bot, you will need to ensure that the DISCORD_BOT_TOKEN environment variable has been set to the token that was generated when creating your bot application using the Discord developer portal.

As this project makes use of python-dotenv, you can accomplish this by creating a file named ".env" and setting the value there.

Example .env file:

```sh
DISCORD_BOT_TOKEN=your_secret_token
```

## Running the Bot

The bot can be run from the terminal with the following command:

```sh
python ./bot.py
```

### Running in a Docker Container

The bot can also be run in a Docker container.

The necessary Dockerfile is included.