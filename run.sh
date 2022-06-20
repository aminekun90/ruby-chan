#!/bin/sh

## Usage:
## if it's the first time change the chmode of this file
##   . chmode +x run.sh
##   . ./run.sh
envpath=server/.env
unamestr=$(uname)
if [ "$unamestr" = 'Linux' ] || [ "$unamestr" = 'Darwin' ]; then

  export $(grep -v '^#' $envpath | xargs -d '\n')

elif [ "$unamestr" = 'FreeBSD' ]; then

  export $(grep -v '^#' $envpath | xargs -0)

fi
source venv/bin/activate
python3 bot.py
