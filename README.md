# TippBot

TippBot is a Discord tip bot.

## Usage

The bot is designed to be deployed using docker.

Edit docker-compose.yml to tweak relevant settings like RPC_PORT and RPC_HOST. Data persistance is advised and is done via /opt/tippbot directory by default.

Bot needs BOT_ID and BOT_TOKEN variables, those are obtained from discord development portal and saved into `bot-variables.env` text file.

To run:

> docker-compose -d

It should just work. If something goes wrong snoop around it's probably easy to fix.

## Tips:

> pc1qrsws36lt7k5l0m8ygvnlje5xmgwt2prwzj7eem