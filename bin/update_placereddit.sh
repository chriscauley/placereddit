#! /bin/bash

#0   */6  *   *   *  django  python /home/django/placereddit/manage.py update_placereddit

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
DIR=/home/django/placereddit/
cd $DIR
source .venv/bin/activate

mkdir -p logs
python manage.py update_placereddit > logs/update_placereddit.log