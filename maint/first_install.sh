#!/bin/sh

# Requirements
# Install python3 and virtualenvwrapper

TORPEDO_VIRTUALENV='devenv'

if [ $TORPEDO_DEV_HOME == '' ]; then
    TORPEDO_DEV_HOME = `cwd` + '../$TORPEDO_VIRTUALENV'
fi

cd $TORPEDO_DEV_HOME
mkvirtualenv -p /usr/local/bin/python3 dev