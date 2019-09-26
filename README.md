# Running the bot for test purpose

## Generate a client ID token

Follow the "Getting Started" section of [this page](https://www.howtogeek.com/364225/how-to-make-your-own-discord-bot/) to get your bot client token.

Then, next to the `bot.py` file, save a `token.tkt` containing only the token previously found.

## Installing the dependencies

This ZdS bot rely on two libraries for the moment:

- `discord.py` for everything related to the discord management.
- `beautifulsoup4` to parse web page and get the result when the user run the `!cherche` command.

To install it all, create a virtualenv and pip install stuff.

```bash
virtualenv venv -p=python3
source venv/bin/activate
pip install -r requirements
```

You are now good to go!

## Adding the bot to your test server

Follow the "How to Add the Bot to Your Server" section of [this page](https://www.howtogeek.com/364225/how-to-make-your-own-discord-bot/) to add the bot to your own Discord test server.
