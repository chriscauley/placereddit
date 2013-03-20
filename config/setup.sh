suod apt-get update
sudo apt-get install postgresql-9.1 postgresql-server-dev-9.1 python-dev git-core \
    emacs23-nox screen mlocate nginx uwsgi uwsgi-plugin-python python-setuptools node-less -y
sudo easy_install pip

# need this to push
git config --global user.email "chris@lablackey.com"
git config --global user.name "chriscauley"

# caching for memcached, probably depracating that soon in favor of varnish
sudo mkdir /var/cache/django
sudo chown chriscauley.chriscauley /var/cache/django/

# python programs
sudo pip install -r requirements.txt 
