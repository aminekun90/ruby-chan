# Ruby Chan [![Python 3.9.7](https://img.shields.io/badge/python-3.10.4+-blue.svg)](https://www.python.org/downloads/release/python-397/)

Meet Ruby chan, she is a Bot for discord.

She can do a lot of things (documentation will be available soon)

- This bot is for private and non commercial use only.


### To update pip requirements:

```bash
pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip install -U
pip freeze > requirements.txt
```