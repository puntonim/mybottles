#!/bin/bash

: '
This script is meant to ease the recreation of a dev db and the loading of sample data.
It makes use of django-extensions'' dumpscript/runscript.

Create new sample data with:
$ manage dumpscript core > scripts/fixture_sample_data1.py
$ manage dumpscript auth.user > scripts/fixture_admin_user.py

The scripts can then be run to import sample data with:
$ manage runscript fixture_sample_data1

Note: you might need to add:
from uuid import UUID
'

# Directory where this file is located.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Ensure we are in debug mode.
./manage.py print_settings | grep "DEBUG.*=.*True"
if [ "$?" -ne "0" ]  # If the previous command has failed.
then
    echo -e "\n ** You seem not to be in the DEV environment (and in DEBUG mode), aborting!\n"
	exit 1
fi

cd $DIR/..

# Set verbosity to print the commands.
set -v

rm db.sqlite3
./manage.py migrate
./manage.py runscript fixture_admin_user

read -p '> Load sample_data1 fixture? y*/n ' answer
if [[ "$answer" != "n" ]]
then
./manage.py runscript fixture_sample_data1
fi

set +v