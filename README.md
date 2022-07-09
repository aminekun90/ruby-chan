# Ruby Chan [![Python 3.10.4](https://img.shields.io/badge/python-3.10.4+-blue.svg)](https://www.python.org/downloads/release/python-3105/)

Meet Ruby chan, she is a Bot for discord.

She can do a lot of things (documentation will be available soon)

- This bot is for private and non commercial use only.


### To update pip requirements:

```bash
pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip install -U
pip freeze > requirements.txt
```

### Make sure you have a valid .env file or ENV variables correctly set:

Replace the ``<something>`` with your values and save everything in ``server/.env`` .

```bash
# .env
DISCORD_BOT_TOKEN=<DISCORD-TOKEN>
CLEAR_DB_HOST=<DB-HOST-IP># Can be localhost
CLEAR_DB_USER=<DBUSER>
CLEAR_DB_PASSWORD=<DB-PASSW>
CLEAR_DB_DATABASE=<DB>
```

### Use docker

Just launch :

```bash
./docker-build-run.sh
```
