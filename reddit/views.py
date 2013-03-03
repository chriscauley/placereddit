from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.cache import cache_page

from .models import SubReddit, Image

import random,datetime

#@cache_page(60 * 15)
def index(request,subreddit=None,nsfw=False):
  if not subreddit:
    r = random.randint(0,SubReddit.objects.filter(nsfw=nsfw).count()-1)
    subreddit = SubReddit.objects.filter(nsfw=nsfw)[r]
  else:
    subreddit = SubReddit.objects.get(name=subreddit)
  if subreddit.nsfw != nsfw:
    pass # return error
  sizes = (
    (100,100),
    (200,200),
    (100,100),
    (200,200),
    (100,100),
    (200,200),
    )
  sizes = sizes*100
  values = {
    'subreddit':subreddit,
    'url': subreddit.get_absolute_url(),
    'randint': lambda: random.choice(range(20)),
    'sizes': sizes,
    }
  return TemplateResponse(request,"reddit.html",values)

@cache_page(60 * 15)
def image(request,subreddit=None,nsfw=False,width=None,height=None,extension=None,num=None):
  sr = get_object_or_404(SubReddit,slug=subreddit,nsfw=bool(nsfw))
  images = Image.objects.filter(subreddit=sr)
  images = images.filter(height__gte=height,width__gte=width)
  image = random.choice(images)
  return image.crop_response(int(width),int(height))

def random_image():
  sr = random.choice(SubReddit.objects.all())
  images = Image.objects.filter(subreddit=sr)
  height =random.choice(range(100,1000))
  width = random.choice(range(100,1000))
  images = images.filter(height__gte=height,width__gte=width)
  if not images:
    print "no image found: %s %sx%s"%(sr,width,height)
    return
  image = random.choice(images)
  return image.crop_response(int(width),int(height))

def test(n=50,f=random_image):
  now = datetime.datetime.now()
  while n>0:
    f()
    n-=1
  print (datetime.datetime.now()-now).seconds
