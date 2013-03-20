suod apt-get update
sudo apt-get install postgresql-9.1 postgresql-server-dev-9.1 python-dev
sudo apt-get install git-core emacs23-nox screen mlocate nginx uwsgi uwsgi-plugin-python

git config --global user.email "chris@lablackey.com"
git config --global user.name "chriscauley"

sudo mkdir /var/cache/django
sudo chown chriscauley.chriscauley /var/cache/django/
sudo pip install -r requirements.txt 

# install node
sudo apt-get update
sudo apt-get install git-core curl build-essential openssl libssl-dev -y
git clone https://github.com/joyent/node.git
cd node
./configure
make
sudo make install
node -v

curl https://npmjs.org/install.sh | sudo sh
npm -v
sudo npm install less
sudo updatedb

echo "you must now create a symlink from lessc to /usr/bin"
