#! /bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
DIR=/home/django/placereddit/
cd $DIR
source .venv/bin/activate

uwsgi -x uwsgi.xml