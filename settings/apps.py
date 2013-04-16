THUMBNAIL_FORMAT = "PNG"

INSTALLED_APPS = (
  'grappelli',
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.sites',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'south',
  'sorl',
  'devserver',
  'main', #abstract classes only
  'compressor',
  'reddit',
)

COMPRESS_ENABLED = True
COMPRESS_PRECOMPILERS = (('text/less', 'lessc {infile} {outfile}'),)
