# place this line in /etc/rc.local
su chriscauley -c 'cd /home/chriscauley/placereddit; uwsgi /usr/bin/uwsgi -s 127.0.0.1:46536 -z 180 -t 180 -M -p 8 -C  -x /home/chriscauley/placereddit/uwsgi.xml' &