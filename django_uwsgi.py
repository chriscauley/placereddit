import os
from django.core.wsgi import get_wsgi_application

os.environ['PYTHON_EGG_CACHE'] = '/tmp/egg_cache'
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

application = get_wsgi_application()